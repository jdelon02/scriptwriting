---
type: "validation"
title: "Writer profile: validation walkthroughs"
description: "Validation source for scriptwriting: docs/validation/historical/writer-walkthroughs.md."
tags: ["scriptwriting", "docs"]
source_path: "docs/validation/historical/writer-walkthroughs.md"
---

> SUPERSEDED: historical walkthrough, not active lifecycle guidance.
> Use ../writer-walkthroughs.md for current validation.

# Writer profile: validation walkthroughs

Thirteen manual walkthroughs. Walkthroughs 1-11 come from the spec
(`docs/knowledge/specs/2026-09-20-writer-profile-design.md`, section 11) and run the Writer. Walkthroughs 12
and 13 run the Reviewer against the new stage-3 rubric, using fixtures with planted defects and known scores.
Anything under "Fail" is a defect in the profile files.

## How to run these

Work in a scratch copy so real series files are not touched:

```bash
SCRATCH=$(mktemp -d)
cp -R /Users/jdelon02/Projects/scriptwriting/. "$SCRATCH/run"
cd "$SCRATCH/run" && rm -rf series && mkdir -p series/episodes/s01e04-why-scripts-fail
```

Create the fixtures below in the scratch copy. For the Writer walkthroughs, install and start the Writer
profile as described in `docs/validation/running-with-hermes.md`. For Walkthroughs 12-13, start the Reviewer
profile the same way and tell it the task for stage 3 has moved to `review`. Unless a walkthrough
says otherwise, reset between walkthroughs by deleting `EP/03-writer.md`, `EP/reviews/`, and (for
Walkthrough 2 only) `series/VOICE.md`.

In the shorthand below, `EP` means `series/episodes/s01e04-why-scripts-fail`.

Record the outcome under each walkthrough as `Result: pass` or `Result: fail, <what happened>`.

### Fixture: SERIES.md

Create `series/SERIES.md`. Both the Artist and Architect boxes are ticked. For Walkthrough 1, change
`[x] Architect` to `[ ] Architect`.

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
- Pipeline: [x] Artist  [x] Architect  [ ] Writer  [ ] Wizard
```

### Fixture A: Artist output

Create `EP/01-artist.md`.

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

### Fixture C: Architect output

Create `EP/02-architect.md`.

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

### Fixture V: voice file

Create `series/VOICE.md`. Skip it for Walkthrough 2 (the Writer must create it).

```markdown
# Voice

## In my own words
- V1 (explaining the series idea to a friend): "Look, most of us just grind harder. The trick is a little every day."
- V2 (something that went wrong): "So I'd spent two weeks on an intro. Two weeks! And then the pitch died in two minutes."
- V3 (making a point land): "Here's the thing. It's never the sentences."

## How I describe my style
- "Casual and a bit self-deprecating. I talk like I'm telling a friend."

## Phrases I use
- "here's the thing"
- "look,"

## Phrases I avoid
- "utilize"
- "leverage"
```

### Fixture E: clean Writer output

Create `EP/03-writer.md` (needs Fixtures A, C, and V). Expected review: **no items, 100%, passed**.

```markdown
# S01E04 — Why Scripts Fail Before You Write Them · Writer

Phase: in review

## Inputs
- Skeleton: 02-architect.md
- Voice: series/VOICE.md
- Target length: "9 minutes"
- Loop order: 1, 2, 3

## Draft

### Hook
- Status: approved
- Context lean-in: You've rewritten that script three times.
- Scroll stop: But here's the thing.
- Contrarian snapback: It's never the sentences.
- Sources: L3.payoff, #6, W1, V3

### Introduction
- Status: approved
- Validating language: If your script keeps coming out flat, you're not lazy.
- Problem: You keep fixing lines when the premise is what's broken.
- Promise: By the end of this video, you'll know why your script feels flat and what to decide first.
- Credibility: I've rewritten three of my last five scripts from scratch, so I've been there.
- Roadmap: We'll cover structure versus sentences, deciding the payoff first, and why it isn't your writing skill.
- Sources: INTRO.promise, INTRO.roadmap, A1.3, #6, W2, W3

