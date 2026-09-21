---
type: spec
title: "Wizard Profile Design"
description: "Design for the Wizard agent profile: the retention edit of the Writer's draft with logged, user-approved changes, plus visual cues (on-screen text, B-roll, chapter markers) that the Wizard may suggest and the user approves."
tags: [scriptwriting, wizard, spec]
---

# Wizard Profile — Design

Date: 2026-09-20
Status: Draft, pending user review

## 1. Context

The Wizard is the fourth and last hat in the four-hat process from
<https://humbleandbrag.com/blog/how-to-write-a-youtube-script> (Artist, Architect, Writer, Wizard). Per the
article, this is "the final pass where you optimise for retention." It takes a complete draft and delivers a
polished, retention-optimized script. Its checklist, in the article's order:

1. Cut jargon.
2. Simplify sentences.
3. Check that curiosity gaps are not closed too early or left open too long.
4. Read the script aloud and cut anything you would never say in conversation.
5. Add visual cues: on-screen text, B-roll notes, and chapter markers.

The article says explicitly that the Wizard does not restructure: "it's much cheaper to restructure a
skeleton than a full draft," so the Wizard assumes the skeleton is sound. Its tone principle: "the more
conversational your delivery feels, the more trust you earn." It also claims the four-hat process cuts writing
time by 40-50% compared to linear writing (unsourced).

This spec covers **only the Wizard profile**. It builds on:
- `docs/knowledge/specs/2026-09-20-artist-profile-design.md`
- `docs/knowledge/specs/2026-09-20-architect-profile-design.md`
- `docs/knowledge/specs/2026-09-20-reviewer-profile-design.md`
- `docs/knowledge/specs/2026-09-20-writer-profile-design.md`

Conventions from those specs are reused and not restated: the five-file profile structure, the storage layers,
the `WORKFLOW.md` gate and return procedure, numbered episode artifacts, the Reviewer's deduction-based
scoring, `series/VOICE.md`, and the placeholder format. This spec also defines the Reviewer's stage-4 rubric
requirements (§9), which the Reviewer spec deferred until the Wizard was designed.

Assumptions (inherited):
- Agents are Hermes profiles (`script-<name>`) installed from this repo (see the Hermes deployment
  spec) and run as tasks/issues in an orchestrator (Paperclip AI, Multica, or Hermes kanban). Only the abstract states `in progress`, `review`
  and `done` are used; concrete status names are unverified.
- Source files are plain markdown with no framework-specific frontmatter (outside the okf bundle). The
  packaging layer converts them to Hermes format when installing.
- Every agent has file read/write access.

## 2. Scope of the Wizard

**In scope**
- Reading `03-writer.md` as the primary input, plus `02-architect.md`, `01-artist.md`, `series/VOICE.md`,
  and `series/SERIES.md` (for the audience).
- The retention edit, in the article's order: jargon and sentences, curiosity-gap timing, the read-aloud test.
- Visual cues: chapter markers, on-screen text, and B-roll notes.
- A final check, then submitting to review and acting on any returned critique.

**Out of scope**
- Restructuring: reordering loops, moving content between sections, changing the skeleton (Architect).
- Adding or rewriting ideas, claims, or facts.
- Short-form videos.
- Scoring or judging the sufficiency of its own output, or marking its own stage complete (Reviewer).

## 3. Repository layout

New files (existing files are unchanged unless §12 says otherwise):

```
profiles/wizard/
  SOUL.md
  AGENTS.md
  SKILLS.md
  STYLE.md
  MEMORY.md
profiles/reviewer/rubrics/
  04-wizard.md            defined in §9, built by the Wizard implementation plan
knowledge/
  wizard-checklist.md     extracted from the article: the retention-edit checklist and its rules
templates/
  04-wizard.md            copied into each episode folder when the Wizard starts
series/episodes/s01e01-<slug>/
  04-wizard.md            the Wizard's per-episode output: the final script
  reviews/04-wizard-review.md    written by the Reviewer
```

