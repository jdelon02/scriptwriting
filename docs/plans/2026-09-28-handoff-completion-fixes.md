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
- [ ] Validate rendered profiles, synchronize knowledge, review the diff, publish source and
  channel instructions, deploy all six profiles, and verify worktree contracts.
- [ ] Reconcile PERS-14/15/16/19 without rewriting accepted history or fabricating approvals.
  Correct pilot claims, preserve recovered Architect content, and retain unresolved release gates.
- [ ] Execute a new isolated pilot with a real Reviewer PR verdict, guarded Reviewer merge,
  Done/Head transfer, actual Head mention and correlated receiving run; verify safe repeat
  reconciliation without duplicate dispatch. Record precisely which wider cases remain untested.
- [ ] Route Architect's remaining creator choices into a concrete next interaction after
  prerequisite reconciliation; do not re-ask recorded content or invent legacy exceptions.

## Verification

Run installer tests, installer preview, knowledge sync/validation and coherent deployment checks.
For live behavior, retain issue/run/comment IDs and GitHub PR/head/merge evidence. An instruction
change is not proof of a successful live transition. PERS-19 stays historical Done, with a correction
record; no retrospective Reviewer approval or second merge. The new pilot is a linked follow-up.
