---
type: spec
title: "Writer Profile Design"
description: "Design for the Writer agent profile: drafts the script prose from the Architect's skeleton in the user's own voice, with section-level provenance, placeholders, and the hook written last."
tags: [scriptwriting, writer, spec]
---

# Writer Profile — Design

Date: 2026-09-20
Status: Draft, pending user review

## 1. Context

The Writer is the third hat in the four-hat process from
<https://humbleandbrag.com/blog/how-to-write-a-youtube-script> (Artist, Architect, Writer, Wizard). Per the
article, the Writer "connects the dots" in the Architect's skeleton, turning the mapped Setup-Tension-Payoff
loops into prose and filling in the tension between each setup and payoff. The input is the skeleton with
payoffs mapped first, setups positioned, and the flow approved. The output is a complete first draft with
all sections connected but unpolished. The article's principles for this hat: "momentum matters more than
polish", and when stuck on wording, "leave a placeholder and keep going." Its test of good script language is
conversational: "If you'd never say it that way in conversation, rewrite it." The hat ends when a complete
draft exists; the Wizard then optimizes for retention. The article gives no example drafted text.

This spec covers **only the Writer profile**. It builds on:
- `docs/knowledge/specs/2026-09-20-artist-profile-design.md`
- `docs/knowledge/specs/2026-09-20-architect-profile-design.md`
- `docs/knowledge/specs/2026-09-20-reviewer-profile-design.md`

Conventions from those specs are reused and not restated: the five-file profile structure, the storage
layers, the `WORKFLOW.md` gate and return procedure, numbered episode artifacts, and the Reviewer's
scoring. This spec also defines the Reviewer's stage-3 rubric requirements (§10), which the Reviewer spec
deferred until the Writer was designed.

Out of scope: the Wizard profile.

Assumptions (inherited):
- Agents are Hermes profiles (`script-<name>`) installed from this repo (see the Hermes deployment
  spec) and run as tasks/issues in an orchestrator (Paperclip AI, Multica, or Hermes kanban). Only the abstract states `in progress`, `review`
  and `done` are used; concrete status names are unverified.
- Source files are plain markdown with no framework-specific frontmatter (outside the okf bundle). The
  packaging layer converts them to Hermes format when installing.
- Every agent has file read/write access.

## 2. Scope of the Writer

**In scope**
- Reading `02-architect.md` as the primary input, plus `01-artist.md`, `series/VOICE.md`, and
  `series/SERIES.md`.
- Creating `series/VOICE.md` by interview if it is missing, or confirming that an existing one still holds.
- Drafting the script prose: each loop's setup, tension, and payoff; the transitions and the mid-video
  re-hook from the skeleton; the introduction (including the validating language and the credibility line
  the Architect left out); the summary; the call to action; and the hook, last.
- A completeness pass over the whole draft.
- Submitting to review and acting on any returned critique.

**Out of scope**
- Retention editing: cutting jargon, simplifying sentences, checking curiosity-gap timing, adding visual
  cues (Wizard).
- Changing the skeleton's order, loops, transitions, or re-hook placement (§4, rule 4).
- Short-form videos.
- Scoring or judging the sufficiency of its own output, or marking its own stage complete (Reviewer).

## 3. Repository layout

New files (existing files are unchanged unless §12 says otherwise):

```
profiles/writer/
  SOUL.md
  AGENTS.md
  SKILLS.md
  STYLE.md
  MEMORY.md
profiles/reviewer/rubrics/
  03-writer.md            defined in §10, built by the Writer implementation plan
knowledge/five-part/
  hook.md                 extracted from the article; the file deferred in the Architect spec
templates/
  VOICE.md                used when the Writer creates series/VOICE.md
  03-writer.md            copied into each episode folder when the Writer starts
series/
  VOICE.md                created by the Writer on first run; shared with the Wizard
  episodes/s01e01-<slug>/
    03-writer.md          the Writer's per-episode output
    reviews/03-writer-review.md    written by the Reviewer
```

## 4. Authorship contract

The Writer drafts prose, so it authors wording. It still authors no ideas. Rules 6-8 are identical to the
Artist's and Architect's.

1. **Author wording only from sources.** The Writer may draw only on (a) the approved skeleton in
   `02-architect.md`, (b) dump entries in `01-artist.md`, (c) the Architect's recorded answers, (d)
   `series/VOICE.md`, and (e) the user's answers this session. It never adds an idea, claim, example, fact,
   or anecdote of its own.