## 4. Authorship contract

The Wizard edits an existing draft, so it changes the user's words. It still adds no ideas. Rules 6-8 are
identical to the other profiles'.

1. **Edit only from sources.** The Wizard may cut, simplify, and tighten using the draft's own words and the
   user's voice (`series/VOICE.md`). A replacement for a jargon term must mean the same thing; when unsure,
   the Wizard asks. It never adds an idea, claim, example, or fact, and never uses a phrase the user said
   they avoid.
2. **Log and approve.** Every change to the script is an entry in the Edit log with an ID (`E<n>`), a type
   (`jargon`, `sentence`, `gap-timing`, `conversational`, or `placeholder`), the before and after text, and a reason. The
   user approves, edits, or rejects each section's changes. A section is final only when the user approves
   it. A rejected edit is recorded and not applied. No change to the script is unlogged. A `placeholder` edit replaces an open placeholder carried over from the Writer draft with text drawn from the user's answer.
3. **Ask, don't fill.** When the Wizard needs information from the user (does the audience know this term,
   what did you mean here), it asks. On "you pick" or "skip" for an edit decision, decline warmly and ask a
   smaller question. Never resolve a doubt by guessing.
4. **No restructuring.** Wording and sentence order *within* a section may change, with approval. Anything
   that would move content *between* sections, reorder loops, or change a transition's or the re-hook's
   placement is recorded under Open threads as a requested structural change and is not applied. That
   belongs to the Architect.
5. **Cues: suggest, label, approve.** Unlike the script itself, the Wizard may *originate* visual cues the
   way an editor would. It uses the user's sources first (the dump's `visuals` entries, the skeleton, the
   user's answers). Every cue records its origin: `user-sourced` with its sources, or `wizard-suggested`. A
   suggestion is final only when the user approves it, and the approval is recorded as a `Q<n>` answer. A
   suggested cue describes what to *show*, and never introduces a claim, statistic, or fact that the script
   or the sources do not already contain.
6. **Active curiosity.** *(Same as the Artist.)* After every answer, ask what it makes you curious about. The
   user's words drive the next question.
7. **Open, non-leading questions.** *(Same as the Artist.)* A question that gathers information never
   contains a suggested answer. A tracked edit or a suggested cue is a proposal, not a question, and is shown
   as such.
8. **No self-assessment.** *(Same as the Artist.)* Never score or certify the sufficiency of the output, and
   never treat the stage as complete. Only the Reviewer passes a stage.

**Why cues differ.** The Artist, Architect, and Writer exist to draw the user's ideas out, so they may not
originate content. Visual cues are editor's craft, and the user has chosen to let the Wizard suggest them,
with every suggestion labeled and approved so the user, the Reviewer, and the person filming can always tell
which ideas came from the user and which the Wizard proposed.

## 5. `04-wizard.md` structure

`## Final script` starts as a copy of the Writer's approved text and is edited in place. It keeps the
Writer's section layout in script order.

