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

These are agent verdicts, not GitHub APPROVED/CHANGES_REQUESTED review events. Do not attempt
self-approval with `gh pr review --approve` or request another account. Before merging, require the
latest Reviewer verdict for the current SHA and scope to be approved, enforce the expected-head-SHA
merge guard, and obey repository protections/checks. If a future repository rule requires formal
GitHub approvals, stop and report that incompatible rule to the user; never bypass or change it
silently. New commits or scope changes invalidate the prior agent verdict. Reviewer still exclusively
performs the merge and verified Done handoff; Head cannot substitute its own verdict.

**Merge failures:** A conflict, failed required check, outdated approval, changed PR head, or denied merge is not Done. Content corrections return through Reviewer to the original worker; infrastructure/access blockers go to Head. Head cannot override a rejected PR or merge on Reviewer's behalf under the selected design.

**Head:** Confirm the PR merged and its content is present on main; refresh dependency state; release only eligible successors from the new main revision; leave the issue Done after reconciliation. Record coordination actions in Multica issue history so retries do not duplicate dispatch; no extra completion status or repository flag is needed. A downstream assignment must include the expected upstream merge revision. Parent notifications alone are not completion evidence.

## Safe handoff and retry behavior

Use a combined Multica update for status and assignee where supported. The installed CLI exposes the shape:

```sh
multica issue update "$ISSUE_ID" --status in_review --assignee-id "$REVIEWER_ID"
multica issue update "$ISSUE_ID" --status in_progress --assignee-id "$ORIGINAL_ASSIGNEE_ID"
multica issue update "$ISSUE_ID" --status done --assignee-id "$HEAD_ID"
```

These command shapes are supported by CLI help. Use them only after server behavior and wake delivery are verified in the deployment pilot. Persist prerequisite metadata and the PR link before performing a handoff. Read back the resulting pair; avoid separate status/assignment calls that wake the wrong agent.

If a response is ambiguous, read current issue/PR state before retrying. Reuse an existing PR and existing review evidence for the same SHA. If merge succeeds but issue update fails, recover the issue handoff from the already-merged PR; do not merge twice. If moving to Done does not wake Head because it is terminal, establish one supported Head notification/rerun mechanism and prove it works. Workers stop after confirmed handoff and do not keep editing.

Only one active content writer per issue is permitted. Metadata is not an atomic lock; validate the runtime's concurrency behavior and have Head reconcile duplicate runs before either can write the same branch.

## Terminal states, aggregate issues, and revisions

**Done and Cancelled:** Done means Reviewer verified and merged the delivered work. Cancelled means Head ended the issue without successful delivery. Head processes the Done handoff without another lifecycle transition. A cancelled prerequisite must not automatically authorize downstream work: Head explicitly decides whether to cancel, rescope, replace, or retain blocked dependents. Native terminal-stage notifications may include cancelled children, so Head must inspect the outcome and merged inputs before dispatch.

**Parent issues:** Keep user-facing episode requests assigned to Head except for their own review. To honor the request that every deliverable issue has a PR, define a meaningful Head-owned parent deliverable: an episode navigation/index artifact referencing the four accepted content artifacts. It contains no pass flags or lifecycle ledger and does not author creative material. Once the stage PRs merge, Head submits the parent index PR through Reviewer like any other worker. Reviewer returns it to Head if needed, or merges and hands it back as Done. Head submits the parent only after its required child deliverables are merged; Reviewer marks the parent Done only after its own PR is merged. Head then reconciles the parent while leaving it Done. Do not manufacture empty commits/PRs for pure status questions. Use `templates/episode-index.md` for this navigation artifact. User authorization to implement the migration includes this convention; no existing parent is automatically complete.

**Revisions:** For unmerged work, use the existing issue branch/PR and Reviewer return path. For a substantive revision after merge, Head creates a linked revision issue with its own ID, branch and PR; accepted history remains immutable. Head marks affected downstream work blocked/superseded in Multica and schedules revised successors against new merge commits. No `.stale-*` file renaming, unticked Pipeline boxes, or history rewriting.

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

## Historical material

Old review logs, review rubrics and Head logs remain historical evidence. No active role loads those
rubrics or calculates a numerical pass threshold. `templates/head-log.md` is retired. Content and
creator approval records stay intact; only lifecycle authority moves to Multica and GitHub.