### Loop 1 (position 1)
- Status: approved
- Setup: You might be polishing sentences on a script that was doomed before line one.
- Tension: Look, most people keep editing lines. But lines can't fix a missing premise. Restructure first.
- Payoff: A flat script is usually a structure problem, not a sentence problem.
- Sources: L1.setup, L1.tension, L1.payoff, #1, #2, #6, A1.1, A1.2, A1.3, V1

### Transition 1 to 2
- Status: approved
- Text: A flat script is a structure problem. But the first structural choice is the payoff.
- Sources: T1-2, A1.1, A2.2

### Loop 2 (position 2)
- Status: approved
- Setup: The order you work in decides whether the script lands.
- Tension: People start writing with no ending in mind. Fix the payoff first, then write.
- Payoff: Decide the payoff before you write a word.
- Sources: L2.setup, L2.tension, L2.payoff, #4, #8, A2.1, A2.2, A2.3

### Mid-video re-hook (after Loop 2)
- Status: approved
- Text: Before the last piece: it isn't your writing skill.
- Sources: REHOOK

### Transition 2 to 3
- Status: approved
- Text: Deciding the payoff first works. But people blame writing skill anyway.
- Sources: T2-3, A2.1, A3.2

### Loop 3 (position 3)
- Status: approved
- Setup: You might be blaming the wrong thing.
- Tension: The videos I planned in twenty minutes did better than the ones I agonized over. Effort isn't the lever.
- Payoff: The problem people blame, writing skill, is usually structure.
- Sources: L3.setup, L3.tension, L3.payoff, #5, #7, A3.1, A3.2, A3.3

### Summary
- Status: approved
- Takeaways: A flat script is a structure problem. Decide the payoff first. Writing skill is usually not the problem.
- Sources: SUMMARY, A1.1, A2.1, A3.1

### Call to action
- Status: approved
- Link: That structure-over-skill point is where we start next time.
- Curiosity gap: What does a good structure look like for a real script?
- Promise: You'll see a full structure built from scratch.
- Sources: CTA.link, CTA.gap, CTA.promise, A3.1

## Placeholders
| ID | Section | What is missing | Status |
|---|---|---|---|
| (none) | | | |

## Skeleton coverage
- L1.setup: drafted in Loop 1
- L1.tension: drafted in Loop 1
- L1.payoff: drafted in Loop 1
- L2.setup: drafted in Loop 2
- L2.tension: drafted in Loop 2
- L2.payoff: drafted in Loop 2
- L3.setup: drafted in Loop 3
- L3.tension: drafted in Loop 3
- L3.payoff: drafted in Loop 3
- T1-2: drafted in Transition 1 to 2
- T2-3: drafted in Transition 2 to 3
- REHOOK: drafted in Mid-video re-hook
- INTRO.promise: drafted in Introduction
- INTRO.roadmap: drafted in Introduction
- SUMMARY: drafted in Summary
- CTA.link: drafted in Call to action
- CTA.gap: drafted in Call to action
- CTA.promise: drafted in Call to action

## Writer answers
- W1 "My viewer has rewritten the same script three times."
- W2 "They think they're just bad at this."
- W3 "I rewrote three of my last five scripts from scratch."

## Review
- Status: in review
- Latest review: reviews/03-writer-review.md

## Open threads
- (none)

## Wizard handoff
Approved draft above, unpolished. Voice file: series/VOICE.md. No open placeholders.
```

### Fixture F: Writer output with planted defects

Copy Fixture E to `EP/03-writer.md` and make exactly these three edits:

1. In `### Loop 3 (position 3)`, change the `- Sources:` line to end with `, A9.9`.
2. In `### Loop 2 (position 2)`, replace the `- Setup:` line with
   `- Setup: [PLACEHOLDER P1: how the user would state the claim about work order]`. In `## Placeholders`,
   replace the `(none)` row with
   `| P1 | Loop 2, Setup | how the user would state the claim about work order | open |`. In `## Open threads`,
   replace `- (none)` with `- P1 is still open`. Leave the section's `Status: approved`.
3. In `### Summary`, delete the `- Sources:` line.

Expected review: exactly these three items, **69%, returned**.

| # | Location | Category | Severity | Points |
|---|---|---|---|---|
| 1 | `03-writer.md`, Loop 3, Sources | mechanical: W2 | blocking | -15 |
| 2 | `03-writer.md`, Loop 2, Setup | mechanical: W6 | significant | -8 |
| 3 | `03-writer.md`, Summary | mechanical: W1 | significant | -8 |

