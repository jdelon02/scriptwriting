# Multica Issue and PR Workflow Migration Plan

> **For agentic workers:** Use `superpowers:executing-plans` to implement this plan task by task after design approval. This document is a proposed migration, not authorization to change live issues, publish profiles, or merge PRs during planning.

**Goal:** Make Multica issues authoritative for ownership and orchestration, and GitHub PR reviews and merged commits authoritative for accepted scriptwriting work.

**Architecture:** Keep the four creative roles and independent Reviewer. Head Script Writer owns intake, decomposition, scheduling, blockers, cancellation, and post-merge reconciliation. Workers publish issue branches; the Reviewer requests changes or approves and merges; the Head reconciles dependencies after the issue reaches Done. Markdown contains creative content and interview context, not lifecycle gates.

**Tech stack:** Existing Markdown profiles and Python Hermes installer; Multica CLI, issue metadata and linked PRs; Git worktrees; GitHub PRs.

**Spec:** The target contract in this document implements the user's requirements of 2026-09-22. Confirmed decisions: Reviewer approves AND merges, marks Done, and assigns Head; Head reconciles dependencies while leaving the issue Done; Done and Cancelled are the only terminal issue statuses; issue branches merge directly into `main` through PRs. No `develop` or release branch layer. Remove scoring and the separate acceptance-criteria framework; require a plain-language Doneness section when Head creates each issue.

## Global constraints

- Users assign new issues only to **Head Script Writer**. The Head delegates subsequent work.
- Work stays in Multica's runtime-provided worktree. Do not create a parallel checkout system.
- Work branch name is exactly the issue identifier, for example `PERS-14`.
- PR title is exactly `<issue identifier> PR`, for example `PERS-14 PR`.
- Commit and push after every completed write of new information to a project deliverable, before asking the next interview question or ending the turn.
- The current worker submits and assigns to **The Reviewer**. The Reviewer returns to the recorded original worker or merges and assigns to the Head.
- Head owns creating issues, global status tracking, blocker management, dependencies, cancellation, and post-merge reconciliation. Narrow handoff operations below are explicit exceptions.
- Head fills in Doneness in the issue description at creation. It describes the observable intended result; it is not a score, completion flag, or separate rubric.
- Preserve creator authorship, source attribution, voice, user approval of substantive content, and the separation of creative roles.
- No Pipeline checkbox, review log, `Phase:` value, or completion text can authorize progress or prove completion.
- Do not overwrite existing uncommitted work. `WORKFLOW.md` already has user edits at planning time.
- Preserve installed credentials, model configuration, learned memory, and unrelated skills during deployment.

## Evidence and deployment boundaries

Read-only inspection on 2026-09-22 found:

| Item | Observed value |
|---|---|
| Profile source repository | `jdelon02/scriptwriting`, this checkout, branch `main` |
| Multica project | `delongpa`, ID `cd7092b1-5ccd-4444-9334-6346c91f10bf` |
| Project content repository | `https://github.com/jdelon02/delongpa-channel` |
| Project resource | `github_repo`, ID `d600497e-7c05-4827-9ce3-ddf154e78528` |
| Workspace | `Personal Stuff`, issue prefix `PERS` |
| Head Script Writer | `de4cfb27-0b82-4694-97bc-053393df54d8` |
| The Reviewer | `89254adf-5859-46e5-b331-8aaa18d3ed36` |
| Script Writing Artist | `84e81aa1-54f8-46c8-a47c-c8f2b8b347c6` |
| Script Architect | `9f97901a-ad33-4333-abb6-5f683dd096c0` |
| Script Writer | `f0d6a12c-e916-4678-bd1e-1daefbe488fe` |
| Script Wizard | `9238018d-84c4-48f6-a0a4-76fc82601e8b` |

The live agents include embedded instructions as well as attached skills. Updating this repository or reinstalling Hermes profiles alone is insufficient: reconcile all active instruction copies.

The current board snapshot has PERS-14 assigned to Head and In Progress; PERS-15 Artist marked Done and assigned to Reviewer; PERS-16 through PERS-18 In Progress. PERS-15 has no parent, and the later stages have different parent IDs. Inspect full relationships before migrating; this is evidence to reconcile, not proof those issues are wrong or their work is missing. This checkout is not the content repository, so absence of content here cannot establish absence there.

