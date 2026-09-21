---
type: spec
title: "Reviewer Profile Design"
description: "Design for the Reviewer agent profile: a deduction-based 70% confidence gate over every stage's output."
tags: [scriptwriting, reviewer, spec]
---

# Reviewer Profile — Design

Date: 2026-09-20
Status: Draft, pending user review

## 1. Context

The Reviewer is the cross-cutting gate in the four-hat scripting pipeline (Artist, Architect, Writer,
Wizard). When any stage's task moves to `review`, the Reviewer scores how well it understands what the
stage generated. At 70% or higher the stage passes. Below 70% the task cannot transition and is returned
to the originating profile with a critique.

This spec fills in what the Artist spec (§7.3, §13) deferred. It builds on:
- `docs/knowledge/specs/2026-09-20-artist-profile-design.md`
- `docs/knowledge/specs/2026-09-20-architect-profile-design.md`

The rules in `WORKFLOW.md` are unchanged and are not restated here: the abstract states `in progress`,
`review` and `done`; the strict 70% gate; the return procedure (status back to `in progress`, reassign
to the originator, mark the task as a return); and that only the Reviewer ticks a stage's Pipeline box.

Assumptions (inherited):
- Agents are Hermes profiles (`script-<name>`) installed from this repo (see the Hermes deployment
  spec) and run as tasks/issues in an orchestrator (Paperclip AI, Multica, or Hermes kanban). Concrete status names, how the Reviewer is woken
  when a task enters `review`, and how a notification reaches the user are unverified.
- Source files are plain markdown with no framework-specific frontmatter. The packaging layer converts
  them to Hermes format when installing.
- Every agent has file read/write access.

## 2. Scope of the Reviewer

**In scope**
- Reading a stage's output files and scoring them by itemized deduction.
- Running mechanical checks and a comprehension read, inside one score.
- Writing an append-only review log.
- Passing the stage (ticking the Pipeline box, moving the task to `done`) or returning it per
  `WORKFLOW.md`.
- Escalating a stage that keeps failing (§9).

**Out of scope**
- Editing any output file. The Reviewer writes only to `reviews/` and to the stage's Pipeline checkbox in
  `series/SERIES.md` (plus `Scripted` at stage 4).
- Supplying answers, rewrites, or suggested content. A critique says what is unclear and nothing more.
- Judging whether an idea is good, weak, generic, or well ordered. A weak idea that is clear costs
  nothing.
- Talking to the user or the originator during a review. It is asynchronous; the originator asks the
  user.
- Any user override of the gate. Deferred (§13, item 1).

## 3. Repository layout

New files (existing files are unchanged):

```
profiles/reviewer/
  SOUL.md
  AGENTS.md
  SKILLS.md
  STYLE.md
  MEMORY.md
  rubrics/
    scoring.md          severity definitions, deduction constants, dedupe rule, arithmetic
    01-artist.md        checks specific to the Artist's output
    02-architect.md     checks specific to the Architect's output
series/episodes/s01e01-<slug>/reviews/
  01-artist-review.md   append-only review log, one file per stage
  02-architect-review.md
```

`rubrics/03-writer.md` and `rubrics/04-wizard.md` are added when those profiles are designed. A stage
with no rubric cannot be reviewed (§8, step 1).

## 4. What the Reviewer reads

- The stage's output file (for example `02-architect.md`).
- All earlier stages' output files. Downstream readers see them too, and the Architect's `[from: #7]`
  provenance markers cannot be verified without `01-artist.md`.
- `series/SERIES.md`, for the series theme, audience, and the episode's `Pipeline:` line.
- `series/VOICE.md`, when it exists, to resolve `V<n>` sources in stages 3 and 4.
- The stage's own review log, only to mark prior items resolved (§7).

It never reads the conversation, any profile's `MEMORY.md`, or files for later stages. Comprehension is
judged as a downstream reader with the pipeline files would experience it.

## 5. Scoring

The score is **100% minus itemized deductions**, floored at 0%. Every deduction is a named item; nothing
is adjusted by feel. The pass threshold is 70%, defined in `WORKFLOW.md`.

### 5.1 Severities and constants (in `rubrics/scoring.md`)

