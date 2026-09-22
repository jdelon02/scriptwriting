---
type: "validation"
title: "Reviewer profile: validation walkthroughs"
description: "Validation source for scriptwriting: docs/validation/historical/reviewer-walkthroughs.md."
tags: ["scriptwriting", "docs"]
source_path: "docs/validation/historical/reviewer-walkthroughs.md"
---

> SUPERSEDED: historical walkthrough, not active lifecycle guidance.
> Use ../reviewer-walkthroughs.md for current validation.

# Reviewer profile: validation walkthroughs

Eleven manual walkthroughs from the spec (`docs/knowledge/specs/2026-09-20-reviewer-profile-design.md`,
section 12). Each one runs the Reviewer on a fixture output file whose defects are planted and known, so the
expected items and score can be checked exactly. Anything under "Fail" is a defect in the profile files.

## How to run these

Work in a scratch copy so real series files are not touched:

```bash
SCRATCH=$(mktemp -d)
cp -R /Users/jdelon02/Projects/scriptwriting/. "$SCRATCH/run"
cd "$SCRATCH/run" && rm -rf series && mkdir -p series/episodes/s01e04-why-scripts-fail
```

Create the fixtures below in the scratch copy. Install and start the Reviewer profile as described in
`docs/validation/running-with-hermes.md` and tell the agent the task has moved to `review` for the stage named in
each walkthrough. Unless a walkthrough says otherwise, reset between walkthroughs by deleting
`series/episodes/s01e04-why-scripts-fail/reviews/` and restoring the fixtures.

In the shorthand below, `EP` means `series/episodes/s01e04-why-scripts-fail`.

Record the outcome under each walkthrough as `Result: pass` or `Result: fail, <what happened>`.

### Fixture: SERIES.md

Create `series/SERIES.md`. The Artist box starts unticked. Tick it (`[x] Artist`) for Walkthrough 3, which
reviews the Architect stage.

```markdown
# The Quiet Craft
> Making things well, slowly

## Overarching Theme
How small habits beat big bursts in creative work

## Audience
Working freelancers who feel behind

## Season 1

### S01E04 — Why Scripts Fail Before You Write Them
- Folder: `episodes/s01e04-why-scripts-fail/`
- Audience: same as series
- Long-form: Why Scripts Fail Before You Write Them
  - [ ] Scripted  [ ] Filmed  [ ] Published
- Short-form (each supports the long-form episode):
  - (none planned yet)
- Pipeline: [ ] Artist  [ ] Architect  [ ] Writer  [ ] Wizard
```

### Fixture A: clean Artist output

Create `EP/01-artist.md`. Expected review: **no items, 100%, passed**.

```markdown
# S01E04 — Why Scripts Fail Before You Write Them · Artist

Phase: in review

## Inputs
- Title: not provided
- Story spine: not provided
- Audience: same as series

## Idea dump
1. [points] "A script fails at the premise, not at the sentences."
2. [examples] "I spent two weeks polishing an intro for a video nobody needed."
3. [anecdotes] "The agency pitch died in the first two minutes, and it was my fault for skipping the outline."
4. [mistakes] "People start writing with no idea what the ending is."
5. [surprises] "The videos I planned in twenty minutes did better than the ones I agonized over."
6. [numbers] "Three of my last five scripts got rewritten from scratch."
7. [misconceptions] "Everyone thinks the problem is writing skill. It's usually structure."
8. [hindsight] "I wish someone told me to decide the payoff before anything else."

## Grand Payoff
- Candidates nominated (by number): 3, 7, 8
- Chosen: "Everyone thinks the problem is writing skill. It's usually structure." (entry #7)
- Why it justifies the click: "Because it tells people the thing they keep blaming isn't the real problem."
- Title test: skipped, no title

## Review
- Status: in review
- Latest review: reviews/01-artist-review.md

## Open threads
- No title provided
- No story spine provided

## Architect handoff
Grand Payoff: "Everyone thinks the problem is writing skill. It's usually structure." (entry #7).
Title and spine not provided. Dump above.
```

