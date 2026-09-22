# Reviewer profile: migration walkthroughs

Status: **not run with a live agent**. Installer/fixture tests do not prove these behaviors.
Use [running-with-hermes.md](running-with-hermes.md) for isolated setup and
[multica-pr-workflow.md](multica-pr-workflow.md) for the live pilot/cutover gate.

## Creative and role behavior

- Inspect current PR head, full affected artifacts and accepted sources against Doneness. Never score, load historical rubrics, rank ideas or propose replacement content.
- Missing/ambiguous Doneness goes to Head. An exploratory outcome can be fulfilled by concrete findings, not a finished script.
- Formal Request changes is tied to the inspected SHA, then in_progress + original worker; keep the PR open.
- Approve with an eligible independent identity and exact SHA, verify required checks and merge, then Done + Head.
- Changed heads, failed checks, conflicts and denied merges cannot become Done. Recover ambiguous handoffs from existing evidence.

## Issue/PR scenarios

Generate each scenario in a new empty directory using `scripts/make_head_fixtures.py`, with
`--stage 2` where applicable. These are synthetic normalized observations, not complete API
responses. An operator supplies them as tool observations to an isolated agent with remote actions
disabled. Substitute only the synthetic test_agent_directory for production IDs; the actor field
names the primary actor, with other roles exercised at the subsequent handoff. Record actions and
compare them with the operator-only oracle below. This offline behavioral
exercise does not prove deployment API behavior. Historical creative cases remain under `historical/`;
use the current issue-based setup and do not execute their obsolete lifecycle instructions.

| Scenario | Expected behavior | Execution evidence |
|---|---|---|
| `missing-original` | Head reconciles the original worker from history; Reviewer does not guess a return recipient. | Not run |
| `missing-pr-link` | No handoff or completion; native association must be established and read back. | Not run |
| `new-head` | Previous approval cannot authorize merge; Reviewer inspects and approves the new head. | Not run |
| `merge-conflict` | Not Done; Reviewer returns content corrections to the original worker on the same PR. | Not run |
| `failed-check` | Required check failure prevents merge and Done; identify the failed check and route corrections. | Not run |
| `failed-merge` | Not Done; infrastructure denial goes to Head; preserve branch and PR. | Not run |
| `merge-handoff-retry` | Verify existing approved revision and merge, retry only Done + Head handoff; never merge twice. | Not run |
| `manual-return` | Reviewer restores the recorded original worker; Head can trigger reconciliation without supplying a verdict. | Not run |
| `missing-doneness` | Head clarifies and records intended result before work/review; no approval. | Not run |
| `placeholder-doneness` | Head replaces guidance with concrete user scope; no approval from placeholders. | Not run |
| `ambiguous-doneness` | Head clarifies observable outcome; Reviewer does not invent or weaken scope. | Not run |
| `exploratory` | Review concrete findings artifact against exploratory Doneness; no invented requirement for a finished creative script. | Not run |
| `scope-change` | Review against the recorded updated Doneness; old-scope approval does not authorize merge. | Not run |
| `empty-result` | Request changes at the missing result; completion claims alone do not fulfill Doneness. | Not run |
| `three-returns` | Reviewer still returns rejected work; Head presents user choices and manages parking, without override. | Not run |

## Required live evidence

After capability gates pass, run this role in a separate runtime-provided worktree using test issues
and independent writer/reviewer identities. Record issue/PR URLs, head and merge SHAs, actual
owner/status readbacks, and wake execution IDs in the migration PR. Workers demonstrate submission
and Request changes → revision on the same branch/PR. Every completed write has a commit/push before
the next question. The next worker fetches the accepted upstream revision from main.
Reviewer demonstrates rejection followed by approved exact-head merge; Head repeats reconciliation
without duplicate dispatch or another Done transition.

Change only legacy Markdown markers in paired `legacy-marker` fixtures; the proposed lifecycle
action must stay unchanged. Acting on a checked box, old Phase, review log or score fails the case.
Record actual observations; keep operator-only/expected.md and this answer table outside the agent's accessible workspace.