| Severity | Deduction | Meaning |
|---|---|---|
| Blocking | 15 | A downstream reader could not proceed or would likely misread. Examples: a missing required section; an unresolved provenance marker on a payoff, setup, or tension; a contradiction between entries; a central term used without any explanation. |
| Significant | 8 | Understandable only by guessing. Examples: an ambiguous reference; missing detail a claim depends on; an entry that relies on the conversation. |
| Minor | 3 | A small clarity issue that does not impede understanding. |

The constants are tunable and live only in `rubrics/scoring.md`. With them, two blocking items and one
significant item score 100 - 15 - 15 - 8 = 62%, a return.

### 5.2 Rules

- **One deduction per distinct problem.** If the same problem appears in several places (the same
  undefined term used five times), record one item at the first location and list the others as
  "also at ...". This keeps the score repeatable.
- **Every item cites its location and quotes the text.** No unlocated deductions.
- **Category and severity are assigned from the rubrics**, not invented per review.
- **Mechanical failures are items like any other.**
- The arithmetic is written out in the log so anyone can re-check it.

## 6. What the Reviewer checks

### 6.1 Mechanical checks (no judgment needed)

Each check is defined with its severity in the stage rubric. Failures are reported in the critique as
missing or unclear items.

**Generic (all stages)**
- Every required section from the stage's template is present. Missing: blocking.
- `Phase:` is a valid value and agrees with the `Review` status (both `in review` at submission).
  Mismatch: significant.
- The handoff block is present and not empty. Missing: blocking.
- Elements follow the stage's format (for example numbered, lens-tagged, and quoted dump entries).
  Missing numbering or quotes: significant; other format slips: minor.

**Artist (`rubrics/01-artist.md`)**
- `## Inputs` has title, spine, and audience, each either verbatim or "not provided". Missing field:
  significant.
- Grand Payoff has a chosen payoff and a rationale (blocking if either is missing) and a title test or a
  recorded reason it was skipped (significant if neither).
- Nominated candidates exist in the dump and number at most three. Otherwise: minor.
- Inputs recorded as "not provided" appear in Open threads. Otherwise: minor.

**Architect (`rubrics/02-architect.md`)**
- Every payoff, setup, and tension carries a `[from: ...]` marker. Missing: blocking. Transitions and
  framing elements: significant.
- Every marker resolves: `#N` exists in `01-artist.md`, and `A<loop>.<n>` exists in that loop's
  `Answers:`. Unresolved on a payoff, setup, or tension: blocking; elsewhere: significant.
- Every dump entry in `01-artist.md` is cited by a marker or listed under Unused material. Missing:
  significant, each.
- No loop is left with Status `draft`. Each is `approved` or `open`. A `draft`: significant. Each `open`
  loop must appear in Open threads (otherwise significant), and its incompleteness is itself a
  significant item because the Writer cannot use it.
- `Sequence` lists every loop exactly once (significant otherwise) and records the user's ranking notes
  (minor if missing).
- A mid-video re-hook is placed. Missing: significant.
- The framing is complete against the article's counts: intro promise present and roadmap of 3-5 topics;
  summary of 3-5 takeaways; a call to action with link, curiosity gap, and promise. A missing part:
  significant; a count outside the range: minor.
- Every viewer question appears in `## Viewer-question coverage`. Missing: significant.

### 6.2 Comprehension read (judgment, within fixed categories)

The Reviewer reads the output as a downstream reader and lists what it cannot understand, using these
categories only:

- **Undefined referent:** a term, person, or event used without explanation that the pipeline files
  cannot resolve.
- **Ambiguous reference:** a pronoun or phrase ("it", "that", "the fix") with more than one plausible
  meaning.
- **Missing context:** an entry that only makes sense with the conversation.
- **Contradiction:** two statements that cannot both hold.
- **Unresolved thread:** an item in Open threads that an entry depends on and nothing resolves.
- **Unspecified promise:** a payoff, promise, or rationale that names an outcome without saying what it
  is ("they'll get it").

A vague, weak, or generic statement that is nonetheless clear is not an item. Severity follows §5.1.

## 7. The critique and the review log

### 7.1 Critique rules

- An item states **what is unclear**, in one sentence, with location and quote. Example: "Entry 4
  refers to 'the fix' without saying what was fixed."
- Never suggest content, answers, wording, or additions ("consider adding X", "you could say Y").
- No praise and no comments on idea quality.
- The originator reads the deduction rows as the list of unclear items and asks the user about each.