The installed CLI supports combined `issue update --status ... --assignee-id ...`, `--no-start`, per-issue metadata, custom properties, staged sub-issues, and reading linked PRs. Its built-in statuses are `backlog`, `todo`, `in_progress`, `in_review`, `done`, `blocked`, and `cancelled`. **The user confirmed that Done and Cancelled are the terminal issue statuses; Completed is not an issue status.** Do not create an additional terminal status. Zero custom property definitions were returned. A completed agent run is not evidence that an issue is Done.

## Target contract

### Ownership and transitions

| From → To | Actor | Required evidence/action | New assignee |
|---|---|---|---|
| Intake → Backlog | Head | Scope request; create or reconcile existing issue; define deliverable and fill in Doneness | Head |
| Backlog → Todo | Head | Scope ready; prerequisite PRs merged; original worker recorded; delegate | Stage worker |
| Todo → In Progress | Head dispatch / worker start acknowledgement | Worker verifies assignment, prepares issue branch in supplied worktree before editing | Stage worker |
| In Progress → In Review | Current worker | All changes committed and pushed; PR created or updated, correct title/base/head, linked to issue | Reviewer |
| In Review → In Progress | Reviewer | Submit Request changes on the PR; retain open PR; retrieve original worker from issue metadata | Original worker |
| In Review → Done | Reviewer | Approve current PR head; merge successfully into `main`; verify merge evidence | Head |
| Done → Done (no status change) | Head | Confirm merge; reconcile parent/dependencies/blockers; release eligible next work | Head |
| Open issue → Cancelled | Head | Record the cancellation decision; reconcile affected dependencies and any open PR; cancellation is not successful delivery | Head |

Workers may read their own assignment and PR to perform these handoffs safely; they do not poll the board, create issues, resolve dependency blockers, close issues, or advance other stages. Reviewer owns only assigned review decisions and the two specified outgoing transitions. Head owns all other orchestration.

Reviewing a submitted issue keeps it **In Review**. Do not apply a generic instruction to mark every agent run In Progress: that would falsely signal returned work and trigger the wrong assignee/branch rules.

On a return, reuse the existing issue branch and PR. “Create and check out on In Progress” means ensure the branch exists and check it out; never reset existing history or make duplicate branches on re-entry.

A manual In Review → In Progress change must be reconciled by Reviewer, which restores the original worker. Verify a status-event wake mechanism or Head-triggered reconciliation exists; instructions alone do not guarantee unattended transitions fire. Head may alert/dispatch Reviewer but does not substitute its own review verdict.

### Sources of truth

- **Multica:** issue ownership, lifecycle status, original worker, episode/stage identity, dependencies, blockers, user decisions, and PR association.
- **GitHub:** PR contents, current head SHA, review findings and verdicts, merge state and merge commit.
- **Git main:** accepted content consumed by downstream issues.
- **Markdown:** episode inputs, quoted interview answers, provenance, drafts, user-approved text, edits and cues. A field such as `Interview step: body` may help resume an interview but never indicates review or completion.

Remove numerical scoring, deductions, pass thresholds, and the separate acceptance-criteria framework from the active workflow. Reviewer compares the PR's actual result with the issue's Doneness, while respecting the existing authorship and provenance rules. Do not introduce a replacement scoring scheme or generic stage checklist. PR review and merge remain the evidence of accepted work.

### Issue template and Doneness

Create `templates/issue.md` as a reusable template for Head to populate in Multica's issue description. It is not a per-issue file to save in the episode repository. Include:

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

Retain escalation after three unsuccessful review rounds, recorded in PR reviews/issue history. Reviewer still returns rejected work as required. Head then handles the user decision and can park the issue using Multica's blocker mechanism. No approval override and no repository release-log entry.

### Branch and worktree protocol