### Fixture B: Artist output with planted defects

Copy Fixture A to `EP/01-artist.md` and make exactly these three edits:

1. Delete the line beginning `- Why it justifies the click:`.
2. Change entry 6 to `6. [numbers] Three of my last five scripts got rewritten from scratch.` (remove the quotation marks).
3. Change entry 8 to `8. [hindsight] "I wish someone told me about the fix earlier."`

Expected review: exactly these three items, **62%, returned**.

| # | Location | Category | Severity | Points |
|---|---|---|---|---|
| 1 | `01-artist.md`, `## Grand Payoff` | mechanical: A3 | blocking | -15 |
| 2 | `01-artist.md`, entry 8 | comprehension: undefined referent | blocking | -15 |
| 3 | `01-artist.md`, entry 6 | mechanical: A2 | significant | -8 |

`Arithmetic: 100 - 15 - 15 - 8 = 62`

(Entry 8 is blocking because "the fix" is central to that entry and nothing in the files says what it is.)

### Fixture C: clean Architect output

Tick `[x] Artist` in the SERIES.md fixture. Keep Fixture A as `EP/01-artist.md`. Create `EP/02-architect.md`.
Expected review: **no items, 100%, passed**.

```markdown
# S01E04 — Why Scripts Fail Before You Write Them · Architect

Phase: in review

## Inputs
- Title: "Why Scripts Fail Before You Write Them"
- Story spine: "I sit down to write." "I want it to land." "I have no structure." "I decide the payoff first." "The script comes together."
- Viewer questions: "Why does my script feel flat?", "Is it me or the process?", "What do I do first?"
- Target length: "9 minutes"
- Loop count: "three"
- Source: 01-artist.md (Grand Payoff: entry #7)

## Loops

### Loop 1
- Status: approved
- Payoff: Viewers see that a flat script is usually a structure problem, not a sentence problem. [from: #1, A1.1]
- Setup: You may be polishing sentences on a script that was doomed before line one. [from: #2, A1.2]
- Tension: People keep editing lines, which cannot fix a missing premise; the contrast is restructuring first. [from: #6, A1.3]
- Answers:
  - A1.1 "A flat script is usually a structure problem."
  - A1.2 "People polish sentences when the premise is the issue."
  - A1.3 "I rewrote three of my last five scripts from scratch."

### Loop 2
- Status: approved
- Payoff: Viewers learn to decide the payoff before writing anything. [from: #8, A2.1]
- Setup: The order you work in decides whether the script lands. [from: A2.2]
- Tension: People start writing with no ending in mind; the contrast is fixing the payoff first. [from: #4, A2.3]
- Answers:
  - A2.1 "Decide the payoff before you write a word."
  - A2.2 "The order you work in decides whether it lands."
  - A2.3 "People start writing without knowing the ending."

### Loop 3
- Status: approved
- Payoff: The problem people blame, writing skill, is usually structure. [from: #7, A3.1]
- Setup: You may be blaming the wrong thing. [from: A3.2]
- Tension: Planned-fast videos beat agonized ones; the contrast shows effort is not the lever. [from: #5, A3.3]
- Answers:
  - A3.1 "It's usually structure, not writing skill."
  - A3.2 "People blame their writing when it's not the problem."
  - A3.3 "The videos I planned in twenty minutes did better."

## Sequence
- Order (first to last): 1, 2, 3
- User's ranking notes: "Loop 3 is the strongest, Loop 1 is second."
- Mid-video re-hook: after Loop 2; what is counterintuitive to come: "It isn't your writing skill."
- Transitions:
  - Loop 1 to Loop 2: A flat script is a structure problem, but the first structural choice is the payoff. [from: A1.1, A2.2] Status: approved
  - Loop 2 to Loop 3: Deciding the payoff first works, but people blame writing skill anyway. [from: A2.1, A3.2] Status: approved

## Framing

### Introduction
- Promise: By the end of this video, you'll know why your script feels flat and what to decide first. [from: A1.1, A2.1]
- Roadmap (3-5 on-screen topics): structure versus sentences; deciding the payoff first; why it is not writing skill [from: A1.1, A2.1, A3.1]

### Summary
- Takeaways (3-5, derived from the payoffs): a flat script is a structure problem; decide the payoff first; writing skill is usually not the problem [from: A1.1, A2.1, A3.1]

### Call to action
- Link (to content covered): the point that structure, not skill, is usually the problem [from: A3.1]
- Curiosity gap (new question): "What does a good structure look like for a real script?"
- Promise (what the next video delivers): "You'll see a full structure built from scratch."

## Viewer-question coverage
- "Why does my script feel flat?": answered in Loop 1
- "Is it me or the process?": answered in Loop 3
- "What do I do first?": answered in Loop 2

## Unused material
- #3 "The agency pitch died in the first two minutes, and it was my fault for skipping the outline."

## Review
- Status: in review
- Latest review: reviews/02-architect-review.md

## Open threads
- (none)

## Writer handoff
Approved loops, sequence, and framing above. Title, spine, and Grand Payoff (entry #7) recorded in Inputs. The hook has not been written.
```

