---
type: "project-instructions"
title: "WORKFLOW"
description: "Project instructions source for scriptwriting: WORKFLOW.md."
tags: ["scriptwriting", "project"]
source_path: "WORKFLOW.md"
---

# WORKFLOW

Workflow version: `multica-pr-v1`.

Users bring new work to **Head Script Writer**. Multica owns issue lifecycle and ownership;
GitHub reviews and verified merges establish accepted work. These instructions define the target
contract. Deployment readiness and actual capability evidence are recorded in
`docs/validation/multica-pr-workflow.md`; do not activate a partial instruction bundle.

A Multica agent is the assignee; its Hermes profile is runtime context. Read this workflow before
substantive episode work, alongside your own profile instructions. Informational role questions do
not require an episode. Missing issue/repository context goes to Head, never a guessed assignment.

## Agent directory

### Deployed instruction identity

The source bundles in scriptwriting are authoritative. Multica stores a generated bootstrap
pointing to the installed Hermes files, not a separately maintained copy of their procedure.
The assigned Multica role skill must match the installed skill. Deploy these together with
`scripts/deploy_multica_profiles.py` in the source repo; its default is a read-only preview.
Use `--check --channel-root <content-repo>` for source/deployment drift verification.

Each installed profile has a `deployment.json` receipt and `profile_guard.py`. Before content
mutation, the Multica bootstrap requires its guard with `--channel-root <assigned-content-repo>`.
Head runs the target role's guard with `--preflight` before dispatch. These checks validate the
exact agent → runtime → Hermes profile mapping, executable contents, instructions, skill and
workflow version. Missing or inconsistent deployment evidence stops dispatch/content mutation.
They do not establish issue readiness, replace Doneness or prove the PR/merge/wake pilot.
Never hand-edit generated workdir AGENTS.md; Multica refreshes it when preparing a new run.

Verified with `multica agent list --output json` on 2026-09-22 in workspace `Personal Stuff`
(`aa1884cb-1770-444b-b66d-4a036cba7e82`, issue prefix `PERS`). These six agents belong to the scripting
workflow; other workspace agents are not interchangeable with them.

| Role used in instructions | Exact Multica agent name | Multica agent UUID | Hermes profile |
|---|---|---|---|
| Artist | Script Writing Artist | `84e81aa1-54f8-46c8-a47c-c8f2b8b347c6` | `script-artist` |
| Architect | Script Architect | `9f97901a-ad33-4333-abb6-5f683dd096c0` | `script-architect` |
| Writer | Script Writer | `f0d6a12c-e916-4678-bd1e-1daefbe488fe` | `script-writer` |
| Wizard | Script Wizard | `9238018d-84c4-48f6-a0a4-76fc82601e8b` | `script-wizard` |
| Reviewer | The Reviewer | `89254adf-5859-46e5-b331-8aaa18d3ed36` | `script-reviewer` |
| Head / Head Script Writer | Head Script Writer | `de4cfb27-0b82-4694-97bc-053393df54d8` | `script-head` |

### Referring to and assigning agents

- Role names in these instructions resolve through this directory. Use the exact Multica name when
  telling the user who owns or receives work; use the UUID for assignment operations.
- Use `multica issue assign <issue-id> --to-id <agent-uuid>` or
  `multica issue update <issue-id> --assignee-id <agent-uuid>`. Names passed through `--to` or
  `--assignee` are fuzzy-matched against members, agents, and squads; do not use fuzzy matching for
  automated routing. In particular, `PeeWee (Architect)` is not the scripting Architect.
- Before first dispatch in a session, Head verifies these identities against the active workspace's
  agent directory. If a mapped ID is missing, archived, or inconsistent with its intended role, stop the
  affected dispatch and reconcile the mapping. Never substitute a similarly named agent. A verified
  rename updates the name here; it does not change the agent UUID. Workers report mapping problems to Head.
- Head records the delegated worker's UUID as issue metadata `original_assignee_id` before handing off
  the stage. This is the worker, not Head as the initial intake assignee. Preserve it through review cycles.
  Reviewer and Head use that recorded UUID for returns and revisions of the same issue; do not infer the
  recipient from a filename, profile name, current Reviewer assignment, or a fuzzy name search. If it is
  absent or no longer valid, Head reconciles the issue history before a return is dispatched.
- When a stage submits for review, the currently assigned worker reassigns it to the Reviewer's mapped
  UUID as part of the handoff. A successful status update alone is not a confirmed reassignment; verify
  the returned issue's assignee. These rules identify recipients; lifecycle rules are defined below.
- Hermes profile names are only for runtime selection and profile-home paths. Do not pass a profile
  name to Multica as an assignee or launch another Hermes session as a substitute for assigning an issue.
  Keep `profiles/<role>/...` source paths and installed profile paths intact. Do not read another agent's
  private memory merely because its profile appears in this directory.

## Stages and artifacts