1. Read the injected issue identifier, current owner and project resource. Resolve the correct content repository; do not use the profile-source repo for episode work.
2. Inspect `git status`, `git worktree list`, current branch, remote URL, and the runtime resource manifest. Fetch `origin` before choosing a base.
3. For a first start, create `<ISSUE-ID>` from fresh `origin/main`. For a continuation, resume `<ISSUE-ID>` or create its tracking branch from `origin/<ISSUE-ID>` without losing local commits. Verify the Head-provided prerequisite merge is in the base.
4. Stay inside the supplied worktree. Multica-managed branch names are runtime bookkeeping, not PR branch names. Do not rename or delete runtime-owned refs to force compliance.
5. If the issue branch is checked out in another worktree, stop editing and report the collision for Head reconciliation. Never use `--ignore-other-worktrees`, force-reset it, or delete a worktree. Reviewer can inspect the PR SHA detached in its own worktree because review does not edit the issue branch.
6. On every completed content-file write, stage only the issue's intended paths, commit with the issue ID, push the issue branch, and confirm the push succeeded. Keep runtime files, credentials and unrelated memory out of commits.
7. If push fails, retain the local commit, stop further content mutation and report the failure to Head. Do not submit review until published HEAD matches local HEAD. Reconcile an ambiguous push result before retrying; no force push by default.
8. Stop content editing after submission. For requested changes, fetch and resume the same branch; each new revision invalidates approval of the prior head.

The first pilot must verify branch switching and resumption in this deployment's **GitHub repository** worktrees. Public documentation describes additional continuation/cleanup behavior for **local-directory** worktrees, which must not be assumed identical. If runtime cleanup conflicts with exact issue branch checkout, resolve the adapter/runtime behavior before deployment; do not silently relax the naming requirement or introduce a second checkout tree.

### Durable issue identity and PR association

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

### PR submission and review protocol

**Worker:** Verify user-declared stage readiness; finish handoff content; commit and push; find an existing open PR for the issue branch before creating one; enforce `<ISSUE-ID> PR`, base `main`, expected head and scope. Put summary, provenance, a reference to the issue's Doneness and evidence of the result, and relevant validation in the PR. Do not create a separate acceptance-criteria list. Verify linked PR association and original worker before assigning Reviewer.

**Reviewer:** Fetch the linked PR from its actual repository and inspect its current head SHA, full affected artifacts and prerequisites. Do not judge from stale local files, a worker's completion claim, or only a diff that omits required context. Compare the result with the issue's Doneness and respect source attribution and creator approval; do not calculate a score or apply the retired stage rubrics. Explain any missing outcome with a concrete PR location. Use formal Request changes for rejection; do not close the PR. On approval, submit an approval bound to the inspected SHA and merge that exact revision under repository rules. Verify merged state and merge commit before moving to Done and handing back to Head.

**Identity requirement:** Reviewer must have a GitHub identity permitted to review worker-authored PRs and merge them. Distinct Multica agents using the same GitHub author identity cannot provide an independent approval. Validate before the pilot. Do not use an ordinary comment as a substitute for required approval.

**Merge failures:** A conflict, failed required check, outdated approval, changed PR head, or denied merge is not Done. Content corrections return through Reviewer to the original worker; infrastructure/access blockers go to Head. Head cannot override a rejected PR or merge on Reviewer's behalf under the selected design.

**Head:** Confirm the PR merged and its content is present on main; refresh dependency state; release only eligible successors from the new main revision; leave the issue Done after reconciliation. Record coordination actions in Multica issue history so retries do not duplicate dispatch; no extra completion status or repository flag is needed. A downstream assignment must include the expected upstream merge revision. Parent notifications alone are not completion evidence.

### Safe handoff and retry behavior

Use a combined Multica update for status and assignee where supported. The installed CLI exposes the shape:

```sh
multica issue update "$ISSUE_ID" --status in_review --assignee-id "$REVIEWER_ID"
multica issue update "$ISSUE_ID" --status in_progress --assignee-id "$ORIGINAL_ASSIGNEE_ID"
multica issue update "$ISSUE_ID" --status done --assignee-id "$HEAD_ID"
```

These are proposed execution commands, not commands run during planning. Verify server behavior and wake delivery in the pilot. Persist prerequisite metadata and the PR link before performing a handoff. Read back the resulting pair; avoid separate status/assignment calls that wake the wrong agent.