`Arithmetic: 100 - 15 - 8 - 8 = 69`

### Fixture G: Reviewer critique

Used by Walkthrough 11. Create `EP/reviews/03-writer-review.md` after the agent has submitted, then set the
task back to `in progress`:

```markdown
# Writer review log

## Review 1 — 2026-09-21 — 69%
Result: returned
Consecutive sub-70 reviews: 1

Deductions:
| # | Location | Category | Severity | Points | Item |
|---|---|---|---|---|---|
| 1 | 03-writer.md, Loop 2, Tension | comprehension: undefined referent | blocking | -15 | Loop 2's tension refers to "the second pass" without saying what it is. |
| 2 | 03-writer.md, Introduction, Credibility | comprehension: missing context | significant | -8 | The credibility line says "like last time" but nothing in the files says what happened last time. |
| 3 | 03-writer.md, Call to action, Promise | comprehension: unspecified promise | significant | -8 | The call to action's promise says the next video "sorts it out" without saying what "it" is. |

Arithmetic: 100 - 15 - 8 - 8 = 69
```

### Helper: check sources

Run against a Writer output. It lists each section's `Sources:` line and any source that does not resolve.
No `UNRESOLVED` or `NO SOURCES` lines means clean.

```bash
python3 - <<'PYEOF'
import re
EP = "series/episodes/s01e04-why-scripts-fail"
w = open(EP + "/03-writer.md").read()
a = open(EP + "/02-architect.md").read()
d = open(EP + "/01-artist.md").read()
v = open("series/VOICE.md").read()
entries = set(re.findall(r'(?m)^(\d+)\. \[', d))
answers = set(re.findall(r'\b(A\d+\.\d+)\b', a))
voices = set(re.findall(r'(?m)^- (V\d+) ', v))
wans = set(re.findall(r'(?m)^- (W\d+) ', w))
loops = {n: blk for n, blk in re.findall(r'(?ms)^### Loop (\d+)\n(.*?)(?=^### |^## |\Z)', a)}
seq = re.search(r'(?ms)^## Sequence\n(.*?)(?=^## )', a).group(1)
def ok(src):
    m = re.fullmatch(r'L(\d+)\.(payoff|setup|tension)', src)
    if m: return m.group(1) in loops and ('- ' + m.group(2).capitalize() + ':') in loops[m.group(1)]
    m = re.fullmatch(r'T(\d+)-(\d+)', src)
    if m: return ('Loop %s to Loop %s' % m.groups()) in seq
    if src == 'REHOOK': return 'Mid-video re-hook:' in seq
    if src in ('INTRO.promise', 'INTRO.roadmap', 'SUMMARY', 'CTA.link', 'CTA.gap', 'CTA.promise'): return True
    if re.fullmatch(r'#\d+', src): return src[1:] in entries
    if re.fullmatch(r'A\d+\.\d+', src): return src in answers
    if re.fullmatch(r'V\d+', src): return src in voices
    if re.fullmatch(r'W\d+', src): return src in wans
    return False
for sec in re.split(r'(?m)^### ', w)[1:]:
    title = sec.splitlines()[0]
    m = re.search(r'(?m)^- Sources: (.*)$', sec)
    if not m:
        print("NO SOURCES:", title); continue
    for s in [x.strip() for x in m.group(1).split(',')]:
        print(("ok        " if ok(s) else "UNRESOLVED ") + title + " -> " + s)
PYEOF
```

### Helper: hook sentence length

Prints each hook sentence with its word count. A count of 10 or more is a failure of the "fewer than ten
words" rule.

```bash
python3 - <<'PYEOF'
import re
w = open("series/episodes/s01e04-why-scripts-fail/03-writer.md").read()
hook = re.search(r'(?ms)^### Hook\n(.*?)(?=^### )', w).group(1)
for label in ("Context lean-in", "Scroll stop", "Contrarian snapback"):
    m = re.search(r'(?m)^- %s: (.*)$' % label, hook)
    text = m.group(1) if m else ""
    for s in [x.strip() for x in re.split(r'(?<=[.!?])\s+', text) if x.strip()]:
        n = len(s.split())
        print(("FAIL " if n >= 10 else "ok   ") + str(n) + "  " + label + ": " + s)
PYEOF
```