Templates are installed per role under `$HERMES_HOME/templates/` (normally
`~/.hermes/profiles/script-<role>/templates/`), as defined in `scripts/profiles.json`.
Resolve template inputs there regardless of the content worktree's current directory. If HERMES_HOME
is unset, use the installed profile directory containing AGENTS.md. For file artifacts, copy templates
into the assigned content repository before filling them in; never modify the installed masters.
Use the issue template to populate the Multica issue description, not a content file. Content repositories
do not need their own template copies. Reviewer receives the active set for reference only;
templates do not add requirements beyond Doneness. The retired head-log template is not installed.

| Stage | Role | Output in `series/episodes/<folder>/` |
|---|---|---|
| 1 | Artist | `01-artist.md`: creator's idea dump and Grand Payoff |
| 2 | Architect | `02-architect.md`: sourced episode skeleton |
| 3 | Writer | `03-writer.md`: approved draft, hook written last |
| 4 | Wizard | `04-wizard.md`: retention edit and approved visual cues |
| Parent | Head | `index.md`: navigation to all four merged artifacts |

Downstream stages consume accepted content from fetched `main`, with the expected prerequisite merge
revision provided by Head. Preserve creator quotations, provenance, content approvals, interview
answers, drafts, edit history, and cues. Section `Status: approved` means creator approval of wording;
it is not issue completion or permission to dispatch another stage.

## Ownership and transitions

| From → To | Actor | Required evidence/action | New assignee |
|---|---|---|---|
| Intake → Backlog | Head | Scope request; create or reconcile existing issue; define deliverable and fill in Doneness | Head |
| Backlog → Todo | Head | Scope ready; prerequisite PRs merged; original worker recorded; delegate | Stage worker |
| Todo → In Progress | Head dispatch / worker start acknowledgement | Worker verifies assignment, prepares issue branch in supplied worktree before editing | Stage worker |
| In Progress → In Review | Current worker | All changes committed and pushed; PR created or updated, correct title/base/head, linked to issue | Reviewer |
| In Review → In Progress | Reviewer | Post changes-requested agent verdict on the PR; retain open PR; retrieve original worker from issue metadata | Original worker |
| In Review → Done | Reviewer | Record approved agent verdict for current PR head; merge successfully into `main`; verify merge evidence | Head |
| Done → Done (no status change) | Head | Confirm merge; reconcile parent/dependencies/blockers; release eligible next work | Head |
| Open issue → Cancelled | Head | Record the cancellation decision; reconcile affected dependencies and any open PR; cancellation is not successful delivery | Head |

Workers may read their own assignment and PR to perform these handoffs safely; they do not poll the board, create issues, resolve dependency blockers, close issues, or advance other stages. Reviewer owns only assigned review decisions and the two specified outgoing transitions. Head owns all other orchestration.

Reviewing a submitted issue keeps it **In Review**. Do not apply a generic instruction to mark every agent run In Progress: that would falsely signal returned work and trigger the wrong assignee/branch rules.

On a return, reuse the existing issue branch and PR. “Create and check out on In Progress” means ensure the branch exists and check it out; never reset existing history or make duplicate branches on re-entry.

A manual In Review → In Progress change must be reconciled by Reviewer, which restores the original worker. Verify a status-event wake mechanism or Head-triggered reconciliation exists; instructions alone do not guarantee unattended transitions fire. Head may alert/dispatch Reviewer but does not substitute its own review verdict.

## Sources of truth

- **Multica:** issue ownership, lifecycle status, original worker, episode/stage identity, dependencies, blockers, user decisions, and PR association.
- **GitHub:** PR contents, current head SHA, review findings and verdicts, merge state and merge commit.
- **Git main:** accepted content consumed by downstream issues.
- **Markdown:** episode inputs, quoted interview answers, provenance, drafts, user-approved text, edits and cues. A field such as `Interview step: body` may help resume an interview but never indicates review or completion.

Remove numerical scoring, deductions, pass thresholds, and the separate acceptance-criteria framework from the active workflow. Reviewer compares the PR's actual result with the issue's Doneness, while respecting the existing authorship and provenance rules. Do not introduce a replacement scoring scheme or generic stage checklist. PR review and merge remain the evidence of accepted work.

## Issue template and Doneness

Use `templates/issue.md` to populate the Multica issue description. It is not a per-issue file to save in the episode repository:

```markdown
## Purpose
<What the user wants this issue to accomplish.>

## Context and inputs
<Episode, stage, source material, repository, and relevant predecessor issues.>

## Deliverable
<What will be produced or changed, and where it belongs.>

## Doneness
<Describe the observable result that means this issue's work is finished,
and where the Reviewer can see it in the PR. State any intentionally
unfinished material or excluded work so the boundary is clear.>
```

The angle-bracket text above is template guidance and must be replaced before issue creation. Every issue, including a parent, gets a specific, nonempty Doneness section. “Done when complete,” “PR created,” a blank checklist, or a placeholder is insufficient. Use plain prose; no points, percentages, or mandatory scoring/checklist format.

