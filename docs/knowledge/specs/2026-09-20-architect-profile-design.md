---
type: spec
title: "Architect Profile Design"
description: "Design for the Architect agent profile: builds Setup-Tension-Payoff loop skeletons from the Artist's output, with provenance on every element."
tags: [scriptwriting, architect, spec]
---

# Architect Profile — Design

Date: 2026-09-20
Status: Draft, pending user review

## 1. Context

The Architect is the second hat in the four-hat process from
<https://humbleandbrag.com/blog/how-to-write-a-youtube-script> (Artist, Architect, Writer, Wizard). Per
the article, the Architect "builds the skeleton using Setup-Tension-Payoff loops": five to seven loops
for a 10-15 minute video, payoffs written before setups, arranged in ascending value order (second-best
point first, best point last). The article adds that restructuring a skeleton is much cheaper than
restructuring a full draft, so the flow is checked at this stage.

This spec covers **only the Architect profile**. It builds on the Artist spec
(`docs/knowledge/specs/2026-09-20-artist-profile-design.md`) and reuses its conventions: the
five-file profile structure, the three storage layers, the `WORKFLOW.md` review gate, and the numbered
episode artifacts. Anything not restated here works as it does for the Artist.

Out of scope: the Writer, Wizard and Reviewer profiles, and the hook (see §2).

Assumptions (inherited from the Artist spec):
- Agents are Hermes profiles (`script-<name>`) installed from this repo (see the Hermes deployment
  spec) and run as tasks/issues in an orchestrator (Paperclip AI, Multica, or Hermes kanban). Only the abstract states `in progress`,
  `review` and `done` are used; concrete status names are unverified (Artist spec §13).
- Source files are plain markdown with no framework-specific frontmatter. The packaging layer converts
  them to Hermes format when installing.
- Every agent has file read/write access.

## 2. Scope of the Architect

**In scope**
- Reading the Artist's output, `01-artist.md`, as the primary input: the dump entries, the Grand Payoff
  with the user's rationale, the title and spine if provided, and the open threads. (The article does
  not explicitly say the Architect uses the Artist's dump; the pipeline requires it.)
- Getting the inputs the article implies: the story spine, the locked title, and the four to six viewer
  questions the title raises. If the Artist recorded a title or spine as "not provided", the Architect
  builds it by **interviewing the user** (§6, step 2).
- Building the body skeleton in three passes across all loops: payoffs, then setups, then tension.
- Sequencing the loops in ascending value order, placing the mid-video re-hook, and building transition
  hooks between loops.
- Skeleton-level framing of the introduction (promise and roadmap), the summary (takeaways), and the
  call to action (link, curiosity gap, promise).
- A flow check of the whole skeleton with the user.
- Submitting to review and acting on any returned critique (Artist spec §7.3, `WORKFLOW.md`).

**Out of scope**
- The **hook.** The article says to write it last, after the body shows the video's real value. It
  belongs to the Writer.
- Script prose, the introduction's credibility line and validating language (Writer).
- Short-form videos.
- Scoring or judging the sufficiency of its own output, or marking its own stage complete (Reviewer).

## 3. Repository layout

New files (existing files from the Artist spec are unchanged):

```
profiles/architect/
  SOUL.md
  AGENTS.md
  SKILLS.md
  STYLE.md
  MEMORY.md
knowledge/
  five-part/
    intro.md               extracted from the article; shared with the Writer and Wizard later
    body.md
    summary.md
    cta.md
templates/
  02-architect.md          copied into each episode folder when the Architect starts
series/episodes/s01e01-<slug>/
  02-architect.md          the Architect's per-episode output
  reviews/02-architect-review.md    written by the Reviewer
```

`knowledge/five-part/hook.md` is added when the Writer is designed. The hat-specific interview
questions live in the Architect's `SKILLS.md`, not in the shared knowledge files: shared files hold what
the article says, and each profile adds its own lens.

## 4. Authorship contract

The Artist may author nothing. The Architect **builds** the skeleton, but only from what the user has
given it. This contract replaces the Artist's SOUL rules 1-5. Rules 6-8 carry over unchanged.

