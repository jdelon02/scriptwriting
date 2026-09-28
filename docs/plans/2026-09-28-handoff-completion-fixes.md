---
type: plan
title: Repair completion evidence and return handoffs
description: Tasks and verification for the PERS-19 pilot audit findings.
tags: [scriptwriting, workflow, recovery]
---

# Repair completion evidence and return handoffs

Scope: implement the five findings from the PERS-19 audit. Preserve episode content,
existing merged history and creator approvals. Provider diagnosis/configuration is excluded.

## Tasks

- [x] Update WORKFLOW.md and affected profiles: Head cannot override Reviewer merge ownership;
  an issue-only verdict, Head polling, or Head merging cannot pass the return-handoff pilot.
- [x] Define evidence required for each pilot boundary and distinguish partial success from
  verified capabilities. Leave untested scenarios and legacy exceptions explicitly unresolved.
- [x] Require current owner/status/gates in final reports and concrete creator requests or
  verified Head notifications when a worker needs a decision.
- [x] Validate the initial fix, synchronize knowledge, review the diff, publish source and
  channel instructions, deploy all six profiles, and verify worktree contracts.
- [ ] Reconcile PERS-14/15/16/19 without rewriting accepted history or fabricating approvals.
  Correct pilot claims, preserve recovered Architect content, and retain unresolved release gates.
- [ ] Execute a new isolated pilot with a real Reviewer PR verdict, guarded Reviewer merge,
  Done/Head transfer, actual Head mention and correlated receiving run; verify safe repeat
  reconciliation without duplicate dispatch. Record precisely which wider cases remain untested.
- [ ] Route Architect's remaining creator choices into a concrete next interaction after
  prerequisite reconciliation; do not re-ask recorded content or invent legacy exceptions.
- [ ] Publish and deploy the follow-up found by PERS-20: resolve full run UUIDs from Multica,
  read all PR findings before merge, and return normal reviews on the reviewed issue itself.

## Verification

Source PR #6 merged as `2d671788b1f9f26278d5725eb49442436fe81791`; channel PR #9 merged
as `44ce2ffd3dbb81bd00c2c22b67c25951254c5b46`. Deployment `1d983afe0e00bd1d5350` passed
all six role, remote skill/prompt, runtime mapping and workflow checks. Forty installer tests passed;
source knowledge validation passed (two existing mention-URI warnings). Independent source review
found no blocking issues. Channel sync exposed preexisting missing frontmatter in the PERS-19
synthetic document; the follow-up pilot must repair it before claiming documentation validation.

The user explicitly approved a one-time PERS-15 native-link exception, conditional on corrected
pilot success. This is recorded in PERS-15 metadata; new submissions still require native linking.
PERS-16 is parked Blocked/Architect with recovery commit `849c1e0` preserved. PERS-19 remains
historical Done/Head with `capability_pilot_result: partial-failed-contract` and concrete evidence.

PERS-20 / channel PR #10 reached a real Reviewer verdict and guarded Reviewer merge
`9e9ee92a46759368a7e5ac522460b32d499c52b9` (head `8c2580675aa27f8224e697a9bd59256d927ea38a`).
Reviewer run `01a0e83f-5830-77ad-b302-f8286c84460f` used a worktree label in its verdict,
missed operator finding `5871054937`, and notified PERS-14 rather than PERS-20. The parent received
Head run `01a0e844-65f6-7b0e-803e-5a37d1779593`; that is not a same-issue return receipt.
Reviewer then failed with a provider 503 after its side effects. User merge attribution was verified
correct. PERS-20 is partial evidence, not a passed pilot; do not release production from its Done label.

Run installer tests, installer preview, knowledge sync/validation and coherent deployment checks.
For live behavior, retain issue/run/comment IDs and GitHub PR/head/merge evidence. An instruction
change is not proof of a successful live transition. PERS-19 stays historical Done, with a correction
record; no retrospective Reviewer approval or second merge. The new pilot is a linked follow-up.