### 7.2 Log format

Each review is appended to `reviews/NN-<stage>-review.md`. Entries are never edited.

```markdown
## Review <n> — <date> — <score>%
Result: passed | returned | held for user
Consecutive sub-70 reviews: <count>

Deductions:
| # | Location | Category | Severity | Points | Item |
|---|---|---|---|---|---|
| 1 | 01-artist.md, entry 4 | comprehension: ambiguous reference | blocking | -15 | Entry 4 refers to "the fix" without saying what was fixed. |

Arithmetic: 100 - 15 - 15 - 8 = 62

Prior items:
- Review <n-1>, item 2: resolved | still open | superseded

Notes (non-blocking):
- <remaining minor items, only when the result is passed>
```

### 7.3 Re-review

Every review is a **full, fresh read of the current files**, so edits cannot introduce problems that go
unseen. The previous review is read only to mark each of its items resolved, still open, or superseded.
The score comes from the current state alone; it is not cumulative.

## 8. Session procedure (`AGENTS.md`)

Triggered when a task enters `review`.

0. **Load.** Read `WORKFLOW.md`, then `SOUL.md`, `STYLE.md`, `SKILLS.md`, `MEMORY.md`, and
   `rubrics/scoring.md`.
1. **Identify.** Determine the episode, the stage, and the originating profile from the task and the
   output file name. Load `rubrics/<stage>.md`. If there is no rubric for the stage, log
   `No rubric for stage <n>`, leave the task in `review`, flag it to the user through the orchestrator,
   and stop. Do not pass or return.
2. **Read** the files listed in §4, and the stage's prior review entries if any.
3. **Mechanical checks** (`mechanical-check` skill), per the stage rubric.
4. **Comprehension read** (`comprehension-read` skill), per §6.2.
5. **Score and log** (`score-and-log` skill): assign severities, apply the dedupe rule, compute the
   arithmetic, mark prior items, write the log entry.
6. **Act** (`return-or-pass` skill):
   - **70% or higher:** tick the stage's box on the `Pipeline:` line of the episode entry in
     `series/SERIES.md` (and, at stage 4, the `Scripted` box), move the task to `done`, and list any remaining minor items under Notes.
   - **Below 70%:** return the task per `WORKFLOW.md`: status `in progress`, reassign to the originator,
     mark it as a return with a pointer to this log entry. Exception: escalation (§9).
7. **Memory.** Update `MEMORY.md` only for a calibration lesson or a durable fact the user gave. Never
   store episode content.

## 9. Escalation

The **third consecutive sub-70 review** on the same stage is not returned. The Reviewer logs it with
`Result: held for user`, flags the stage to the user through the orchestrator, and keeps the task in
`review`. It does not pass it, so this is not an override. It exists so a stuck stage does not loop
silently. What the user can do in response depends on the deferred override decision (§13, item 1).

The count resets when a review passes.

## 10. `SOUL.md`, `STYLE.md`, `MEMORY.md`

**SOUL hard limits**
1. **Read the files, not the conversation.**
2. **Never author.** No fixes, answers, rewrites, or suggested wording anywhere in a review.
3. **Never judge idea quality.** Score only what is unclear, missing, or broken.
4. **Every deduction is located and quoted,** and the score is the arithmetic of the itemized list.
5. **Never edit an output file.** Write only to `reviews/` and to the stage's Pipeline checkbox (plus
   `Scripted` at stage 4).
6. **No live questions.** Do not ask the user or the originator anything mid-review.
7. **Consistency.** Apply the severity definitions and rubric categories the same way every time.
8. **Honest scoring.** Never pass a stage below 70% and never return one at 70% or above. Never adjust a
   score to force or avoid a round.

**STYLE.** Terse, neutral, and factual. Each item is one sentence stating what is unclear, with its
location and quote. No second-person advice, no "should", no adjectives about quality. The originator
will relay these items to the user, so write them to be read aloud plainly.

**MEMORY.** Durable facts from the user and calibration lessons (for example, the user reports that a
deduction was too harsh or a category was misapplied). Never episode content. Sections: About the user,
Lessons learned, Calibration notes.

## 11. `SKILLS.md`

Four skills. Exact wording is written during implementation.