If a response is ambiguous, read current issue/PR state before retrying. Reuse an existing PR and existing review evidence for the same SHA. If merge succeeds but issue update fails, recover the issue handoff from the already-merged PR; do not merge twice. If moving to Done does not wake Head because it is terminal, establish one supported Head notification/rerun mechanism and prove it works. Workers stop after confirmed handoff and do not keep editing.

Only one active content writer per issue is permitted. Metadata is not an atomic lock; validate the runtime's concurrency behavior and have Head reconcile duplicate runs before either can write the same branch.

### Terminal states, aggregate issues, and revisions

**Done and Cancelled:** Done means Reviewer verified and merged the delivered work. Cancelled means Head ended the issue without successful delivery. Head processes the Done handoff without another lifecycle transition. A cancelled prerequisite must not automatically authorize downstream work: Head explicitly decides whether to cancel, rescope, replace, or retain blocked dependents. Native terminal-stage notifications may include cancelled children, so Head must inspect the outcome and merged inputs before dispatch.

**Parent issues:** Keep user-facing episode requests assigned to Head except for their own review. To honor the request that every deliverable issue has a PR, define a meaningful Head-owned parent deliverable: an episode navigation/index artifact referencing the four accepted content artifacts. It contains no pass flags or lifecycle ledger and does not author creative material. Once the stage PRs merge, Head submits the parent index PR through Reviewer like any other worker. Reviewer returns it to Head if needed, or merges and hands it back as Done. Head submits the parent only after its required child deliverables are merged; Reviewer marks the parent Done only after its own PR is merged. Head then reconciles the parent while leaving it Done. Do not manufacture empty commits/PRs for pure status questions. Approve this aggregate-deliverable convention before implementation.

**Revisions:** For unmerged work, use the existing issue branch/PR and Reviewer return path. For a substantive revision after merge, Head creates a linked revision issue with its own ID, branch and PR; accepted history remains immutable. Head marks affected downstream work blocked/superseded in Multica and schedules revised successors against new merge commits. No `.stale-*` file renaming, unticked Pipeline boxes, or history rewriting.

## Alternatives considered

1. **Recommended: issue branches into main with explicit role handoffs.** Matches the user's selected model, makes accepted inputs available between worktrees, and requires no new orchestration service.
2. **Classic Gitflow with develop/release branches.** Adds a separate integration/publication lifecycle; user selected direct-to-main instead.
3. **Stacked stage branches or file-based completion mirrors.** Adds dependency and synchronization complexity; not selected. Creative files remain, but lifecycle mirrors are removed.

## Implementation tasks

### Task 1 — Prove the Multica/GitHub contract before changing profiles

**Files:** Create `docs/validation/multica-pr-workflow.md` as the operator runbook and capability evidence.

- [ ] Confirm use of the built-in `done` and `cancelled` keys; no additional terminal status is needed.
- [ ] Verify project repository/default branch, actual supplied worktree, branch checkout/resumption, and runtime cleanup after a pushed commit.
- [ ] Verify GitHub writer/reviewer identities and repository approval/merge requirements. Required checks must be named; absence of CI is not a passing CI run.
- [ ] Verify native PR association and how its URL is exposed. Establish an actual link and read it back, not just an issue comment.
- [ ] Verify combined status+assignee updates and reviewer/head wake behavior, including terminal Done and a manual return transition.
- [ ] Verify staged sibling notifications for Done and Cancelled, and that cancelled predecessors do not silently release dependent content work. Record supported dependency operations rather than inventing `link`/`unblock` commands absent from the installed CLI.
- [ ] Record pass/fail evidence for each operation. Stop rollout on failures; continue independent documentation work.

**Verification:** A small authorized pilot demonstrates the proposed transitions on this deployment, or documents the exact capability requiring configuration before rollout. No production issue is used to probe unknown status keys.

### Task 2 — Replace the shared workflow and content templates

**Files:** Modify `WORKFLOW.md`; create `templates/issue.md` using the issue template above; modify `templates/01-artist.md`, `02-architect.md`, `03-writer.md`, `04-wizard.md`, `episode-entry.md`; assess `templates/SERIES.md` and `VOICE.md`; retire operational use of `templates/head-log.md`. Add `templates/episode-index.md` only if the parent-deliverable convention is approved.

