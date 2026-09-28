---
type: "validation"
title: "Multica PR workflow: capability evidence and cutover runbook"
description: "Validation source for scriptwriting: docs/validation/multica-pr-workflow.md."
tags: ["scriptwriting", "docs"]
source_path: "docs/validation/multica-pr-workflow.md"
---

# Multica PR workflow: capability evidence and cutover runbook

## Current disposition

**Profile alignment deployed on 2026-09-27; full episode rollout still gated by the pilot below.**
See the dated deployment addendum below. The original 2026-09-22 observations are retained as
history, not a description of the current installed instructions. This document records observed capability
and explicit gaps. It is not episode lifecycle state. Evidence was collected on 2026-09-22 from
source baseline `486c402`, branch `multica-pr-workflow`. The approved target is the
[migration plan](../superpowers/plans/2026-09-22-multica-issue-pr-workflow.md).

During the original 2026-09-22 implementation, no live issue was mutated, no profile was installed,
and no production run was dispatched. A completed installer or fixture test is not a successful orchestration pilot.

## 2026-09-27 profile alignment deployment

The user authorized fixes 1–3 from the profile/run audit. The deployment command completed
successfully for all six roles at content revision `ff79e9f10b63bcca4a62`. Its final fresh
readback reported: `PASS: all six profiles, remote prompts/skills, runtime mappings and channel workflow agree.`
All six deployment receipts contain that revision; no deployment-pending markers remain.

- Canonical rendered instructions and templates were installed with `--no-config --no-bundled-skills`.
  Multica embedded procedures were replaced with short installed-bundle bootstraps, and the existing
  assigned role skill IDs were updated in place. No production episode run was dispatched.
- Exact agent/runtime/profile/launcher mappings were verified. The installed guard checks actual
  `HERMES_HOME`, launch overrides, executable and instruction hashes, remote prompt/skill content,
  and the assigned checkout's workflow before content work. Head checks the target before dispatch.
  Failed or interrupted deployments leave every role blocked until complete verification.
- The Architect's existing sourced-draft instructions now reach both local and remote instruction
  surfaces. The outdated mandatory interview-pass walkthrough was corrected.
- The complete Python suite passed **102 tests**, including **16 deployment tests**. Independent
  review identified partial activation and unchecked launcher drift; both received failing
  regression cases and fixes before deployment.
- Backup: `/private/tmp/scriptwriting-deployment-20260927/before.json`. Test output:
  `/private/tmp/scriptwriting-deployment-tests.log`. These local paths are operator evidence,
  not portable repository artifacts.

An isolated local Hermes Architect one-shot exited successfully. It identified itself as Architect,
accepted a sourced setup draft without another three-pass interview, and kept missing tension open
while continuing independent work after one clarification. However, its sample changed the supplied
answer ID `A1` to `A1.1`, and its draft wording broadened the source slightly. Thus the two targeted
workflow decisions were observed; citation fidelity and overall creative quality did not receive a
clean pass. Output: `/private/tmp/scriptwriting-architect-smoke/result.log`. The supplied role skill
was included in this diagnostic prompt; this was not a new Multica issue, a test of generated workdir
instructions, or an end-to-end production pilot.

The supplied PERS-16 channel checkout's WORKFLOW.md was synchronized while preserving its preamble
and unpublished episode outline. That workflow change is **local and uncommitted**; publishing it to
channel main and refreshing other worktrees remains a normal reviewed change. Older checkouts will
fail the new workflow drift check until updated. Existing run contexts are not rewritten; start a new
run to receive the new Multica bootstrap. No PERS-14–18 lifecycle reconciliation, PR association,
merge/wake pilot, or production restart was performed. Those gates remain open.

## 2026-09-28 recovery and legacy reconciliation

The user authorized audit fixes 4–6. See [progress/handoff/migration evidence](progress-handoffs-legacy.md)
for instruction changes, recovered historical PR evidence, administrative issue reconciliation and
remaining release gates. The earlier snapshots below remain historical observations.

## Capability evidence

