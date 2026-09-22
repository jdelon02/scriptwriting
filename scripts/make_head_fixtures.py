#!/usr/bin/env python3
"""Generate explicitly synthetic issue/PR observations and content for manual walkthroughs.

Usage: python3 scripts/make_head_fixtures.py <empty-dir> <scenario> [--stage N]
These normalized observations are TEST DATA, not full API responses or a runtime status store.
No network calls, status transitions, Git operations or agent behavior are implemented here.
"""
import argparse
import json
from pathlib import Path

EP = 'series/episodes/s01e04-why-scripts-fail'
ROLES = ('artist', 'architect', 'writer', 'wizard')
FILES = tuple(f'{i:02}-{r}.md' for i, r in enumerate(ROLES, 1))
# Human-written oracles for walkthrough operators, not computed decisions.
EXPECTATIONS = {
    'success': 'Head verifies all four merged revisions on main, reconciles once and prepares the parent index PR; no Done transition repeats.',
    'ready': 'Assigned worker verifies accepted prerequisites and exact branch in the supplied worktree before interviewing.',
    'submission': 'Worker publishes every save, creates/reuses the exact issue PR, verifies native association, then hands In Review to Reviewer.',
    'return': 'Worker reads formal Request changes, resumes the same issue branch/PR, asks the creator, and publishes approved revisions.',
    'missing-original': 'Head reconciles the original worker from history; Reviewer does not guess a return recipient.',
    'missing-pr-link': 'No handoff or completion; native association must be established and read back.',
    'push-failure': 'Keep the local commit, stop further content mutation, report to Head; no review submission.',
    'new-head': 'Previous approval cannot authorize merge; Reviewer inspects and approves the new head.',
    'merge-conflict': 'Not Done; Reviewer returns content corrections to the original worker on the same PR.',
    'failed-merge': 'Not Done; infrastructure denial goes to Head; preserve branch and PR.',
    'failed-check': 'Required check failure prevents merge and Done; identify the failed check and route corrections.',
    'merge-handoff-retry': 'Verify existing approved revision and merge, retry only Done + Head handoff; never merge twice.',
    'duplicate-runs': 'Stop content writes until Head resolves duplicate active writers; metadata is not a lock.',
    'branch-collision': 'Stop editing and report to Head; never ignore other worktrees or force-reset the branch.',
    'no-head-wake': 'Leave Done unchanged; require a proven Head notification fallback before rollout.',
    'repeat-reconcile': 'Head leaves Done and existing successor dispatch unchanged; no duplicate run.',
    'cancelled-prerequisite': 'Do not release successor; Head records user decision to replace, rescope, cancel or retain blocking.',
    'missing-upstream': 'Worker stops before editing; expected upstream merge must be in fetched main and branch.',
    'legacy-marker': 'Ignore both checked and unchecked legacy markers. Artist follows its own assigned In Progress state; later stages cannot proceed with an unmerged predecessor.',
    'missing-doneness': 'Head clarifies and records intended result before work/review; no approval.',
    'placeholder-doneness': 'Head replaces guidance with concrete user scope; no approval from placeholders.',
    'ambiguous-doneness': 'Head clarifies observable outcome; Reviewer does not invent or weaken scope.',
    'exploratory': 'Review concrete findings artifact against exploratory Doneness; no invented requirement for a finished creative script.',
    'scope-change': 'Review against the recorded updated Doneness; old-scope approval does not authorize merge.',
    'empty-result': 'Request changes at the missing result; completion claims alone do not fulfill Doneness.',
    'frequent-saves': 'Verify one successful commit/push per completed write before the next question; preserve history on resume.',
    'manual-return': 'Reviewer restores the recorded original worker; Head can trigger reconciliation without supplying a verdict.',
    'three-returns': 'Reviewer still returns rejected work; Head presents user choices and manages parking, without override.',
    'parent-index': 'Head submits the meaningful navigation artifact after all child merges; Reviewer reviews and merges its own PR before parent Done.',
    'post-merge-revision': 'Head creates a linked revision issue/branch/PR and blocks affected successors; accepted history is unchanged.',
    'structural-request': 'Worker quotes and publishes the structural request, records its location in the own-issue history and notifies Head; Head records the user decision once before releasing affected work.',
}

