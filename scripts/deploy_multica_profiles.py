#!/usr/bin/env python3
"""Preview, apply, or check coherent Hermes/Multica scripting instructions."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

import install_profiles as installer
import profile_guard as guard

ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = 'aa1884cb-1770-444b-b66d-4a036cba7e82'
ACTIVE = {'queued', 'dispatched', 'running', 'waiting_local_directory'}


def require_idle(runs):
    active = [r['id'] for r in runs if r.get('status') in ACTIVE]
    if active:
        raise ValueError('Scripting runs are active: ' + ', '.join(active))


def revision(files):
    return guard.digest(json.dumps(files, sort_keys=True))[:20]


def sync_workflow(current, canonical):
    guard.workflow_body(current)
    return current[:current.index('Workflow version:')] + guard.workflow_body(canonical)


def directory():
    rows = re.findall(r'^\| ([^|]+) \| ([^|]+) \| \x60([^\x60]+)\x60 \| \x60script-([^\x60]+)\x60 \|$',
                      (ROOT / 'WORKFLOW.md').read_text(), re.M)
    entries = {role: {'name': name.strip(), 'agent_id': aid} for _, name, aid, role in rows}
    if set(entries) != set(installer.SHORTS):
        raise ValueError('Canonical workflow must identify all six scripting roles')
    return entries


def rendered(role, entry):
    name = 'script-' + role
    source = ROOT / 'profiles' / role
    files = {
        'SOUL.md': installer.render_soul((source / 'SOUL.md').read_text(), name, 'script-'),
        'AGENTS.md': installer.render_agents((source / 'AGENTS.md').read_text(), 'script-'),
        'STYLE.md': installer.render_style((source / 'STYLE.md').read_text(), 'script-'),
        'SKILL.md': installer.render_skill((source / 'SKILLS.md').read_text(), name, entry['skill_description'], 'script-'),
        'profile_guard.py': (ROOT / 'scripts/profile_guard.py').read_text(),
    }
    for filename in entry['templates']:
        files['templates/' + filename] = (ROOT / 'templates' / filename).read_text()
    return files


def bootstrap(role, name, agent_id, home, rev):
    return f"""# {name}

Scripting deployment: {rev}. Multica agent: {agent_id}. Hermes profile: script-{role}.
Your authoritative role instructions are the installed files in {home}.
Read {home}/SOUL.md, {home}/AGENTS.md, {home}/STYLE.md and
{home}/SKILL.md before answering. They define your authorship boundaries and procedure.
Earlier conversation descriptions of your role or workflow do not replace these files.
Do not launch another profile to perform your own assigned role.

