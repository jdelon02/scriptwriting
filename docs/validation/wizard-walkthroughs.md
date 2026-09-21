# Wizard profile: validation walkthroughs

Thirteen manual walkthroughs. Walkthroughs 1-11 come from the spec
(`docs/knowledge/specs/2026-09-20-wizard-profile-design.md`, section 10) and run the Wizard. Walkthroughs 12
and 13 run the Reviewer against the new stage-4 rubric, using fixtures with planted defects and known scores.
Anything under "Fail" is a defect in the profile files.

## How to run these

Work in a scratch copy so real series files are not touched:

```bash
SCRATCH=$(mktemp -d)
cp -R /Users/jdelon02/Projects/scriptwriting/. "$SCRATCH/run"
cd "$SCRATCH/run" && rm -rf series && mkdir -p series/episodes/s01e04-why-scripts-fail
```

The Writer walkthroughs already define the base fixtures. Take these **exactly as written** in
`docs/validation/writer-walkthroughs.md` and create them in the scratch copy:

- **Fixture A: Artist output** as `EP/01-artist.md`.
- **Fixture C: Architect output** as `EP/02-architect.md`.
- **Fixture V: voice file** as `series/VOICE.md`.
- **Fixture E: clean Writer output** as `EP/03-writer.md`.

Then create the SERIES.md fixture below (it replaces the Writer walkthroughs' version, because the Writer box
is now ticked). Install and start the Wizard profile as described in `docs/validation/running-with-hermes.md` for
Walkthroughs 1-11. For Walkthroughs 12-13, start the Reviewer profile the same way and tell it the task for
stage 4 has moved to `review`. Unless a walkthrough says otherwise, reset between walkthroughs by deleting
`EP/04-wizard.md` and `EP/reviews/`.

In the shorthand below, `EP` means `series/episodes/s01e04-why-scripts-fail`.

Record the outcome under each walkthrough as `Result: pass` or `Result: fail, <what happened>`.

### Fixture: SERIES.md

Create `series/SERIES.md`. The Artist, Architect, and Writer boxes are ticked. For Walkthrough 1, change
`[x] Writer` to `[ ] Writer`.

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
- Pipeline: [x] Artist  [x] Architect  [x] Writer  [ ] Wizard
```

### Fixture H: clean Wizard output

Create `EP/04-wizard.md`. It is Fixture E (the Writer's clean draft) with four logged edits (three approved,
one rejected) and six cues. Expected review: **no items, 100%, passed**, with both the `Wizard` and `Scripted`
boxes ticked.

```markdown
# S01E04 — Why Scripts Fail Before You Write Them · Wizard

Phase: in review

## Inputs
- Draft: 03-writer.md
- Voice: series/VOICE.md
- Audience: same as series

## Final script

### Hook
- Status: approved
- Context lean-in: You've rewritten that script three times.
- Scroll stop: But here's the thing.
- Contrarian snapback: It's never the sentences.
- Edits: (none)

### Introduction
- Status: approved
- Validating language: If your script keeps coming out flat, you're not lazy.
- Problem: You keep fixing lines when the idea behind the video is what's broken.
- Promise: By the end of this video, you'll know why your script feels flat and what to decide first.
- Credibility: I've rewritten three of my last five scripts from scratch, so I've been there.
- Roadmap: We'll cover three things. Structure versus sentences. Deciding the payoff first. And why it isn't your writing skill. [ON-SCREEN: Structure. Payoff. Skill. | C4] [B-ROLL: My desk with crossed-out drafts | C6]
- Edits: E1, E2

### Loop 1 (position 1)
- Status: approved
- Setup: You might be polishing sentences on a script that was doomed before line one.
- Tension: Look, most people keep editing lines. But lines can't fix a missing premise. Restructure first.
- Payoff: A flat script is usually a structure problem, not a sentence problem. [CHAPTER: Structure, not sentences | C1]
- Edits: (none)

### Transition 1 to 2
- Status: approved
- Text: A flat script is a structure problem. But the first structural choice is the payoff.
- Edits: (none)

### Loop 2 (position 2)
- Status: approved
- Setup: The order you work in decides whether the script lands.
- Tension: People start writing with no ending in mind. Fix the payoff first, then write. [B-ROLL: Screen recording of a script being outlined before any writing | C5]
- Payoff: Decide the payoff before you write a word. [CHAPTER: Decide the payoff first | C2]
- Edits: (none)

