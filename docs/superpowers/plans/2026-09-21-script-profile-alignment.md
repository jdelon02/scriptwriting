---
type: "plan"
title: "Scripting Profile Alignment Implementation Plan"
description: "Plan source for scriptwriting: docs/superpowers/plans/2026-09-21-script-profile-alignment.md."
tags: ["scriptwriting", "docs"]
source_path: "docs/superpowers/plans/2026-09-21-script-profile-alignment.md"
---

# Scripting Profile Alignment Implementation Plan

**Goal:** Correct the six scripting source profiles and reinstall without losing live state.
**Architecture:** Source profiles remain authoritative. Use the existing Hermes renderer and installer;
SKILLS.md becomes SKILL.md, source paths become profile-home paths, and live memory stays untouched.
**Tech stack:** Markdown and the existing Python installer.
**Spec:** User-approved five-step plan in this session.

## Constraints
- Only the six scripting profiles are in scope.
- Preserve live memory, configuration, credentials, and unrelated skills.
- Preserve user-led content, independent review, and the 70 percent gate.

## Tasks
- [x] Correct Reviewer memory boundaries, four-stage checks, and escalation routing.
- [x] Reconcile Architect open-element progression and neutral Artist acknowledgements.
- [x] Add role-specific context loading and informational-request exceptions to all six source SOUL files.
- [x] Run existing installer tests and inspect rendered source output.
- [x] Back up managed installed files, reinstall with config and bundled-skill changes disabled.
- [x] Compare installed output against rendering and verify live-state preservation.

## Verification
33 installer tests passed. All six installed profiles match source rendering; skill and memory links resolve. Live memory, configuration, credentials, and unrelated skills were unchanged. Backups: each profile state-snapshots/20260921-222125-profile-alignment/. No commits or publication performed.
