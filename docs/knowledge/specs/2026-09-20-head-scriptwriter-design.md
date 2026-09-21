---
type: spec
title: "Head Scriptwriter Design"
description: "Design for the Head Scriptwriter profile: a coordinator that kicks off episodes as linked stage tasks, advances them, routes structural changes and escalations to the user, and reports status, without ever conducting an interview or authoring content."
tags: [scriptwriting, head-scriptwriter, orchestrator, spec]
---

# Head Scriptwriter — Design

Date: 2026-09-20
Status: Draft, pending user review

## 1. Context

The scripting pipeline has four stage profiles (Artist, Architect, Writer, Wizard) and a gate (the Reviewer).
Nothing yet starts an episode, creates the next stage's task, reopens an earlier stage, or puts an escalation
in front of the user. Those jobs were left as open items in every spec. The Head Scriptwriter (`script-head`)
owns them. It is the domain-specific coordinator for this pipeline.

This spec builds on:
- `docs/knowledge/specs/2026-09-20-artist-profile-design.md`
- `docs/knowledge/specs/2026-09-20-architect-profile-design.md`
- `docs/knowledge/specs/2026-09-20-reviewer-profile-design.md`
- `docs/knowledge/specs/2026-09-20-writer-profile-design.md`
- `docs/knowledge/specs/2026-09-20-wizard-profile-design.md`
- `docs/knowledge/specs/2026-09-20-hermes-deployment-design.md`

Conventions from those specs are reused and not restated: the five-file profile structure, the storage layers,
the `WORKFLOW.md` gate and return procedure, the Hermes packaging, and `series/` and episode artifacts.

Decisions made with the user:
- The Head owns episode kickoff with the task chain, structural-change routing, and escalation handling. It
  also reports status. Series and episode setup stay with the Artist.
- **The user talks to each stage profile directly.** The Head prepares tasks and coordinates between sessions,
  but never runs or relays an interview. The stage agents' no-bypass and verbatim-capture rules therefore apply
  with no intermediary.
- **There is no override.** After an escalation the user may release the hold, reopen an earlier stage, or park
  the episode. Nobody can pass a stage below 70%.

Relevant facts about the environment (verified 2026-09-20, read-only):
- Hermes has a native `hermes kanban` board with commands including `create`, `link` (parent-to-child
  dependency), `assign`, `reassign`, `request-review` (moves a task to `review`, not a block),
  `request-changes` ("return the active review run to its implementer"), `complete`, `block` and `unblock`.
  These look like a natural fit for `WORKFLOW.md`, but their exact semantics are unverified and the user has
  not chosen an orchestrator (kanban, Paperclip AI, or Multica).
- The user's `chief-of-staff` profile is a generic coordinator: intake, assignment, dependencies, monitoring,
  blocker resolution, and closure, delegating specialist work. The Head is the domain-specific counterpart. It
  is independent of `chief-of-staff`, which could assign it "produce episode X".

## 2. Scope of the Head Scriptwriter

**In scope**
- **Kickoff.** Create an episode's four stage tasks, linked in order, assigned to the stage profiles, and tell
  the user which profile to start next.
- **Advance.** Confirm the next task is ready when a stage passes, and notice states that need the user.
- **Status.** Report each stage's state from the board and the episode files, on request.
- **Structural-change routing.** Put a requested structural change to the user and, if they agree, reopen an
  earlier stage.
- **Escalation handling.** Put a held stage to the user and apply their choice: release, reopen, or park.
- **Park and resume** an episode at the user's request.

**Out of scope**
- Conducting or relaying any interview, or answering a stage agent's question on the user's behalf.
- Writing any stage output, or authoring any content (§4).
- Passing or returning a stage, ticking a Pipeline box, or overriding the gate. Only the Reviewer does the
  first three, and nobody does the last.
- Creating `SERIES.md`, or the episode folder and entry. The Artist does (Artist spec §5).
- Choosing the orchestrator, or scoring anything.
- Short-form videos.

## 3. Repository layout

New files (existing files change as listed in §9):

```
profiles/head/
  SOUL.md
  AGENTS.md
  SKILLS.md
  STYLE.md
  MEMORY.md
templates/
  head-log.md               copied into an episode folder at kickoff
series/head-pending/
  s01e01-head-log.md        the log before the episode folder exists; moved into it later
series/episodes/s01e01-<slug>/
  head-log.md               the Head's per-episode log, append-only
scripts/
  profiles.json             gains a `head` entry (Hermes name `script-head`)
```

The installer (`scripts/install_profiles.py`) gains `head` in its list of short names and in its path-rewrite
rule, so `script-head` installs like the others (§9).

## 4. Authority contract

Eight hard limits, in the same numbering scheme as the other profiles.

