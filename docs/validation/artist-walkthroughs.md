---
type: "validation"
title: "Artist profile: migration walkthroughs"
description: "Validation source for scriptwriting: docs/validation/artist-walkthroughs.md."
tags: ["scriptwriting", "docs"]
source_path: "docs/validation/artist-walkthroughs.md"
---

# Artist profile: migration walkthroughs

Status: **not run with a live agent**. Installer/fixture tests do not prove these behaviors.
Use [running-with-hermes.md](running-with-hermes.md) for isolated setup and
[multica-pr-workflow.md](multica-pr-workflow.md) for the live pilot/cutover gate.

## Creative and role behavior

- Cold start: with an assigned ready issue, ask title, tagline, theme and audience separately; record the exact words and publish each completed write.
- “You pick” or “make something up” produces a smaller open question, never invented content.
- Preserve weak/off-topic dump entries without judgment or paraphrase. Nominate payoff candidates only from existing entries; the creator chooses.
- Resume recorded interview answers without repeating them, but obey external issue state and ownership.
- Handoff preserves the chosen payoff, rationale and source entries; only the user declares readiness.

## Issue/PR scenarios

Generate each scenario in a new empty directory using `scripts/make_head_fixtures.py`, with
`--stage 1` where applicable. These are synthetic normalized observations, not complete API
responses. An operator supplies them as tool observations to an isolated agent with remote actions
disabled. Substitute only the synthetic test_agent_directory for production IDs; the actor field
names the primary actor, with other roles exercised at the subsequent handoff. Record actions and
compare them with the operator-only oracle below. This offline behavioral
exercise does not prove deployment API behavior. Historical creative cases remain under `historical/`;
use the current issue-based setup and do not execute their obsolete lifecycle instructions.

| Scenario | Expected behavior | Execution evidence |
|---|---|---|
| `ready` | Assigned worker verifies accepted prerequisites and exact branch in the supplied worktree before interviewing. | Not run |
| `submission` | Worker publishes every save, creates/reuses the exact issue PR, verifies native association, then hands In Review to Reviewer. | Not run |
| `return` | Worker reads the SHA-bound changes-requested Reviewer verdict comment, resumes the same issue branch/PR, asks the creator, and publishes approved revisions. | Not run |
| `push-failure` | Keep the local commit, stop further content mutation, report to Head; no review submission. | Not run |
| `missing-pr-link` | No handoff or completion; native association must be established and read back. | Not run |
| `frequent-saves` | Verify one successful commit/push per completed write before the next question; preserve history on resume. | Not run |
| `legacy-marker` | Ignore both checked and unchecked legacy markers. Artist follows its own assigned In Progress state; later stages cannot proceed with an unmerged predecessor. | Not run |

## Required live evidence

After capability gates pass, run this role in a separate runtime-provided worktree using test issues
and the shared user gh account and distinct worker/Reviewer agent roles. Record issue/PR URLs, head and merge SHAs, actual
owner/status readbacks, and wake execution IDs in the migration PR. Workers demonstrate submission
and Request changes → revision on the same branch/PR. Every completed write has a commit/push before
the next question. The next worker fetches the accepted upstream revision from main.
Reviewer demonstrates rejection followed by approved exact-head merge; Head repeats reconciliation
without duplicate dispatch or another Done transition.

Change only legacy Markdown markers in paired `legacy-marker` fixtures; the proposed lifecycle
action must stay unchanged. Acting on a checked box, old Phase, review log or score fails the case.
Record actual observations; keep operator-only/expected.md and this answer table outside the agent's accessible workspace.