For example, an Artist issue might say: “The episode's `01-artist.md` contains the creator's recorded idea dump and chosen Grand Payoff, with enough context for the Architect to continue. Any material the creator intentionally leaves open is identified. The PR contains this handoff.” This defines the requested outcome; it does not mark the issue complete.

Head derives Doneness from the user's request and the delegated scope. If the intended outcome is unclear, clarify it before creating the issue rather than inventing one. For an intentionally exploratory issue, the outcome can be a concrete findings/recommendation artifact instead of a predetermined creative answer.

Workers use Doneness to understand their task and reference it in the PR. Reviewer explains any gap against it in the PR review, without inventing additional requirements. If Doneness is missing, ambiguous, or conflicts with the request, Head resolves the scope; Reviewer does not silently rewrite it or approve the issue. Head records substantive scope changes in issue history, and a changed outcome requires review against the updated scope. Do not weaken Doneness merely to pass submitted work.

For existing issues, Head fills in Doneness from the actual request and current scope before resuming the migrated workflow. Editing Doneness never itself changes status, proves completion, or unblocks another issue.

Retain escalation after three unsuccessful review rounds, recorded in Reviewer verdict comments/issue history. Reviewer still returns rejected work as required. Head then handles the user decision and can park the issue using Multica's blocker mechanism. No approval override and no repository release-log entry.

## Branch and worktree protocol

1. Read the injected issue identifier, current owner and project resource. Resolve the correct content repository; do not use the profile-source repo for episode work.
2. Inspect `git status`, `git worktree list`, current branch, remote URL, and the runtime resource manifest. Fetch `origin` before choosing a base.
3. For a first start, create `<ISSUE-ID>` from fresh `origin/main`. For a continuation, resume `<ISSUE-ID>` or create its tracking branch from `origin/<ISSUE-ID>` without losing local commits. Verify the Head-provided prerequisite merge is in the base.
4. Stay inside the supplied worktree. Multica-managed branch names are runtime bookkeeping, not PR branch names. Do not rename or delete runtime-owned refs to force compliance.
5. If the issue branch is checked out in another worktree, stop editing and report the collision for Head reconciliation. Never use `--ignore-other-worktrees`, force-reset it, or delete a worktree. Reviewer can inspect the PR SHA detached in its own worktree because review does not edit the issue branch.
6. On every completed content-file write, stage only the issue's intended paths, commit with the issue ID, push the issue branch, and confirm the push succeeded. Keep runtime files, credentials and unrelated memory out of commits.
7. If push fails, retain the local commit, stop further content mutation and report the failure to Head. Do not submit review until published HEAD matches local HEAD. Reconcile an ambiguous push result before retrying; no force push by default.
8. Stop content editing after submission. For requested changes, fetch and resume the same branch; each new revision invalidates approval of the prior head.

Before live cutover, the pilot must verify branch switching and resumption in this deployment's **GitHub repository** worktrees. Public documentation describes additional continuation/cleanup behavior for **local-directory** worktrees, which must not be assumed identical. If runtime cleanup conflicts with exact issue branch checkout, resolve the adapter/runtime behavior before deployment; do not silently relax the naming requirement or introduce a second checkout tree.

## Durable issue identity and PR association

Head populates these metadata keys before dispatch:

| Key | Meaning |
|---|---|
| `workflow_version` | `multica-pr-v1` |
| `original_assignee_id` | Implementing agent UUID; immutable during review cycles. This is the delegated worker, not the initial intake Head. |
| `episode_id`, `stage` | Episode and creative role; `head` for an aggregate issue |
| `repository` | Canonical remote URL |
| `branch` | Exact issue identifier |
| `base_branch` | `main` |
| `prerequisite_issue_ids` | Predecessor references under the selected native dependency representation |

The deployed metadata CLI stores `prerequisite_issue_ids` as text. Write a JSON-encoded array of
issue UUIDs (including `[]` for no predecessors), then parse that value once when reading it.
Accept a native array if the API supplies one; malformed or ambiguous values stop dispatch for
Head reconciliation. Do not treat a nonempty serialized string as a satisfied dependency.

Use native fields for parent and stage ordering. Prefer a single Head-owned episode parent with four staged sibling issues. Stage ordinals are scheduling groups, not a replacement for verifying actual merged inputs. Do not confuse setting `parent` with creating a blocking relationship.

Worker submission records the PR URL and submitted head SHA in issue metadata as recovery evidence. It must also verify the PR appears in Multica's actual linked-PR relation. A description link or metadata key alone is not enough.

Multica documents automatic association from issue IDs in branch names or PR titles. Both required naming rules satisfy that convention when integration is enabled. The installed CLI has `issue pull-requests` to verify the relation, but no PR-URL option on `issue update`. Determine whether the user's visible PR URL field is this native relation or another deployed field. If auto-link is absent, configure the supported integration or use a verified write API; do not invent a CLI flag or claim success from a comment.

