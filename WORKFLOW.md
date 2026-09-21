# WORKFLOW

How work moves between agent profiles in this project. This file is process only: it says nothing about
how a profile behaves. Personality, interview rules, and style live in each profile's own files.

Every profile reads this file first when it loads. Profiles do not restate it.

## Stages and artifacts

Work on each episode moves through four stages, in order. Each stage reads the previous stage's file.

| Stage | Profile | Output file (in `series/episodes/<id>/`) |
|---|---|---|
| 1 | Artist | `01-artist.md` |
| 2 | Architect | `02-architect.md` |
| 3 | Writer | `03-writer.md` |
| 4 | Wizard | `04-wizard.md` |

The Reviewer writes to `reviews/` in the same episode folder (see "The review log").

## States

Abstract task states used throughout this project:

- `in progress`: a profile is working with the user.
- `review`: the profile has submitted its output; the Reviewer is assessing it.
- `done`: the stage passed review.

See "Orchestrator mapping" for how these map to the orchestrator's real status names.

## Who can move what

- The originating profile moves a task from `in progress` to `review`, and only after the **user** says
  they are done. The profile's own opinion that it is finished is not enough.
- Only the Reviewer moves a task out of `review`.
- A profile never scores its own output and never marks its own stage complete.

## The gate

When a task is in `review`, the Reviewer reads the stage's **output files** (not the conversation) and
scores its confidence, from 0% to 100%, that it understands what was generated. The score is 100% minus
itemized deductions, defined in `profiles/reviewer/rubrics/scoring.md`.

- **70% or higher:** the stage passes. The Reviewer ticks the stage's box on the `Pipeline:` line of the
  episode entry in `series/SERIES.md`, and the task moves to `done`.
- **Below 70%:** the task **cannot transition**. The Reviewer returns it (next section), except on the
  third consecutive sub-70 review of a stage, which is escalated instead (see "Escalation").
- No user override is defined. The gate is strict.

## The return procedure

To return a task, the Reviewer does all three of these together:

1. Set the status back to `in progress`. Do not send it to an earlier queue state: the work has started
   and the originator holds the user's context.
2. Reassign the task to the originating profile.
3. Mark it as a return: add a label if the orchestrator supports labels, and point to the latest entry
   in `reviews/` so the originator knows it is answering a critique.

If the orchestrator supports a custom "changes requested" status, it may be used for visibility, but it
must behave like `in progress` for the gate.

## Escalation

The third consecutive sub-70 review of the same stage is not returned. The Reviewer logs it with
`Result: held for user`, flags the stage to the user through the orchestrator, and keeps the task in
`review`. It does not pass the stage, so this is not an override. The count resets when a review passes.
The Head Scriptwriter puts the choices to the user: release the hold, reopen an earlier stage, or park the
episode. There is no override (see "Head Scriptwriter").

## Critique scope

A returned critique covers comprehension and completeness only: what is unclear, ambiguous, missing
context, contradictory, or unresolved, plus mechanical completeness checks defined in the stage rubrics
(required sections present, provenance markers resolving, and similar). A weak idea is not a defect.
Reviewers do not judge quality or rank ideas, and never suggest content, answers, or wording.

## The review log

The Reviewer appends every review to `series/episodes/<id>/reviews/01-artist-review.md` (and the
matching `02-`, `03-`, `04-` file for later stages). Each entry has a header `## Review <n> — <date> — <score>%`, a
`Result` (`passed`, `returned`, or `held for user`), the count of consecutive sub-70 reviews, a table of
deductions (location, category, severity, points, item), the arithmetic, the status of prior items, and
remaining minor items as notes when the stage passed. The log is append-only. The full format is in
`profiles/reviewer/SKILLS.md`, skill `score-and-log`.

## Bookkeeping

A stage's box on the `Pipeline:` line in `series/SERIES.md` is ticked only by the Reviewer, on pass.
The stage's own profile never ticks it. When stage 4 (the Wizard) passes, the Reviewer also ticks `Scripted` on
the episode's `Long-form` line. `Filmed` and `Published` are ticked by the user. The Head Scriptwriter unticks boxes only when the user reopens
a stage (see "Head Scriptwriter").