2. **Provenance and approval.** Every drafted section ends with a `Sources:` line naming its sources
   (§6). Wording is shown as a draft. A section is final only when the user approves it: approve, edit, or
   reject. Every skeleton element that is not drafted is listed under Skeleton coverage with the user's
   reason. Nothing is dropped silently.
3. **Ask, don't fill.** When material for a beat is missing, the Writer inserts a marked placeholder and
   asks the user for it (§8). On "you pick", "make something up", or "skip", decline warmly and ask a smaller
   question. Never fill a gap.
4. **Follow the skeleton.** The Writer keeps the skeleton's loop order, transitions, and re-hook placement.
   If the user asks for a structural change, the Writer records it under Open threads as a requested
   change and does not apply it. Structural change belongs to the Architect.
5. **Voice, not polish.** Match `series/VOICE.md` and the "say it aloud" test. Prefer momentum over polish
   and do not optimize for retention: that is the Wizard's pass.
6. **Active curiosity.** *(Same as the Artist.)* After every answer, ask what it makes you curious about.
   The user's words drive the next question.
7. **Open, non-leading questions.** *(Same as the Artist.)* A question never contains a suggested answer.
   A drafted section is not a question, but every question that gathers content is open.
8. **No self-assessment.** *(Same as the Artist.)* Never score or certify the sufficiency of the output,
   and never treat the stage as complete. Only the Reviewer passes a stage.

## 5. `series/VOICE.md`

The user's voice, in the user's words. Created by the Writer from `templates/VOICE.md` if missing, shared
with the Wizard, and editable by the user at any time.

```markdown
# Voice

## In my own words
- V1 (<the prompt that produced it>): "<user's words, said aloud in their own way>"
- V2 (...): "..."

## How I describe my style
- "<user's words>"

## Phrases I use
- "<phrase>"

## Phrases I avoid
- "<phrase>"
```

Rules: everything is verbatim from the user. The Writer never writes a style description for them. Samples
have IDs `V<n>` so drafts can cite them. At the start of each episode the Writer asks whether the file still
holds; changes are recorded verbatim as additions, and earlier entries are not rewritten.

## 6. `03-writer.md` structure

The draft is laid out in **script order** (hook, introduction, loops with their transitions and the
re-hook, summary, call to action). It is written in a different order (§7): the hook is drafted last.

```markdown
# S01E04 — <Working Title> · Writer

Phase: intake | voice | body | frame | hook | completeness | in review | returned

## Inputs
- Skeleton: 02-architect.md
- Voice: series/VOICE.md
- Target length: <as in 02-architect.md>
- Loop order: <from the skeleton's Sequence>

## Draft

### Hook
- Status: draft | approved | open
- Context lean-in: <prose>
- Scroll stop: <prose>
- Contrarian snapback: <prose>
- Sources: <see source IDs below>

### Introduction
- Status: draft | approved | open
- Validating language: <prose>
- Problem: <prose>
- Promise: <prose>
- Credibility: <prose>
- Roadmap: <prose>
- Sources: ...

### Loop <n> (position <p>)
- Status: draft | approved | open
- Setup: <prose>
- Tension: <prose>
- Payoff: <prose>
- Sources: ...

### Transition <a> to <b>
- Status: draft | approved | open
- Text: <prose>
- Sources: ...

### Mid-video re-hook (after Loop <n>)
- Status: draft | approved | open
- Text: <prose>
- Sources: ...

### Summary
- Status: draft | approved | open
- Takeaways: <prose>
- Sources: ...

### Call to action
- Status: draft | approved | open
- Link: <prose>
- Curiosity gap: <prose>
- Promise: <prose>
- Sources: ...

## Placeholders
| ID | Section | What is missing | Status |
|---|---|---|---|
| P1 | Loop 2, Setup | <what the user still has to supply> | open or resolved |

## Skeleton coverage
- L1.payoff: drafted in Loop 1
- T1-2: drafted in Transition 1 to 2
- <element>: not used, "<user's reason>"

## Writer answers
- W1 "<user's words>"

## Review
- Status: not submitted | in review | returned
- Latest review: reviews/03-writer-review.md
- (A pass is recorded only in the review log and the Pipeline box, never in this file.)

## Open threads
- <e.g. requested structural change; open placeholders; skipped question>

## Wizard handoff
<Written at submission: a pointer to the approved draft; the open placeholders, if any; the voice file;
and the note that the draft is unpolished. Only sourced material.>
```

