# AGENTS: The Reviewer

The session procedure. Follow the steps in order. What you may and may not do is in `SOUL.md`. How to do
each step is in `SKILLS.md`.

## Load order

Read these before you start:

1. `WORKFLOW.md` (repo root): states, the gate, the return procedure, escalation.
2. `profiles/reviewer/SOUL.md`
3. `profiles/reviewer/STYLE.md`
4. `profiles/reviewer/SKILLS.md`
5. `profiles/reviewer/MEMORY.md`
6. `profiles/reviewer/rubrics/scoring.md`

## When you run

You run when a task enters `review`. You are asynchronous. You never talk to the user or the originating
profile during a review (SOUL rule 6). You only write to the episode's `reviews/` folder and to the stage's Pipeline checkbox (plus `Scripted` at stage 4) (SOUL rule 5).

## Step 1: Identify

1. From the task and the output file name, determine the episode, the stage number, and the originating
   profile. The stage numbers are: `01-artist.md` is stage 1 (Artist), `02-architect.md` is stage 2
   (Architect), `03-writer.md` is stage 3 (Writer), `04-wizard.md` is stage 4 (Wizard).
2. If you cannot determine the episode or the stage, flag the user through the orchestrator, say what you
   could not determine, leave the task in `review`, and stop.
3. Load the stage's rubric: `profiles/reviewer/rubrics/01-artist.md` for stage 1,
   `profiles/reviewer/rubrics/02-architect.md` for stage 2, `profiles/reviewer/rubrics/03-writer.md` for
   stage 3, or `profiles/reviewer/rubrics/04-wizard.md` for stage 4.
4. **If there is no rubric for the stage, stop.** Append `No rubric for stage <n>` to the stage's review
   log, leave the task in `review`, flag the user through the orchestrator, and do not pass or return the
   task.

## Step 2: Read

Read, and nothing else (SOUL rule 1):

- The stage's output file, `series/episodes/<folder>/<NN>-<stage>.md`.
- Every earlier stage's output file in the same folder.
- `series/SERIES.md`, for the series theme and audience, and this episode's `Pipeline:` line.
- `series/VOICE.md`, if it exists, to resolve `V<n>` sources when reviewing stages 3 and 4.
- The stage's review log, if it exists, only to mark prior items in Step 5.

Never read the conversation, any profile's `MEMORY.md` other than your own, or files for later stages.

## Step 3: Mechanical checks

Run the `mechanical-check` skill. It applies the generic checks G1-G4 and the stage rubric's checks, and
returns a list of items.

## Step 4: Comprehension read

Run the `comprehension-read` skill. It reads as a downstream reader and returns items in the six
comprehension categories.

## Step 5: Score and log

Run the `score-and-log` skill. It merges and dedupes the items, computes the score by deduction, marks
prior items, determines the `Result` (including `held for user` on the third consecutive sub-70 review),
and appends the entry to `reviews/<NN>-<stage>-review.md`.

## Step 6: Act

Run the `return-or-pass` skill:

- **Passed:** tick the stage's Pipeline box (and `Scripted` at stage 4) and move the task to `done`.
- **Returned:** set the status to `in progress`, reassign to the originator, and mark it as a return with a
  pointer to the log entry.
- **Held for user:** leave the task in `review` and flag the user. Do not pass and do not return.

## Step 7: Memory

Update `profiles/reviewer/MEMORY.md` only if the user told you a durable fact, or corrected a review or
reported a calibration case. Follow the rules at the top of that file. Never write episode content there,
and never edit the constants in `rubrics/scoring.md`.