Use titles/branch identifiers for linking and omit automatic close-intent phrases in PR bodies. Let Reviewer perform the explicit merged → Done handoff. This avoids integration-driven closure racing assignment and preserves the explicit Reviewer-to-Head handoff.

## PR submission and review protocol

**Worker:** Verify user-declared stage readiness; finish handoff content; commit and push; find an existing open PR for the issue branch before creating one; enforce `<ISSUE-ID> PR`, base `main`, expected head and scope. Put summary, provenance, a reference to the issue's Doneness and evidence of the result, and relevant validation in the PR. Do not create a separate acceptance-criteria list. Verify linked PR association and original worker before assigning Reviewer.

**Reviewer:** Fetch the linked PR from its actual repository and inspect its current head SHA, full affected artifacts and prerequisites. Do not judge from stale local files, a worker's completion claim, or only a diff that omits required context. Compare the result with the issue's Doneness and respect source attribution and creator approval; do not calculate a score or apply the retired stage rubrics. Explain any missing outcome with a concrete PR location. For rejection, post the SHA-bound changes-requested agent verdict described below and keep the PR open. For acceptance, post the SHA-bound approved agent verdict and merge that exact revision under repository rules. Verify merged state and merge commit before moving to Done and handing back to Head.

**GitHub account and attribution:** All agents use the user's authenticated `gh` account,
`jdelon02`; agents do not have separate GitHub accounts. All new commits use author
`Jeremy DeLong <chefjeremy@delongaz.com>`, the user-selected personal identity. Verify effective
Git author/committer identity in each worktree before writing commits, and preserve this attribution
through merge. Do not use agent identities or add agent co-author trailers. GitHub authentication
comes from the existing gh login; username/email configure attribution, not a separate agent login.

**Agent review under one account:** Reviewer is a distinct Multica role, not a separate GitHub user.
Record both verdicts as PR comments under `jdelon02`: `Agent verdict: changes-requested` or
`Agent verdict: approved`. Include the issue ID, mapped Reviewer UUID, executing Multica run ID,
inspected head SHA, current Doneness/scope reference, and concrete findings or outcome evidence.
Record the comment URL/ID, run ID and inspected SHA in issue history before handoff. On recovery,
correlate that comment with the actual Reviewer-assigned run and issue history; the shared GitHub
username or an arbitrary worker comment alone does not establish a Reviewer decision.

Resolve the executing run from `multica issue runs <issue-id> --output json`: use the full `id`
of the running row matching the assigned issue, mapped Reviewer and current trigger. If multiple
rows match, resolve the trigger before posting a verdict. A worktree name such as
`pers-20-f8286c84460f`, a session ID, or a placeholder is not a run ID. Read the posted verdict back
and compare its run ID and SHA with the authoritative records before merging.

Read all current PR discussion and review comments, including human/operator findings, before the
verdict and again immediately before merge. Address each material unresolved finding explicitly.
Do not limit this check to prior agent verdicts. A requested correction to the pilot's own workflow
description is part of its accuracy requirement and cannot be ignored as unrelated to Doneness.

These are agent verdicts, not GitHub APPROVED/CHANGES_REQUESTED review events. Do not attempt
self-approval with `gh pr review --approve` or request another account. Before merging, require the
latest Reviewer verdict for the current SHA and scope to be approved, enforce the expected-head-SHA
merge guard, and obey repository protections/checks. If a future repository rule requires formal
GitHub approvals, stop and report that incompatible rule to the user; never bypass or change it
silently. New commits or scope changes invalidate the prior agent verdict. Reviewer still exclusively
performs the merge and verified Done handoff; Head cannot substitute its own verdict.

**Merge failures:** A conflict, failed required check, outdated approval, changed PR head, or denied merge is not Done. Content corrections return through Reviewer to the original worker; infrastructure/access blockers go to Head. Head cannot override a rejected PR or merge on Reviewer's behalf under the selected design.

An agent dispatch cannot override this division of responsibility. If Head requests an ordinary
review with "do not merge; I will reconcile", Reviewer reports the conflict to Head instead of
treating an issue-thread verdict as completion. Head corrects the request; Reviewer then follows
the PR-verdict, guarded merge and verified return path. A specifically authorized read-only audit
remains read-only and cannot count as a normal review/merge/handoff pilot.

**Head:** Confirm the PR merged and its content is present on main; refresh dependency state; release only eligible successors from the new main revision; leave the issue Done after reconciliation. Record coordination actions in Multica issue history so retries do not duplicate dispatch; no extra completion status or repository flag is needed. A downstream assignment must include the expected upstream merge revision. Parent notifications alone are not completion evidence.

## Revision-specific handoff evidence