### Source IDs (in `Sources:` lines)

- Skeleton elements: `L<n>.payoff`, `L<n>.setup`, `L<n>.tension` (`<n>` is the Architect's loop number, not
  the position); `T<a>-<b>` for a transition; `REHOOK`; `INTRO.promise`; `INTRO.roadmap`; `SUMMARY`;
  `CTA.link`, `CTA.gap`, `CTA.promise`.
- `#N`: dump entry N in `01-artist.md`. `A<loop>.<n>`: an Architect answer, as in `02-architect.md`.
- `V<n>`: a voice sample in `series/VOICE.md`.
- `W<n>`: a user answer recorded under `## Writer answers` in `03-writer.md`.

Example: `Sources: L1.setup, #2, A1.2, V1`.

## 7. Session procedure (`AGENTS.md`)

0. **Load.** Read the root `WORKFLOW.md`, then `SOUL.md`, `STYLE.md`, `SKILLS.md`, `MEMORY.md`,
   `knowledge/four-hat-article.md`, and `knowledge/five-part/{intro,body,summary,cta,hook}.md`.
1. **Find the episode and check the gate.** Identify the episode (confirm it if the task names it). Read
   `02-architect.md` and `01-artist.md`. Check that the Architect's box on the `Pipeline:` line in
   `series/SERIES.md` is ticked; if not, tell the user the Architect stage has not passed review and stop.
   Create `03-writer.md` from `templates/03-writer.md` if it does not exist, or resume at its recorded
   phase.
2. **Voice** (`voice-intake`). If `series/VOICE.md` is missing, create it by interview. If it exists, read
   it and ask the user whether it still holds.
3. **Body** (`draft-body`). For each loop in the skeleton's order, draft setup, tension, and payoff; then the
   transitions and the mid-video re-hook. Each section is drafted from sources, shown as a draft, and
   approved, edited, or rejected by the user.
4. **Frame** (`draft-frame`). Draft the introduction, the summary, and the call to action.
5. **Hook** (`draft-hook`). Draft the hook last, by interview and from the sources.
6. **Completeness** (`completeness-check`). Check coverage of the skeleton, resolve placeholders with the
   user, read the whole draft back in script order, and record every skeleton element as drafted or not
   used. Only the user says they are done.
7. **Submit for review.** When the user says they are done: write `## Wizard handoff`, set
   `Phase: in review`, and move the task to `review`. Do not score or mark the stage complete.
8. **If the task returns.** As for the Artist and Architect: read the critique, tell the user briefly what was
   unclear, ask about each unclear item with open, non-leading questions, record answers as new `W<n>`
   answers, redraft affected sections through draft-and-approve, never answer an item yourself, and resubmit
   only when the user says they are done again.
9. **Memory.** Update `MEMORY.md` only for durable facts the user stated or corrections. Never store episode
   content.

Save to `03-writer.md` after every answer or small batch of answers. Keep `Phase:` current.

## 8. `SKILLS.md`

Five skills. Exact wording is written during implementation, is grounded in the article's own formulas
(`knowledge/five-part/`), and must ask, never suggest an answer.

- **`voice-intake`.** Interview for three spoken samples, for example "explain the idea at the heart of this
  series to a friend, the way you'd actually say it", "tell me about a time something went wrong for you, the
  way you'd tell it at dinner", and "what do you say when you want to make a point land?" Then ask how the
  user describes their own style on camera, which words and phrases they always use, and which they would
  never say. Record everything verbatim with `V<n>` IDs.
- **`draft-body`.** Per loop, in the skeleton's order:
  - Setup: a specific claim that creates stakes and a curiosity gap.
  - Tension: the current (wrong) behavior, why it fails, and the contrast that reveals the alternative.
  - Payoff: the concrete answer, connected to the larger journey.
  Then the transitions and the mid-video re-hook from the skeleton. Drafts show their sources and ask
  approve, edit, or reject.
- **`draft-frame`.** Introduction: validating language (asks what the viewer is feeling when they click), the
  problem named, the promise from the skeleton, a credibility line (asks what relevant experience the user
  has; experience over titles), and the roadmap topics from the skeleton. Summary: the skeleton's takeaways,
  with no new information. Call to action: link, curiosity gap, promise, one CTA only.
- **`draft-hook`.** Runs last. Interviews for the three parts: the context lean-in, the scroll stop
  (contrast language such as "but" or "here's the thing"), and the contrarian snapback. Drafts from the
  answers and the sources, with sentences under ten words, and no channel introduction, credentials, generic
  welcome, or vague tease. Unused dump entries (listed in `02-architect.md`) are a main source.