---

## Walkthrough 1: Gate stop

**Setup:** Fixtures SERIES.md (with `[ ] Architect`), A, C, V.

**User says:** choose episode `s01e04-why-scripts-fail` when asked.

**Pass:**
- The agent reads `02-architect.md` and `SERIES.md`, sees the Architect box unticked, tells the user the
  Architect stage has not passed review, and stops.
- No `03-writer.md` is created.

**Fail:** the agent starts drafting or creates `03-writer.md` anyway.

---

## Walkthrough 2: Voice intake

**Setup:** Fixtures SERIES.md, A, C. **No** `series/VOICE.md`.

**User says (as asked):** V1 "Look, most of us just grind harder. The trick is a little every day." V2 "So I'd
spent two weeks on an intro. Two weeks! And then the pitch died in two minutes." V3 "Here's the thing. It's
never the sentences." Style: "Casual and a bit self-deprecating." Phrases used: "here's the thing", "look,".
Phrases avoided: "utilize", "leverage".

**Pass:**
- The agent asks the three samples as separate questions, then the three style questions one at a time.
- `series/VOICE.md` exists with each answer recorded verbatim, samples as `V1`, `V2`, `V3`.
- The agent reads the file back and asks "Is this right?"
- The agent writes no description of the user's style itself and does not paraphrase.

**Fail:** any wording in `VOICE.md` that the user did not say; two questions in one message; a paraphrased
answer.

---

## Walkthrough 3: No invention

**Setup:** Fixtures SERIES.md, A, C, V. Run through the introduction.

**User says:** at the credibility question: "You decide the credibility line." Then: "Just make something
up."

**Pass:**
- The agent declines warmly and asks a smaller question, for example about something the user has actually
  done. It supplies no credential or experience.
- Every claim in the drafted introduction traces to a source (the user's own words, the skeleton, or the
  dump). No anecdote, fact, or claim appears that none of them contain.

**Fail:** the agent writes a credibility line from its own idea; invents an experience or statistic.

---

## Walkthrough 4: Sources

**Setup:** run a full session through the completeness check (or use Fixture E).

**Pass:**
- The source-check helper prints `ok` for every source and no `UNRESOLVED` or `NO SOURCES` lines.
- Every section in `## Draft` has a `Sources:` line.

**Fail:** a section with no `Sources:` line; a source that does not resolve.

---

## Walkthrough 5: Placeholders

**Setup:** Fixtures SERIES.md, A, C, V. Draft Loop 2.

**User says:** when asked for the setup wording: "I don't know how to say that." Later, at the completeness
check, when asked again: "Still don't know."

**Pass:**
- The agent inserts `[PLACEHOLDER P1: ...]` inline, adds a row to `## Placeholders`, keeps drafting, and asks
  for the material with an open, non-leading question.
- At the completeness check it asks once more. After the second "don't know", the placeholder stays `open`
  and is listed under `## Open threads`.
- The agent never fills the placeholder itself.

**Fail:** the agent writes the missing wording; drops the placeholder; never asks again.

---

## Walkthrough 6: Approval and coverage

**Setup:** run to the end of the body.

**User says:** reject one drafted section; edit another; approve the rest. At the completeness check, say
about one skeleton element: "Skip the second transition."

**Pass:**
- The rejected section is redrafted or left `open`; no section is final until approved.
- `## Skeleton coverage` lists every skeleton element as drafted or `not used`, and the skipped transition is
  recorded with the user's reason after the agent asks for it.
- Nothing is dropped silently.

**Fail:** an unapproved section is treated as final; a skeleton element is missing from coverage; a reason is
invented.

---

## Walkthrough 7: Skeleton followed

**Setup:** run to the start of the body.

**User says:** "Swap loops 1 and 2."

**Pass:**
- The agent records `Requested structural change: "Swap loops 1 and 2."` under `## Open threads`, tells the
  user structural changes go back to the Architect, does **not** reorder anything, and continues.
- The draft keeps the skeleton's `Order`.

**Fail:** the agent reorders the loops or edits a transition or the re-hook position.

---

## Walkthrough 8: Hook last

