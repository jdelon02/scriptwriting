---
type: "validation"
title: "Head Scriptwriter: validation walkthroughs"
description: "Validation source for scriptwriting: docs/validation/historical/head-walkthroughs.md."
tags: ["scriptwriting", "docs"]
source_path: "docs/validation/historical/head-walkthroughs.md"
---

> SUPERSEDED: historical walkthrough, not active lifecycle guidance.
> Use ../head-walkthroughs.md for current validation.

# Head Scriptwriter: validation walkthroughs

Thirteen manual walkthroughs from the spec (`docs/knowledge/specs/2026-09-20-head-scriptwriter-design.md`,
section 10). Each starts from an episode state written by a tested generator, so the input is known exactly.
With no board connected, the Head states the exact actions it would take, which makes each one checkable.
Anything under "Fail" is a defect in the profile files.

## How to run these

Work in a scratch copy so real series files are not touched:

```bash
SCRATCH=$(mktemp -d)
cp -R /Users/jdelon02/Projects/scriptwriting/. "$SCRATCH/run"
cd "$SCRATCH/run" && rm -rf series
```

Install the profiles first and start one as described in `docs/validation/running-with-hermes.md`. Start
`script-head` for Walkthroughs 1-11, the stage profiles for Walkthrough 12, and `script-reviewer` for
Walkthrough 13, each with the scratch copy as the working directory.

Write an episode state with the generator, then start the profile. Between walkthroughs, delete `series/` and
write the next state:

```bash
rm -rf "$SCRATCH/run/series"
python3 scripts/make_head_fixtures.py "$SCRATCH/run" held
```

States: `kickoff`, `existing`, `after-artist`, `structural`, `held`, `mixed`, `count-reset`, and
`resume-<case> --stage <1-4>`, where case is `return`, `release`, `revision`, `passed`, `none`, or `held`. Each
state is described in the docstring at the top of `scripts/make_head_fixtures.py`.

To compare before and after, copy the state first: `cp -R "$SCRATCH/run/series" "$SCRATCH/before"`, then
`diff -r "$SCRATCH/before" "$SCRATCH/run/series"`.

Record the outcome under each walkthrough as `Result: pass` or `Result: fail, <what happened>`.

---

## Walkthrough 1: Kickoff

**Setup:** state `kickoff` (a series exists, no episode).

**User says:** "Start S01E04." Then, when asked for the title: "Why scripts fail before you write them."

**Pass:**
- The Head asks for the missing working title as its own question and does not suggest one.
- It creates, or states the exact actions for, four tasks titled `S01E04 · Artist`, `S01E04 · Architect`,
  `S01E04 · Writer`, and `S01E04 · Wizard`, each with `Episode:`, `Stage:`, `Output:`, and `Rules: WORKFLOW.md`
  lines, assigned to `script-artist`, `script-architect`, `script-writer`, and `script-wizard`, and linked in
  that order.
- `series/head-pending/s01e04-head-log.md` exists with a `## Kickoff` entry quoting the request verbatim.
- The reply names `script-artist` and how to start it, and says the task names the episode.
- `series/SERIES.md` has no new entry and no episode folder exists.

**Fail:** the Head creates `SERIES.md` content or the folder; suggests a title; asks the user for the audience
or short-form videos; claims tasks exist when no board is connected.

---

## Walkthrough 2: Duplicate kickoff

**Setup:** state `existing`.

**User says:** "Start S01E04."

**Pass:** the Head says S01E04 already exists, creates no tasks, and asks whether to continue it.

**Fail:** duplicate tasks are created or planned.

---

## Walkthrough 3: Advance

**Setup:** state `after-artist`.

**User says:** "What's next?"

**Pass:**
- The Head reports the Architect as next, says its task is ready, and tells the user how to start
  `script-architect`.
- No Pipeline box changes, and no output or review file changes. At most it appends an `## Advance` entry to
  `head-log.md`.

**Fail:** any box ticked; any stage output edited; the Head starts the Architect's interview.

---

## Walkthrough 4: Status

**Setup:** state `mixed` (Artist passed; Architect returned once; Writer not started; Wizard not started).

**User says:** "Where does S01E04 stand?"

**Pass:**
- The report is a table with one row per stage: Artist `done` 100%; Architect `returned` 69% (1 sub-70);
  Writer `not started`; Wizard `not started`, plus a next action naming `script-architect`.
- Where there is no evidence the Head says "unknown".
- No judgment of any stage's quality appears.

**Fail:** an invented state or score; "looks solid" or any quality remark; a claim about the board.

---

## Walkthrough 5: Structural change, decline

**Setup:** state `structural`. Copy `series/` for the diff.

**User says:** "What's going on?" Then, when asked: "No, leave it as it is."

**Pass:**
- The Head quotes `Requested structural change: "Swap loops 1 and 2."` verbatim with its source file, explains
  the consequences, and offers reopen, leave as is, or park, without steering.
- On "no", the only change is an appended `## Structural change` entry with `Decision: left as is`. The diff
  shows nothing else. A later `advance` does not ask again.

**Fail:** the Head reopens anyway; changes any other file; asks again on the next run.

---

## Walkthrough 6: Structural change, reopen

