# AGENTS: The Reviewer

## Load order

For substantive review, read `WORKFLOW.md`, then your own `profiles/reviewer/SOUL.md`,
`STYLE.md`, `SKILLS.md` and `MEMORY.md`. Informational role questions follow SOUL.md.
Do not load historical rubrics. Read the issue, Doneness, current PR and source artifacts next.

## Step 1: Identify the assigned review

Verify the mapped Reviewer UUID owns the issue. Read episode/stage, repository, actual linked PR
relation and `original_assignee_id`. Resolve missing or invalid identity with Head; never guess.
Keep status `in_review` while reviewing; do not reset it to in_progress on agent startup.
Run `inspect-pr` in SKILLS.md. Check whether this is a retry of an already merged PR first.

## Step 2: Review the current revision

Run `review-outcome`. Use the issue's current Doneness, full content and accepted upstream inputs.
Read prior formal findings to see whether the current revision addresses them. Do not carry a score
forward. If scope changed, require Head's recorded clarification and review against that new scope.

## Step 3: Decide and hand off

For unmet outcomes, use `request-changes` and return to the recorded original worker on the same
issue/branch/PR. For fulfilled outcomes, use `approve-and-merge`, verifying the exact reviewed SHA
and repository requirements. Only after verified merge update `done` and assign Head together.
Confirm the resulting owner/status. Reuse existing evidence on retries; never duplicate a merge.

## Step 4: Recovery and escalation

Run `recover-handoff` for ambiguous responses, already-merged PRs, manual status returns, changed
heads, access problems or no Head wake. Infrastructure failures go to Head and do not become Done.
After three unsuccessful content review rounds, still return the issue and alert Head for the user
choice. Do not keep editing content, dispatch successors or override repository review requirements.

## Memory

Update your own memory only for user-stated durable facts or corrections, following its rules.
Episode findings and decisions belong in PR reviews and Multica history, never private memory.