Before assigning Reviewer, the worker verifies that local HEAD, the remote issue branch head and
PR head all identify the same intended commit. Record a handoff in the issue containing repository,
branch, PR URL, submitted head SHA, artifact paths and creator-approved scope. Persist the PR URL
and submitted SHA in metadata, verify native PR association, then perform and read back the combined
owner/status update. Distinguish local-only, committed-only, pushed, PR-linked and handed-off states;
name the exact failed boundary rather than saying “submitted” after a partial operation.

Reviewer fetches the linked PR's actual head in its supplied worktree and checks the artifact paths
at that SHA. Pulling Reviewer's default branch cannot prove a submitted artifact is absent. Compare
the fetched PR head with the submitted SHA; a changed head requires assessment of the new revision
and invalidates earlier approval. A missing artifact claim must identify the inspected repository,
SHA and path. Missing association or inaccessible revision is a handoff blocker, not a content verdict.

On retry, inspect existing local/remote commits, PR, metadata and owner/status before writing or
creating anything. Reuse the existing publication and retry only the incomplete boundary. A provider
failure never proves that the prior operation had no side effects.

## Safe handoff and retry behavior

For a transfer of responsibility, update status and assignee together with `--no-start`, then
post the explicit recipient mention and verify its run under **Recipient dispatch evidence**.
Suppressing the assignment wake gives the comment a single intended dispatch boundary.
The installed CLI exposes these shapes:

```sh
multica issue update "$ISSUE_ID" --status in_review --assignee-id "$REVIEWER_ID" --no-start
multica issue update "$ISSUE_ID" --status in_progress --assignee-id "$ORIGINAL_ASSIGNEE_ID" --no-start
multica issue update "$ISSUE_ID" --status done --assignee-id "$HEAD_ID" --no-start
```

These command shapes are supported by CLI help. Use them only after server behavior and wake delivery are verified in the deployment pilot. Persist prerequisite metadata and the PR link before performing a handoff. Read back the resulting pair; avoid separate status/assignment calls that wake the wrong agent.

If a response is ambiguous, read current issue/PR state before retrying. Reuse an existing PR and existing review evidence for the same SHA. If merge succeeds but issue update fails, recover the issue handoff from the already-merged PR; do not merge twice. If moving to Done does not wake Head because it is terminal, establish one supported Head notification/rerun mechanism and prove it works. Workers stop after confirmed handoff and do not keep editing.

Only one active content writer per issue is permitted. Metadata is not an atomic lock; validate the runtime's concurrency behavior and have Head reconcile duplicate runs before either can write the same branch.

## Recipient dispatch evidence

A posted request, a queued recipient run, and a completed result are separate facts. The sender
must verify its permitted handoff on the target issue before saying the recipient was notified,
started, or is working. Writing a local request file, mentioning a role in prose, successful comment
creation, and unchanged assignment do not prove dispatch.

1. Read target ownership/status and existing runs before sending. Reuse a matching queued/running
   run or completed result for the same request/revision; do not create duplicates. An old unrelated
   run is not a receipt. Keep the request comment ID and relevant submitted SHA or legacy refs.
2. For each responsibility transfer, apply the authorized status and mapped assignee together using
   `--no-start`; read back both before notifying. Then post exactly one handoff comment on the target
   issue containing the actual agent mention (syntax below), the requested next action,
   source issue/request ID and PR/SHA or finding/run evidence. Read it back in full to verify the
   actual mention link. Prose such as "Reviewer" is not a mention. A mention alone still does not
   prove a run. Do not combine an assignment-triggered wake with another mention/rerun blindly.
   If recovering a partial handoff, inspect existing comments/runs first and reuse its dispatch;
   do not repost an already-delivered mention. If an earlier update unexpectedly queued a run,
   reconcile it before adding a second trigger. Follow the CLI's required parent-thread routing.
   Required transfers: Head → worker (Todo), worker → Reviewer (In Review), Reviewer → original
   worker (In Progress), and Reviewer → Head (Done after verified merge). Block/cancel decisions
   remain Head-owned and must not dispatch stopped work. Todo → In Progress by the same worker
   is a start acknowledgement: retain assignment, suppress extra wake, and do not mention yourself.
   For normal review returns and completion, the target is the issue whose ownership changes,
   including synthetic pilots: returning PERS-20 means mentioning Head on PERS-20 and verifying
   the Head run on PERS-20. Reporting to a parent afterward does not replace that receipt. Only
   the explicitly bounded legacy-audit path below uses the parent as its return target.
3. Read `multica issue runs <target-issue> --output json`. Match the recipient agent UUID, target
   issue, request/trigger (or the returned dispatch run ID), and creation time. Record the actual run
   ID, observed status and request reference in Multica history. `queued` means queued; `running`
   means started. A completed run requires inspecting its result; failed/cancelled means dispatch
   occurred but execution did not complete. Never claim acceptance merely from run completion.