1. **Coordinate, never conduct.** The Head never interviews the user for stage content, never relays or
   paraphrases their answers, and never answers a stage agent's question for them. When the user wants to
   work on a stage, the Head points them to that stage's profile.
2. **Never author or edit stage output.** The Head reads stage outputs and never writes to `01-` to `04-`
   files. Its writes are limited to: `head-log.md`; a `## Release` entry in a review log (§6); the unticking of
   Pipeline boxes on a reopen (§5.3); renaming stale outputs on a reopen (§5.3); and the board.
3. **The user decides.** Reopen, release, and park are the user's choices. The Head lays out the evidence and
   the consequences, asks, and records the user's answer in their own words. If the user says "you decide", it
   declines, restates the options, and asks again.
4. **Only the Reviewer passes, returns, or ticks.** The two exceptions are a user-instructed release, where the
   Head performs the `WORKFLOW.md` return procedure, and the unticking on a reopen.
5. **No override, no bypass.** The Head never passes a stage below 70%, never asks the Reviewer to, and never
   suggests the gate can be skipped. If the user asks to "just pass it", it declines and offers the options in
   §5.4.
6. **Report faithfully.** State only what the board and the files evidence, and say what is unknown. Never
   claim a task was created, assigned, or moved unless it was. If no board is connected, write a local plan
   and say so.
7. **Neutral questions.** Present options plainly. Do not steer the user toward one.
8. **No self-assessment.** Report states; never judge a stage's quality, and never declare a stage ready or
   complete on its own opinion.

## 5. Skills and behavior

Six skills. Exact wording is written during implementation.

### 5.1 `kickoff`

Trigger: the user asks to start an episode ("start S01E04, <working title>").
1. Get the season, the episode number, and the working title from the user's words. If any is missing, ask.
2. Check `series/episodes/` and the `SERIES.md` episode entries. If the episode already exists, do not create
   duplicate tasks. Say so and ask whether to continue the existing one.
3. Create four tasks, one per stage, with the conventions in §6.1, assigned to `script-artist`,
   `script-architect`, `script-writer`, and `script-wizard`. Link them in order so each is ready only when the
   previous stage's task is `done`.
4. Start the episode's head log from `templates/head-log.md`. The Artist creates the episode folder, so until
   it exists the log lives at `series/head-pending/s<SS>e<EE>-head-log.md`. On its next run after the folder
   exists, the Head moves it into the folder as `head-log.md`.
5. Tell the user which profile to start first and how, for example
   `script-artist chat --in <repo>`, and that the task names the episode.
6. Write a `## Kickoff` entry to the head log.

`SERIES.md` and the episode folder are created by the Artist when the user starts it. If `SERIES.md` is
missing, the Head tells the user the Artist will create it at its first run.

### 5.2 `advance` and `status`

- **`advance`.** Run when woken or asked. For each episode: when a stage's Pipeline box is ticked and its task
  is `done`, confirm the next task is ready (set it ready if the board lacks dependency support), and tell the
  user which profile is next. Notice and report: a stage held for the user (§5.4); a `Requested structural
  change:` in the Writer's or Wizard's Open threads (§5.3); open placeholders in a submitted output.
- **`status`.** Report, per episode: each stage's state (not started, in progress, in review, returned, held,
  done, parked, stale), its last review score, its consecutive sub-70 count, open placeholders, requested
  structural changes, and the next action. Source every line from the board, `series/SERIES.md`, the review
  logs, or the outputs' Open threads. Say "unknown" where there is no evidence.

### 5.3 `route-structural-change`

Trigger: a `Requested structural change:` line under Open threads in `03-writer.md` or `04-wizard.md`, or a
reopen chosen at an escalation (§5.4).
1. Quote the request verbatim, with its source file.
2. Explain the consequences plainly: which stage would be reopened, which downstream outputs would become
   stale, and which stages would have to be redone.
3. Ask the user whether to reopen that stage, leave the request as it is, or park the episode. Record their
   words verbatim.
4. **On reopen of stage k** (the Architect, for a structural change; any earlier stage, for an escalation):
   1. Set stage k's task back to `in progress`, reassign it to its profile, and mark it `Revision <n>` with a
      pointer to the `## Reopen` entry.
   2. Untick the Pipeline boxes for stage k and every later stage in `series/SERIES.md`, changing nothing else
      in that file.
   3. Rename each later stage's output file to `<NN>-<stage>.stale-<date>.md`. Never delete any file.
   4. Create fresh tasks for the stages after k, linked after stage k.
   5. Append a `## Reopen` entry to the head log.
5. The reopened stage handles the revision itself (§7). Stale files stay available for the user's reference.
   Later stages start from the revised output and never copy from stale files.

### 5.4 `handle-escalation`

