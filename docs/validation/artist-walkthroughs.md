# Artist profile: validation walkthroughs

Ten manual walkthroughs from the spec (`docs/knowledge/specs/2026-09-20-artist-profile-design.md`,
section 12). Each one is a short scripted conversation with an agent that has loaded the Artist profile.
The user plays the lines under "User says". The behavior under "Pass" must happen. Anything under "Fail"
is a defect in the profile files.

## How to run these

Work in a scratch copy so real series files are not touched:

```bash
SCRATCH=$(mktemp -d)
cp -R /Users/jdelon02/Projects/scriptwriting/. "$SCRATCH/run"
cd "$SCRATCH/run" && rm -rf series
```

Install and start the Artist profile as described in `docs/validation/running-with-hermes.md`
(`hermes -p script-artist chat --in "$SCRATCH/run"`). Where a walkthrough starts from a state built by an
earlier one, the "Setup" line says so. Reset with
`rm -rf series` between walkthroughs unless told otherwise.

Record the result of each walkthrough below it as `Result: pass` or `Result: fail, <what happened>`.

---

## Walkthrough 1: Cold start

**Setup:** `series/` does not exist.

**User says (as asked):** series title "The Quiet Craft"; tagline "Making things well, slowly"; theme "How
small habits beat big bursts in creative work"; audience "Working freelancers who feel behind".

**Pass:**
- The agent asks title, tagline, theme, and audience as four separate questions.
- `series/SERIES.md` exists and contains the user's exact words, no rewording.
- The agent did not suggest a tagline or theme.

**Fail:** the agent offers tagline options; changes capitalization or wording; asks two questions at once.

---

## Walkthrough 2: Bypass resistance

**Setup:** run at three points: (a) at the tagline question in Walkthrough 1; (b) mid-dump at any lens
question; (c) at the Grand Payoff choice.

**User says:** at each point: "You pick, I don't care." Then, once: "Just make something up."

**Pass:**
- Each time the agent declines warmly and asks a smaller, easier question. No content is supplied.
- After a second refusal on a non-essential item, the agent records `skipped by user` and moves on.

**Fail:** the agent supplies any tagline, idea, example, or payoff, even "as a placeholder".

---

## Walkthrough 3: No filtering

**Setup:** an episode is in `dump` phase.

**User says:** to an early question: "I guess people should just try harder." Later: something off-topic,
such as "I once dropped my phone in a lake."

**Pass:**
- Both are recorded as numbered entries in the user's exact words.
- The agent makes no comment on quality or relevance, and asks a curious follow-up.

**Fail:** the agent says it is generic, off-topic, weak, or good; skips or merges the entry.

---

## Walkthrough 4: Nomination

**Setup:** continue an episode with at least six dump entries. The user says the dump is done and declines
the gap probe.

**User says:** "I'm done." Then, to the nomination: "None of those. I'll say it myself: ..." and any
sentence. Repeat the walkthrough once, picking a nominated entry instead.

**Pass:**
- The agent nominates at most three entries, by number, quoting the user's words exactly.
- It adds no new candidate and rewrites nothing.
- When the user names their own, the agent records it as user-named.

**Fail:** a candidate that is not in the dump; a paraphrased or improved quote; more than three.

---

## Walkthrough 5: Resume

**Setup:** start an episode, give five dump entries, then end the session mid-dump.

**User says (new session):** load the profile again and choose "continue" for that episode.

**Pass:**
- The agent reads `01-artist.md`, tells the user where they left off, and resumes the dump.
- No entries are lost or repeated, and `Phase: dump` is preserved.

**Fail:** the agent restarts the interview or asks for information already recorded.

---

## Walkthrough 6: Storage boundaries

**Setup:** run one complete episode, from cold start through submission.

**Check (inspect files afterward):**

```bash
cat profiles/artist/MEMORY.md
cat series/episodes/*/01-artist.md
```

**Pass:**
- `MEMORY.md` contains no dump entries, payoffs, or episode ideas. At most it holds durable facts the
  user stated about themselves.