4. If no matching run exists, report **request posted; dispatch unconfirmed**. Head checks again for
   a concurrent run before a single explicit `multica issue rerun <target-issue> --output json`, only
   with the correct current assignee, authorized scope and passing deployment preflight. Read back
   its returned run ID and target state. If rejected or still unconfirmed, record the exact blocker;
   do not loop retries or change terminal status just to wake an agent. Workers escalate through
   their allowed Head notification path; this grants no successor-dispatch authority.

For a bounded legacy audit, Head's existing request plus `legacy_reconciliation: pending` authorizes
this dispatch recovery while leaving the issue Done and assigned to Reviewer. Do not reopen content,
reassign it to Head, or ask the creator to repeat authorization. If the runtime refuses to dispatch
on Done, report that capability gap; do not bypass it with an in_progress transition. For the audit result, Reviewer must post an explicit
Head mention (syntax below) in a handoff on the Head-owned
episode parent, linking the finding comment and actual Reviewer run ID and naming the reconciliation
action. Keep the parent assigned to Head in its appropriate current status; do not mark the episode
Done merely because an audit finished. Verify the corresponding Head run before declaring the result
handed back. This own-audit return notification is permitted; it grants no successor scheduling.
"Head will verify" is an unfinished handoff without that receipt.

Actual mention syntax in the posted Multica comment (not inside a code block there):

```text
[@Exact Agent Name](mention://agent/<mapped-uuid>)
[@Head Script Writer](mention://agent/de4cfb27-0b82-4694-97bc-053393df54d8)
```


## Terminal states, aggregate issues, and revisions

**Done and Cancelled:** Done means Reviewer verified and merged the delivered work. Cancelled means Head ended the issue without successful delivery. Head processes the Done handoff without another lifecycle transition. A cancelled prerequisite must not automatically authorize downstream work: Head explicitly decides whether to cancel, rescope, replace, or retain blocked dependents. Native terminal-stage notifications may include cancelled children, so Head must inspect the outcome and merged inputs before dispatch.

**Parent issues:** Keep user-facing episode requests assigned to Head except for their own review. To honor the request that every deliverable issue has a PR, define a meaningful Head-owned parent deliverable: an episode navigation/index artifact referencing the four accepted content artifacts. It contains no pass flags or lifecycle ledger and does not author creative material. Once the stage PRs merge, Head submits the parent index PR through Reviewer like any other worker. Reviewer returns it to Head if needed, or merges and hands it back as Done. Head submits the parent only after its required child deliverables are merged; Reviewer marks the parent Done only after its own PR is merged. Head then reconciles the parent while leaving it Done. Do not manufacture empty commits/PRs for pure status questions. Use `templates/episode-index.md` for this navigation artifact. User authorization to implement the migration includes this convention; no existing parent is automatically complete.

**Revisions:** For unmerged work, use the existing issue branch/PR and Reviewer return path. For a substantive revision after merge, Head creates a linked revision issue with its own ID, branch and PR; accepted history remains immutable. Head marks affected downstream work blocked/superseded in Multica and schedules revised successors against new merge commits. No `.stale-*` file renaming, unticked Pipeline boxes, or history rewriting.

## Completion reports and capability evidence

Before a final coordination report, Head reads back affected issue status, assignee and release
metadata, plus relevant PRs and recipient runs. Reconcile contradictory gate fields on the parent
and affected children; preserve historical evidence with a dated correction rather than rewriting
old comments. If an action occurs after a report, post a superseding report in the same thread.
Never defer an authorized dispatch merely to obtain another turn: dispatch and correlate it in
the current run, or name the actual blocker. A completed agent run is not a completed issue.

For each pilot capability, record expected behavior, observed behavior and evidence separately:

| Capability | Required evidence |
|---|---|
| Native PR association | Native issue relation naming the actual repository and PR |
| Revision-specific review | GitHub PR verdict URL, inspected head SHA, Reviewer UUID and actual Reviewer run ID |
| Reviewer merge | Reviewer run's guarded merge action, merged PR head and merge SHA, artifact on fetched main |
| Reviewer return | Combined Done/Head readback, actual Head mention comment ID, correlated receiving Head run |
| Head reconciliation | Receiving Head result verifies the same verdict/merge and reconciles affected gates |
| Safe repeat | A subsequent reconciliation reads existing evidence and produces no duplicate review, merge or successor dispatch |

Head polling within its original run is not a receiving Head run. Head merging is not Reviewer
merge evidence. A skipped check is skipped, even if its status API reports success. Missing or
untested evidence stays pending/failed; never shorten the pilot's Doneness to make it pass. A
bounded pilot proves only its exercised capabilities, not the runbook's untested return, failure,
four-stage or parent-index scenarios. Already-merged defective pilots receive a correction and a
linked follow-up issue/PR; never fabricate retrospective approval or merge them again.

Head records proposed legacy gate exceptions with the affected issue/PR, reason, owner and exact
decision needed. Only an explicit user decision can waive a required release gate; generic recovery
authorization is not that decision. Missing CLI syntax alone does not establish that no supported
API/integration operation exists. Until resolved or explicitly waived, retain the gate and continue
independent authorized work.

