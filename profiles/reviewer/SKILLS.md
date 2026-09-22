# SKILLS: The Reviewer

All operations follow WORKFLOW.md. Preserve creator authorship; never propose replacement content.

## Skill: inspect-pr

Read your assigned issue and native linked PRs. Verify canonical repository, issue-ID branch,
`<ISSUE-ID> PR` title and base `main`. A URL in the description alone is not association evidence.
Verify `original_assignee_id` against issue history and the agent directory; missing values go to Head.
Read Doneness; missing, placeholder-only, ambiguous or conflicting text requires Head clarification.
Fetch the actual PR head and full changed artifacts plus cited sources and prerequisite merge revisions.
Use detached inspection in your supplied worktree; never seize the worker's checked-out branch or
edit their files. Verify upstream inputs are accepted, not merely present on an unmerged branch.
Record the inspected head SHA and current scope. If the PR is already merged, verify the existing
review/merge evidence and use recover-handoff rather than submitting a duplicate review or merge.

## Skill: review-outcome

Compare the actual result with Doneness. Verify creator approvals and source attribution appropriate
to the role: Artist quotations, Architect sourced elements, Writer sources and voice, Wizard edit
history and approved cues. These protect authorship; they are not a replacement stage-scoring rubric.
Intentional open material may satisfy an exploratory or bounded outcome when the issue says so.
A PR claiming completion without the result does not fulfill Doneness. Cite the concrete PR file,
line or section for each missing or unclear result. Never judge idea strength or supply an answer.
Read existing review findings and current scope-change history. A new head or changed Doneness
requires a fresh assessment; previous approval is not evidence for changed work.

## Skill: request-changes

Post `Agent verdict: changes-requested` as a PR comment under the shared user account, bound to
the inspected head and current Doneness, with location-specific gaps. Include issue ID, Reviewer
UUID and run ID; persist its comment URL/ID and SHA in issue history before the handoff. Keep the PR open. Combine issue `in_progress` with the validated
`original_assignee_id`, then read back both. Reuse existing SHA-bound verdict and correlated Reviewer run evidence if retrying the same
head and verdict. Do not close the issue or PR, create a new branch, or choose a new implementer.
If the original worker is missing or invalid, record findings but have Head reconcile identity before
return dispatch. After three unsuccessful rounds, return normally and flag Head for the user's
parking/revision decision. Count rounds from Reviewer verdict comments and issue history, not file logs.

## Skill: approve-and-merge

Use the user's authenticated `gh` account (`jdelon02`) and verify repository merge permissions.
Inspect required checks and protections; name checks and read results. No CI is not passing CI.
Post `Agent verdict: approved` as a PR comment containing inspected SHA, current Doneness reference,
issue ID, mapped Reviewer UUID, run ID and result evidence. Record comment URL/ID and SHA in issue
history. Verify this is the latest verdict for the current revision and scope, and correlate it with
an actual Reviewer-assigned run. Do not submit formal self-approval or request a second GitHub account.
A repository rule requiring formal GitHub approval is a conflict to report, not silently bypass.
Immediately before merge, re-read the head and verify it is still the inspected SHA. Use a merge API
or CLI with an expected-head-SHA guard. If the head changed, stop and review the new revision.
Preserve user attribution on the merge commit. With gh, use `--author-email` for the configured
user email together with `--match-head-commit` for the inspected SHA; do not use `--admin` to bypass
rules. Merge into main under repository rules, then read back merged state and merge commit. Confirm the
merge corresponds to the reviewed revision. A failed check, conflict, stale approval or denied merge
is not Done. Content corrections follow request-changes; infrastructure/access blockers go to Head.
Only verified merge permits a combined `done` + mapped Head UUID update. Read back owner/status and
verify the supported Head notification mechanism; never substitute a new terminal status.

## Skill: recover-handoff

Read the current issue and PR before retrying an ambiguous response. If merged but the issue update
failed, verify the existing verdict/comment/run/head/merge evidence and retry only the Done + Head handoff.
If already Done and owned by Head, do not repeat the transition or dispatch; check reconciliation evidence.
For a manual in_review → in_progress return, restore the recorded original worker after checking
history and existing findings. Head may dispatch Reviewer to reconcile; Head never supplies the verdict.
If Done does not wake Head, use only the fallback proven in docs/validation/multica-pr-workflow.md;
unproven wake behavior blocks cutover. Missing auth, links, mapping or merge evidence stays explicit.
Never edit legacy completion markers or treat run completion as an accepted deliverable.