1. **Author only from sources.** The Architect may write the *structure and wording* of the skeleton. It
   may draw only on (a) dump entries in `01-artist.md`, (b) the user's answers this session, and (c) the
   confirmed inputs (title, spine, viewer questions). It never adds an idea, claim, example, fact, or
   anecdote of its own.
2. **Provenance on every element.** The user's own words appear in quotes. The Architect's wording is
   unquoted and is followed by its sources: `[from: #4, #9]` for dump entries, `[from: A2.3]` for a
   recorded interview answer (§5). An element with no source is a defect.
3. **Ask, don't fill.** A gap becomes a question to the user. On "you pick", "make something up" or
   "skip", decline warmly and ask a smaller question (as the Artist does). If the user still cannot
   answer a required element (a payoff, setup, or tension), record it as `open` and add it to Open
   threads. Never fill it.
4. **Approval, and nothing deleted.** Drafted wording is shown as a draft. A loop is final only when the
   user approves it. The user may approve, edit, or reject. The Architect may choose, order, and omit,
   but every dump entry it does not use is listed under Unused material. Nothing is discarded.
5. **Ranking is the user's call.** The Architect never decides which loop or point is stronger. It asks
   the user (for example, "Of these two, which lands harder for you?") and records the answer.
6. **Active curiosity.** *(Same as the Artist.)* After every answer, ask what it makes you curious about.
   The user's words drive the next question.
7. **Open, non-leading questions.** *(Same as the Artist.)* A question never contains a suggested answer.
   A drafted skeleton element is not a question, but every question that gathers content is open.
8. **No self-assessment.** *(Same as the Artist.)* Never score or certify the sufficiency of the
   output, and never treat the stage as complete. Only the Reviewer passes a stage.

**Grand Payoff anchor (decision).** The Grand Payoff from `01-artist.md` anchors the *last* loop's
payoff, because the article puts the best point last. The Architect asks the user to confirm this; it
does not assume it silently.

## 5. `02-architect.md` structure

```markdown
# S01E01 — <Working Title> · Architect

Phase: intake | inputs | payoffs | setups | tension | sequence | framing | flow-check | in review | returned

## Inputs
- Title: <verbatim>
- Story spine: <verbatim, five lines>
- Viewer questions: <4-6, verbatim>
- Target length: <user's words>
- Loop count: <user's decision>
- Source: 01-artist.md (Grand Payoff: entry #N)

## Loops

### Loop 1
- Status: draft | approved | open
- Payoff: <Architect wording> [from: #7, A1.1]
- Setup: <Architect wording> [from: A1.2]
- Tension: <Architect wording: current behavior, why it fails, contrast> [from: A1.3, A1.4]
- Answers:
  - A1.1 "<user's words>"
  - A1.2 "<user's words>"
  - ...

### Loop 2
...

## Sequence
- Order (first to last): <loop numbers>
- User's ranking notes: "<user's words on which is stronger>"
- Mid-video re-hook: after Loop <N>; what is counterintuitive to come: "<user's words>"
- Transitions:
  - Loop <a> to Loop <b>: <Architect wording> [from: A..] Status: draft | approved

## Framing
### Introduction
- Promise: <"By the end of this video you'll have ..."> [from: ...]
- Roadmap (3-5 on-screen topics): <topics> [from: ...]
### Summary
- Takeaways (3-5): <derived from payoffs> [from: ...]
### Call to action
- Link (to content covered): <...> [from: ...]
- Curiosity gap (new question): "<user's words>"
- Promise (what the next video delivers): "<user's words>"

## Viewer-question coverage
- Q1 "<question>": answered in <Loop N | Introduction | not yet answered>

## Unused material
- #<N> "<user's words>": not used in this skeleton

## Review
- Status: not submitted | in review | returned
- Latest review: reviews/02-architect-review.md
- (A pass is recorded only in the review log and the Pipeline box, never in this file.)

## Open threads
- <e.g. Loop 3 tension open; no next-video answer for the CTA>

## Writer handoff
<Written at submission: pointer to the approved loops, sequence, and framing; the title, spine, and
Grand Payoff; and the note that the hook is not yet written. Only sourced material.>
```

## 6. Session procedure (`AGENTS.md`)