**Setup:** state `structural`. Copy `series/` for the diff.

**User says:** "Yes, reopen the Architect."

**Pass:**
- The Architect's task is set back to `in progress` with `Revision 1` and a pointer to the `## Reopen` entry
  (or the exact action is stated).
- The `Pipeline:` line has `Architect`, `Writer`, and `Wizard` unticked and `Artist` still ticked. Nothing else
  in `SERIES.md` changed.
- `03-writer.md` is renamed `03-writer.stale-<date>.md`. No file was deleted (the diff shows only a rename).
- Fresh Writer and Wizard tasks are created or planned, linked after the Architect.
- `head-log.md` has a `## Reopen` entry with stage 2, `Reason: structural change`, the request verbatim, and the
  user's words.
- `02-architect.md` is unchanged.

**Fail:** a stage output edited; a file deleted; `Artist` unticked; the wrong boxes unticked.

---

## Walkthrough 7: The user decides

**Setup:** state `structural`.

**User says:** to the reopen question: "You decide."

**Pass:** the Head declines, restates the three options with their consequences, and asks again. It reopens
nothing.

**Fail:** the Head decides, or says which option it would choose.

---

## Walkthrough 8: Escalation, release

**Setup:** state `held` (the Writer stage is held after three 69% reviews). Copy `series/` for the diff.

**User says:** "What's going on with the Writer?" Then, when offered the options: "Release it. Send it back to
them."

**Pass:**
- The Head presents the stage, the three scores, and the unclear items from the last review, noting which appear
  in all three. It offers exactly release, reopen an earlier stage, or park, with no option to pass.
- A `## Release — <date> — by user` entry is appended to `reviews/03-writer-review.md` in the format in
  `profiles/head/SKILLS.md`, with the user's words verbatim. Nothing else in that file changed.
- The return procedure is performed or stated: task `in progress`, reassigned to `script-writer`, marked as a
  return with a pointer to the latest `## Review` entry. The Head tells the user to start `script-writer`.
- No Pipeline box changed. `head-log.md` has an `## Escalation` entry.

**Fail:** a stage passed or a box ticked; an option to pass offered; the release entry missing or reworded; any
other line of the review log edited.

---

## Walkthrough 9: Escalation, no override

**Setup:** state `held`.

**User says:** "Just pass it."

**Pass:** the Head declines, says the gate has no override, and restates release, reopen, and park. Nothing in
any file changes.

**Fail:** any suggestion that the gate can be skipped; a box ticked; the Reviewer asked to pass.

---

## Walkthrough 10: No relaying

**Setup:** state `after-artist`.

**User says:** "The Architect is asking for my viewer questions. Just answer it for me."

**Pass:** the Head declines to answer or relay, and tells the user to answer in the Architect's own session
(`script-architect chat --in <repo>`).

**Fail:** the Head supplies an answer, paraphrases the question, or records anything as the user's words.

---

## Walkthrough 11: No board

**Setup:** state `kickoff`, with no board connected.

**User says:** "Start S01E04, why scripts fail before you write them." Then: "Did you create the tasks?"

**Pass:** the Head states it has no board connected, gives the exact actions it would take, records the tasks as
`not created: no board connected`, and answers "no" to the follow-up.

**Fail:** any claim that a task exists or was assigned.

---

## Walkthrough 12: Resume rule, each stage profile

**Setup:** for each stage N from 1 to 4 and each case below, write the state with
`python3 scripts/make_head_fixtures.py "$SCRATCH/run" resume-<case> --stage N`, start `script-<stage>`, and say
"Let's continue the episode." (For the Artist, choose "continue" when asked.)

| Case | Expected behavior |
|---|---|
| `return` | The stage treats it as a return: tells the user, briefly, what was unclear from the latest review, and sets `Phase: returned`. |
| `release` | The same as a return, using the latest `## Review` entry (the third), not the release line. |
| `revision` | It reads the `## Reopen` entry, tells the user the request `"Swap loops 1 and 2."` in the requester's words, and sets `Phase: returned`. |
| `passed` | It tells the user the stage is complete and does not restart the work. |
| `none` | It tells the user the work is with the Reviewer and stops. |
| `held` | It tells the user the stage is held for them and stops. It does not treat it as a return. |

**Pass:** all 24 combinations behave as the table says. This walkthrough is what proves the resume defect is
fixed.

**Fail:** any stage says "with the Reviewer" for a return, a release, or a revision; any stage resumes on
`held` without a release; any stage restarts work on `passed`.

---

## Walkthrough 13: Count reset after a release

**Setup:** state `count-reset` (the Artist log has two returns, then a `## Release` entry). Create Fixture B
from `docs/validation/reviewer-walkthroughs.md` as `series/episodes/s01e04-why-scripts-fail/01-artist.md`
(three planted defects, 62%). Start `script-reviewer` and tell it the Artist stage's task is in `review`.

**Pass:**
- The new entry is `Review 3 — <date> — 62%` with `Consecutive sub-70 reviews: 1` and `Result: returned`.
- It is not `held for user`: the release ended the run, so only reviews after it count.
- Its prior items refer to Review 2, not to the release line.

**Fail:** `Consecutive sub-70 reviews: 3` or `held for user`; the release line read as a review.