### Fixture D: review log with two prior returns

Create `EP/reviews/01-artist-review.md`. It is the prior history for the escalation walkthrough.

```markdown
# Artist review log

## Review 1 — 2026-09-21 — 62%
Result: returned
Consecutive sub-70 reviews: 1

Deductions:
| # | Location | Category | Severity | Points | Item |
|---|---|---|---|---|---|
| 1 | 01-artist.md, ## Grand Payoff | mechanical: A3 | blocking | -15 | Grand Payoff has a chosen payoff but no rationale. |
| 2 | 01-artist.md, entry 8 | comprehension: undefined referent | blocking | -15 | Entry 8 refers to "the fix" and nothing in the files says what it is. |
| 3 | 01-artist.md, entry 6 | mechanical: A2 | significant | -8 | Entry 6 has no quotation marks around the user's words. |

Arithmetic: 100 - 15 - 15 - 8 = 62

## Review 2 — 2026-09-22 — 62%
Result: returned
Consecutive sub-70 reviews: 2

Deductions:
| # | Location | Category | Severity | Points | Item |
|---|---|---|---|---|---|
| 1 | 01-artist.md, ## Grand Payoff | mechanical: A3 | blocking | -15 | Grand Payoff has a chosen payoff but no rationale. |
| 2 | 01-artist.md, entry 8 | comprehension: undefined referent | blocking | -15 | Entry 8 refers to "the fix" and nothing in the files says what it is. |
| 3 | 01-artist.md, entry 6 | mechanical: A2 | significant | -8 | Entry 6 has no quotation marks around the user's words. |

Arithmetic: 100 - 15 - 15 - 8 = 62

Prior items:
- Review 1, item 1: still open
- Review 1, item 2: still open
- Review 1, item 3: still open
```

### Helper: verify the arithmetic

Run against any review log. Each printed pair must be equal: the header score, then 100 minus the sum of
the Points column.

```bash
python3 - EP/reviews/01-artist-review.md <<'EOF'
import re, sys
s = open(sys.argv[1]).read()
for blk in re.split(r'(?m)^## Review ', s)[1:]:
    score = int(re.match(r'\d+ — \S+ — (\d+)%', blk).group(1))
    pts = sum(int(m) for m in re.findall(r'\|\s*-(\d+)\s*\|', blk))
    print(score, max(0, 100 - pts), "OK" if score == max(0, 100 - pts) else "MISMATCH")
EOF
```

### Helper: check items for forbidden words

Prints any advice word found in the Item column outside quoted text. No output means clean.