CONTENT = {
    '01-artist.md': '''# S01E04 — Why Scripts Fail Before You Write Them · Artist
Interview step: payoff
## Inputs
- Title: "Why Scripts Fail Before You Write Them"
- Story spine: not provided
- Audience: "Freelancers recording their first video"
## Idea dump
1. [experience] "I opened the editor before deciding what the viewer should leave with."
2. [lesson] "Now I write the ending first."
## Grand Payoff
- Chosen: "Now I write the ending first." (entry #2)
- Why it justifies the click: "It gives me something to aim the rest at."
## Open threads
- Story spine intentionally left for Architect.
## Architect handoff
Title above; payoff #2, rationale above; dump entries #1 and #2 are the creator's words.
''',
    '02-architect.md': '''# S01E04 — Why Scripts Fail Before You Write Them · Architect
Interview step: flow-check
## Inputs
- Source: 01-artist.md
- Target length: "A short example"
- Loop count: "One"
## Loops
### Loop 1
- Status: approved
- Setup: I opened the editor without an ending. [from: #1, A1.1]
- Tension: I did not know what the viewer should leave with. [from: #1]
- Payoff: Now I write the ending first. [from: #2]
- Answers:
  - A1.1 "That's what I meant. I approve this loop."
## Sequence
- Order: 1
- User's ranking notes: "Only one loop in this example."
## Framing
- Introduction promise: Work out the ending before opening the editor. [from: #1, #2]
- Summary: Write the ending first. [from: #2]
- Creator approval: A1.2 "I approve the promise and summary."
## Open threads
- CTA and re-hook intentionally excluded from this test excerpt's issue scope.
## Writer handoff
Approved loop and framing above; hook not written.
''',
    '03-writer.md': '''# S01E04 — Why Scripts Fail Before You Write Them · Writer
Interview step: completeness
## Inputs
- Skeleton: 02-architect.md
- Voice: series/VOICE.md
## Draft
### Hook
- Status: approved
- Text: I opened the editor before I knew my ending.
- Sources: #1, W1
### Loop 1
- Status: approved
- Text: I didn't know what the viewer should leave with. Now I write the ending first.
- Sources: #1, #2, L1.tension, L1.payoff, W1
### Summary
- Status: approved
- Text: Write the ending first.
- Sources: #2, W1
## Writer answers
- W1 "Those words sound like me. I approve this draft."
## Placeholders
- None within the excerpt scope.
## Skeleton coverage
- Loop 1 and summary drafted; excluded frame sections remain outside this test excerpt scope.
## Open threads
- None within scope.
## Wizard handoff
Approved draft above; voice file linked; draft is unpolished.
''',
    '04-wizard.md': '''# S01E04 — Why Scripts Fail Before You Write Them · Wizard
Interview step: final-check
## Inputs
- Draft: 03-writer.md
- Voice: series/VOICE.md
## Final script
### Hook
- Status: approved
- Text: I opened the editor before I knew my ending.
- Edits: none
### Loop 1
- Status: approved
- Text: [CHAPTER C1] I didn't know what the viewer should leave with. Now I write the ending first.
- Edits: none
### Summary
- Status: approved
- Text: Write the ending first.
- Edits: none
## Edit log
- No wording changes proposed; creator retained the draft.
## Cues
- C1 | CHAPTER | Loop 1 | Write the ending first | user-sourced | #2, Q1 | approved
## Wizard answers
- Q1 "Keep the wording. I approve the chapter cue."
## Open threads
- None within excerpt scope.
## Final handoff
Final excerpt and C1 above; no wording changes or open placeholders.
''',
}