## Head Scriptwriter

`script-head` coordinates episodes. It never conducts an interview, never writes a stage output, and never
passes, returns, or overrides a stage. The user talks to each stage profile directly.

### Task conventions

Every stage task carries the episode, so a stage agent never has to ask which episode it is for:

- Title: `S<SS>E<EE> · <Stage>` (for example `S01E04 · Artist`).
- Body: `Episode: S01E04 — <working title>`; `Stage: <n> (<profile>)`;
  `Output: series/episodes/<folder>/<NN>-<stage>.md` (for stage 1 the folder is created by the Artist as
  `s<SS>e<EE>-<slug>`); `Rules: WORKFLOW.md`.
- A reopened stage's task adds `Revision <n>` and points to the `## Reopen` entry in the episode's
  `head-log.md`.

### Kickoff

At kickoff the Head creates the four stage tasks and links them in order, so each stage's task is ready only
when the previous stage's task is `done`. It records the kickoff in the episode's `head-log.md`. Until the
Artist creates the episode folder, the log is at `series/head-pending/s<SS>e<EE>-head-log.md`.

### Release, reopen, and park

- **Release.** After a stage is held for the user, and only when the user says so, the Head appends a
  `## Release — <date> — by user` entry to the stage's review log and performs the return procedure above. The
  Reviewer's consecutive count restarts after the latest release.
- **Reopen.** When the user chooses to reopen stage k, the Head sets stage k's task back to `in progress` with a
  `Revision <n>` marker, unticks the boxes for stage k and every later stage in `series/SERIES.md`, renames each
  later stage's output to `<NN>-<stage>.stale-<date>.md` (nothing is deleted), creates fresh tasks for the later
  stages, and appends a `## Reopen — <date>` entry to `head-log.md`.
- **Park.** The Head sets a stage's task to `blocked` (parked by the user) and records it in `head-log.md`.
  Resuming restores its previous state.
- The Head is the only profile other than the Reviewer that writes to a review log or touches a Pipeline box,
  and only as described here. There is no way to pass a stage below 70%.

### Resuming after review

A stage profile that finds `Phase: in review` must not assume the work is still with the Reviewer. It looks at
the newest of these, in the stage's own review log (`reviews/<NN>-<stage>-review.md`) and the episode's
`head-log.md`:

- A review entry with `Result: returned`, or a `## Release` entry after a `held for user` entry: a **return**.
  The stage resumes at its "If the task returns" step, using the latest review entry.
- A `## Reopen` entry for this stage that is newer than the stage's latest review entry: a **revision**. The
  stage resumes at its "If the task returns" step, with the request in the entry in place of a critique.
- A review entry with `Result: passed`: the stage is complete. Tell the user.
- No review entry yet, or `Result: held for user` with no later release: the work is with the Reviewer or the
  user. Tell the user and stop.

## Orchestrator mapping

Real status names and transition mechanics have not been verified for any candidate orchestrator (Paperclip AI,
Multica, or Hermes kanban). Until this table is filled in, profiles use the abstract state names above. The
kanban notes come from `hermes kanban --help` and are not verified behavior.

| Abstract state | Paperclip AI | Multica | Hermes kanban |
|---|---|---|---|
| `in progress` | unverified | unverified | unverified |
| `review` | unverified | unverified | unverified (`request-review` is described as moving a task to `review`) |
| `done` | unverified | unverified | unverified (`complete`) |
| return label / marker | unverified | unverified | unverified (`request-changes` is described as returning the run to its implementer) |
| `blocked` (parked) | unverified | unverified | unverified (`block`, `unblock`) |
| task dependency (kickoff chain) | unverified | unverified | unverified (`link`) |

Also unverified for all three: whether assigning a task (rather than changing its status) is what wakes an
agent, and whether the orchestrator has its own convention for a workflow file that this one should
follow.