```bash
python3 - EP/reviews/01-artist-review.md <<'EOF'
import re, sys
bad = re.compile(r'\b(should|consider|could|try|suggest|better|weak|good|great|strong|improve|add|change|rewrite|replace|fix)\b', re.I)
for line in open(sys.argv[1]):
    if line.startswith('|') and not line.startswith('|---') and not line.startswith('| #'):
        item = line.rstrip().rstrip('|').split('|')[-1]
        item = re.sub(r'"[^"]*"', '', item)
        for m in bad.findall(item):
            print("FORBIDDEN WORD:", m, "in:", item.strip())
EOF
```

---

## Walkthrough 1: Clean pass

**Setup:** Fixtures SERIES.md (Artist box unticked) and A. Stage: 1 (Artist).

**Pass:**
- The review finds no items: `Result: passed`, `Arithmetic: 100`, score 100%.
- The Artist box in SERIES.md is ticked (`[x] Artist`), and nothing else in SERIES.md changed
  (`diff` against the fixture shows only that one character change).
- The agent moves the task to `done`, or states the exact transition it would make if no orchestrator is
  connected.
- `EP/01-artist.md` is unchanged.

**Fail:** any deduction on a clean file; a ticked box other than Artist; any edit to an output file.

---

## Walkthrough 2: Planted defects

**Setup:** Fixtures SERIES.md and B. Stage: 1.

**Pass:**
- The log entry contains exactly the three items in the Fixture B table, with those categories,
  severities, and points, and `Arithmetic: 100 - 15 - 15 - 8 = 62`.
- `Result: returned`, `Consecutive sub-70 reviews: 1`.
- The arithmetic helper prints `62 62 OK`.
- Nothing else above a minor item appears.

**Fail:** a missing planted item; a different score; an item outside the rubrics; a mismatched arithmetic.

---

## Walkthrough 3: Mechanical, Architect

**Setup:** Fixtures SERIES.md (Artist ticked), A, and C. Then make exactly these three edits to
`EP/02-architect.md`:

1. In Loop 2, change the Setup marker `[from: A2.2]` to `[from: #99, A2.2]`.
2. Delete the `#3` line under `## Unused material` (leave `(none)` or an empty list).
3. Delete the `- User's ranking notes:` line under `## Sequence`.

Stage: 2 (Architect).

**Expected review: exactly three items, 74%, passed:**

| # | Location | Category | Severity | Points |
|---|---|---|---|---|
| 1 | `02-architect.md`, Loop 2, Setup | mechanical: X2 | blocking | -15 |
| 2 | `01-artist.md`, entry 3 | mechanical: X3 | significant | -8 |
| 3 | `02-architect.md`, `## Sequence` | mechanical: X5 | minor | -3 |

`Arithmetic: 100 - 15 - 8 - 3 = 74`

**Pass:**
- Exactly those three items appear, with the right severities.
- `Result: passed`. The Architect box is ticked. The minor item is repeated under
  `Notes (non-blocking)`.
- The arithmetic helper prints `74 74 OK`.

**Fail:** the broken `#99` marker is missed; entry 3 is not flagged; the score differs; the Architect box
is not ticked on a pass.

---

## Walkthrough 4: No authorship

**Setup:** run Walkthrough 2 (Fixture B) and keep its log.

**Pass:**
- The forbidden-words helper prints nothing.
- No item contains suggested wording, an answer, or an addition (read each item).
- No item says an idea is good or weak.

**Fail:** any advice or suggested content, for example "Entry 8 should say what the fix was."

---

## Walkthrough 5: No quality judgment

**Setup:** Fixtures SERIES.md and A, with one edit: change entry 2 to
`2. [examples] "People should just try harder."` Stage: 1.

**Pass:**
- The review finds no items and gives 100%, `Result: passed`. A weak idea that is clear costs nothing.
- The log contains no comment about the quality of entry 2.

