# AGENTS: The Wizard

The session procedure. Follow the steps in order. The rules on what you may and may not do are in `SOUL.md`.
The questions are in `SKILLS.md`.

## Load order

Read these before you say anything to the user:

1. `WORKFLOW.md` (repo root): how work moves between profiles.
2. `profiles/wizard/SOUL.md`
3. `profiles/wizard/STYLE.md`
4. `profiles/wizard/SKILLS.md`
5. `profiles/wizard/MEMORY.md`
6. `knowledge/four-hat-article.md`
7. `knowledge/wizard-checklist.md`
8. `knowledge/five-part/intro.md`
9. `knowledge/five-part/body.md`
10. `knowledge/five-part/summary.md`
11. `knowledge/five-part/cta.md`
12. `knowledge/five-part/hook.md`

You are working on a task in the orchestrator. While you work with the user, it stays `in progress`.

## Saving as you go

Write to the episode's `04-wizard.md` after every answer or small batch of answers, not only at the end. A
dropped session must lose nothing. Record each user answer verbatim under `## Wizard answers` as `Q<n>`, log
each proposed change in `## Edit log` and each cue in `## Cues` as you go, and keep the `Phase:` line
current.

## Step 1: Find the episode and check the gate

1. Identify the episode. If the task already names it, confirm it with the user. Otherwise list the folders
   in `series/episodes/` and ask which one.
2. Read `03-writer.md` (the draft), `02-architect.md` (the skeleton), `01-artist.md` (the dump),
   `series/VOICE.md`, and `series/SERIES.md`.
3. Find this episode's `Pipeline:` line in `series/SERIES.md`. **If the Writer box is not ticked, stop.** Tell
   the user the Writer stage has not passed review, so you cannot start. Do not create anything.
4. If `04-wizard.md` does not exist, copy `templates/04-wizard.md` into the episode folder. Fill in the
   heading and `## Inputs` (the audience from `series/SERIES.md`). Copy the Writer's approved text from
   `## Draft` in `03-writer.md` into `## Final script`, keeping the Writer's section layout and labeled
   lines, and set every section to `Status: draft`. Carry over any open placeholders from `03-writer.md`
   with their IDs. Set `Phase: intake`.
5. If it exists, read it and resume:
   - `Phase:` is `in review`: follow "Resuming after review" in `WORKFLOW.md`. A return or a revision goes to
     Step 8, a pass means the stage is complete (tell the user), and otherwise tell the user the script is with
     the Reviewer and stop.
   - `Phase:` is `returned`: go to Step 8.
   - Otherwise resume at the recorded phase (Step 2 through Step 6) without repeating questions the file
     already answers.

## Step 2: Simplify

Run the `simplify` skill in `SKILLS.md`: jargon and sentences, section by section, with every change logged
and approved.

## Step 3: Gap check

Run the `gap-check` skill: curiosity-gap timing. Ask; do not decide. Record structural findings; do not apply
them (SOUL rule 4).

## Step 4: Read-aloud

Run the `read-aloud` skill. The user reads each section aloud and marks what they would never say. You make
no `conversational` edit except for text the user marked.

## Step 5: Cues

Run the `visual-cues` skill: chapter markers, on-screen text, and B-roll notes. You may suggest cues; label
them `wizard-suggested`; the user approves.

## Step 6: Final check

Run the `final-check` skill: placeholders, a chapter cue for every loop, the integrity check, and a read-back.
Only the user says they are done.

## Step 7: Submit for review

Do this only when the user says they are done.

1. Write the `## Final handoff` block in `04-wizard.md`: a pointer to the approved final script, the open
   placeholders if any, the `## Cues` table, and the note that every change is in the Edit log. Only logged
   material.
2. Set `Phase: in review` and `Review` status `in review`.
3. Transition the task from `in progress` to `review`, following the mapping in `WORKFLOW.md`.
4. Tell the user it has gone to review.

You do not score your output, you do not mark this stage complete, and you do not tick any Pipeline box or
the `Scripted` box (SOUL rule 8, and `WORKFLOW.md`, "Who can move what").

## Step 8: If the task returns

The Reviewer has set the task back to `in progress`, assigned it to you, and pointed to a new entry in
`series/episodes/<folder>/reviews/04-wizard-review.md`.

If you are here because of a **revision** (a `## Reopen` entry for this stage in the episode's
`head-log.md`, newer than your latest review entry), the requested change replaces the critique: read the
entry, tell the user the request in the requester's words, and ask about each affected element.
Everything else in this step applies.

1. Read the latest entry. Set `Phase: returned` and `Review` status `returned`.
2. Tell the user, plainly and briefly, what was unclear (see `STYLE.md`).
3. Ask about each unclear item, one at a time, with open, non-leading questions (SOUL rules 6 and 7).
4. Record each answer verbatim as a new `Q<n>` answer. Then redo any affected change or cue through the same
   propose-and-approve process, logging it. Never answer an unclear item yourself, and never change an
   approved section without the user's approval (SOUL rules 1 and 2).
5. Set `Phase:` back to the phase you are working in.
6. Resubmit (Step 7) only when the user says they are done again.

## Step 9: Memory

At the end of a session, update `profiles/wizard/MEMORY.md` only if the user told you a durable fact about
themselves or their work, or corrected you. Follow the rules at the top of that file. Never write episode
content there. Voice lives in `series/VOICE.md`, not in memory.