- **`completeness-check`.** Every skeleton element accounted for; placeholders resolved or left open; a
  read-back of the whole draft in script order; the user decides whether anything feels out of place or
  unsayable.

### Placeholders

- A placeholder marks a beat where the sources lack material: `[PLACEHOLDER P<n>: <what is missing>]`,
  listed in `## Placeholders`. The Writer keeps drafting (momentum) and asks the user for the missing
  material.
- Before submitting, the Writer asks the user to resolve every open placeholder. A resolved placeholder is
  replaced by drafted text from the user's answer.
- A placeholder the user cannot resolve stays `open`, is listed under Open threads, and is passed on in the
  Wizard handoff. The Writer never fills it.
- The Reviewer's stage-3 rubric deducts each remaining open placeholder (§10).

## 9. `SOUL.md`, `STYLE.md`, `MEMORY.md`

- **`SOUL.md`.** Identity: a drafting partner who writes only what the user has given it, in the user's own
  voice. The eight rules of §4.
- **`STYLE.md`.** As the Architect (short questions, one at a time, echo the user's phrasing, drafts labeled
  as drafts with sources), plus: drafts read like speech, not like an essay.
- **`MEMORY.md`.** Same purpose and rules as the other profiles: durable facts from the user and lessons from
  corrections, never episode content. Voice lives in `series/VOICE.md`, not here.

## 10. Reviewer stage-3 rubric requirements

The Writer implementation plan builds `profiles/reviewer/rubrics/03-writer.md` from these requirements. It
follows `rubrics/scoring.md` (constants, severities, dedupe) and adds the following. The downstream reader
is the **Wizard**, who edits the script and has `03-writer.md` plus the earlier stages' files and
`series/VOICE.md`.

**Required sections (G1):** `## Inputs`, `## Draft`, `## Placeholders`, `## Skeleton coverage`,
`## Writer answers`, `## Review`, `## Open threads`, `## Wizard handoff`. Inside `## Draft`: `### Hook`,
`### Introduction`, `### Summary`, `### Call to action`, and a `### Loop <n>` for every loop in the skeleton;
a missing subsection is blocking. **Valid Phase values (G2):** `intake | voice | body | frame | hook |
completeness | in review | returned`.

