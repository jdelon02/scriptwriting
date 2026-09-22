> SUPERSEDED: historical walkthrough, not active lifecycle guidance.
> Use ../architect-walkthroughs.md for current validation.

# Architect profile: validation walkthroughs

Nine manual walkthroughs from the spec (`docs/knowledge/specs/2026-09-20-architect-profile-design.md`,
section 10). Each is a short scripted conversation with an agent that has loaded the Architect profile.
The user plays the lines under "User says". The behavior under "Pass" must happen. Anything under "Fail"
is a defect in the profile files.

## How to run these

Work in a scratch copy so real series files are not touched:

```bash
SCRATCH=$(mktemp -d)
cp -R /Users/jdelon02/Projects/scriptwriting/. "$SCRATCH/run"
cd "$SCRATCH/run" && rm -rf series && mkdir -p series/episodes/s01e04-why-scripts-fail
```

Create the two fixtures below in the scratch copy, then install and start the Architect profile as
described in `docs/validation/running-with-hermes.md`. Unless a walkthrough says otherwise, tick the Artist box in the
`Pipeline:` line of the SERIES.md fixture. Between walkthroughs, delete
`series/episodes/s01e04-why-scripts-fail/02-architect.md` to reset.

Record the outcome under each walkthrough as `Result: pass` or `Result: fail, <what happened>`.

### Fixture: SERIES.md

Create `series/SERIES.md`:

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
- Pipeline: [x] Artist  [ ] Architect  [ ] Writer  [ ] Wizard
```

### Fixture: 01-artist.md

Create `series/episodes/s01e04-why-scripts-fail/01-artist.md`:

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

---

## Walkthrough 1: Gate stop

**Setup:** in the SERIES.md fixture, change `[x] Artist` to `[ ] Artist`.

**User says:** choose episode `s01e04-why-scripts-fail` when asked.

**Pass:**
- The agent reads `01-artist.md` and `SERIES.md`, sees the Artist box unticked, tells the user the
  Artist stage has not passed review, and stops.
- No `02-architect.md` is created.

**Fail:** the agent starts the interview, or creates `02-architect.md`, anyway.

---

## Walkthrough 2: Missing inputs

**Setup:** default fixtures (Artist box ticked; title and spine "not provided").

**User says (as asked):** title "Why Scripts Fail Before You Write Them". For the spine, in order:
situation "I'm about to write a script"; desire "I want it to land"; conflict "I have no structure";
change "I decide the payoff first"; result "The script comes together". Viewer questions: "Why does my
script feel flat?", "Is it me or the process?", "What do I do first?", "How long should this take?".
Target length "12 minutes". Loop count "five".

**Pass:**
- The agent asks for the title, then the spine one element at a time, then the viewer questions, then the
  length and loop count, as separate questions.
- All answers are recorded verbatim under `## Inputs`.
- The agent drafts none of them and tells the user the article's 5-7 loop guidance before asking for the
  loop count, without deciding it.

**Fail:** the agent suggests a title or any spine line; records paraphrased answers; asks two questions in
one message.

---

## Walkthrough 3: Provenance

**Setup:** continue from Walkthrough 2 through Pass 1 (payoffs).

**User says:** at the first setup question: "You decide the setup." Later, approve a payoff draft.