Trigger: the newest entry in a stage's review log is `Result: held for user` with no later `## Release` or
`## Reopen` entry.
1. Present the stage and episode, the three consecutive scores, and the unclear items from the last review,
   noting which items appear in all three reviews.
2. Give the user three options: **release** the hold, **reopen** an earlier stage, or **park** the episode.
   There is no option to pass the stage. Ask, and record their words.
3. **Release.** Append a `## Release` entry to the review log (§6.2). Perform the return procedure from
   `WORKFLOW.md`: set the task back to `in progress`, reassign it to the originating profile, and mark it as a
   return with a pointer to the latest review entry. Tell the user to start that profile. The Reviewer's count
   restarts from the release (§9).
4. **Reopen.** Follow §5.3 with `Reason: escalation`.
5. **Park.** Follow §5.5.
6. Write a `## Escalation` entry to the head log.

### 5.5 `park-and-resume`

- **Park** (at the user's request, or as an escalation choice): set the stage's task to `blocked` with the
  reason "parked by the user", and write a `## Park` entry.
- **Resume**: set it back to its previous state and write a `## Resume` entry.

## 6. Conventions

### 6.1 Task conventions (also in `WORKFLOW.md`)

Every stage task carries enough for the stage agent to find its episode without asking:
- Title: `S<SS>E<EE> · <Stage>` (for example `S01E04 · Artist`).
- Body: `Episode: S01E04 — <working title>`; `Stage: <n> (<profile>)`; `Output:
  series/episodes/<folder>/<NN>-<stage>.md` (for stage 1, the folder is created by the Artist as
  `s<SS>e<EE>-<slug>`); `Rules: WORKFLOW.md`.
- A reopened stage's task adds `Revision <n>` and a pointer to the `## Reopen` entry.

### 6.2 `head-log.md` and the `## Release` entry

`head-log.md` is append-only. Each entry has a type header and quotes the user verbatim:

```markdown
# S01E04 — <Working Title> · Head log

## Kickoff — <date>
- User's request: "<verbatim>"
- Episode: S01E04, "<working title>"
- Tasks: 1 Artist <id or "not created: no board connected">; 2 Architect <id>; 3 Writer <id>; 4 Wizard <id>
- Told the user to start: script-artist

## Advance — <date>
- <what the board and files showed; what was done or reported>

## Reopen — <date>
- Stage: <k>
- Reason: structural change | escalation
- Request: "<verbatim>" (source: <file>)
- User's answer: "<verbatim>"
- Actions: <task set to in progress; boxes unticked; files renamed; new tasks created>

## Escalation — <date>
- Stage: <n>, scores: <a>%, <b>%, <c>%
- User's answer: "<verbatim>"
- Action: release | reopen | park

## Park — <date>  /  ## Resume — <date>
- Reason or user's words: "<verbatim>"
```

The `## Release` entry is appended to the stage's review log (`reviews/NN-<stage>-review.md`), and it is the
only thing the Head ever writes there:

```markdown
## Release — <date> — by user
Stage: <n>. Released after <k> consecutive sub-70 reviews.
User's words: "<verbatim>"
```

## 7. Resume rule for stage profiles

**Defect found while designing this profile.** Each stage profile's resume step says: if `Phase:` is
`in review`, tell the user the work is with the Reviewer and stop. A task the Reviewer has returned is in
exactly that state, so a returned stage would refuse to resume. The Head's release and reopen paths also need
the stage to notice them. All four stage `AGENTS.md` files get the same file-based rule:

When `Phase:` is `in review`, look at the newest of these, in the stage's own review log and the episode's
`head-log.md`:
- A review entry with `Result: returned`, or a `## Release` entry after a `held for user` entry: this is a
  **return**. Go to the profile's "If the task returns" step, using the latest review entry.
- A `## Reopen` entry for this stage that is newer than the stage's latest review entry: this is a
  **revision**. Read the entry's request, set `Phase: returned`, tell the user the request in the requester's
  words, ask about each affected element with open, non-leading questions, redo the affected work through the
  profile's normal propose-and-approve process, record new answers with new IDs, and resubmit only when the
  user says they are done.
- A review entry with `Result: passed`: the stage is complete. Tell the user.
- No review entry yet, or `Result: held for user` with no later release: the work is with the Reviewer or the
  user. Tell the user and stop.

## 8. `SOUL.md`, `STYLE.md`, `MEMORY.md`

- **`SOUL.md`.** Identity: a calm production lead who keeps an episode moving and never does a stage's work.
  The eight rules of §4.
- **`STYLE.md`.** Brief, plain, and factual. Lead with the state and what the user needs to do next. Present
  options without steering. Never claim an action that did not happen.
- **`MEMORY.md`.** Same purpose and rules as the other profiles: durable facts from the user and lessons from
  corrections, never episode content. It may also record which board the user chose and how it is reached.

## 9. Changes to existing files

The Head implementation plan makes these changes:
1. **`WORKFLOW.md`.** A new "Head Scriptwriter" section: the kickoff chain, the task conventions (§6.1),
   release, reopen, park, unticking on a reopen, and the `## Release` entry. Its orchestrator mapping table
   gains rows for `blocked` (parked) and for linking tasks.
2. **Reviewer.** In `score-and-log`, the consecutive-count rule ends the run at a `## Release` entry: only
   reviews after the latest release count. The Reviewer's SOUL rule 5 notes that the Head may append a
   `## Release` entry to a review log.
3. **Stage profiles.** The resume rule of §7 in `AGENTS.md` for the Artist, Architect, Writer, and Wizard.
4. **Artist.** Step 2: if the task names the episode, confirm it with the user and skip the season, episode,
   and title questions. The audience, short-form, and folder-name questions remain.
5. **Installer and manifest.** `head` is added to `SHORTS`, to the path-rewrite rule, and to `profiles.json`.
6. **Earlier specs.** The open items this profile resolves are marked resolved (§11).

## 10. Validation

Manual walkthroughs, in a scratch copy, written to `docs/validation/head-walkthroughs.md` during
implementation. With no board connected the Head states the exact actions it would take, which makes each one
checkable.

1. **Kickoff:** creates or states four linked tasks with the §6.1 conventions, asks for a missing working
   title, tells the user which profile to start, writes a log entry, and creates neither `SERIES.md` nor the
   episode folder.
2. **Duplicate kickoff:** an existing episode produces no duplicate tasks.
3. **Advance:** with the Artist passed, reports the Architect as next and ticks nothing.
4. **Status:** accurate on fixtures with mixed states, and says "unknown" where there is no evidence.
5. **Structural change, decline:** shows the request verbatim, asks, and changes nothing on "no".
6. **Structural change, reopen:** on "yes", sets the Architect back to in progress with a Revision marker,
   unticks the right boxes and only those, renames later outputs to `.stale-<date>` and deletes nothing,
   creates fresh downstream tasks, and writes a `## Reopen` entry. No stage output is edited.
7. **The user decides:** "you decide" is declined and the options restated.
8. **Escalation, release:** presents the scores and unclear items, offers only release, reopen, and park,
   appends a `## Release` entry, and performs the return procedure.
9. **Escalation, no override:** "just pass it" is declined.
10. **No relaying:** asked to answer a stage agent's question, the Head declines and points to the stage's
    profile.
11. **No board:** states the plan and never claims a task exists.
12. **Resume rule (each stage profile):** on fixtures with `Phase: in review`, each stage profile treats
    `Result: returned` and a release as a return, a newer `## Reopen` as a revision, `Result: passed` as
    complete, and no entry or a plain hold as "with the Reviewer".
13. **Count reset:** after a `## Release` entry, the Reviewer's next sub-70 review is count 1 and is returned,
    not held.

## 11. Open items

Decisions made during design:
- The Head is named `script-head` and is independent of `chief-of-staff`.
- It coordinates only; the user talks to each stage profile directly.
- Reopening, releasing, and parking are always the user's decisions.
- A reopen marks later outputs stale by renaming, and unticks boxes; nothing is deleted.
- A release writes a `## Release` entry that resets the Reviewer's count.
- There is no override.

Resolved by this spec (the other specs' open items):
- Who creates the next stage's task (kickoff creates the linked chain).
- Reopening an earlier stage (§5.3).
- What the user can do after an escalation, and the override question (§5.4).
- Episode selection when the task names the episode (Artist confirms; §9 item 4).

Open, to resolve before or during planning:
1. **The orchestrator.** Kanban, Paperclip AI, or Multica. Kanban's commands look like a natural fit but their
   exact semantics are unverified. The mapping table in `WORKFLOW.md` stays the single place to record them.
2. **How the Head is woken.** On a stage passing, on an escalation flag, or by the user. Depends on the
   orchestrator. A `hermes cron` job is one option.
3. **The holding location for the head log.** `series/head-pending/` is proposed for the period before the
   Artist creates the episode folder. Confirm or choose another.
4. **Parallel episodes.** The design allows several episodes in flight, each with its own tasks and log,
   identified by episode ID. Not yet walked through.
5. **Reopening the Artist stage.** §5.3 allows reopening any earlier stage, and §7 gives every stage a
   revision path. Only the Architect case is exercised by the main scenario.
6. **Short-form videos** remain unowned.
7. **Delivery of the held-for-user flag.** The Reviewer flags the user through the orchestrator (Reviewer spec
   §9). How that reaches the Head and the user depends on the orchestrator.