## Worker start and resume

Before any content edit, read your assigned issue, its current owner/status, Doneness, metadata,
linked PRs, and Head-provided prerequisite merge revisions. Validate the repository and branch under
the protocol above. Verify each required merge is an ancestor of both fetched `origin/main` and the
issue branch, and read the required upstream artifacts from that accepted history. Stop for Head
if an input is absent, stale, cancelled, or the branch belongs to another active writer.

- `todo`: acknowledge only your own assigned start as `in_progress`, then prepare the issue branch.
- `in_progress`, assigned to you: resume the recorded interview step. If there is Request changes,
  read the current PR review and revise on the same issue branch and PR; preserve creator approvals.
- `in_review`: stop editing. Reviewer retains this status while inspecting the PR.
- `done`: confirm the linked merged PR; report completion and do not resume editing.
- `blocked` or `cancelled`, or assigned elsewhere: do not write. Head reconciles the next action.
- Missing/ambiguous Doneness or assignment: Head resolves it before work proceeds.

`Interview step:` remembers a conversation location only. Historical `Phase:`, `Pipeline`, review
logs and `head-log.md` never override the issue/PR state; retain historical files without updating
them. An old checked box cannot release work. Filmed/Published remain user-maintained content metadata.
After a merge, requested changes require a new revision issue, never reopening the merged branch.

## Questions, skips and approvals

Workers check recorded sources before asking. Ask only when the answer materially affects the agreed
result; group up to three related short questions when useful. No role must ask after every answer.
After one focused clarification leaves a gap unresolved, retain it visibly and continue independent
work; explore further when the creator wants to. Silence does not mean skip or approval.

An explicit skip of optional work is recorded once and honored. Do not equate skipping with inventing
content. Required outcomes or structural changes still need Head scope reconciliation; explain the
specific consequence once rather than repeatedly asking. Artist still never authors ideas. Writer
still drafts only from sources; Wizard applies only approved logged edits and cues.

One explicit reply may approve a clearly named group of sections, edits or cues at the presented
wording version. Record scope, stable IDs, version and source reply. Changed wording needs renewed
approval; unchanged approvals remain valid. Permission to continue drafting, optional skips and
approval of unrelated content never substitute for approval or readiness to submit.

When creator input is the remaining step, the assigned worker presents the exact version/sections
and a focused grouped request on its issue in the current turn. State who should respond and what
that reply enables; do not end with only "approval needed" or "Head can schedule interaction".
Reuse an already-posted unanswered request by linking it rather than asking again. Keep the current
worker assignment; waiting for creator wording approval does not transfer ownership to Reviewer.
If a scope, prerequisite or policy decision belongs to Head, use one actual Head mention on the
Head-owned parent, with the source issue, publication revision, decision needed and run evidence;
verify the receiving run. This narrow escalation permits no successor dispatch. If production is
blocked, report the gate instead of starting a creative interview.

## Recovering progress and readable artifacts

Before a status answer, resumed interview, or new content question, the worker reconciles the
current artifact with relevant issue comments and published commits. For each disputed section,
identify its recorded answers and stable IDs, current wording, explicit approval reference/version,
and actual remaining gap. Reuse answered inputs. An agent's earlier “complete” claim is not creator
approval; an old progress label is not evidence that recorded material is missing. If evidence
conflicts, explain the specific discrepancy and recover the supported state before proceeding.

Truncated output is incomplete evidence. Read the omitted section or bounded comment pages before
claiming an answer or file is absent. After a failed run, inspect files, git status, remote commits,
PRs and issue history: a failed run may already have saved, pushed, or handed off work.

Write Markdown with real line breaks. After each completed save, read the affected sections back
from disk and verify expected headings, answers, source IDs and approval records survived before
committing/pushing. If a document is serialized as one physical line with literal `\n` separators,
preserve the original and repair only verified serialization damage; never blindly replace escaped
sequences in quotations or code. Verify the repair's content before publication. If repair cannot
be established safely, report the defect without restarting the interview. Recovery writes still
require the assigned worker, permitted issue state and normal publication protocol.

Keep four facts separate in status reports: content drafted, creator-approved scope, published
revision, and issue review/merge state. Report uncertainty precisely instead of converting one into
another. Recovered answers remain usable even when publication or approval is unresolved. If an answer is
missing from the artifact but present in a creator comment, recover it from that comment with its
existing ID; do not ask the creator to supply it again. Ask only when both sources lack necessary
content or contain a material conflict. Missing approval is not missing source material, and it does
not stop independent drafting allowed by the role; keep such drafts explicitly unapproved.

## Worker submission