- [ ] Incorporate existing user edits, then replace abstract states, file gates, and orchestrator candidate tables with the confirmed target contract.
- [ ] Document the authority matrix and narrow own-issue operations for workers/Reviewer.
- [ ] Add the issue template with required Doneness; Head must replace guidance with the concrete intended outcome before creating any issue.
- [ ] Specify first-start, return, submission, review, merge, recovery, Head reconciliation, cancellation, and post-merge revision rules.
- [ ] Remove `Pipeline`, stage `Review Status`, review-log pointers, and lifecycle values from `Phase`. Retain interview progress under a clearly non-authoritative content field.
- [ ] Preserve episode metadata, interview answers, provenance, creator approvals, drafts, editing history and cues.
- [ ] Keep filming/publishing information as content metadata if useful, but never use it to authorize script issue completion.
- [ ] Preserve old review files as historical material; do not delete user evidence. Remove their use from active instructions.

**Verification:** A reader can determine ownership and next action using Multica and PR evidence alone; templates cannot pass a stage by toggling a text field.

### Task 3 — Align the four worker profiles

**Files:** `profiles/{artist,architect,writer,wizard}/{SOUL,AGENTS,SKILLS,STYLE,MEMORY}.md` where relevant; `scripts/profiles.json` descriptions.

- [ ] Replace checkbox prerequisite checks with Head-provided ready assignment and verification that required merged content exists in fetched main.
- [ ] Add issue branch setup before any content edit, and commit/push after each completed write.
- [ ] Replace submit logic with publish → PR create/reuse → verify issue association → In Review + Reviewer handoff.
- [ ] Replace review-log resumption with assigned issue context and PR Request changes against the current branch.
- [ ] Prohibit task creation, global status polling, blocker clearing, closing, or downstream dispatch by workers.
- [ ] Preserve all stage-specific creative and authorship behavior, including direct user interviews and Writer's hook-last sequence.

**Verification:** Each worker completes one submission and one return scenario without checking a Pipeline box or creating a review-log file.

### Task 4 — Align Reviewer and Head roles

**Files:** `profiles/reviewer/{SOUL,AGENTS,SKILLS,STYLE,MEMORY}.md`; all five `profiles/reviewer/rubrics/*.md`; `profiles/head/{SOUL,AGENTS,SKILLS,STYLE,MEMORY}.md`; `scripts/profiles.json`.

- [ ] Retire scoring and all five review rubrics from active loading; preserve historical files as superseded references. Review the issue's Doneness without adding a replacement criteria framework; retain role-level authorship/provenance rules.
- [ ] Replace score-and-log/pass-and-tick operations with inspect PR → Request changes or Approve → verified merge → issue handoff.
- [ ] Require stable original-assignee lookup, correct current SHA, and Head escalation for infrastructure failures.
- [ ] Replace Head filesystem status inference and log-writing commands with native issue/PR inspection and dependency reconciliation.
- [ ] Make Head the only intake/decomposition/scheduling/cancellation owner, with Reviewer exclusively marking merged work Done; record original workers before delegation.
- [ ] Require Head to populate Doneness at creation, clarify ambiguous outcomes, and record scope changes. Reviewer identifies gaps against that section and never changes its meaning to pass a PR.
- [ ] Specify staged sibling issue topology, user-led parking/revision decisions, post-merge revision issues, and parent deliverable treatment.
- [ ] Remove obsolete scoring thresholds and checkbox/log evidence claims from role descriptions and communication examples.

**Verification:** Reviewer cannot mark unmerged work Done; Head cannot treat a checked box as evidence or override a PR rejection; repeated handoffs preserve the original worker.

### Task 5 — Replace behavioral fixtures and validate failure paths

**Files:** Refactor `scripts/make_head_fixtures.py`; update all six `docs/validation/*-walkthroughs.md` and `docs/validation/running-with-hermes.md`; use existing `scripts/test_install_profiles.py`; mark superseded specs in `docs/knowledge/specs/index.md` and plans in `docs/knowledge/plans/index.md`.