Before substantive episode work, run:
python3 {home}/profile_guard.py --channel-root <actual-assigned-content-repository>
Head also checks the intended worker's deployed mapping before dispatch.
A failed identity/deployment check stops content mutation and dispatch; report its exact error.
Informational role questions follow the installed SOUL exception and need no episode or board.
An explicit identity smoke test may run the guard without --channel-root.
Read WORKFLOW.md from the assigned content repository for issue and PR transitions.
The role's allowed transitions take precedence over generic platform lifecycle defaults:
workers never mark Done; Reviewer follows WORKFLOW.md for ordinary review and explicit read-only
legacy audits. A new Done transition requires verified merge; Head reconciles Done without reopening it.
Use only your own installed memory under its rules. Use installed templates.
Do not use retired Phase/Pipeline fields, scoring rubrics or head-log files as lifecycle authority.
"""


def cli(*args):
    return guard.command_json(['multica', '--workspace-id', WORKSPACE, *args])


def build_plan(profiles_dir):
    agents = {a['id']: a for a in cli('agent', 'list', '--output', 'json')}
    runtimes = cli('runtime', 'list', '--output', 'json')
    runtime_profiles = cli('runtime', 'profile', 'list', '--output', 'json')
    manifest = installer.load_manifest()
    identities = directory()
    files = {role: rendered(role, manifest[role]) for role in installer.SHORTS}
    rev = revision({'roles': files, 'workflow': (ROOT / 'WORKFLOW.md').read_text(),
                    'deployer': Path(__file__).read_text(), 'identities': identities})
    plans = []
    for role in installer.SHORTS:
        ident = identities[role]
        agent = agents[ident['agent_id']]
        if agent.get('archived_at') or agent.get('name') != ident['name']:
            raise ValueError(f'{role}: canonical agent is archived or renamed')
        home = (profiles_dir / ('script-' + role)).resolve()
        executable = str(Path.home() / '.local/bin' / ('script-' + role))
        matches = [p for p in runtime_profiles if p.get('enabled') and p.get('command_name') == '/usr/bin/env'
                   and p.get('fixed_args') == ['HERMES_HOME=' + str(home), executable]]
        if len(matches) != 1:
            raise ValueError(f'{role}: expected exactly one matching launch profile, got {len(matches)}')
        profile = matches[0]
        matches = [r for r in runtimes if r.get('profile_id') == profile['id'] and r.get('provider') == 'hermes'
                   and r.get('runtime_mode') == 'local']
        if len(matches) != 1:
            raise ValueError(f'{role}: expected exactly one local Hermes runtime, got {len(matches)}')
        runtime = matches[0]
        skills = [s for s in agent.get('skills', []) if s['name'] == 'script-' + role and s.get('enabled')]
        if len(skills) != 1:
            raise ValueError(f'{role}: missing or ambiguous enabled role skill')
        skill = cli('skill', 'get', skills[0]['id'], '--with-content', '--output', 'json')
        if agent.get('custom_args') or agent.get('runtime_config'):
            raise ValueError(f'{role}: reconcile launch overrides before deployment')
        wrapper = Path(executable).read_text()
        if not re.search(r'exec\s+\S*hermes\s+-p\s+' + re.escape('script-' + role) + r'\s+"\$@"', wrapper):
            raise ValueError(f'{role}: unexpected Hermes executable wrapper')
        receipt = dict(ident, role=role, home=str(home), executable=executable, workspace_id=WORKSPACE,
                       revision=rev, runtime_id=runtime['id'], runtime_profile_id=profile['id'],
                       executable_sha256=guard.digest(wrapper),
                       skill_id=skill['id'], skill_sha256=guard.digest(files[role]['SKILL.md']),
                       files={n: guard.digest(t) for n, t in files[role].items()},
                       workflow_sha256=guard.digest(guard.workflow_body((ROOT / 'WORKFLOW.md').read_text())))
        receipt['instructions'] = bootstrap(role, ident['name'], ident['agent_id'], home, rev)
        plans.append({'receipt': receipt, 'files': files[role], 'agent': agent, 'skill': skill,
                      'runtime': runtime, 'profile': profile})
    return plans


def check_plan(plans, channel_root):
    errors = []
    for plan in plans:
        r = plan['receipt']
        issues = guard.validate(r, plan['agent'], plan['runtime'], plan['profile'], plan['skill'],
                                channel_root=channel_root)
        receipt_path = Path(r['home']) / 'deployment.json'
        if not receipt_path.exists() or json.loads(receipt_path.read_text()) != r:
            issues.append('deployment receipt missing or differs from source')
        errors.extend(f"{r['role']}: {e}" for e in issues)
    return errors


def apply(plans, channel_root, backup_dir):
    for plan in plans:
        require_idle(cli('agent', 'tasks', plan['receipt']['agent_id'], '--output', 'json'))
    workflow = channel_root / 'WORKFLOW.md'
    before = workflow.read_text()
    after = sync_workflow(before, (ROOT / 'WORKFLOW.md').read_text())
    backup_dir.mkdir(parents=True, exist_ok=False)
    backup_dir.chmod(0o700)
    backup = {'channel_root': str(channel_root), 'workflow': before, 'roles': []}
    for plan in plans:
        r = plan['receipt']
        home = Path(r['home'])
        previous = {}
        for name in [*plan['files'], 'deployment.json']:
            path = home / name
            previous[name] = path.read_text() if path.exists() else None
        backup['roles'].append({'agent_id': r['agent_id'], 'home': str(home),
                                'instructions': plan['agent']['instructions'],
                                'runtime_id': plan['agent']['runtime_id'],
                                'skill_id': r['skill_id'], 'skill_content': plan['skill']['content'],
                                'skill_description': plan['skill'].get('description', ''),
                                'files': previous})
    (backup_dir / 'before.json').write_text(json.dumps(backup, indent=2) + '\n')
    print(f'Backup: {backup_dir}', flush=True)
    # Block every installed guard until the complete bundle has passed readback.
    for plan in plans:
        (Path(plan['receipt']['home']) / 'deployment.pending').write_text(str(backup_dir) + '\n')
    subprocess.run([sys.executable, str(ROOT / 'scripts/install_profiles.py'), '--no-config',
                    '--no-bundled-skills', '--profiles-dir', str(Path(plans[0]['receipt']['home']).parent)],
                   check=True)
    if before != after:
        workflow.write_text(after)
    for plan in plans:
        r = plan['receipt']
        home = Path(r['home'])
        (home / 'profile_guard.py').write_text(plan['files']['profile_guard.py'])
        skill_path = backup_dir / (r['role'] + '-SKILL.md')
        skill_path.write_text(plan['files']['SKILL.md'])
        cli('skill', 'update', r['skill_id'], '--content-file', str(skill_path),
            '--description', installer.load_manifest()[r['role']]['skill_description'], '--output', 'json')
        cli('agent', 'update', r['agent_id'], '--instructions', r['instructions'],
            '--runtime-id', r['runtime_id'], '--output', 'json')
        errors = guard.check_live(r, channel_root, allow_pending=True)
        if errors:
            raise ValueError(f"{r['role']}: " + '; '.join(errors))
        print(f"Verified {r['role']} {r['revision']}", flush=True)
    for plan in plans:
        r = plan['receipt']
        (Path(r['home']) / 'deployment.json').write_text(json.dumps(r, indent=2) + '\n')
    for plan in plans:
        (Path(plan['receipt']['home']) / 'deployment.pending').unlink()


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    action = p.add_mutually_exclusive_group()
    action.add_argument('--apply', action='store_true')
    action.add_argument('--check', action='store_true')
    p.add_argument('--channel-root', type=Path, required=True)
    p.add_argument('--profiles-dir', type=Path, default=Path.home() / '.hermes/profiles')
    p.add_argument('--backup-dir', type=Path)
    args = p.parse_args(argv)
    try:
        plans = build_plan(args.profiles_dir)
        if args.apply:
            backup = args.backup_dir or Path('/private/tmp') / ('script-profile-deploy-' +
                       datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
            apply(plans, args.channel_root.resolve(), backup)
            plans = build_plan(args.profiles_dir)
        errors = check_plan(plans, args.channel_root)
        for error in errors:
            print(error)
        if not errors:
            print('PASS: all six profiles, remote prompts/skills, runtime mappings and channel workflow agree.')
        elif not args.check and not args.apply:
            print('Preview only. Use --apply to synchronize after reviewing the differences.')
        return 1 if errors and (args.check or args.apply) else 0
    except (KeyError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'DEPLOYMENT FAILED: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