After the user declares readiness, write the stage handoff, commit and push it before the next
question or end of turn. Publish every completed write throughout the interview, including shared
series/voice content within the issue's authorized scope. Follow the PR protocol above: create or
reuse the exact branch's PR, verify native issue association, persist URL and submitted head SHA,
verify `original_assignee_id`, then combine `in_review` with Reviewer assignment and read back both.
An unsuccessful publish, PR association or handoff is not a successful submission. Stop after
confirmed handoff. Workers never create issues, poll global status, clear blockers, close issues,
or dispatch successors. Head alone handles global orchestration.

## Structural requests and scope changes

Writer and Wizard preserve the creator's structural request verbatim in `Open threads` without
applying it. After committing and pushing that content write, record the quotation and exact
file/section plus commit link in **their own Multica issue history**, and notify the mapped Head
through the deployment's verified notification mechanism. This own-issue notification is permitted;
it is not permission to create tasks, clear blockers or dispatch Architect. If notification fails,
report the failure to the user and pause affected content edits rather than claiming it was routed.

Head acknowledges the request in issue history and records the user's decision once. Do not submit
or advance affected work while a required structural decision is unresolved. Head checks outstanding
requests in the issue/PR context before submission reconciliation and successor dispatch. If the user
wants to revise already merged structure, Head creates a linked Architect revision issue and blocks
or supersedes affected downstream work in Multica. If the user withdraws/defers the request, record
that decision and any scope change; the worker does not invent it. A retry reuses the recorded
request/decision, avoiding duplicate revision issues. Content Open threads preserve the creative
context; issue history and Head's action determine routing and scheduling.

## Reconciling legacy issues

Head performs a bounded migration before resuming legacy work. Snapshot descriptions, metadata,
status/owner, parent/stage, comments, runs, linked PRs, repository refs and dirty artifacts. Preserve
original descriptions and historical review claims. Do not dispatch while reconciling; use verified
no-start updates and read back every change. An idle check alone is not a scheduler lock.

1. Recover scope and original workers from the actual request, comments and run history. Add specific
   Doneness and durable identity metadata without weakening or inventing the requested outcome.
   Record an unresolved scope question once when evidence cannot settle it; continue independent
   reconciliation. Record legacy branch refs separately from the future exact issue-ID branch.
   A target branch in metadata is not proof that it exists. Before worker resume, reconcile the
   legacy commits and dirty work in the supplied worktree; establish the issue-ID branch from
   preserved work without reset, forced checkout or discarded changes. Check worktree collisions
   and accepted-main ancestry. Do not treat migrated work as a blank first start from main or
   rewrite runtime-owned refs; unresolved branch recovery remains a Head blocker.
2. Reparent the four existing stage issues as staged siblings under the Head-owned episode parent.
   Record predecessor IDs; native stage order alone never establishes accepted inputs. Preserve IDs
   and history; do not create replacement issues solely to make the board look new.
3. Inspect actual publication and merge history even when the native linked-PR list is empty. Record
   discovered legacy PR/head/merge identities as recovery evidence. A metadata URL does not repair
   native association. Verify artifact presence on fresh main; never manufacture an empty PR or
   relabel an old numerical review as a current SHA-bound approval.
4. Preserve historical Done while marking its acceptance reconciliation unresolved in metadata when
   current evidence is insufficient; block successors explicitly. Head does not fabricate a Reviewer
   verdict or reopen a verified merged revision. For an already-merged legacy PR,
   Head may explicitly request a read-only legacy acceptance reconciliation by the mapped Reviewer
   on the existing Done issue, recording `legacy_reconciliation: pending` and the historical
   repository/PR/head/merge refs. This narrow audit does not reopen the issue, merge again, or grant
   general permission to edit Done work. The legacy branch/title and absent native association are
   recorded exceptions for this audit only; Head must verify the refs directly on GitHub.
   Reviewer records an issue-history finding bound to its actual Reviewer run, inspected PR head,
   merge commit, artifact paths and current Doneness: `accepted-legacy` or `revision-required`.
   This is a present assessment of historical delivery, not a fabricated pre-merge verdict. Missing
   creator approval or unresolved scope prevents acceptance. Head verifies the finding and records
   its evidence before changing `legacy_reconciliation` to `verified`; native association remains
   a separately recorded integration gate. Substantive corrections use a linked revision issue.
5. Park unstarted or prerequisite-blocked work using the deployed native blocker/status mechanism,
   with reason and release evidence recorded. Keep the intended worker identity; do not leave work
   in_progress merely because an old assignment used that status. Preserve unpublished content and
   return recovery to its owning worker when eligible. Do not push or rewrite its creative draft as
   an administrative migration.
6. Read back descriptions, metadata, sibling relationships, owner/status and run lists. Record what
   changed and remaining gates. Only Head releases a successor after verified upstream acceptance,
   deployment alignment and the capability pilot. Metadata completion alone is not readiness.

## Historical material

Old review logs, review rubrics and Head logs remain historical evidence. No active role loads those
rubrics or calculates a numerical pass threshold. `templates/head-log.md` is retired. Content and
creator approval records stay intact; only lifecycle authority moves to Multica and GitHub.