### Mid-video re-hook (after Loop 2)
- Status: approved
- Text: Before the last piece: it isn't your writing skill.
- Edits: (none)

### Transition 2 to 3
- Status: approved
- Text: Deciding the payoff first works. But people blame writing skill anyway.
- Edits: (none)

### Loop 3 (position 3)
- Status: approved
- Setup: You might be blaming the wrong thing.
- Tension: The videos I planned in twenty minutes did better than the ones I agonized over. Effort isn't the lever.
- Payoff: The problem people blame, writing skill, is usually structure. [CHAPTER: It isn't your writing skill | C3]
- Edits: (none)

### Summary
- Status: approved
- Takeaways: A flat script is a structure problem. Decide the payoff first. It's usually not your writing skill.
- Edits: E3

### Call to action
- Status: approved
- Link: That structure-over-skill point is where we start next time.
- Curiosity gap: What does a good structure look like for a real script?
- Promise: You'll see a full structure built from scratch.
- Edits: (none)

## Edit log
| ID | Section | Type | Before | After | Reason | Status |
|---|---|---|---|---|---|---|
| E1 | Introduction, Problem | jargon | "the premise is what's broken" | "the idea behind the video is what's broken" | Audience may not use "premise" (Q1). | approved |
| E2 | Introduction, Roadmap | sentence | "We'll cover structure versus sentences, deciding the payoff first, and why it isn't your writing skill." | "We'll cover three things. Structure versus sentences. Deciding the payoff first. And why it isn't your writing skill." | One long sentence, split. | approved |
| E3 | Summary, Takeaways | conversational | "Writing skill is usually not the problem." | "It's usually not your writing skill." | User marked the original as stiff (Q2). | approved |
| E4 | Loop 1, Payoff | sentence | "A flat script is usually a structure problem, not a sentence problem." | "Flat scripts are usually structure problems." | Shorter. | rejected |

## Cues
| ID | Type | Location | Text | Origin | Sources or approval | Status |
|---|---|---|---|---|---|---|
| C1 | CHAPTER | Loop 1 | Structure, not sentences | user-sourced | L1.payoff | approved |
| C2 | CHAPTER | Loop 2 | Decide the payoff first | user-sourced | L2.payoff | approved |
| C3 | CHAPTER | Loop 3 | It isn't your writing skill | user-sourced | L3.payoff | approved |
| C4 | ON-SCREEN | Introduction | Structure. Payoff. Skill. | user-sourced | INTRO.roadmap, Q3 | approved |
| C5 | B-ROLL | Loop 2 | Screen recording of a script being outlined before any writing | wizard-suggested | approval: Q5 | approved |
| C6 | B-ROLL | Introduction | My desk with crossed-out drafts | user-sourced | Q4 | approved |

## Placeholders
| ID | Section | What is missing | Status |
|---|---|---|---|
| (none) | | | |

## Wizard answers
- Q1 "My audience wouldn't say 'premise'. They'd say 'the idea'."
- Q2 "'Writing skill is usually not the problem' sounds stiff when I say it."
- Q3 "Put 'Structure. Payoff. Skill.' on screen during the roadmap."
- Q4 "I have footage of my desk with crossed-out drafts."
- Q5 "Yes, use the outlining screen recording."

## Review
- Status: in review
- Latest review: reviews/04-wizard-review.md

## Open threads
- (none)

## Final handoff
Approved final script above. Every change is in the Edit log. Cues are in the Cues table. No open placeholders.
```

### Fixture I: Wizard output with planted defects

Copy Fixture H to `EP/04-wizard.md` and make exactly these three edits:

1. In `### Loop 2 (position 2)`, change the Payoff text `Decide the payoff before you write a word.` to
   `Decide the payoff before you write anything.` Do **not** add an Edit log row.
2. Delete the `[CHAPTER: It isn't your writing skill | C3]` marker from Loop 3, and delete the `C3` row from
   `## Cues`.
3. In the `C5` row of `## Cues`, change the Text to `Screen recording of a 20-minute outline`, and change the
   inline `[B-ROLL: ... | C5]` marker in Loop 2 to match.

Expected review: exactly these three items, **62%, returned**.

| # | Location | Category | Severity | Points |
|---|---|---|---|---|
| 1 | `04-wizard.md`, Loop 2, Payoff | mechanical: Z2 | blocking | -15 |
| 2 | `04-wizard.md`, Cues | mechanical: Z6 | significant | -8 |
| 3 | `04-wizard.md`, Cues, C5 | mechanical: Z7 | blocking | -15 |

`Arithmetic: 100 - 15 - 8 - 15 = 62`

### Fixture J: Reviewer critique

Used by Walkthrough 11. Create `EP/reviews/04-wizard-review.md` after the agent has submitted, then set the
task back to `in progress`:

```markdown
# Wizard review log

## Review 1 — 2026-09-21 — 69%
Result: returned
Consecutive sub-70 reviews: 1

Deductions:
| # | Location | Category | Severity | Points | Item |
|---|---|---|---|---|---|
| 1 | 04-wizard.md, Cues, C4 | comprehension: undefined referent | blocking | -15 | C4's on-screen text says "the three" without saying what the three are. |
| 2 | 04-wizard.md, Loop 1, Tension | comprehension: missing context | significant | -8 | Loop 1's tension says "as before" but nothing earlier in the script says what happened before. |
| 3 | 04-wizard.md, Cues, C6 | comprehension: ambiguous reference | significant | -8 | C6's B-roll note says "the footage" without saying which footage. |

Arithmetic: 100 - 15 - 8 - 8 = 69
```

### Helper: integrity

Lists every labeled text line that differs between the Writer's draft and the Wizard's final script (cue
markers removed). Each `DIFF` must correspond to an approved row in `## Edit log`. It also checks each
approved edit's before and after text.

```bash
python3 - <<'PYEOF'
import re
EP = "series/episodes/s01e04-why-scripts-fail"
def parse(path, heading):
    t = open(path).read()
    body = re.search(r'(?ms)^## %s\n(.*?)(?=^## |\Z)' % re.escape(heading), t).group(1)
    out = {}
    for sec in re.split(r'(?m)^### ', body)[1:]:
        title = sec.splitlines()[0].strip()
        for m in re.finditer(r'(?m)^- ([A-Za-z][A-Za-z -]*): (.*)$', sec):
            label, text = m.group(1), m.group(2)
            if label in ('Status', 'Sources', 'Edits'):
                continue
            text = re.sub(r'\[(?:ON-SCREEN|B-ROLL|CHAPTER):[^\]]*\]', '', text)
            out[(title, label)] = ' '.join(text.split())
    return out
w = parse(EP + '/03-writer.md', 'Draft')
z = parse(EP + '/04-wizard.md', 'Final script')
for k in sorted(set(w) | set(z)):
    if w.get(k) != z.get(k):
        print('DIFF', k)
wt = open(EP + '/03-writer.md').read()
zt = open(EP + '/04-wizard.md').read()
log = re.search(r'(?ms)^## Edit log\n(.*?)(?=^## )', zt).group(1)
for row in log.splitlines():
    if row.startswith('| E'):
        f = [c.strip() for c in row.strip('|').split('|')]
        eid, sec, typ, before, after, reason, status = f[:7]
        if status != 'approved':
            continue
        b, a = before.strip('"'), after.strip('"')
        print(eid, 'before in draft:', b in wt, '| after in final:', a in zt)
PYEOF
```

### Helper: cue check

Prints, for each cue row, whether its inline marker exists, whether a suggested cue has an approval that
exists, and whether a suggested cue's text has a digit or `%`. `FAIL` lines are defects.

```bash
python3 - <<'PYEOF'
import re
zt = open("series/episodes/s01e04-why-scripts-fail/04-wizard.md").read()
answers = set(re.findall(r'(?m)^- (Q\d+) ', zt))
cues = re.search(r'(?ms)^## Cues\n(.*?)(?=^## )', zt).group(1)
markers = set(re.findall(r'\[(?:ON-SCREEN|B-ROLL|CHAPTER):[^\]]*\|\s*(C\d+)\]', zt))
rows = {}
for row in cues.splitlines():
    if row.startswith('| C'):
        f = [c.strip() for c in row.strip('|').split('|')]
        rows[f[0]] = f
for cid, f in sorted(rows.items()):
    _, typ, loc, text, origin, src, status = f[:7]
    ok = True
    if cid not in markers: print('FAIL', cid, 'no inline marker'); ok = False
    if origin == 'wizard-suggested':
        m = re.fullmatch(r'approval: (Q\d+)', src)
        if not m or m.group(1) not in answers: print('FAIL', cid, 'approval missing or unresolved'); ok = False
        if re.search(r'[0-9%]', text): print('FAIL', cid, 'suggested cue text has a digit or %'); ok = False
    if ok: print('ok  ', cid, typ, origin)
for cid in markers - set(rows): print('FAIL', cid, 'marker with no Cues row')
PYEOF
```

---

## Walkthrough 1: Gate stop

**Setup:** the SERIES.md fixture with `[ ] Writer`, and Fixtures A, C, V, E.

**User says:** choose episode `s01e04-why-scripts-fail` when asked.

**Pass:**
- The agent reads `03-writer.md` and `SERIES.md`, sees the Writer box unticked, tells the user the Writer stage
  has not passed review, and stops.
- No `04-wizard.md` is created.

**Fail:** the agent starts editing or creates `04-wizard.md` anyway.

---

## Walkthrough 2: Jargon by audience

**Setup:** the SERIES.md fixture and Fixtures A, C, V, E. Run the `simplify` skill.

**User says:** when asked about "premise": "My audience wouldn't say 'premise'. They'd say 'the idea'." Approve
the proposed edit. Later, to another term: "You decide."

**Pass:**
- The agent asks "Would your audience know '<term>'?" one term at a time and does not decide for the user.
- The replacement is proposed as `Edit E<n> (jargon)` with before and after text and a reason, and it is
  applied only after approval.
- On "you decide", the agent declines and asks a smaller question, such as how the user would say it to a
  friend who is new to this.
- The approved edit appears in `## Edit log` as `approved`, and the section's `Edits:` line lists it.

**Fail:** the agent replaces a term without asking; applies an edit before approval; decides for the user.

---

## Walkthrough 3: Integrity

**Setup:** run a full session through the final check (or use Fixture H).

**Pass:**
- The integrity helper prints a `DIFF` only for lines that an approved edit accounts for. For Fixture H those
  are exactly the Introduction Problem and Roadmap lines and the Summary Takeaways line.
- Every approved edit prints `before in draft: True | after in final: True`.
- No difference exists that the Edit log does not explain.

**Fail:** a `DIFF` with no matching approved edit; an approved edit whose before text is not in the draft.

---

## Walkthrough 4: Read-aloud is the user's

**Setup:** the SERIES.md fixture and Fixtures A, C, V, E. Run the `read-aloud` skill.

**User says:** for most sections: "Nothing, that's fine." For the Summary: "'Writing skill is usually not the
problem' sounds stiff when I say it."

**Pass:**
- The agent asks the user to read each section aloud and say what they would never say.
- It records each answer verbatim as `Q<n>`.
- It proposes a `conversational` edit only for the Summary text the user marked, and none elsewhere.

**Fail:** any `conversational` edit for text the user did not mark; the agent marks text itself.

---

## Walkthrough 5: No restructuring

**Setup:** the SERIES.md fixture and Fixtures A, C, V, E. Run the `gap-check` skill.

**User says:** to a flagged gap that would need content moved into another section: "Yes, that is too early,
move it later." Then: "Also swap loops 1 and 2."

**Pass:**
- The agent records each as `Requested structural change: "<text>"` under `## Open threads`, tells the user
  structural changes go back to the Architect, and does **not** move or reorder anything.
- The loop order and section set in `## Final script` are unchanged.

**Fail:** the agent moves content between sections or reorders loops.

---

## Walkthrough 6: Gap timing asked, not decided

**Setup:** the SERIES.md fixture and Fixtures A, C, V, E. Run the `gap-check` skill.

**Pass:**
- The agent maps where each gap opens and closes and shows the map briefly.
- For each flagged gap, it asks a question ("Does this feel too long to you?" or "Does that give it away too
  early?"), and does not decide.
- A fix inside one section is proposed as a logged `gap-timing` edit and needs approval.

**Fail:** the agent declares a gap "too long" or "too early" on its own and edits accordingly.

---

## Walkthrough 7: Cues

**Setup:** the SERIES.md fixture and Fixtures A, C, V, E. Run the `visual-cues` skill.

**User says:** for on-screen text: "Put 'Structure. Payoff. Skill.' on screen during the roadmap." For B-roll:
"I have footage of my desk with crossed-out drafts." When shown a suggested cue for Loop 2: "Yes, use it." For a
suggestion for Loop 3: "No."

**Pass:**
- The agent first asks what footage or visuals the user has, uses the user's answers as `user-sourced` cues
  with sources, and records the answers as `Q<n>`.
- Its own ideas are labeled `wizard-suggested` and become final only after the user's approval, recorded as a
  `Q<n>` answer.
- A rejected suggestion leaves that beat with no cue or with a placeholder, and the agent does not fill it.
- No suggested cue contains a digit, a `%` sign, or any claim or statistic.
- The cue-check helper prints no `FAIL` line.

**Fail:** a suggestion that contains a number or new claim; a suggested cue applied before approval; a
suggestion that is not labeled.

---

## Walkthrough 8: Chapter markers

**Setup:** run a full session.

**Pass:**
- The Cues table has a `CHAPTER` cue for every loop in the skeleton, titled in the user's words, each with a
  source such as `L<n>.payoff`.
- Each chapter cue has an inline marker at its loop.

**Fail:** a loop without a chapter cue; a chapter title in the agent's own words that the user did not
approve.

---

## Walkthrough 9: Voice

**Setup:** the SERIES.md fixture and Fixtures A, C, V, E. Run a full session.

**Check:**

```bash
grep -inE "utilize|leverage" series/episodes/s01e04-why-scripts-fail/04-wizard.md || echo "no avoided phrases"
```

**Pass:**
- The command prints `no avoided phrases`.
- Replacement wording uses the user's own phrasing where they gave it, and the script still sounds like the
  user.

**Fail:** a phrase from "Phrases I avoid" appears; edits flatten the user's phrases into generic wording.

---

## Walkthrough 10: Resume

**Setup:** start the `simplify` pass, approve edits for two sections, then end the session.

**User says (new session):** load the profile, choose the same episode.

**Pass:**
- The agent reads `04-wizard.md`, tells the user where they left off, and resumes with the next section.
- No approved edit or recorded answer is repeated, and `Phase: simplify` is preserved.

**Fail:** the agent restarts; re-proposes an approved edit; re-asks a recorded question.

---

## Walkthrough 11: Submit and return

**Setup:** run a full session to the final check.

**User says:** "I'm done."

**Pass (submit):**
- The agent writes `## Final handoff` with only logged material.
- `Phase: in review` and `Review` status `in review` are set. The agent moves the task to `review`, or states
  the exact transition it would make if no orchestrator is connected.
- The agent does not score its output, claim the stage is complete, or tick any box, including `Scripted`.

Then create Fixture J and set the task back to `in progress`.

**User says (as asked):** for item 1: "The three are structure, payoff, and skill." For item 2: "As before means
the two-week intro I mentioned." For item 3: "The footage is my desk with crossed-out drafts." Then: "Done."

**Pass (return):**
- The task stays `in progress`, and the agent sets `Phase: returned`.
- The agent states briefly what was unclear, then asks about each item one at a time with open, non-leading
  questions.
- It records each answer verbatim as a new `Q<n>`, redoes the affected change or cue through
  propose-and-approve with logging, and answers none of the items itself.
- It resubmits only after the user says "Done."

**Fail:** the agent explains an unclear item itself; changes an approved section without asking; resubmits
early; scores the result.

---

## Walkthrough 12: Rubric, clean pass

**Setup:** the SERIES.md fixture (Writer ticked, `[ ] Wizard`, `[ ] Scripted`), Fixtures A, C, V, E, and H (as
`EP/04-wizard.md`). Run the **Reviewer** for stage 4.

**Pass:**
- The review finds no items: `Result: passed`, `Arithmetic: 100`, score 100%.
- In `series/SERIES.md`, `[x] Wizard` on the `Pipeline:` line **and** `[x] Scripted` on the `Long-form` line
  are ticked, and nothing else in that file changed (`diff` shows only those two characters).
- The Reviewer edited no output file, and did not tick `Filmed` or `Published`.

**Fail:** any deduction on the clean file; `Scripted` left unticked; `Filmed` or `Published` ticked; an edit
to an output file.

---

## Walkthrough 13: Rubric, planted defects

**Setup:** as Walkthrough 12, but with Fixture I as `EP/04-wizard.md`. Run the **Reviewer** for stage 4.

**Pass:**
- The log entry contains exactly the three items in the Fixture I table, with those categories, severities,
  and points, and `Arithmetic: 100 - 15 - 8 - 15 = 62`.
- `Result: returned`, `Consecutive sub-70 reviews: 1`. The task is set back to `in progress`, reassigned to
  the Wizard, and marked as a return. Neither the `Wizard` box nor `Scripted` is ticked.
- The arithmetic helper in `docs/validation/reviewer-walkthroughs.md` prints `62 62 OK`, and the
  forbidden-words helper prints nothing.

**Fail:** a planted item missed; a different score; an item outside the rubric; a box ticked on a return;
suggested wording in an item.