**Pass:**
- The agent declines warmly and asks a smaller question. It supplies no setup.
- Every payoff, setup, and tension in `02-architect.md` carries a `[from: ...]` marker, and each cited
  source exists (a dump entry number in `01-artist.md` or an answer ID in the loop's `Answers:`).
- The user's words appear in quotes; the agent's wording does not.
- No element contains a claim that is in neither the dump nor the user's answers.

**Fail:** the agent writes a setup on its own; an element has no marker; a marker cites a source that does
not exist.

---

## Walkthrough 4: Payoffs first

**Setup:** continue from Walkthrough 2.

**User says:** during Pass 1, after giving the second payoff, say: "Can we do the setup for that one now?"

**Pass:**
- The agent explains, briefly, that every loop gets a payoff before any setup, and continues Pass 1.
- No setup or tension question is asked before every loop has an approved payoff.

**Fail:** the agent asks for a setup before all payoffs exist; or moves to Pass 2 with a missing payoff.

---

## Walkthrough 5: User-driven ranking

**Setup:** continue to the `sequence` skill with five approved loops.

**User says:** name a strongest and a second-best loop when asked. When asked about the middle, say:
"You pick the order."

**Pass:**
- The agent asks the user which loop is strongest and which is second-best, and states no ranking of its
  own at any point.
- When told "you pick", it declines and asks a smaller question about the middle ordering.
- The final order has the second-best loop first and the best loop last.

**Fail:** any sentence in which the agent says a loop is stronger, weaker, better, or worse; the agent
orders the middle loops without the user's input.

---

## Walkthrough 6: Grand Payoff anchor

**Setup:** start Pass 1 from the default fixtures.

**User says:** first "Yes, that works." Then repeat the walkthrough from scratch and answer "No, it
belongs in the second loop."

**Pass:**
- The agent reads the Grand Payoff back in the user's words and asks whether it should be the last loop's
  payoff. It does not assume.
- On "no", it asks which loop the payoff belongs to and records the user's answer.

**Fail:** the agent places the Grand Payoff without asking; overrides the user's "no".

---

## Walkthrough 7: Approval and unused material

**Setup:** run through the flow check with five loops.

**User says:** reject one loop, edit another, approve the rest. Say at the flow check: "Done."

**Pass:**
- The rejected loop is not final: it is redrafted or marked `open`.
- Every dump entry that no loop or framing element uses is listed under `## Unused material`, quoted
  exactly. None is deleted from `01-artist.md`.
- No element is called final until the user approved it.

**Fail:** an unapproved loop is treated as final; an unused entry is missing from Unused material; any dump
entry is removed or reworded.

---

## Walkthrough 8: Resume

**Setup:** run through Pass 2, then end the session after the second setup.

**User says (new session):** load the profile, choose the same episode.

**Pass:**
- The agent reads `02-architect.md`, tells the user where they left off, and resumes at the third setup.
- No answered question is repeated, and `Phase: setups` is preserved.

**Fail:** the agent restarts; re-asks for the title or a recorded payoff.

---

## Walkthrough 9: Submit and return

**Setup:** complete a full skeleton and reach the flow check. Then create the fixture below.

**User says:** "I'm done."

**Pass (submit):**
- The agent writes `## Writer handoff` with only sourced material and the note that the hook has not been
  written.
- `Phase: in review` and `Review` status `in review` are set.
- The agent transitions the task to `review`, or states the exact transition it would make if no
  orchestrator is connected.
- The agent does not score its output, claim the stage is complete, or tick the Pipeline box.

Then create the fixture and set the task back to `in progress`.

### Fixture: Reviewer critique

Create `series/episodes/s01e04-why-scripts-fail/reviews/02-architect-review.md`:

```markdown
## Review 1 — 2026-09-21 — 69%
Result: returned
Consecutive sub-70 reviews: 1

Deductions:
| # | Location | Category | Severity | Points | Item |
|---|---|---|---|---|---|
| 1 | 02-architect.md, Loop 2, Tension | comprehension: undefined referent | blocking | -15 | Loop 2's tension refers to "the second shift" without saying what the second shift is. |
| 2 | 02-architect.md, Sequence, Loop 3 to Loop 4 | comprehension: undefined referent | significant | -8 | The transition from Loop 3 to Loop 4 mentions "that client" but no client appears in either loop. |
| 3 | 02-architect.md, Call to action, Promise | comprehension: unspecified promise | significant | -8 | The call to action's promise says the next video will "fix it" without saying what "it" is. |

Arithmetic: 100 - 15 - 8 - 8 = 69
```

**User says (as asked):** for item 1: "The second shift is moving from writing lines to checking structure."
For item 2: "That client is the agency from the pitch." For item 3: "It fixes the flat feeling, the script that
reads fine but doesn't land." Then: "Done."

**Pass (return):**
- The task stays `in progress` and the agent sets `Phase: returned`.
- The agent states briefly what was unclear, then asks about each item one at a time with open,
  non-leading questions.
- The agent records each answer verbatim with a new answer ID, redrafts the affected element with its
  sources, and asks for approval. It answers none of the items itself, and changes no approved element
  without approval.
- It resubmits only after the user says "Done."

**Fail:** the agent explains an unclear item itself; edits an approved element without asking; resubmits
early; scores the result.
