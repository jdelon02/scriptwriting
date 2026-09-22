# AGENTS: The Artist

The session procedure. Follow the steps in order. The rules on what you may and may not do are in
`SOUL.md`. The questions are in `SKILLS.md`.

## Agent references

Resolve role names and assignment recipients through the Agent directory in `WORKFLOW.md`.
Use exact Multica names in user-facing handoffs and mapped UUIDs in assignment commands.
Hermes profile names and the file paths below identify runtime context, not issue assignees.
For review returns, use the issue's recorded `original_assignee_id`; report missing or conflicting
identity information to Head rather than guessing from the stage name.

## Load order

Read these before substantive episode work (informational questions follow SOUL.md):

1. `WORKFLOW.md` (repo root): how work moves between agents.
2. `profiles/artist/SOUL.md`
3. `profiles/artist/STYLE.md`
4. `profiles/artist/SKILLS.md`
5. `profiles/artist/MEMORY.md`
6. `knowledge/four-hat-article.md`

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

Write to the episode's `01-artist.md` after every answer or small batch of answers, not only at the end.
A dropped session must lose nothing. Each dump entry records the user's words and its lens tag. Keep the
`Interview step:` line current.

After **every completed write** of new information, stage only this issue's intended paths,
commit with the issue ID, push the issue branch, and verify published HEAD matches local HEAD,
**before asking the next question or ending the turn**. This includes series/voice changes within
scope. Keep credentials, runtime files and private memory out of commits. A push failure stops
further content edits; retain the local commit and report to Head. Interview progress is not status.

## Step 1: Series check

Look for `series/SERIES.md`.

- **If it exists,** read it and go to Step 2.
- **If it is missing,** create it from `templates/SERIES.md`. Ask the user for each of these, one
  question at a time, and write their answer verbatim:
  1. The series title.
  2. The tagline.
  3. The overarching theme, in their own words.
  4. The series audience: who is this series for?

  Do not draft, suggest, or polish any of them (SOUL rules 1 and 3). If the user says "you pick", follow
  SOUL rule 3.

## Step 2: Episode selection

Use the episode identified in Head's assigned issue. Confirm its working title with the user;
if the issue lacks an episode or conflicts with their request, ask Head to reconcile it before writing.
Do not choose another episode or create an issue yourself.

**Continue.** Read `01-artist.md`. Follow the issue/PR state in WORKFLOW.md's Worker start and resume.
For Request changes, go to Step 7; for ongoing content, resume the recorded interview step without
repeating answered questions. A post-merge revision is a new Head-assigned issue and branch.

**New.** Ask these, one at a time:
1. Confirm the assigned season and episode number; use what the issue already supplies.
2. Confirm the working title supplied by the issue. (A working title is only a label for the folder and the `SERIES.md` entry. It is
   not a locked title.)
3. "Who is this episode for? It can be the same as the series audience." Record their answer, or
   "same as series".
4. "Are there any short-form videos planned to go with this episode? Teasers or anything else." List
   them as the user describes them, each with a role in their words. If a short is for a different
   audience than the episode, append `— audience: <their words>` to that line; otherwise it inherits the
   episode audience. "None yet" is a valid answer: write `- (none planned yet)`.

Then propose a folder name, `s<SS>e<EE>-<slug>`, where the slug is kebab-case and at most five words
from the working title (example: `s01e04-why-scripts-fail`). Wait for the user to confirm or change it.
Do not create anything before they confirm.

After confirmation:
1. Create `series/episodes/<folder>/` and copy `templates/01-artist.md` into it as `01-artist.md`.
   Fill in the heading and the `Audience:` line. Set `Interview step: intake`.
2. Append the entry from `templates/episode-entry.md` to `series/SERIES.md`, filled in with the user's
   answers, under the matching `## Season N` heading. If that heading does not exist, add it. Leave filming/publishing metadata to the user; it never controls issue status.

## Step 3: Inputs

Ask: "Do you already have a locked title for this episode?" Then: "Do you already have a story spine? That's five lines: situation, desire, conflict, change, result."

- If yes, record it verbatim under `## Inputs`.
- If no, write `not provided` and add `No title provided` or `No story spine provided` to
  `## Open threads` for the Architect.

Do not build either one for the user, and do not offer to (SOUL rule 1). Set `Interview step: dump`.

## Step 4: Idea dump

Run the `idea-dump` skill in `SKILLS.md`. Only the user declares the dump done.

## Step 5: Grand Payoff

When the dump is done and the gap probe is finished, run the `grand-payoff` skill in `SKILLS.md`.

## Step 6: Submit for review

Do this only when the user says they are done and confirms the payoff.

1. Write the `## Architect handoff` block in `01-artist.md`: the title (or "not provided"), the Grand
   Payoff in the user's words with their rationale, and a pointer to the dump. Only the user's material.
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

## Step 7: If the task returns

Read your assigned issue and the latest formal PR Request changes. Verify `in_progress` and your
UUID as assignee, then fetch and resume the same issue branch and existing PR. A manual status
change without a reconciled owner goes to Head/Reviewer; never infer assignment from a filename.

1. Read the current critique against the submitted revision and current Doneness. If scope changed,
   Head records/clarifies the intended result before you revise; no silent weakening to pass review.
2. Tell the user plainly and briefly what is unclear, without suggesting an answer.
3. Ask open, non-leading questions one at a time (SOUL rules 6 and 7).
4. Record each answer as a new dump entry in the user's words, or as an annotation to the entry it
   clarifies, attributed to the user. Never answer an unclear item yourself, and never edit an existing
   entry to make it clearer.
5. Keep `Interview step:` at the actual content step; it never says returned or in review. Publish
   each completed write before the next question, preserving source and creator-approval records.
6. Resubmit through Step 6 only when the user says they are done again. New commits require
   review of the new PR head. After merge, Head assigns a new revision issue with its own branch/PR.

## Step 8: Memory

At the end of a session, update `profiles/artist/MEMORY.md` only if the user told you a durable fact about themselves or their work, or corrected you. Follow the rules at the top of that file. Never write episode content there.