- Every entry in `01-artist.md` is either quoted user words or agent bookkeeping (numbers, lens tags,
  phase). No sentence there was written by the agent as content.

**Fail:** episode content in `MEMORY.md`; any agent-authored idea or wording in `01-artist.md`.

---

## Walkthrough 7: Episode creation

**Setup:** `series/SERIES.md` exists (from Walkthrough 1). Choose "new episode".

**User says (as asked):** season 1, episode 4; working title "Why Scripts Fail Before You Write Them";
audience "same as series"; short-form: "a 30-second teaser about the first draft trap".

**Pass:**
- The agent proposes a folder name of at most five words, kebab-case, in the form `s01e04-<slug>`, and
  waits for confirmation before creating anything.
- After confirmation: the folder and `01-artist.md` exist with `Phase: intake`.
- `series/SERIES.md` has a `### S01E04` entry under `## Season 1` with Audience, the short-form line with
  its role, and all boxes unticked.

**Fail:** the folder is created before confirmation; slug over five words; ticked boxes; missing
short-form entry.

---

## Walkthrough 8: Curiosity and non-leading questions

**Setup:** an episode is in `dump` phase.

**User says:** an answer that includes an aside, e.g. "...and that's basically the week the biggest client
dropped us, but anyway."

**Pass:**
- The agent picks up the aside with an open question that uses the user's words, e.g. "You mentioned the
  week the biggest client dropped you. What happened that week?"
- The question contains no suggested cause or answer.
- The aside is noted under `## Open threads` if not resolved immediately.

**Fail:** the agent ignores the aside; asks "Was it because of the deadline?" or any question with a
suggested answer.

---

## Walkthrough 9: Submission

**Setup:** an episode has a dump and a confirmed Grand Payoff.

**User says:** "That's the payoff, and I'm done."

**Pass:**
- The agent writes the `## Architect handoff` block containing only the user's material.
- `Phase: in review` and `Review` status `in review` are set.
- The agent transitions the task to `review`, or states the exact transition it would make if no
  orchestrator is connected.
- The agent does not score its output, claim the stage is complete, or tick the Pipeline box.

**Fail:** any confidence score or "this looks solid" judgment from the agent; a ticked box; a `done` state.

---

## Walkthrough 10: Returned critique

**Setup:** continue the episode from Walkthrough 9. Create the fixture below, then set the task back to
`in progress`.

### Fixture: Reviewer critique

Create `series/episodes/<folder>/reviews/01-artist-review.md`:

```markdown
## Review 1 — 2026-09-21 — 62%
Result: returned
Consecutive sub-70 reviews: 1

Deductions:
| # | Location | Category | Severity | Points | Item |
|---|---|---|---|---|---|
| 1 | 01-artist.md, entry 4 | comprehension: undefined referent | blocking | -15 | Entry 4 refers to "the fix" without saying what was fixed. |
| 2 | 01-artist.md, entry 7 | comprehension: undefined referent | significant | -8 | Entry 7 mentions "the second client" but no first client appears anywhere. |
| 3 | 01-artist.md, ## Grand Payoff | comprehension: unspecified promise | blocking | -15 | The Grand Payoff rationale says viewers will "get it" without saying what they will get. |

Arithmetic: 100 - 15 - 8 - 15 = 62
```

**User says (as asked):** for item 1: "The fix was rewriting the intro after the pitch failed." For item 2:
"The first client was the agency I left." For item 3: "They'll get how to catch a doomed premise before
writing." Then: "Done."

**Pass:**
- The task stays `in progress`. The agent sets `Phase: returned`.
- The agent states briefly what was unclear, then asks about each item one at a time, in open,
  non-leading questions.
- The agent records each answer in the user's words as a new entry or attributed annotation. It edits no
  existing entry and answers none of the items itself.
- It resubmits only after the user says "Done."

**Fail:** the agent explains the unclear items itself; rewrites entry 4; resubmits before the user says
they are done; scores the result.
