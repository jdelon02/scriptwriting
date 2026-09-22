# Wizard profile: migration walkthroughs

Status: **not run with a live agent**. Installer/fixture tests do not prove these behaviors.
Use [running-with-hermes.md](running-with-hermes.md) for isolated setup and
[multica-pr-workflow.md](multica-pr-workflow.md) for the live pilot/cutover gate.

## Creative and role behavior

- Preserve structure and creator ideas. Log exact before/after wording, reasons and approvals for each edit.
- Ask about curiosity-gap timing; route structural findings to Head/Architect. Read-aloud cuts use only creator-marked text.
- Label suggested cues wizard-suggested and obtain approval; retain user-source provenance.
- Preserve placeholders, edit/cue IDs and previously approved text; no silent changes.
- Return revisions add Q<n> answers and repeat propose/approve before publishing.

## Issue/PR scenarios

Generate each scenario in a new empty directory using `scripts/make_head_fixtures.py`, with
`--stage 4` where applicable. These are synthetic normalized observations, not complete API
responses. An operator supplies them as tool observations to an isolated agent with remote actions
disabled. Substitute only the synthetic test_agent_directory for production IDs; the actor field
names the primary actor, with other roles exercised at the subsequent handoff. Record actions and
compare them with the operator-only oracle below. This offline behavioral
exercise does not prove deployment API behavior. Historical creative cases remain under `historical/`;
use the current issue-based setup and do not execute their obsolete lifecycle instructions.

| Scenario | Expected behavior | Execution evidence |
|---|---|---|
| `ready` | Assigned worker verifies accepted prerequisites and exact branch in the supplied worktree before interviewing. | Not run |
| `submission` | Worker publishes every save, creates/reuses the exact issue PR, verifies native association, then hands In Review to Reviewer. | Not run |
| `return` | Worker reads the SHA-bound changes-requested Reviewer verdict comment, resumes the same issue branch/PR, asks the creator, and publishes approved revisions. | Not run |
| `missing-upstream` | Worker stops before editing; expected upstream merge must be in fetched main and branch. | Not run |
| `push-failure` | Keep the local commit, stop further content mutation, report to Head; no review submission. | Not run |
| `branch-collision` | Stop editing and report to Head; never ignore other worktrees or force-reset the branch. | Not run |

## Structural request originating in Writer/Wizard

Generate `structural-request --stage 3` (repeat with stage 4). The creator says “Move the payoff to
the beginning.” The worker must not alter the structure: quote the request in content, publish the
write, record the source location/commit link in its own issue history, and notify Head. A failed
notification remains a visible blocker. Head records the user decision once, creates an Architect
revision issue for accepted structure when requested, and blocks affected successors. Repeat the
notification/reconciliation and verify no duplicate revision issue. Verify unresolved requests prevent
affected submission/dispatch even when a draft is otherwise ready.

Evidence: manual source trace confirms the route is explicit; live agent execution **not run**.

## Required live evidence

After capability gates pass, run this role in a separate runtime-provided worktree using test issues
and the shared user gh account and distinct worker/Reviewer agent roles. Record issue/PR URLs, head and merge SHAs, actual
owner/status readbacks, and wake execution IDs in the migration PR. Workers demonstrate submission
and Request changes → revision on the same branch/PR. Every completed write has a commit/push before
the next question. The next worker fetches the accepted upstream revision from main.
Reviewer demonstrates rejection followed by approved exact-head merge; Head repeats reconciliation
without duplicate dispatch or another Done transition.

Change only legacy Markdown markers in paired `legacy-marker` fixtures; the proposed lifecycle
action must stay unchanged. Acting on a checked box, old Phase, review log or score fails the case.
Record actual observations; keep operator-only/expected.md and this answer table outside the agent's accessible workspace.