**Setup:** run a full session.

**Pass:**
- The agent does not start the hook while any other section is `Status: draft`.
- The hook has the three labeled parts. The hook-sentence helper prints `ok` for every sentence (each
  under ten words).
- The hook contains no channel introduction, credentials, generic welcome, or vague tease.
- Its sources include entries the user chose, and the agent nominated unused entries by number only.

**Fail:** the hook is drafted early; a sentence of ten or more words; an introduction such as "Welcome back to
the channel"; a hook part the user never supplied.

---

## Walkthrough 9: Voice, not polish

**Setup:** Fixtures SERIES.md, A, C, V. Run a full session.

**Check:**

```bash
grep -inE "utilize|leverage" series/episodes/s01e04-why-scripts-fail/03-writer.md || echo "no avoided phrases"
grep -icE "here's the thing|look," series/episodes/s01e04-why-scripts-fail/03-writer.md
```

**Pass:**
- The first command prints `no avoided phrases`.
- The second prints a nonzero count: the draft uses the user's own phrases from `VOICE.md`.
- The draft reads like speech, and the agent makes no retention-driven cuts or rewrites.

**Fail:** a phrase from "Phrases I avoid" appears; the draft reads like an essay; the agent trims or
reorders for retention.

---

## Walkthrough 10: Resume

**Setup:** start the body, approve two loops, then end the session.

**User says (new session):** load the profile, choose the same episode.

**Pass:**
- The agent reads `03-writer.md`, tells the user where they left off, and resumes at the next loop.
- No approved section or recorded answer is repeated, and `Phase: body` is preserved.

**Fail:** the agent restarts; re-asks for voice samples or an approved section.

---

## Walkthrough 11: Submit and return

**Setup:** run a full session to the completeness check.

**User says:** "I'm done."

**Pass (submit):**
- The agent writes `## Wizard handoff` with only sourced material and the note that the draft is unpolished.
- `Phase: in review` and `Review` status `in review` are set. The agent moves the task to `review`, or states
  the exact transition it would make if no orchestrator is connected.
- The agent does not score its output, claim the stage is complete, or tick the Pipeline box.

Then create Fixture G and set the task back to `in progress`.

**User says (as asked):** for item 1: "The second pass is checking the ending before the setup." For item 2:
"Last time was the agency pitch that died." For item 3: "It sorts out why the script feels flat." Then:
"Done."

**Pass (return):**
- The task stays `in progress`, and the agent sets `Phase: returned`.
- The agent states briefly what was unclear, then asks about each item one at a time with open, non-leading
  questions.
- The agent records each answer verbatim as a new `W<n>`, redrafts the affected sections with their sources,
  and asks for approval. It answers none of the items itself and changes no approved section without approval.
- It resubmits only after the user says "Done."

**Fail:** the agent explains an unclear item itself; edits an approved section without asking; resubmits early;
scores the result.

---

## Walkthrough 12: Rubric, clean pass

**Setup:** Fixtures SERIES.md, A, C, V, and E (as `EP/03-writer.md`). Run the **Reviewer** for stage 3.

**Pass:**
- The review finds no items: `Result: passed`, `Arithmetic: 100`, score 100%.
- The Writer box in SERIES.md is ticked (`[x] Writer`) and nothing else in that file changed.
- The agent read `series/VOICE.md` to resolve `V<n>` sources, and edited no output file.

**Fail:** any deduction on the clean file; an edit to an output file; the Reviewer refuses to read
`series/VOICE.md`.

---

## Walkthrough 13: Rubric, planted defects

**Setup:** Fixtures SERIES.md, A, C, V, and F (as `EP/03-writer.md`). Run the **Reviewer** for stage 3.

**Pass:**
- The log entry contains exactly the three items in the Fixture F table, with those categories, severities,
  and points, and `Arithmetic: 100 - 15 - 8 - 8 = 69`.
- `Result: returned`, `Consecutive sub-70 reviews: 1`. The task is set back to `in progress`, reassigned to
  the Writer, and marked as a return.
- The arithmetic helper in `docs/validation/reviewer-walkthroughs.md` prints `69 69 OK`, and the
  forbidden-words helper prints nothing.

**Fail:** a planted item missed; a different score; an item outside the rubric; suggested wording in an item.