```markdown
# S01E04 — <Working Title> · Wizard

Phase: intake | simplify | gap-check | read-aloud | cues | final-check | in review | returned

## Inputs
- Draft: 03-writer.md
- Voice: series/VOICE.md
- Audience: <as in series/SERIES.md, or this episode's audience>

## Final script

### Hook
- Status: draft | approved | open
- Context lean-in: <text, with inline cue markers>
- Scroll stop: <text>
- Contrarian snapback: <text>
- Edits: E1, E4

### Introduction
- Status: draft | approved | open
- Validating language: <text>
- Problem: <text>
- Promise: <text>
- Credibility: <text>
- Roadmap: <text>
- Edits: ...

### Loop <n> (position <p>)
- Status: draft | approved | open
- Setup: <text>
- Tension: <text>
- Payoff: <text>
- Edits: ...

### Transition <a> to <b>
### Mid-video re-hook (after Loop <n>)
### Summary
### Call to action
(Same shape: Status, the labeled text lines, Edits.)

## Edit log
| ID | Section | Type | Before | After | Reason | Status |
|---|---|---|---|---|---|---|
| E1 | Loop 2, Tension | jargon | "<exact text>" | "<exact text>" | <why> | approved or rejected |

## Cues
| ID | Type | Location | Text | Origin | Sources or approval | Status |
|---|---|---|---|---|---|---|
| C1 | CHAPTER | Loop 1 | <title> | user-sourced | L1.payoff | approved |
| C2 | B-ROLL | Loop 2 | <note> | wizard-suggested | approval: Q3 | approved |
| C3 | ON-SCREEN | Introduction | <text> | user-sourced | #5, Q1 | approved |

## Placeholders
| ID | Section | What is missing | Status |
|---|---|---|---|

## Wizard answers
- Q1 "<user's words>"

## Review
- Status: not submitted | in review | returned
- Latest review: reviews/04-wizard-review.md
- (A pass is recorded only in the review log and the Pipeline box, never in this file.)

## Open threads
- <requested structural changes, open placeholders, skipped questions>

## Final handoff
<Written at submission: a pointer to the approved final script; the open placeholders, if any; the
Cues table; and the note that every change is in the Edit log. Only logged material.>
```

### Inline cue markers

Cues appear in the text at the beat they belong to, and each has a row in `## Cues`:
- `[ON-SCREEN: <text> | C1]`
- `[B-ROLL: <note> | C2]`
- `[CHAPTER: <title> | C3]`

Placeholders keep the Writer's format, `[PLACEHOLDER P<n>: <what is missing>]`. Placeholders still open from
`03-writer.md` keep their IDs; new ones continue the numbering.

### IDs

- `E<n>`: an edit. `C<n>`: a cue. `Q<n>`: a user answer recorded under `## Wizard answers`.
- Cue sources use the existing IDs: `#N` (dump entries), `A<loop>.<n>` (Architect answers), `V<n>` (voice
  samples), `W<n>` (Writer answers), skeleton IDs such as `L1.payoff`, and `Q<n>`.

## 6. Session procedure (`AGENTS.md`)

0. **Load.** Read the root `WORKFLOW.md`, then `SOUL.md`, `STYLE.md`, `SKILLS.md`, `MEMORY.md`,
   `knowledge/four-hat-article.md`, `knowledge/wizard-checklist.md`, and `knowledge/five-part/*.md`.
1. **Find the episode and check the gate.** Identify the episode. Read `03-writer.md`, `02-architect.md`,
   `01-artist.md`, `series/VOICE.md`, and `series/SERIES.md`. Check that the Writer's box on the `Pipeline:`
   line is ticked; if not, tell the user the Writer stage has not passed review and stop. Create
   `04-wizard.md` from `templates/04-wizard.md` if it does not exist, copying the Writer's approved text into
   `## Final script` with every section at `Status: draft`, or resume at its recorded phase.
2. **Simplify** (`simplify`). Jargon and sentences, section by section.
3. **Gap check** (`gap-check`). Curiosity-gap timing.
4. **Read-aloud** (`read-aloud`). The user reads each section aloud and marks what they would never say.
5. **Cues** (`visual-cues`). Chapter markers, on-screen text, and B-roll notes.
6. **Final check** (`final-check`). Re-ask unresolved placeholders, confirm a chapter cue for every loop and
   that every change is logged, and read the whole script back. Only the user says they are done.
7. **Submit for review.** When the user says they are done: write `## Final handoff`, set `Phase: in review`,
   and move the task to `review`. Do not score or mark the stage complete.
8. **If the task returns.** As for the other profiles: read the critique, tell the user briefly what was
   unclear, ask about each item with open, non-leading questions, record answers as new `Q<n>` answers,
   redo the affected changes through log-and-approve, never answer an item yourself, and resubmit only when
   the user says they are done again.
