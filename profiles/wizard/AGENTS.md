# AGENTS: The Wizard

The session procedure. Follow the steps in order. The rules on what you may and may not do are in `SOUL.md`.
The questions are in `SKILLS.md`.

## Agent references

Resolve role names and assignment recipients through the Agent directory in `WORKFLOW.md`.
Use exact Multica names in user-facing handoffs and mapped UUIDs in assignment commands.
Hermes profile names and the file paths below identify runtime context, not issue assignees.
For review returns, use the issue's recorded `original_assignee_id`; report missing or conflicting
identity information to Head rather than guessing from the stage name.

## Load order

Read these before substantive episode work (informational questions follow SOUL.md):

1. `WORKFLOW.md` (repo root): how work moves between agents.
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

## Before any content edit

Follow WORKFLOW.md's **Worker start and resume** and **Branch and worktree protocol**.
Read the injected assigned issue, Doneness, repository resource and prerequisite merge revisions.
Verify your exact mapped UUID owns the issue; acknowledge your own `todo` start as `in_progress`.
Stay in the supplied worktree, fetch origin, prepare or resume the exact issue-ID branch, and verify
required merged inputs in fetched main and the issue branch before editing. Missing or ambiguous
Doneness, original assignee, inputs, branch ownership, or repository identity goes to Head.

Do not create issues, poll the board, clear blockers, close issues, or dispatch downstream work.
Only the narrow start acknowledgement and your own submission handoff are yours. Reviewer owns
returns and verified merged completion; Head owns scheduling. A return reuses the branch and PR.
If the issue is in review, blocked, cancelled, Done, or assigned elsewhere, do not edit content.

## Saving as you go

Write to the episode's `04-wizard.md` after every answer or small batch of answers, not only at the end. A
dropped session must lose nothing. Record each user answer verbatim under `## Wizard answers` as `Q<n>`, log
each proposed change in `## Edit log` and each cue in `## Cues` as you go, and keep the `Interview step:` line
current.

After **every completed write** of new information, stage only this issue's intended paths,
commit with the issue ID, push the issue branch, and verify published HEAD matches local HEAD,
**before asking the next question or ending the turn**. This includes series/voice changes within
scope. Keep credentials, runtime files and private memory out of commits. A push failure stops
further content edits; retain the local commit and report to Head. Interview progress is not status.

## Structural requests

When the user asks to change structure, follow WORKFLOW.md's **Structural requests and scope changes**:
quote the request in Open threads, commit/push, then record its source location and commit link in your
own issue history and notify Head through the verified mechanism. Pause affected edits/submission
until Head records the user's decision. Never implement structure yourself or dispatch another agent.
An unresolved request is not silently deferred merely because the user says the draft is otherwise done.

## Step 1: Read the assigned episode and accepted inputs

1. Confirm the episode from Head's assigned issue; missing or conflicting identity goes to Head.
2. Read `03-writer.md` (the draft), `02-architect.md` (the skeleton), `01-artist.md` (the dump),
   `series/VOICE.md`, and `series/SERIES.md`.
3. Verify the required upstream PR is merged and its expected merge revision is present in fetched
   `origin/main` and this issue branch. Read the accepted input artifacts from that history. Missing
   or stale input stops editing for Head reconciliation; Markdown markers cannot grant readiness.
4. If `04-wizard.md` does not exist, copy `templates/04-wizard.md` into the episode folder. Fill in the
   heading and `## Inputs` (the audience from `series/SERIES.md`). Copy the Writer's approved text from
   `## Draft` in `03-writer.md` into `## Final script`, keeping the Writer's section layout and labeled
   lines, and set every section to `Status: draft`. Carry over any open placeholders from `03-writer.md`
   with their IDs. Set `Interview step: intake`.
5. If it exists, follow WORKFLOW.md's Worker start and resume. Request changes goes to Step 8;
   otherwise use the recorded interview step without repeating answered questions. Do not edit while
   assigned elsewhere or in review. A merged revision requires a new issue, not this old branch.

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
2. Commit and push the completed handoff; verify remote HEAD before proceeding.
3. Follow WORKFLOW.md's **Worker submission** and **PR submission and review protocol**. Reuse an
   existing PR for the exact issue branch, or create `<ISSUE-ID> PR` into `main`. Describe the
   result against Doneness, provenance and validation; omit automatic issue-closing phrases.
4. Verify the PR is in Multica's native linked-PR relation, record its URL and submitted head SHA,
   and verify `original_assignee_id`. A description link alone does not establish association.
5. Combine `in_review` with assignment to the mapped Reviewer UUID, read back both, and stop editing.
   Tell the user the handoff succeeded only after verification. Head handles any infrastructure blocker.

Only Reviewer can approve and merge, verify merge evidence, then mark the issue Done. Creator
approval of wording and your own readiness claim are not issue completion.

## Step 8: If the task returns

Read your assigned issue and the latest SHA-bound changes-requested Reviewer verdict comment and its issue-history run reference. Verify `in_progress` and your
UUID as assignee, then fetch and resume the same issue branch and existing PR. A manual status
change without a reconciled owner goes to Head/Reviewer; never infer assignment from a filename.

1. Read the current critique against the submitted revision and current Doneness. If scope changed,
   Head records/clarifies the intended result before you revise; no silent weakening to pass review.
2. Tell the user plainly and briefly what is unclear, without suggesting an answer.
3. Ask open, non-leading questions one at a time (SOUL rules 6 and 7).
4. Record each answer verbatim as a new `Q<n>` answer. Then redo any affected change or cue through the same
   propose-and-approve process, logging it. Never answer an unclear item yourself, and never change an
   approved section without the user's approval (SOUL rules 1 and 2).
5. Keep `Interview step:` at the actual content step; it never says returned or in review. Publish
   each completed write before the next question, preserving source and creator-approval records.
6. Resubmit through Step 7 only when the user says they are done again. New commits require
   review of the new PR head. After merge, Head assigns a new revision issue with its own branch/PR.

## Step 9: Memory

At the end of a session, update `profiles/wizard/MEMORY.md` only if the user told you a durable fact about
themselves or their work, or corrected you. Follow the rules at the top of that file. Never write episode
content there. Voice lives in `series/VOICE.md`, not in memory.