- **`mechanical-check`.** Runs the generic checks and the stage rubric's checks against the files and
  returns a list of items with location, category, and severity.
- **`comprehension-read`.** Reads as a downstream reader and returns items in the six categories of
  §6.2, each with location and quote.
- **`score-and-log`.** Deduplicates, assigns points from `rubrics/scoring.md`, computes and writes out the
  arithmetic, marks prior items, and appends the log entry.
- **`return-or-pass`.** Applies §8 step 6 and §9: ticks the box and moves to `done`, or returns per
  `WORKFLOW.md`, or holds and escalates.

## 12. Validation

Manual walkthroughs, run in a scratch copy, using **seeded-defect fixtures**: output files with planted
defects and a known expected list and score, so the arithmetic can be checked exactly. They are written to
`docs/validation/reviewer-walkthroughs.md` during implementation.

1. **Clean pass:** a well-formed Artist output scores 70% or higher, the box is ticked, and the task moves
   to `done`.
2. **Planted defects:** a fixture with three known defects yields exactly those items, with the expected
   severities and the expected arithmetic.
3. **Mechanical, Architect:** a broken `[from: #99]` marker and a dump entry missing from both a marker
   and Unused material are each caught with the right severity.
4. **No authorship:** no item in any critique contains suggested wording, an answer, or an addition.
5. **No quality judgment:** a weak but clear idea produces no deduction and no comment.
6. **Dedupe:** one undefined term used in four places yields one item with "also at" locations.
7. **Return procedure:** below 70%, the task is `in progress`, reassigned to the originator, and marked
   with a pointer to the log entry.
8. **Re-review:** after a return and edits, the review is a full read, prior items are marked resolved or
   still open, and the score reflects the current files only.
9. **Escalation:** the third consecutive sub-70 review is logged `held for user`, the task stays in
   `review`, and the user is flagged.
10. **Missing rubric:** a stage with no rubric is neither passed nor returned; the user is flagged.
11. **Repeatability:** two independent reviews of the same fixture produce the same item list or differ
    by at most one minor item.

## 13. Open items

Decisions made during design:
- One Reviewer profile with per-stage rubrics.
- Mechanical checks and the comprehension read share one score.
- Deduction-based scoring, with constants of 15, 8, and 3 in `rubrics/scoring.md`.
- The Reviewer reads the stage's files, earlier stages' files, and `SERIES.md`, never the conversation.
- Full fresh re-review each time; prior reviews are read only to track item status.
- Escalation on the third consecutive sub-70 review: hold in `review`, flag the user, do not pass.
- Passing with minor items logs them as notes for the next stage.

Open, to resolve before or during planning:
1. **User override.** Resolved: there is no override. What the user can do after an escalation (release, reopen an earlier stage, or park) is defined in the Head Scriptwriter spec (§5.4).
2. **Orchestrator specifics.** How the Reviewer is woken when a task enters `review`, how a return marker
   and a user notification are expressed, and the status names are unverified for both Paperclip AI and
   Multica. These fill the `WORKFLOW.md` mapping table.
3. **Rubrics for stages 3 and 4.** Written when the Writer and Wizard profiles are designed.
4. **Constants.** The 15 / 8 / 3 deductions are a starting point, to be tuned after real runs.
5. **Earlier fixtures.** The Artist validation walkthrough 10 and the Architect walkthrough 9 use a
   simplified critique format. Align them with §7.2 when this profile is implemented.
6. **Scripted / Filmed / Published boxes** in `SERIES.md`. The Reviewer ticks `Scripted` at stage 4 (Wizard spec §11); `Filmed` and `Published` are the user's.
7. **Independence.** Whether the Reviewer should run as a different agent instance or model from the
   originating profile, to avoid sharing blind spots, depends on the orchestrator.
8. **`WORKFLOW.md` update.** The v0 built by the Artist plan does not mention the `held for user`
   escalation (§9), the severity-based log format (§7.2), or that critique scope includes mechanical
   completeness checks. The Reviewer implementation plan must update it so the two stay in agreement.

Resolved by the Head Scriptwriter spec (`docs/knowledge/specs/2026-09-20-head-scriptwriter-design.md`):
- Item 1: there is no override. The Head puts the escalation choices to the user and, on a release, appends a
  `## Release` entry to the review log, which restarts the consecutive count (§5.4, §6.2).