9. **Memory.** Update `MEMORY.md` only for durable facts the user stated or corrections. Never store episode
   content.

Save to `04-wizard.md` after every answer or small batch of answers. Keep `Phase:` current.

## 7. `SKILLS.md`

Five skills, in the article's order. Exact wording is written during implementation, is grounded in the
article's checklist (`knowledge/wizard-checklist.md`), and must ask, never suggest an answer, when gathering
information.

- **`simplify`.** Per section, in script order.
  - **Jargon:** the Wizard identifies candidate terms and asks the user, "Would your audience know '<term>'?"
    using the audience in `SERIES.md`. If not, it proposes a same-meaning replacement, using the user's own
    wording from `VOICE.md` and the dump where possible.
  - **Sentences:** the Wizard identifies long or multi-clause sentences and proposes splits or trims using the
    same words. The article gives no length threshold for the body, so this is judged and shown, not
    enforced. (The hook's under-ten-words rule still holds.)
  - Every proposal is a logged edit with a reason; the user approves each section's changes.
- **`gap-check`.** Map each curiosity gap to where it opens and where it closes: the hook, the intro promise,
  each loop's setup and payoff, the re-hook, and the CTA's gap. Flag a gap that closes too early (for example,
  the payoff given away in the hook, roadmap, or setup) or stays open too long. The article gives no
  threshold, so the Wizard asks the user, "Does this feel too long to you?", and does not decide. A fix inside
  one section is a logged `gap-timing` edit. A fix that needs content moved between sections is recorded as a
  requested structural change and not applied.
- **`read-aloud`.** For each section, ask the user to read it aloud and say what they would never say in
  conversation, quoting their words as `Q<n>`. Propose cuts or rewordings only for text the user marked, as
  logged `conversational` edits. The Wizard cannot make this judgment for the user.
- **`visual-cues`.**
  - **Chapter markers:** one for each loop, derived from the skeleton's loops and payoffs, named in the
    user's words.
  - **On-screen text:** from the intro promise and roadmap, the takeaways, and the user's own key phrases.
  - **B-roll notes:** first ask, "What footage or visuals do you already have or plan to shoot for this
    part?" Then use the dump's `visuals` entries (nominate by number, quoting the user) and the user's
    answers. The Wizard may then *suggest* further cues as an editor would, each labeled `wizard-suggested`,
    with no new claim, statistic, or fact.
  - Every cue gets an ID and a row in `## Cues`, and a suggested one needs the user's recorded approval.
    If the user rejects every suggestion for a beat, the cue stays open with a placeholder.
- **`final-check`.** Re-ask each open placeholder once; confirm a chapter cue exists for every loop; confirm
  that every difference between the Writer's text and the final script is a logged, approved edit; read the
  whole script back in order; the user decides whether it is done.

## 8. `SOUL.md`, `STYLE.md`, `MEMORY.md`, knowledge

- **`SOUL.md`.** Identity: an editor who improves what the user has already said, never what the user has yet
  to say. The eight rules of §4.
- **`STYLE.md`.** As the Writer (short questions, one at a time, echo the user's phrasing), plus: show each
  change as a before and after with its reason; keep cue suggestions clearly marked as suggestions.
- **`MEMORY.md`.** Same purpose and rules as the other profiles. Never episode content.
- **`knowledge/wizard-checklist.md`.** Extracted from the article, in the article's own terms, with the source
  URL, fetch date, and a note that it is a paraphrase. The time-saving claim is marked unsourced.

## 9. Reviewer stage-4 rubric requirements

The Wizard implementation plan builds `profiles/reviewer/rubrics/04-wizard.md` from these requirements. It
follows `rubrics/scoring.md` (constants, severities, dedupe) and adds the following. The downstream reader is
**the person filming and editing**, who has `04-wizard.md` plus the earlier stages' files and
`series/VOICE.md`.

**Required sections (G1):** `## Inputs`, `## Final script`, `## Edit log`, `## Cues`, `## Placeholders`,
`## Wizard answers`, `## Review`, `## Open threads`, `## Final handoff`. Inside `## Final script`: `### Hook`,
`### Introduction`, `### Summary`, `### Call to action`, and a `### Loop <n>` for every loop in the skeleton; a
missing subsection is blocking. **Valid Phase values (G2):** `intake | simplify | gap-check | read-aloud |
cues | final-check | in review | returned`.

| ID | Check | Severity |
|---|---|---|
| Z1 | Every Edit log row has an ID, section, type (`jargon`, `sentence`, `gap-timing`, `conversational`, or `placeholder`), before text, after text, reason, and status. One item per row with a missing part. | Significant |
| Z2 | **Unlogged change.** After removing inline cue markers, each labeled text line in `## Final script` matches the corresponding line in `03-writer.md`, unless an `approved` edit accounts for the difference. One item per line that differs without one. | Blocking |
| Z3 | **Phantom edit.** Each `approved` edit's before text appears verbatim in `03-writer.md` in the named section, and its after text appears in the final script. One item per edit that fails either. | Blocking |
| Z4 | The set of sections and the order of loops in `## Final script` match `03-writer.md`. One item per mismatch. | Blocking |
| Z5 | Every cue is `user-sourced` with `Sources` that resolve, or `wizard-suggested` with an `approval: Q<n>` that exists in `## Wizard answers`. Missing or unresolved: one item per cue. Every inline cue marker has a row in `## Cues` and every row has a marker: one minor item per mismatch. | Significant or minor |
| Z6 | A `CHAPTER` cue exists for every loop in the skeleton. One item per loop without one. | Significant |
| Z7 | A `wizard-suggested` cue whose text contains a digit or a `%` sign. One item per cue: it may be a new claim. | Blocking |
| Z8 | Hook sentences in the final script have fewer than ten words. A sentence of ten or more is minor; report one item listing all of them. | Minor |
| Z9 | No section in `## Final script` has `Status: draft`. Each is `approved` or `open`. A `draft` section is one item. An `open` section is itself one item. | Significant |
| Z10 | Every inline `[PLACEHOLDER P<n>: ...]` appears in `## Placeholders` and vice versa (minor per mismatch). Each remaining `open` placeholder is an item: blocking in the Hook or a loop's Payoff, significant elsewhere. Each must also appear in `## Open threads` (minor if not). | Blocking, significant, or minor |

G3 applies to `## Final handoff`.

**Comprehension focus.** Look hardest at: cues that do not say what to show ("show the chart" with no chart
identified); on-screen text that refers to nothing in the script; B-roll notes with undefined referents; a
script line that lost the meaning it needed after an edit (for example, a cut removed the antecedent of a
later pronoun); and contradictions between a cue and the script. A conversational cut or a short sentence that
is clear is not an item, and neither is a cue you would not have chosen. Never judge cue quality.

## 10. Validation

Manual walkthroughs with an agent that has loaded the profile, in a scratch copy, written to
`docs/validation/wizard-walkthroughs.md` during implementation. They start from fixture `03-writer.md`,
`02-architect.md`, `01-artist.md`, `series/VOICE.md`, and `series/SERIES.md`.

1. **Gate stop:** the Writer's Pipeline box is not ticked. The agent stops and says why.
2. **Jargon by audience:** the agent asks whether the audience knows a term instead of deciding. A same-meaning
   replacement is logged as an `E<n>` edit and approved before it is applied.
3. **Integrity:** after a full session, every difference between the Writer's text and the final script is a
   logged, approved edit, and no edit's before text is missing from the draft. A helper script checks this.
4. **Read-aloud is the user's:** the agent asks the user to read each section aloud and makes no
   `conversational` edit except for text the user marked.
5. **No restructuring:** a gap that would need content moved between sections, and a user request to swap two
   loops, are each recorded as a requested structural change and not applied.
6. **Gap timing asked, not decided:** the agent maps the gaps and asks whether a stretch feels too long. It
   does not decide.
7. **Cues:** user-sourced cues cite the dump's `visuals` entries by number; suggested cues are labeled
   `wizard-suggested` and need a recorded approval; a suggestion containing a statistic is not proposed; if the
   user rejects every suggestion for a beat, the cue stays open with a placeholder.
8. **Chapter markers:** a `CHAPTER` cue exists for every loop.
9. **Voice:** edits keep the user's `VOICE.md` phrases and never introduce a phrase from "Phrases I avoid".
10. **Resume:** end mid-pass, restart, and the agent resumes at the recorded phase without repeating
    questions.
11. **Submit and return:** on "done" the agent writes the final handoff and moves the task to `review`
    without scoring. Given a fixture critique in the Reviewer's log format with three unclear items, it asks
    about each without answering any.
12. **Rubric, clean pass:** the Reviewer scores a clean fixture 100%, passes it, and ticks both the Wizard and
    `Scripted` boxes.
13. **Rubric, planted defects:** a fixture with known planted defects yields exactly the expected items and
    score.

## 11. Ticking `Scripted`

Passing stage 4 finishes the scripting work for the episode. The Reviewer therefore ticks, in the episode's
entry in `series/SERIES.md`, both the `Wizard` box on the `Pipeline:` line and the `Scripted` box on the
`Long-form` line. `Filmed` and `Published` are ticked by the user. This changes the Reviewer's "one Pipeline
checkbox" limit for stage 4 only (§12, item 3).

## 12. Open items

Decisions made during design:
- The Wizard proposes edits from the draft's own words, logs each with a reason, and the user approves each
  section's changes.
- The Wizard may originate visual cues as an editor would; each is labeled by origin and approved by the
  user, and may not introduce a new claim, statistic, or fact.
- Structural findings are recorded and not applied; sentence order may change within a section with approval.
- The Reviewer ticks `Scripted` on the Wizard's pass.
- Edit, cue, and answer IDs are `E<n>`, `C<n>`, and `Q<n>`.
- The read-aloud test is performed by the user; jargon is judged against the audience by asking the user.

Open, to resolve before or during planning:
1. **User override and orchestrator specifics.** Inherited from the Reviewer and Artist specs. The override question is resolved: there is none (Head Scriptwriter spec §5.4). Orchestrator specifics remain open.
2. **Reopening an earlier stage.** *(Resolved: the Head Scriptwriter reopens it at the user's request, Head Scriptwriter spec §5.3.)* `WORKFLOW.md` still has no path to send a task back to the Architect. The
   Writer and the Wizard now both record requested structural changes that nothing acts on. Needs a decision,
   likely in `WORKFLOW.md`.
3. **Reviewer patch.** The Reviewer's limit (its SOUL rule 5 and its `return-or-pass` skill) is "the one
   Pipeline checkbox for the stage." Stage 4 needs "and `Scripted` on the `Long-form` line." The Wizard
   implementation plan patches the Reviewer files and the Reviewer spec, as the Writer plan did for
   `VOICE.md`.
4. **Stage-4 rubric.** Built by the Wizard implementation plan from §9.
5. **The finished script.** The final script lives inside `04-wizard.md` among edit logs and tables. Whether a
   clean export (script text and cues only, no logs) should exist for the person filming is undecided.
6. **Sentence-length and gap thresholds.** The article gives none for the body, so both are judged and asked
   about, not enforced.
7. **Time-saving claim.** The article's 40-50% claim is unsourced and recorded as such; nothing in the design
   depends on it.

Resolved by the Head Scriptwriter spec (`docs/knowledge/specs/2026-09-20-head-scriptwriter-design.md`):
- Item 1: there is no override (§5.4).
- Item 2: on a requested structural change the Head asks the user and, if they agree, reopens the earlier
  stage: it sets the task back to in progress, unticks the later boxes, renames later outputs as stale, and
  creates fresh downstream tasks (§5.3).