| Check | Actual observation | Disposition |
|---|---|---|
| Terminal statuses | Public Multica issue docs specify built-in `done` and `cancelled` as terminal; installed CLI accepts status keys as strings. Existing PERS-15 readback is `done`. No production probe used. | Contract confirmed; no new status needed. |
| Project resource | `multica project resource list cd7092b1-5ccd-4444-9334-6346c91f10bf --output json` returned GitHub repository `https://github.com/jdelon02/delongpa-channel`, resource `d600497e-7c05-4827-9ce3-ddf154e78528`. | Repository mapping verified; subsequent gh recheck confirms main. |
| Agent directory | Readback matches all six UUIDs in WORKFLOW.md. All six reported idle and max_concurrent_tasks=6. | Mapping verified; idle is a snapshot, not a concurrency lock or cutover guarantee. |
| GitHub authentication | `gh auth status` after user login confirms jdelon02 via keyring outside the sandbox; repository API calls succeed. Composio remains unconnected. | RESOLVED: use the user-selected gh connection. No agent-specific accounts. |
| Shared GitHub account | User explicitly requires all agents to use their account and all commits to be attributed to them. Local author is Jeremy DeLong <chefjeremy@delongaz.com>. | Separate-account requirement removed. Reviewer records SHA-bound agent verdict comments; correlate its run in Multica before merge. |
| Default branch, protections, checks | Both repos use main, with protected=false and no active rulesets. Channel has zero Actions workflows. | No configured formal-review gate observed; no CI run claimed. Recheck actual PR requirements before merge. |
| Native PR association | `multica issue pull-requests PERS-15 --output json` returned `{"pull_requests": []}`. CLI provides readback but issue update has no PR URL flag. | No link demonstrated. Empty relation alone does not prove integration is disabled; verify using a test PR. |
| Combined status/owner update | `multica issue update --help` exposes `--status`, `--assignee-id`, `--no-start`. | Syntax verified; server atomicity and wake delivery NOT TESTED. |
| Staged siblings | `multica issue create --help` exposes `--parent` and `--stage`; docs describe parent wake after all staged children are Done or Cancelled. | Syntax/documented behavior only; cancelled input handling must be proven in pilot. |
| Head wake on Done/manual return | `multica issue rerun --help` exists; no terminal-state rerun/wake test executed. | NOT VERIFIED; no fallback is yet approved as operational. |
| Runtime worktree/cleanup | This is the source checkout, not an injected content task. No GitHub-resource worktree switched/resumed/cleaned up. | NOT VERIFIED; exact issue branch and cleanup are pilot gates. |
| One active writer | Per-agent concurrency limit is six; same-issue branch serialization not observed. | NOT VERIFIED; duplicate-run and branch-collision cases must be exercised. |

### Authentication recheck after user login

`gh auth status` succeeded outside the sandbox as `jdelon02` using the macOS keyring. The sandboxed
check misleadingly reported an invalid token; no re-login is needed. GitHub API readbacks confirm
admin/push/pull access to both `jdelon02/scriptwriting` and `jdelon02/delongpa-channel`, each with
`main` as its default branch. Both main branches report `protected: false`, and both repositories
return no active rulesets. The channel repository has zero Actions workflows and no open PRs.
These observations do not constitute a passing CI run or a native PR-association test.

Composio remains unconnected, but the user-selected `gh` path works. The user clarified that all
agents share `jdelon02` and commits must use their identity; a separate Reviewer account is no longer
a prerequisite. GitHub disallows formal self-approval, so the workflow uses explicit agent verdict
comments with SHA, Reviewer UUID and run correlation. This preserves separate agent responsibilities
without inventing another GitHub identity. Remaining gates are native linking/wake/worktree pilot
behavior and coherent deployment. No live mutation was performed during the authentication recheck.


## Existing work snapshot

`multica issue list --project cd7092b1-5ccd-4444-9334-6346c91f10bf --output json` (selected fields):

| Issue | State | Owner | Parent / stage | Metadata |
|---|---|---|---|---|
| PERS-14 | in_progress | Head | none / none | empty |
| PERS-15 | done | Reviewer | none / 1 | empty; native PR list empty |
| PERS-16 | in_progress | Architect | 01a0c5ab-a9ec-7e4a-864b-c6dc6a5c4df1 / 2 | empty |
| PERS-17 | in_progress | Writer | 01a0c5ab-dabd-7e0c-ba37-778bdbde7852 / 3 | empty |
| PERS-18 | in_progress | Wizard | 01a0c5ab-ef81-7f2a-91a0-0d7849f53ddc / 4 | empty |

Head must read full descriptions/history and actual branches/artifacts before populating Doneness
or changing relationships. Neither these labels nor missing content in the profile repository proves
the creative work is complete or absent. Preserve existing history; no speculative correction was made.

## Profile comparison before migration

The prior read-only comparison used the installer's actual renderers. Artist/Architect/Writer had
matching SOUL, STYLE and skill outputs, but stale AGENTS assignment rules. Wizard also had a minor
SOUL wording difference. Head and Reviewer differed across AGENTS/SOUL/STYLE/skills. All five rubric
files matched before retirement. Five memory templates matched; Head learned memory differed and
must be preserved. Both root SKILL.md and MEMORY.md were symlinks for all six profiles.