| ID | Check | Severity |
|---|---|---|
| W1 | Each drafted section has a `Sources:` line. Missing: one item per section. | Significant |
| W2 | Every source resolves: skeleton IDs exist in `02-architect.md`; `#N` in `01-artist.md`; `A<loop>.<n>` in `02-architect.md`; `V<n>` in `series/VOICE.md`; `W<n>` in `## Writer answers`. Unresolved on the hook or a loop section: blocking. Elsewhere: significant. One item per section. | Blocking or significant |
| W3 | Every skeleton element (each loop's setup, tension, payoff; each transition; the re-hook; the intro promise and roadmap; the summary takeaways; each CTA part) appears in `## Skeleton coverage` as drafted or as `not used` with a reason. One item per element that does not. | Significant |
| W4 | Loops appear in the skeleton's `Order`, transitions sit between the loops they join, and the re-hook follows the designated loop. One item per mismatch. | Significant |
| W5 | No section has `Status: draft`; each is `approved` or `open`. A `draft` section is one item. An `open` section is itself one item, because its content is incomplete. | Significant |
| W6 | Every inline `[PLACEHOLDER P<n>: ...]` appears in `## Placeholders`, and every listed placeholder appears inline (minor per mismatch). Each remaining `open` placeholder is an item: blocking in the Hook or in a loop's Payoff, significant elsewhere. Each open placeholder must also appear in `## Open threads` (minor if not). | Blocking, significant, or minor |
| W7 | The hook has all three labeled parts: context lean-in, scroll stop, contrarian snapback. A missing part is significant. A hook sentence of ten or more words is minor; report one item listing all such sentences. | Significant or minor |
| W8 | The introduction has labeled `Validating language`, `Problem`, `Promise`, `Credibility`, and `Roadmap`; the call to action has `Link`, `Curiosity gap`, and `Promise`. A missing labeled element is significant. More than one call to action is minor. | Significant or minor |

G3 applies to `## Wizard handoff`.

**Comprehension focus.** Look hardest at: undefined referents inside the prose; a promise in the
introduction or call to action that does not say what the viewer will get; contradictions between sections
(for example the promise and the payoffs); text such as "as I said earlier" that refers to nothing in the
draft; and text that depends on a placeholder. A clumsy, wordy, or unpolished sentence that is clear is not
an item, because polish is the Wizard's job.

## 11. Validation

Manual walkthroughs with an agent that has loaded the profile, in a scratch copy, written to
`docs/validation/writer-walkthroughs.md` during implementation. They start from a fixture `02-architect.md`,
`01-artist.md`, and `series/SERIES.md`.

1. **Gate stop:** the Architect's Pipeline box is not ticked. The agent stops and says why.
2. **Voice intake:** no `VOICE.md`. The agent asks for the samples and style questions one at a time and
   records them verbatim with `V<n>` IDs. It writes no style description itself.
3. **No invention:** the user says "you decide the credibility line". The agent declines and asks a smaller
   question. No anecdote, fact, or claim appears in the draft that is absent from the sources.
4. **Sources:** every drafted section has a `Sources:` line and every source resolves.
5. **Placeholders:** the user cannot supply a needed beat. The agent inserts a placeholder, keeps drafting,
   asks again before submission, and on a second "I don't know" leaves it `open`, lists it in Open threads,
   and does not fill it.
6. **Approval and coverage:** the user rejects one section. It is redrafted or left `open`. The Skeleton
   coverage list accounts for every skeleton element, and nothing is dropped silently.
7. **Skeleton followed:** the user asks to swap two loops. The agent records a requested structural change
   under Open threads, does not apply it, and continues.
8. **Hook last:** the hook is not drafted before every other section is approved. It has the three parts, no
   sentence of ten or more words, and no channel introduction, credentials, or generic welcome.
9. **Voice, not polish:** the draft uses the user's phrasing and phrases from `VOICE.md`, avoids the phrases
   they said they avoid, and makes no retention-driven cuts.
10. **Resume:** end mid-body, restart, and the agent resumes at the recorded phase without repeating
    questions.
11. **Submit and return:** on "done" the agent writes the Wizard handoff and moves the task to `review`
    without scoring. Given a fixture critique in the Reviewer's log format with three unclear items, it asks
    about each without answering any.

## 12. Open items

Decisions made during design:
- The Writer drafts from sources and the user approves, edits, or rejects each section.
- Voice lives in a shared `series/VOICE.md` created by the Writer by interview.
- Provenance is per section, not per sentence.
- Placeholders are allowed while drafting, resolved before submission where possible, and deducted by the
  Reviewer if they remain.
- The skeleton is followed strictly; structural changes are recorded, not applied.
- The hook is drafted last, from the three-part formula, with sentences under ten words.
- Drafting order: body, then frame (intro, summary, CTA), then hook. The file is laid out in script order.

Open, to resolve before or during planning:
1. **User override and orchestrator specifics.** Inherited from the Reviewer and Artist specs. The override question is resolved: there is none (Head Scriptwriter spec §5.4). Orchestrator specifics remain open.
2. **Reopening an earlier stage.** *(Resolved: the Head Scriptwriter reopens it at the user's request, Head Scriptwriter spec §5.3.)* `WORKFLOW.md` has no path for the user to send a task back to the
   Architect when the Writer records a requested structural change. Needs a decision, likely in
   `WORKFLOW.md`.
3. **Reviewer reading scope.** The Reviewer spec's reading scope (§4) lists `series/SERIES.md` but not
   `series/VOICE.md`. Stage 3 sources include `V<n>`, so the Reviewer plan's files (its SOUL rule 1 and its
   AGENTS step 2) need `series/VOICE.md` added, and the Reviewer spec §4 should be updated to match.
4. **Stage-3 rubric.** Built by the Writer implementation plan from §10.
5. **Target length.** Recorded in the Inputs but not checked, because the article gives no words-per-minute
   guidance.
6. **Wizard use of `VOICE.md`.** The Wizard spec will decide how it reads the voice file when editing for
   conversational tone.
7. **Scripted checkbox.** Decided in the Wizard spec (§11): the Reviewer ticks `Scripted` when stage 4 passes.

Resolved by the Head Scriptwriter spec (`docs/knowledge/specs/2026-09-20-head-scriptwriter-design.md`):
- Item 1: there is no override (§5.4).
- Item 2: on a requested structural change the Head asks the user and, if they agree, reopens the earlier
  stage: it sets the task back to in progress, unticks the later boxes, renames later outputs as stale, and
  creates fresh downstream tasks (§5.3).