- [ ] Change Head fixtures from file-based review histories to sample Multica issue/PR responses plus actual content artifacts. Name fixtures as test data, not a runtime status store.
- [ ] Cover successful four-stage flow, rejection/resubmission, missing original assignee, missing PR relation, push failure, stale approval/new head, merge conflict, failed merge, merged-PR/failed-status-update recovery, duplicate runs and branch ownership collision.
- [ ] Cover no Head wake on Done, repeated Head reconciliation without another status transition, cancelled prerequisites, downstream worktree missing an upstream merge, and a misleading legacy Pipeline checkbox.
- [ ] Verify that changing Markdown completion markers never changes the expected decision.
- [ ] Cover a missing, placeholder-only or ambiguous Doneness section; an exploratory issue with a concrete findings deliverable; a scope change during review; and a PR that claims completion but lacks the stated result. Confirm no score or legacy rubric determines the decision.
- [ ] Verify frequent saves produce corresponding commits/pushes and that a return preserves branch/PR identity.
- [ ] Run `python3 -m unittest scripts/test_install_profiles.py -v`; inspect rendered profiles for correct paths and shared workflow references.
- [ ] Run the live pilot only after Task 1 prerequisites and test issue scope are established; retain issue/PR links and commits as evidence.

**Verification:** Behavioral walkthroughs pass with real content in separate worktrees, including at least one Request changes → worker revision → approved merge cycle. Installer tests alone do not prove orchestration.

### Task 6 — Deploy consistently and reconcile existing work

**Scope:** Profile source repository; installed Hermes profiles; Multica agent instructions/attached skills; shared workflow/templates/knowledge in the channel repository. Actual content repository paths must be inspected before editing.

- [ ] Head schedules a controlled cutover between active runs; capture current issue ownership, branches, PRs and instruction versions.
- [ ] Publish the approved source changes through an issue branch and reviewed PR. Preserve unrelated changes and live memory/configuration.
- [ ] Deliver shared workflow/templates/knowledge to `delongpa-channel` through its own reviewed PR. Avoid assuming the profile repository is available in an episode worktree.
- [ ] Reinstall all six Hermes profiles with configuration and bundled-skill changes disabled, using the existing installer and backups.
- [ ] Update the matching six Multica instruction/skill copies from the same source revision; compare rendered/embedded instructions and verify runtime profile selection.
- [ ] Have Head reconcile PERS-14 through PERS-18 against actual branches, content, PRs and parent relationships. Do not pass or close anything solely from its current board label. Recover historical artifacts through normal branches and review if needed.
- [ ] Have Head populate Doneness on existing issues from their actual scope before resuming them under the new workflow.
- [ ] Start one episode pilot; verify user intake goes to Head and each accepted stage appears in the next worker's fetched main.
- [ ] Record rollout evidence in the migration issue/PR, not a new per-episode completion file.

**Rollback:** Head stops new dispatch and records the blocker; preserve pushed branches, PRs and issue history. Restore the last coherent instruction bundle if needed, without deleting accepted content, resetting branches, or reviving file-based completion as authoritative.

## Planning verification and unresolved deployment checks

This plan was checked against all nine numbered requirements (the request repeats number 4), the confirmed merge owner, and the selected branch model. No live issue, assignment, PR, branch, installed profile or active workflow was changed during planning.

Implementation is conditional on resolving: PR association behavior, GitHub reviewer identity, exact branch behavior in GitHub-repository worktrees, and reliable wake/dispatch behavior. These are explicit capability checks in Task 1, not assumed supported APIs.

Scoring and the separate acceptance-criteria framework are removed from this proposed workflow; Doneness in the issue description defines the intended result. The remaining design proposal requiring review is a meaningful episode index PR for the Head-owned parent. The requested operational plan is complete as a reviewable draft; it has not been deployed.

## Sources

- Local: `WORKFLOW.md`, all role procedures, `profiles/reviewer/rubrics/scoring.md`, templates, installer tests and Head fixtures.
- Read-only Multica CLI: project/resource listing, project issue snapshot, agent identities, workspace/property inspection and command help.
- [Multica issues](https://multica.ai/docs/issues): built-in/custom statuses and staged sub-issue behavior.
- [Multica project resources](https://multica.ai/docs/project-resources): repository resources and worktree behavior; distinguish local-directory details from GitHub repository execution.
- [Multica GitHub integration](https://multica.ai/docs/github-integration): automatic PR association and close-intent merge behavior.
- [GitHub required reviews](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews): authors cannot approve their own PRs.