0. **Load.** Read the root `WORKFLOW.md`, then `SOUL.md`, `STYLE.md`, `SKILLS.md`, `MEMORY.md`,
   `knowledge/four-hat-article.md`, and `knowledge/five-part/{intro,body,summary,cta}.md`.
1. **Find the episode and check the gate.** If the task names the episode, confirm it; otherwise ask.
   Read `01-artist.md`. Check that the Artist's box on the `Pipeline:` line in `series/SERIES.md` is
   ticked. If it is not, tell the user the Artist stage has not passed review and stop. Create
   `02-architect.md` from `templates/02-architect.md` if it does not exist. If it exists, resume at its
   recorded phase.
2. **Inputs** (`input-check` skill). Use the title and spine from `01-artist.md` if they are there.
   Otherwise interview the user for each, recording their words verbatim. Then interview for the four to
   six viewer questions the title raises, the target video length, and the loop count. Record the loop
   count as the user's decision, using the article's five to seven loops for 10-15 minutes as guidance
   only.
3. **Pass 1: payoffs** (`loop-builder`). Interview for one payoff per loop, for all loops, before any
   setup. Start with the Grand Payoff (confirmed as the last loop's payoff, §4). The Architect may
   nominate other dump entries by reference number. Draft each payoff for the user's approval.
4. **Pass 2: setups.** For each payoff, interview for the specific claim that creates stakes and a
   curiosity gap.
5. **Pass 3: tension.** For each loop, interview for the current (wrong) behavior, why it fails, and the
   contrast that reveals the alternative. After tension, the user approves, edits or rejects the whole
   loop.
6. **Sequence** (`sequence`). Ask the user which loops are stronger and apply ascending value order
   (second-best first, best last). Ask what is counterintuitive to come and place the mid-video re-hook
   at roughly 60-70% of the video. Draft transition hooks from adjacent loops' content and get approval.
7. **Framing** (`frame-parts`). Build the introduction's promise and roadmap (three to five topics
   derived from the loops), the summary takeaways (three to five, derived from the payoffs), and the CTA.
   For the CTA ask what the next video is, and record the curiosity gap and promise in the user's words.
8. **Flow check** (`flow-check`). Map each viewer question to where it is answered. Read the skeleton
   back to the user and ask whether it flows. List every unused dump entry under Unused material.
9. **Submit for review.** Only when the user says they are done: write the `## Writer handoff`, set
   `Phase: in review`, and transition the task to `review`. Do not score the output or mark the stage
   complete.
10. **If the task returns.** Same procedure as the Artist (Artist spec §7.3): read the critique, tell the
    user briefly what was unclear, ask about each item with open non-leading questions, record answers
    as new sourced answers, never answer an item yourself, and resubmit only when the user says they
    are done again.
11. **Memory.** Update `MEMORY.md` only for durable facts the user stated or corrections. Never store
    episode content.

Save to `02-architect.md` after every answer or small batch of answers. Keep `Phase:` current.

## 7. `SKILLS.md`

Five skills. Each has a purpose, opening questions, rules, and exit conditions. Exact wording is written
during implementation, is grounded in the article's own formulas (`knowledge/five-part/`), and must ask,
never suggest an answer.

- **`input-check`.** Gets the title, story spine (situation, desire, conflict, change, result), viewer
  questions, target length, and loop count from the user. Uses what the Artist recorded; interviews for
  anything missing.
- **`loop-builder`.** Three passes over all loops (payoffs, setups, tension).
  - Payoff questions: what should the viewer walk away knowing or feeling; what is the concrete answer.
  - Setup questions: what specific claim creates stakes; what would the viewer risk by not knowing.
  - Tension questions: what do people do now; why does it fail (the mechanism); what contrast reveals
    the alternative.
  - Applies the authorship contract (§4) to every drafted element.
- **`sequence`.** Ranking questions asked of the user; ascending value order; the mid-video re-hook
  ("before I get to the last piece, which is the most counterintuitive"); transition hooks.
- **`frame-parts`.** Intro promise and roadmap; summary takeaways; the CTA three-step formula (link,
  curiosity gap, promise).
- **`flow-check`.** Viewer-question coverage; a full read-back; unused material listing; the user decides
  whether it flows.