At the 2026-09-22 source migration, installed instructions remained on their old version pending
controlled cutover. The 2026-09-27 addendum supersedes that deployment status.

## Offline source verification

- Full suite: 47 tests passed (`python3 -m unittest discover -s scripts -p 'test_*.py' -v`).
- Generated and parsed all 31 scenario packages with operator-only expected actions isolated from
  agent observations; all six revised profiles rendered without source-profile path leaks.
- Independent review found two source gaps: structural requests lacked an explicit Head notification
  route, and fixtures had contradictory stage states. Both were corrected. Seven fixture regression
  cases and one installer operator-guidance case were observed failing before their fixes, then passing.
- Writer/Wizard structural requests now flow through published quotation → own-issue notification →
  Head's recorded user decision → revision/blocking and successor checks. This was manually traced in
  source and added as a walkthrough, not represented as live behavioral execution.
- Historical creative procedures and walkthrough content were preserved. `git diff --check` passed.

The user's single-account correction is covered by a fixture regression proving both actors share
a GitHub account while verdict comments retain distinct Reviewer run evidence (observed RED→GREEN).

The review also identified installer launch guidance and expected-answer leakage; both were fixed
because they could misdirect deployment or invalidate behavioral evidence. No review findings are
being deferred as minor polish. Live capabilities and deployment remain explicitly unverified.

## Safe capability pilot (not yet executed)

1. Verify the shared gh account is jdelon02 in the actual worker/Reviewer runtimes and effective Git
   author/committer identity is the user's. Read repository merge permissions, rulesets and required
   checks. Use SHA-bound agent verdict comments, not formal self-approval; if rules require formal
   GitHub approvals, report the conflict instead of silently changing rules or requesting an agent
   account. Verify Multica integration authorization includes the source and content repositories.
2. Head defines isolated test scope in a dedicated test episode/issue family. Test content is explicitly
   synthetic and cannot modify real episodes. Use one Head parent and four staged siblings, initially
   backlog so creating/assigning them does not dispatch unknown work. Populate Doneness and durable
   identity metadata before moving eligible work out of backlog.
3. In the supplied GitHub-resource worktree, verify exact issue branch creation from fetched main,
   per-save commits/pushes, branch resumption across runs, worktree ownership and cleanup after push.
   Preserve runtime refs and uncommitted work; stop on collisions rather than making another checkout.
4. Create `<ISSUE-ID> PR` into main using that branch, without close-intent phrases. Read
   `multica issue pull-requests <id> --output json` and the issue UI's PR field. Verify the exact PR
   URL/repository/branch appears in the native relation. If absent, fix supported integration/API
   configuration; do not claim success from metadata or a comment.
5. Exercise a worker → Reviewer combined status/owner handoff and read back both plus the new run ID.
   Reviewer posts a changes-requested agent verdict comment at the actual head, returns to original worker, then worker
   resumes the same branch/PR, publishes the revision and resubmits. Also test a manual status-only
   return and prove Reviewer/Head reconciliation wakes the proper original worker.
6. Reviewer posts an approved agent verdict comment with inspected SHA, issue ID, agent UUID and run
   ID, records its comment reference in issue history, and merges that exact head under repo rules. Verify merge
   state/commit, then sets Done + Head together. Prove Head wakes and reconciles while leaving Done
   unchanged. If terminal assignment does not wake Head, validate a supported rerun/notification
   mechanism on the test scope; do not assume CLI help proves terminal delivery.
7. Repeat reconciliation and prove no duplicate successor dispatch. Verify the successor's fetched main
   contains the expected upstream merge. Repeat through all four stages and the meaningful parent-index
   PR. Record exact PR/head/merge identities and issue owner/status readbacks at every boundary.
8. On separate test cases, exercise cancelled staged siblings, push failure, missing original assignee,
   missing PR association, duplicate runs, branch collision, new head after approval, merge/check failure,
   and merged-PR/failed-handoff recovery. Alter only historical Markdown markers and show decisions
   remain unchanged. Run missing/placeholder/ambiguous Doneness, scope change, exploratory findings,
   and missing-result cases. Keep expected and observed results separate.

Record all operation outcomes and links in the migration issue/PR. Stop rollout on any failure;
continue independent source validation. Test transitions never use production issues as probes.

## Publication and coherent deployment

This is the original cutover checklist. The 2026-09-27 addendum records the completed profile
alignment; publication, episode reconciliation and the capability pilot remain separate gates:

