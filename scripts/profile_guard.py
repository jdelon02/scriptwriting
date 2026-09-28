#!/usr/bin/env python3
"""Read-only verification of a deployed scripting profile. Standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def workflow_body(text):
    start = text.find('Workflow version:')
    if start < 0:
        raise ValueError('WORKFLOW.md has no workflow version marker')
    return text[start:].strip() + '\n'


def command_json(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=90)
    if result.returncode:
        raise ValueError(f'{args[0:3]} failed: {result.stderr.strip()}')
    return json.loads(result.stdout)


def validate(receipt, agent, runtime, profile, skill, actual_home=None, channel_root=None, allow_pending=False):
    errors = []
    home = Path(receipt['home'])
    if (home / 'deployment.pending').exists() and not allow_pending:
        errors.append('deployment pending; do not dispatch or edit content')
    if 'executable_sha256' in receipt:
        executable = Path(receipt['executable'])
        if not executable.is_file() or digest(executable.read_text()) != receipt['executable_sha256']:
            errors.append('runtime executable drift')
    if actual_home is not None and Path(actual_home).resolve() != home.resolve():
        errors.append(f"HERMES_HOME mismatch: expected {home}, got {actual_home}")
    if agent.get('id') != receipt['agent_id'] or agent.get('archived_at'):
        errors.append('agent identity is missing or archived')
    if agent.get('runtime_id') != receipt['runtime_id']:
        errors.append('agent runtime mapping mismatch')
    if runtime.get('id') != receipt['runtime_id'] or runtime.get('profile_id') != receipt['runtime_profile_id']:
        errors.append('runtime profile mapping mismatch')
    if runtime.get('provider') != 'hermes':
        errors.append('runtime provider must be hermes')
    expected_args = ['HERMES_HOME=' + str(home), receipt['executable']]
    if (profile.get('id') != receipt['runtime_profile_id'] or not profile.get('enabled')
            or profile.get('command_name') != '/usr/bin/env'
            or profile.get('fixed_args') != expected_args):
        errors.append('runtime launch command/profile home mismatch')
    if agent.get('custom_args') or agent.get('runtime_config'):
        errors.append('agent launch override needs explicit reconciliation')
    if agent.get('instructions') != receipt['instructions']:
        errors.append('Multica instructions differ from deployed bootstrap')
    if not any(s.get('id') == receipt['skill_id'] and s.get('enabled')
               for s in agent.get('skills', [])):
        errors.append('role skill assignment missing or disabled')
    if skill.get('id') != receipt['skill_id'] or digest(skill.get('content', '')) != receipt['skill_sha256']:
        errors.append('Multica skill differs from installed role skill')
    for name, expected in receipt['files'].items():
        path = home / name
        if not path.is_file() or digest(path.read_text()) != expected:
            errors.append(f'installed file drift: {name}')
    if channel_root is not None:
        try:
            body = workflow_body((Path(channel_root) / 'WORKFLOW.md').read_text())
            if digest(body) != receipt['workflow_sha256']:
                errors.append('channel WORKFLOW.md contract drift')
        except (OSError, ValueError) as exc:
            errors.append(f'channel WORKFLOW.md: {exc}')
    return errors


def check_live(receipt, channel_root=None, actual_home=None, allow_pending=False):
    base = ['multica', '--workspace-id', receipt['workspace_id']]
    agent = command_json(base + ['agent', 'get', receipt['agent_id'], '--output', 'json'])
    runtimes = command_json(base + ['runtime', 'list', '--output', 'json'])
    profiles = command_json(base + ['runtime', 'profile', 'list', '--output', 'json'])
    runtime = next((r for r in runtimes if r['id'] == receipt['runtime_id']), {})
    profile = next((p for p in profiles if p['id'] == receipt['runtime_profile_id']), {})
    skill = command_json(base + ['skill', 'get', receipt['skill_id'], '--with-content', '--output', 'json'])
    return validate(receipt, agent, runtime, profile, skill, actual_home, channel_root, allow_pending)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--channel-root', type=Path, help='Required before episode edits; assigned repository root')
    p.add_argument('--preflight', action='store_true',
                   help='Head/operator checks a target role before dispatch; do not compare caller HERMES_HOME')
    args = p.parse_args(argv)
    try:
        receipt = json.loads(Path(__file__).with_name('deployment.json').read_text())
        actual_home = os.environ.get('HERMES_HOME')
        if not actual_home and not args.preflight:
            raise ValueError('HERMES_HOME is unset; cannot verify the executing profile')
        errors = check_live(receipt, args.channel_root, None if args.preflight else actual_home)
        if errors:
            raise ValueError('; '.join(errors))
        print(f"PASS {receipt['role']} {receipt['revision']}")
        return 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f'PROFILE CHECK FAILED: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
