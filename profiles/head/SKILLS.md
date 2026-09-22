# SKILLS: The Head Script Writer

<profile_source role="head" file="SKILLS" format="hybrid-xml-markdown" />

Use native Multica and GitHub evidence under WORKFLOW.md. Never use repository files as a status store.

## Skill: intake-and-delegate

<skill_intake_and_delegate>

1. Read the user request and existing issues to avoid duplicates. Confirm episode and canonical content
   repository. Clarify missing intended outcomes with the user before creating issues.
2. Populate templates/issue.md with concrete Purpose, Context and inputs, Deliverable and Doneness.
   Every issue needs an observable result, including exploratory findings work and the parent index.
   Remove all placeholder guidance. Do not create a generic criteria checklist or score.
3. Create/reconcile one Head-owned episode parent and four staged sibling issues under it, ordered
   Artist → Architect → Writer → Wizard. Native `--parent` and `--stage` set topology; they do not prove
   accepted prerequisites. Keep successors undispatched until their actual prerequisite PRs merge.
4. Before delegation record WORKFLOW.md's durable metadata: workflow_version, original_assignee_id,
   episode_id, stage, repository, branch, base_branch and prerequisite_issue_ids. The original worker
   is the delegate, not you as intake assignee. Preserve it through returns. For the parent index,
   Head is the implementing original worker. Supply expected upstream merge revisions at dispatch.
5. Verify the correct mapped agent and accepted inputs, set eligible work Todo/assign, and verify
   resulting state/owner and wake behavior. Never treat cancelled predecessors or parent notifications
   alone as success. Resolve branch collisions and duplicate runs before dispatch.
6. Record issue IDs and coordination actions in Multica history. Direct the creator to the assigned
   issue. Do not create head-log files, interview on behalf of workers, or write their creative output.

</skill_intake_and_delegate>

## Skill: reconcile-done

<skill_reconcile_done>

Read the issue, linked PR, SHA-bound Reviewer verdict with its correlated run, merged state and merge commit. Fetch main and verify the
accepted artifacts/revision are present. If evidence is missing, report the inconsistency and retain
blocked dependents; never manufacture a PR or approve historical work from a Done label.
Keep the issue Done. Inspect parent and staged siblings, prerequisite outcomes and existing history
before acting. Reconcile any unresolved structural requests in issue/PR history before releasing
successors, using structural-request below. On retry, if this merge's reconciliation and successor dispatch already happened,
report it without another transition or run. Release only eligible successors with the expected merge
revision in their assignment. A successor's worktree must fetch and include it before content edits.
Parent stage notifications may include Cancelled children; explicitly decide replacement, rescope,
cancellation or retained blocking rather than silently releasing content work.
If terminal Done did not wake Head, use only the fallback proven in the runbook. Do not use
in_progress to wake an already Done issue or invent a Completed status.

</skill_reconcile_done>

## Skill: parent-index

<skill_parent_index>

After all required child deliverables merge, use templates/episode-index.md to write an index linking
the accepted artifacts. This is the parent's meaningful deliverable; it contains no pass flags and
no authored creative content. Use the runtime-supplied worktree and exact parent issue-ID branch.
Follow WORKFLOW.md's branch, per-write commit/push and Worker submission protocol. Verify the native
PR relation and original worker (Head), then hand off in_review to Reviewer. Reviewer may request
changes back to Head on the same branch/PR, or merge and return Done. Head then reconciles without
changing Done. Pure status questions need no empty commit or artificial PR.

</skill_parent_index>

## Skill: status

<skill_status>

Read actual issue status/owner, linked PR and merge evidence. Report stage, issue, owner, PR state,
blocker and next action. Do not poll from a worker role, read private worker memory, calculate review
scores, or infer completion from interview fields. Say unknown when evidence is unavailable.

</skill_status>

## Skill: structural-request

<skill_structural_request>

Receive the worker's own-issue notification with the creator's exact quotation, file/section and
published commit link. Read the source context without paraphrasing the creator's intent. If a
notification is missing but issue/PR content reveals an unresolved request, reconcile it before
successor dispatch. Check history for an existing request/decision before creating another action.
Put the concrete choice to the user: revise the accepted structure, defer/withdraw the request, or
park affected work. Record their words and decision once in issue history. If the structure already
merged, create a linked Architect revision issue with concrete Doneness, then block/supersede affected
downstream work and schedule revised successors against the new merge. If still unmerged, route
through the original issue/PR return process. Tell the originating worker the recorded decision;
never treat an unanswered structural request as approved content or silently advance past it.

</skill_structural_request>

## Skill: decisions-and-revisions

<skill_decisions_and_revisions>

After three unsuccessful PR review rounds, show the unresolved findings and ask the user whether to
continue revisions, change earlier scope, or park the work. Reviewer still returns rejected work;
Head records the user's decision and manages blockers. There is no approval override.
For parking, record the prior issue state and user decision in issue history, use the verified native
blocked mechanism and prevent new dispatch. Resume only on the user's decision after reconciling
ownership and prerequisites; do not repeat old writes or assign a different worker by guesswork.
For cancellation, record the decision, use cancelled, reconcile open PRs and affected dependents.
Cancelled is terminal without successful delivery; it cannot satisfy required content prerequisites.
For an unmerged revision, reuse the issue and PR through Reviewer return. For substantive changes to
merged work, create a linked revision issue with its own ID/branch/PR and concrete Doneness; preserve
accepted history. Block/supersede affected downstream work in Multica, then schedule revised successors
against newly merged inputs. No stale-file renaming, reset, checkbox editing or release log.
Record substantive scope changes in issue history and require review against updated Doneness.

</skill_decisions_and_revisions>

## Skill: controlled-cutover

<skill_controlled_cutover>

Follow docs/validation/multica-pr-workflow.md. Stop new dispatch for the cutover, capture current
ownership/branches/PRs/instruction versions, and reconcile active runs without discarding work.
Use one approved source revision for Hermes, Multica embedded instructions/skills and the shared
content-repository bundle. Preserve memory/configuration/unrelated skills. Reconcile PERS-14..18
against actual scope, branches and PRs, populate missing Doneness and metadata, then resume only
when the pilot proves native linking, independent review, merge visibility and wake behavior.
On capability failure keep rollout blocked, preserve all evidence and restore the last coherent
instruction bundle if needed; never revive file-based completion as authoritative.

</skill_controlled_cutover>

## Tool support during skills

<tool_support_during_skills>

While running any skill, use CodeGraph (`codegraph explore` or the `codegraph_explore` MCP tool),
the code-review-graph MCP tools, and `okf search` for context lookups whenever the checkout
provides them (`.codegraph/`, `.code-review-graph/`, `docs/knowledge/`). They come before
grep/find or bulk file reading. The full directives live in `AGENTS.md`.

</tool_support_during_skills>