1. Head schedules cutover between active runs, stops new dispatch, and snapshots issue ownership,
   branches/PRs, instruction versions, agent runtime/profile selection and attached skill IDs.
2. Head creates a migration deliverable issue for this source change. Publish the source branch under
   that issue's exact ID and reviewed PR convention. The local `multica-pr-workflow` branch is a
   preparation branch, not a fabricated Multica issue identifier. No force push or direct main push.
3. Deliver WORKFLOW.md, templates/, knowledge/ and docs/validation/multica-pr-workflow.md to the actual
   channel checkout through its own reviewed PR. Inspect that checkout first; preserve user content.
4. Back up managed instructions/supporting files for all six installed profiles; record hashes of
   existing memory/config without displaying secrets. Install from the reviewed source revision with
   `python3 scripts/install_profiles.py --no-config --no-bundled-skills`. Do not refresh config.
5. Update all six Multica embedded instruction and attached skill copies from that same source revision;
   read them back and compare. Confirm each runtime selects the corresponding script profile. Compare
   installed AGENTS/SOUL/STYLE/skill files with rendered output, including symlink targets. Verify live
   memory, config, credentials and unrelated skills stayed unchanged.
6. Head reconciles PERS-14..18 from real issue history, content and PRs, adds Doneness from actual scope,
   records original workers, and resolves parent/prerequisite representation. Existing Done is not merge
   evidence. Recover historical work through normal branches/review; never fabricate an empty PR.
7. Resume only after the pilot/capability evidence and coherent bundle checks pass. Record accepted
   revision and rollout evidence in the migration issue/PR, not an episode completion file.

## PERS-19 audit correction — 2026-09-28

PERS-19 is historical Done with PR `jdelon02/delongpa-channel#8`, head
`796d1524edc03e4cad6d6d9919097ea9f88c07b9`, merge
`a0e4c81f387dcd17b1ea247f303287245327c178`. Its native PR association and independent
Reviewer inspection succeeded. It did **not** pass the complete workflow pilot:

- Head run `01a0e80a-3f26-7725-819c-80c868522d8f` instructed Reviewer not to merge.
- Reviewer run `01a0e814-6d1e-764d-b942-9d9695d9eb0b` posted an issue-thread verdict only.
  GitHub had no agent verdict comment; CodeRabbit reported success but skipped its review.
- Head merged without the expected-head guard, then separately assigned Head and set Done.
  No Reviewer-to-Head mention or correlated receiving Head run established the return path.
- Head's "all seven gates passed" and production release claims exceeded the evidence.

Preserve this history. A new isolated linked pilot must exercise the missing boundaries under
WORKFLOW.md **Completion reports and capability evidence**. Do not count operator repairs as agent
behavior or turn a narrow successful pilot into proof of untested runbook cases. PERS-15's absent
native association remains a separate unresolved gate until supported repair or explicit user decision.

## PERS-20 follow-up evidence — 2026-09-28

Channel PR #10 merged at `9e9ee92a46759368a7e5ac522460b32d499c52b9`, head
`8c2580675aa27f8224e697a9bd59256d927ea38a`. Reviewer run
`01a0e83f-5830-77ad-b302-f8286c84460f` posted GitHub verdict comment `5871133519` and
merged with the expected-head guard; merge author attribution is correct. However, it wrote the
worktree label `pers-20-f8286c84460f` as its run ID, missed operator finding `5871054937`, and
used the legacy-audit parent return route for a normal pilot. PERS-14 received Head run
`01a0e844-65f6-7b0e-803e-5a37d1779593`; PERS-20 had no normal receiving Head run at that boundary.
Reviewer subsequently failed with provider 503 after the merge and notification. Preserve those
side effects and the historical Done state. This partial result does not satisfy the corrected
pilot or authorize production release. Provider diagnosis remains outside this recovery scope.

## Rollback

Head stops new dispatch and records the blocker. Preserve pushed branches, PRs, accepted commits,
issue history and learned memory. Restore the last coherent instruction bundle if needed; do not
reset content history, delete worktrees, or restore Markdown completion fields as authoritative.

## Sources and evidence limits

- [Multica issues](https://multica.ai/docs/issues): built-in status meanings and staged terminal notifications.
- [Multica GitHub integration](https://multica.ai/docs/github-integration): native PR linking and close-intent behavior.
- [Multica project resources](https://multica.ai/docs/project-resources): repository worktree context; local-directory behavior is not assumed identical.
- [GitHub required reviews](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews): GitHub self-approval limitation; agent verdict comments do not claim formal approval.
- Local CLI help/readbacks described above. Documentation and CLI syntax are evidence of a contract,
  not proof of successful live transitions on this deployment.