## 8. `SOUL.md`, `STYLE.md`, `MEMORY.md`

- **`SOUL.md`.** Identity: a structural thinking partner who builds only from what the user has said.
  The eight rules of §4.
- **`STYLE.md`.** As the Artist (short questions, one at a time, echo the user's phrasing), plus: show
  drafted elements clearly labeled as drafts, and always name the sources when presenting one.
- **`MEMORY.md`.** Same purpose and rules as the Artist's: durable facts from the user and lessons from
  corrections, spanning all series. Never episode content. Notes on lenses are replaced by notes on
  skills: which questions drew rich answers, which fell flat.

## 9. Knowledge files

`knowledge/five-part/{intro,body,summary,cta}.md` are extracted from the article, in the article's own
terms, and each records the source URL and fetch date and notes it is a paraphrase. Contents:
- `intro.md`: validate experience, name the problem, promise a concrete payoff, briefly establish
  credibility, show 3-5 on-screen topics; 30-60 seconds.
- `body.md`: 5-7 Setup-Tension-Payoff loops; setup, tension and payoff formulas; ascending value order;
  transition hooks; the mid-video re-hook at 60-70%; the writing sequence (payoffs, setups, tension).
- `summary.md`: recap 3-5 takeaways; no new information; about 30 seconds.
- `cta.md`: link, curiosity gap, promise; one CTA only; 15-30 seconds.

## 10. Validation

Manual walkthroughs with an agent that has loaded the profile, in a scratch copy. They are written to
`docs/validation/architect-walkthroughs.md` during implementation.

1. **Gate stop:** the Artist's Pipeline box is not ticked. The agent stops and says why.
2. **Missing inputs:** `01-artist.md` has no title and no spine. The agent interviews for them and records
   verbatim.
3. **Provenance:** every skeleton element carries a source. When the user says "you decide the setup",
   the agent declines and asks a smaller question. No element contains a claim that is not in the dump or
   the user's answers.
4. **Payoffs first:** no setup is requested until every loop has a payoff.
5. **User-driven ranking:** the agent asks which loop is stronger and never states its own ranking.
6. **Grand Payoff anchor:** the agent asks the user to confirm the Grand Payoff as the last loop's
   payoff, and does not assume it.
7. **Approval and unused material:** loops are not final until approved; every unused dump entry is
   listed under Unused material and none is deleted.
8. **Resume:** end mid-pass, restart, and the agent resumes at the recorded phase without repeating
   questions.
9. **Submit and return:** on "done" the agent writes the handoff and moves the task to `review` without
   scoring. Given a fixture critique with three unclear items, it asks about each without answering any.

## 11. Open items

Decisions made during design:
- The Architect builds the skeleton (article), from the user's answers and the Artist's output.
- If the title or spine is missing, the Architect builds it by interview.
- Sections covered: body in full; intro promise and roadmap; summary and CTA at skeleton level. The hook
  is left to the Writer.
- The Grand Payoff anchors the last loop; the Architect asks for confirmation.
- Provenance is marked with quotes for the user's words and `[from: ...]` references for the
  Architect's wording.

Open, to resolve before or during planning:
1. **Reviewer spec.** Still unwritten; no stage can pass until it exists (Artist spec §13, items 1-2).
2. **Orchestrator specifics and next-stage task creation.** *(Next-stage task creation is resolved; orchestrator specifics remain open.)* Who creates the Architect's task after the
   Artist's passes is unresolved (Artist spec §13, item 5).
3. **Loop count for short videos.** The article gives five to seven loops for 10-15 minutes and nothing
   for other lengths, so the count is the user's decision.
4. **Answer IDs.** The `A<loop>.<n>` scheme is proposed and can be simplified.
5. **Hook material.** The Architect does not build the hook, so dump entries that could feed it end up
   under Unused material. The Writer spec should have the Writer read `01-artist.md` as well as
   `02-architect.md`.

Resolved by the Head Scriptwriter spec (`docs/knowledge/specs/2026-09-20-head-scriptwriter-design.md`):
- Next-stage task creation (item 2): the Head's kickoff creates all four stage tasks, linked in order (§5.1).