**Fail:** any deduction or remark about entry 2's quality or specificity.

---

## Walkthrough 6: Dedupe

**Setup:** Fixtures SERIES.md and A, with these edits so that one undefined term appears in four places:

- Entry 3: insert `, and the reset took a week` before the final period of the quoted text.
- Entry 5: change to `5. [surprises] "Applying the reset in twenty minutes did better than agonizing."`
- Entry 6: change to `6. [numbers] "The reset got rewritten from scratch three times."`
- Entry 8: change to `8. [hindsight] "I wish someone told me about the reset earlier."`

Stage: 1.

**Pass:**
- There is exactly one item for "the reset", an undefined referent, at entry 3 (the first location), with
  `also at` listing entries 5, 6, and 8.
- Its severity is the highest among its occurrences (blocking if the term is central to any of them,
  otherwise significant).
- The arithmetic helper prints an OK line.

**Fail:** four separate deductions for the same term; the "also at" locations are missing.

---

## Walkthrough 7: Return procedure

**Setup:** run Walkthrough 2 (Fixture B), which scores 62% on a first review.

**Pass:**
- The log entry has `Result: returned`.
- The agent sets the task back to `in progress`, reassigns it to the Artist profile, and marks it as a
  return with a pointer to the new log entry, or states the exact three actions it would take if no
  orchestrator is connected.
- No Pipeline box is ticked. No output file is edited.

**Fail:** the task stays in `review`; the task is sent to an earlier queue state; the reassignment or the
pointer is missing; a box is ticked.

---

## Walkthrough 8: Re-review

**Setup:** run Walkthrough 2 so the log has Review 1 (62%). Then edit `EP/01-artist.md` to fix all three
defects (restore the rationale line, put the quotation marks back on entry 6, restore entry 8 to the
Fixture A wording) and make one **new** defect: delete the `- Title test:` line. Run the review again.

**Pass:**
- Review 2 is a full fresh read. Its `Prior items:` marks Review 1's three items `resolved`.
- The one new item is `mechanical: A4`, significant, -8. The score is **92%**, `Result: passed`.
- The score reflects the current files only: it is not lowered by the earlier defects.
- Consecutive sub-70 reviews is 0.

**Fail:** prior deductions carried over; a resolved item marked `still open`; the new defect missed.

---

## Walkthrough 9: Escalation

**Setup:** Fixtures SERIES.md, B (as `EP/01-artist.md`), and D (as `EP/reviews/01-artist-review.md`). Stage: 1.

**Pass:**
- The new entry is Review 3, score 62%, `Consecutive sub-70 reviews: 3`, `Result: held for user`.
- The task stays in `review`: it is neither returned nor passed. No Pipeline box is ticked.
- The agent flags the user through the orchestrator (or states how it would), naming the stage, the
  episode, the three scores, and the log path.
- The agent does not offer or apply any override.

**Fail:** the task is returned or passed; no user flag; an override is invented.

---

## Walkthrough 10: Missing rubric

**Setup:** Fixtures SERIES.md and A, plus a file `EP/03-writer.md` containing a few lines of text. Tell the
agent the task for stage 3 (Writer) has moved to `review`.

**Pass:**
- The agent appends `No rubric for stage 3` to `EP/reviews/03-writer-review.md`.
- The task stays in `review`: neither passed nor returned. The user is flagged.
- No score is produced and no box is ticked.

**Fail:** the agent invents a rubric, scores the file, or returns or passes the task.

---

## Walkthrough 11: Repeatability

**Setup:** Fixtures SERIES.md and B. Run the review twice in two fresh sessions, deleting `EP/reviews/`
between runs.

**Pass:**
- Both runs give the same item list, or the two lists differ by at most one minor item.
- Both runs give the same severities for the same items, and both arithmetic helpers print OK.

**Fail:** different severities for the same problem; scores that differ by more than one minor item's
points.