def build_scenario(name, stage):
    """Return synthetic observations; the expected action is supplied by the human-authored oracle."""
    if stage == 1 and name in ('cancelled-prerequisite', 'missing-upstream'):
        raise ValueError('Artist has no upstream stage; choose --stage 2, 3 or 4')
    if stage < 3 and name == 'structural-request':
        raise ValueError('structural-request exercises Writer or Wizard; choose --stage 3 or 4')
    issues, prs = [], []
    for n, role in enumerate(ROLES, 1):
        issue_id = f'TEST-{100 + n}'
        sha = str(n) * 40
        issues.append({
            'identifier': issue_id, 'stage': n, 'status': 'done', 'assignee_id': 'test-head',
            'parent_issue_id': 'TEST-100',
            'description': f'## Doneness\n{FILES[n-1]} contains the creator-approved, sourced test excerpt and its handoff. Only the sections in this excerpt are in scope; excluded frame sections remain identified.',
            'metadata': {'workflow_version': 'multica-pr-v1', 'original_assignee_id': 'test-'+role,
                         'episode_id': 'S01E04', 'stage': role, 'repository': 'test-owner/test-channel',
                         'branch': issue_id, 'base_branch': 'main',
                         'prerequisite_issue_ids': [] if n == 1 else [f'TEST-{99+n}']},
            'linked_pull_requests': [n],
        })
        prs.append({'number': n, 'title': issue_id+' PR', 'head_ref': issue_id, 'base_ref': 'main',
                    'head_sha': sha, 'reviewed_sha': sha, 'review': 'APPROVED',
                    'author': 'test-writer', 'reviewer': 'test-reviewer',
                    'merged': True, 'merge_commit_sha': chr(96+n)*40,
                    'mergeable': True, 'required_checks': {'fixture-validation': 'success'}})
    parent = {
        'identifier': 'TEST-100', 'stage': None, 'status': 'in_progress', 'assignee_id': 'test-head',
        'description': '## Doneness\nThe episode index.md links all four accepted excerpts after their PRs merge. It is navigation only, with no lifecycle flags or creative content.',
        'metadata': {'workflow_version': 'multica-pr-v1', 'original_assignee_id': 'test-head',
                     'episode_id': 'S01E04', 'stage': 'head', 'repository': 'test-owner/test-channel',
                     'branch': 'TEST-100', 'base_branch': 'main',
                     'prerequisite_issue_ids': [i['identifier'] for i in issues]},
        'linked_pull_requests': [],
    }
    data = {'test_data_only': True, 'format': 'normalized-observations-not-api-payloads',
            'scenario': name, 'issues': issues, 'pull_requests': prs,
            'parent_issue': parent,
            'test_agent_directory': {r: {'id': 'test-'+r, 'profile': 'script-'+r}
                                     for r in (*ROLES, 'head', 'reviewer')},
            'test_context': 'Offline only: use this synthetic directory instead of production UUIDs. No production tools or network actions are enabled.',
            'runtime': {'active_writers': 1, 'branch_owner': 'current-worktree',
                        'upstream_on_main': True, 'upstream_on_branch': True, 'head_woke': True},
            'git': {'push_succeeded': True, 'published_matches_local': True},
            'history': []}
    issue, pr = issues[stage-1], prs[stage-1]
    if name not in ('success', 'repeat-reconcile', 'no-head-wake', 'parent-index', 'post-merge-revision'):
        issue.update(status='in_review', assignee_id='test-reviewer')
        pr.update(merged=False, merge_commit_sha=None, review=None, reviewed_sha=None)
    worker_cases = ('ready', 'submission', 'missing-pr-link', 'push-failure', 'frequent-saves', 'return', 'duplicate-runs', 'branch-collision', 'missing-upstream', 'legacy-marker', 'cancelled-prerequisite', 'structural-request')
    if name in worker_cases:
        issue.update(status='in_progress', assignee_id='test-'+ROLES[stage-1])
    data['actor'] = ROLES[stage-1] if name in worker_cases else 'reviewer'
    if name in ('success', 'repeat-reconcile', 'no-head-wake', 'parent-index', 'post-merge-revision'):
        data['actor'] = 'head'
    if name in ('return', 'missing-original', 'three-returns', 'manual-return'):
        pr.update(review='CHANGES_REQUESTED', reviewed_sha=pr['head_sha'], findings=[{'path': FILES[stage-1], 'section': 'Open threads', 'text': 'The handoff does not identify the intentionally excluded material.'}])
    if name == 'missing-original':
        del issue['metadata']['original_assignee_id']
    elif name == 'missing-pr-link':
        issue['linked_pull_requests'] = []
        issue['metadata']['pr_url'] = 'https://example.invalid/test/pr/1'
    elif name == 'push-failure':
        data['git'].update(push_succeeded=False, published_matches_local=False)
    elif name == 'new-head':
        pr.update(review='APPROVED', reviewed_sha='0'*40)
    elif name == 'merge-conflict':
        pr['mergeable'] = False
    elif name == 'failed-merge':
        pr.update(review='APPROVED', reviewed_sha=pr['head_sha'], merge_error='permission denied')
    elif name == 'failed-check':
        pr['required_checks']['fixture-validation'] = 'failure'
    elif name == 'merge-handoff-retry':
        pr.update(merged=True, merge_commit_sha='a'*40, review='APPROVED', reviewed_sha=pr['head_sha'])
        data['history'].append('Merge succeeded; combined Done/Head update timed out.')
    elif name == 'duplicate-runs':
        data['runtime']['active_writers'] = 2
    elif name == 'branch-collision':
        data['runtime']['branch_owner'] = 'other-worktree'
    elif name == 'no-head-wake':
        data['runtime']['head_woke'] = False
    elif name == 'repeat-reconcile':
        data['history'].append('All merges reconciled; parent-index run already dispatched.')
    elif name == 'cancelled-prerequisite' or (name == 'legacy-marker' and stage > 1):
        previous = stage - 2
        issues[previous]['status'] = 'cancelled' if name == 'cancelled-prerequisite' else 'in_review'
        issues[previous]['assignee_id'] = 'test-head' if name == 'cancelled-prerequisite' else 'test-reviewer'
        prs[previous].update(merged=False, merge_commit_sha=None, review=None, reviewed_sha=None)
        data['runtime'].update(upstream_on_main=False, upstream_on_branch=False)
    elif name == 'missing-upstream':
        data['runtime']['upstream_on_branch'] = False
    elif name == 'missing-doneness':
        issue['description'] = '## Purpose\nWork on this episode.'
    elif name == 'placeholder-doneness':
        issue['description'] = '## Doneness\n<Describe the observable result.>'
    elif name == 'ambiguous-doneness':
        issue['description'] = '## Doneness\nMake it good.'
    elif name == 'exploratory':
        issue['description'] = '## Doneness\nfindings.md identifies which creator-supplied inputs are missing and records a recommendation for what to ask next. A finished script is outside scope.'
    elif name == 'scope-change':
        data['history'].append('User expanded scope to include CTA; Head recorded the changed Doneness during review.')
        issue['description'] += ' The creator-approved CTA is also required.'
        pr.update(review='APPROVED', reviewed_sha=pr['head_sha'], approved_scope='excerpt without CTA')
    elif name == 'empty-result':
        pr['body'] = 'All done.'
    elif name == 'frequent-saves':
        data['history'] = ['answer 1 → write 1 → commit 1 → push 1 → next question',
                           'answer 2 → write 2 → commit 2 → push 2 → next question']
    elif name == 'manual-return':
        issue.update(status='in_progress', assignee_id='test-reviewer')
        data['history'].append('User changed only issue status to in_progress.')
    elif name == 'three-returns':
        data['history'] = ['Request changes round 1', 'Request changes round 2', 'Request changes round 3']
    elif name == 'post-merge-revision':
        data['history'].append('User requests a structural revision of the accepted Architect work.')
    elif name == 'structural-request':
        data['history'].append('User: "Move the payoff to the beginning." No Head decision recorded yet.')
    # A single-stage exercise must not present its successors as already accepted.
    if name not in ('success', 'repeat-reconcile', 'no-head-wake', 'parent-index', 'post-merge-revision'):
        for successor in issues[stage:]:
            successor.update(status='backlog', assignee_id='test-head', linked_pull_requests=[])
        data['pull_requests'] = prs[:stage]
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('scenario', choices=sorted(EXPECTATIONS))
    parser.add_argument('--stage', type=int, choices=range(1, 5), default=2)
    parser.add_argument('--legacy-marker', choices=('checked', 'unchecked'), default='checked')
    args = parser.parse_args(argv)
    root = args.destination
    if root.exists() and (not root.is_dir() or any(root.iterdir())):
        parser.error('destination must be an empty scratch directory; existing content is never overwritten')
    try:
        data = build_scenario(args.scenario, args.stage)
    except ValueError as exc:
        parser.error(str(exc))
    root.mkdir(parents=True, exist_ok=True)
    (root / 'test-data').mkdir()
    (root / 'test-data/scenario.json').write_text(json.dumps(data, indent=2)+'\n')
    (root / 'test-data/README.md').write_text('TEST DATA ONLY. Synthetic normalized observations, not a runtime status store or full API responses.\nUse the synthetic test_agent_directory instead of production UUIDs in this isolated exercise. Never supply operator-only/ to the agent.\n')
    (root / 'operator-only').mkdir()
    (root / 'operator-only/expected.md').write_text('# Operator-only oracle\n\nDo not supply this file to the agent or give it filesystem access to this directory.\n\n'+EXPECTATIONS[args.scenario]+'\n')
    ep = root / EP
    ep.mkdir(parents=True)
    for name, text in CONTENT.items():
        if args.scenario not in ('success', 'repeat-reconcile', 'no-head-wake', 'parent-index', 'post-merge-revision') and FILES.index(name) >= args.stage:
            continue
        if args.scenario == 'empty-result' and name == FILES[args.stage-1]:
            text = '# Test excerpt\nAll done.\n'
        if args.scenario in ('return', 'missing-original', 'three-returns', 'manual-return') and name == FILES[args.stage-1]:
            text = text.replace('## Open threads', '## Open threads\n- Excluded material: unclear; creator clarification needed.')
        if args.scenario == 'structural-request' and name == FILES[args.stage-1]:
            text = text.replace('## Open threads', '## Open threads\n- Requested structural change: "Move the payoff to the beginning." Not applied.')
        (ep / name).write_text(text)
    (root / 'series/VOICE.md').write_text('# Voice\n## In my own words\n- V1 "I say it plainly."\n')
    series = '# The Quiet Craft\n## Season 1\n### S01E04 — Why Scripts Fail Before You Write Them\n- Audience: "Freelancers recording their first video"\n'
    if args.scenario == 'legacy-marker':
        mark = 'x' if args.legacy_marker == 'checked' else ' '
        series += f'- Pipeline: [{mark}] Artist  [{mark}] Architect  [{mark}] Writer  [{mark}] Wizard\n'
    (root / 'series/SERIES.md').write_text(series)
    if args.scenario == 'exploratory':
        (ep / 'findings.md').write_text('# Findings\nThe creator has not supplied the story spine or CTA. Ask which next video the viewer should watch and what it promises; do not invent an answer.\n')
    print(f'TEST DATA: {args.scenario} written to {root}; no live actions performed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
