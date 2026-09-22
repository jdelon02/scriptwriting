# Head profile: migration walkthroughs

Status: **not run with a live agent**. Installer/fixture tests do not prove these behaviors.
Use [running-with-hermes.md](running-with-hermes.md) for isolated setup and
[multica-pr-workflow.md](multica-pr-workflow.md) for the live pilot/cutover gate.

## Creative and role behavior

- Populate concrete Doneness before creating any issue, including the parent.
- Use one parent with four staged siblings. Record original workers before dispatch and release successors only on actual merged inputs.
- Reconcile accepted work while leaving Done unchanged; repeated reconciliation never duplicates dispatch.
- Cancelled predecessors require an explicit decision. After three rejected rounds, present user choices and manage parking without overriding Reviewer.
- Parent index links merged artifacts through its own reviewed PR. Post-merge revisions use new issues and preserve history.

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
| `success` | Head verifies all four merged revisions on main, reconciles once and prepares the parent index PR; no Done transition repeats. | Not run |
| `no-head-wake` | Leave Done unchanged; require a proven Head notification fallback before rollout. | Not run |
| `repeat-reconcile` | Head leaves Done and existing successor dispatch unchanged; no duplicate run. | Not run |
| `cancelled-prerequisite` | Do not release successor; Head records user decision to replace, rescope, cancel or retain blocking. | Not run |
| `duplicate-runs` | Stop content writes until Head resolves duplicate active writers; metadata is not a lock. | Not run |
| `branch-collision` | Stop editing and report to Head; never ignore other worktrees or force-reset the branch. | Not run |
| `missing-doneness` | Head clarifies and records intended result before work/review; no approval. | Not run |
| `scope-change` | Review against the recorded updated Doneness; old-scope approval does not authorize merge. | Not run |
| `three-returns` | Reviewer still returns rejected work; Head presents user choices and manages parking, without override. | Not run |
| `parent-index` | Head submits the meaningful navigation artifact after all child merges; Reviewer reviews and merges its own PR before parent Done. | Not run |
| `post-merge-revision` | Head creates a linked revision issue/branch/PR and blocks affected successors; accepted history is unchanged. | Not run |

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
and independent writer/reviewer identities. Record issue/PR URLs, head and merge SHAs, actual
owner/status readbacks, and wake execution IDs in the migration PR. Workers demonstrate submission
and Request changes → revision on the same branch/PR. Every completed write has a commit/push before
the next question. The next worker fetches the accepted upstream revision from main.
Reviewer demonstrates rejection followed by approved exact-head merge; Head repeats reconciliation
without duplicate dispatch or another Done transition.

Change only legacy Markdown markers in paired `legacy-marker` fixtures; the proposed lifecycle
action must stay unchanged. Acting on a checked box, old Phase, review log or score fails the case.
Record actual observations; keep operator-only/expected.md and this answer table outside the agent's accessible workspace.
