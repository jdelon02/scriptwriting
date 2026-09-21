#!/usr/bin/env python3
"""Write Head Scriptwriter walkthrough fixtures into a scratch copy of the repo.

Usage: python3 scripts/make_head_fixtures.py <scratch-repo-dir> <state> [--stage N]

States:
  kickoff            series exists, no episode yet
  existing           S01E04 already exists (Artist in progress)
  after-artist       Artist passed
  structural         Artist and Architect passed; the Writer's Open threads hold a requested structural change
  held               Artist and Architect passed; the Writer stage is held after three sub-70 reviews
  mixed              Artist passed; Architect returned once; Writer not started
  resume-return      stage N: Phase in review, latest review returned
  resume-release     stage N: held, then a Release entry
  resume-revision    stage N: passed earlier, then a Reopen entry in head-log.md
  resume-passed      stage N: latest review passed
  resume-none        stage N: submitted, no review entry yet
  resume-held        stage N: held for user, no release
  count-reset        Artist stage: two returns, then a Release entry (for the Reviewer's count-reset test)
"""
import sys
from pathlib import Path

EP = "series/episodes/s01e04-why-scripts-fail"
STAGES = {1: ("01-artist.md", "Artist"), 2: ("02-architect.md", "Architect"), 3: ("03-writer.md", "Writer"), 4: ("04-wizard.md", "Wizard")}
BOXES = ["Artist", "Architect", "Writer", "Wizard"]

SERIES_HEAD = """# The Quiet Craft
> Making things well, slowly

## Overarching Theme
How small habits beat big bursts in creative work

## Audience
Working freelancers who feel behind

## Season 1
"""


def series_md(ticked=(), episode=True):
    if not episode:
        return SERIES_HEAD
    pipe = "  ".join("[%s] %s" % ("x" if b in ticked else " ", b) for b in BOXES)
    return SERIES_HEAD + """
### S01E04 — Why Scripts Fail Before You Write Them
- Folder: `episodes/s01e04-why-scripts-fail/`
- Audience: same as series
- Long-form: Why Scripts Fail Before You Write Them
  - [ ] Scripted  [ ] Filmed  [ ] Published
- Short-form (each supports the long-form episode):
  - (none planned yet)
- Pipeline: %s
""" % pipe


def stage_md(n, phase="in review", open_threads="- (none)"):
    fname, name = STAGES[n]
    return """# S01E04 — Why Scripts Fail Before You Write Them · %s

Phase: %s

## Inputs
- (fixture: only the fields the walkthroughs read are present)

## Review
- Status: %s
- Latest review: reviews/%s

## Open threads
%s
""" % (name, phase, phase if phase in ("in review", "returned") else "in review", fname.replace(".md", "-review.md"), open_threads)


def review_entry(n, num, score, result, count, items=None):
    fname = STAGES[n][0]
    if items is None:
        items = [
            ("%s, entry 4" % fname, "comprehension: undefined referent", "blocking", -15,
             'Entry 4 refers to "the fix" and nothing in the files says what it is.'),
            ("%s, entry 7" % fname, "comprehension: undefined referent", "significant", -8,
             'Entry 7 mentions "the second client" but no first client appears anywhere.'),
            ("%s, Summary" % fname, "mechanical: W1", "significant", -8, "Summary has no Sources line."),
        ]
    rows = "\n".join("| %d | %s | %s | %s | %d | %s |" % ((i + 1,) + r) for i, r in enumerate(items)) or "| - | (none) | | | 0 | |"
    total = sum(r[3] for r in items)
    score = 100 + total  # always derived from the items, never passed in
    arithmetic = "100 " + " ".join("- %d" % abs(r[3]) for r in items) + " = %d" % score if items else "100"
    return """## Review %d — 2026-09-2%d — %d%%
Result: %s
Consecutive sub-70 reviews: %d

Deductions:
| # | Location | Category | Severity | Points | Item |
|---|---|---|---|---|---|
%s

Arithmetic: %s
""" % (num, num, score, result, count, rows, arithmetic)


def review_log(n, entries):
    return "# %s review log\n\n" % STAGES[n][1] + "\n".join(entries)


def release_entry(n, k):
    return """## Release — 2026-09-25 — by user
Stage: %d. Released after %d consecutive sub-70 reviews.
User's words: "Keep going, send it back to them."
""" % (n, k)


def head_log(extra=""):
    return """# S01E04 — Why Scripts Fail Before You Write Them · Head log

## Kickoff — 2026-09-20
- User's request: "Start S01E04, why scripts fail before you write them."
- Episode: S01E04, "Why Scripts Fail Before You Write Them"
- Tasks: 1 Artist T-101; 2 Architect T-102; 3 Writer T-103; 4 Wizard T-104
- Told the user to start: script-artist
""" + extra


def reopen_entry(k):
    return """
## Reopen — 2026-09-26
- Stage: %d
- Reason: structural change
- Request: "Swap loops 1 and 2." (source: 03-writer.md)
- User's answer: "Yes, reopen the Architect."
- Actions: task set to in progress (Revision 1); boxes unticked; later outputs renamed .stale
""" % k


def put(root, rel, text):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def main(argv):
    root, state = argv[1], argv[2]
    stage = int(argv[argv.index("--stage") + 1]) if "--stage" in argv else 3
    ep = EP
    if state == "kickoff":
        put(root, "series/SERIES.md", series_md(episode=False)); return
    put(root, "series/SERIES.md", series_md(ticked={
        "existing": (), "after-artist": ("Artist",), "structural": ("Artist", "Architect"), "held": ("Artist", "Architect"),
        "mixed": ("Artist",)}.get(state, tuple(BOXES[:stage - 1]))))
    if state == "existing":
        put(root, ep + "/01-artist.md", stage_md(1, phase="dump")); return
    if state in ("after-artist", "mixed", "structural", "held"):
        put(root, ep + "/01-artist.md", stage_md(1))
        put(root, ep + "/reviews/01-artist-review.md", review_log(1, [review_entry(1, 1, 100, "passed", 0, items=[])]))
        put(root, ep + "/head-log.md", head_log())
    if state == "mixed":
        put(root, ep + "/02-architect.md", stage_md(2, phase="returned"))
        put(root, ep + "/reviews/02-architect-review.md", review_log(2, [review_entry(2, 1, 62, "returned", 1)]))
    if state in ("structural", "held"):
        put(root, ep + "/02-architect.md", stage_md(2))
        put(root, ep + "/reviews/02-architect-review.md", review_log(2, [review_entry(2, 1, 100, "passed", 0, items=[])]))
    if state == "structural":
        put(root, ep + "/03-writer.md", stage_md(3, open_threads='- Requested structural change: "Swap loops 1 and 2."'))
    if state == "held":
        put(root, ep + "/03-writer.md", stage_md(3))
        put(root, ep + "/reviews/03-writer-review.md", review_log(3, [
            review_entry(3, 1, 69, "returned", 1), review_entry(3, 2, 69, "returned", 2), review_entry(3, 3, 69, "held for user", 3)]))
    if state.startswith("resume-"):
        case = state[len("resume-"):]
        fname = STAGES[stage][0]
        put(root, ep + "/" + fname, stage_md(stage))
        put(root, ep + "/head-log.md", head_log(reopen_entry(stage) if case == "revision" else ""))
        log = {
            "return": [review_entry(stage, 1, 69, "returned", 1)],
            "release": [review_entry(stage, 1, 69, "returned", 1), review_entry(stage, 2, 69, "returned", 2),
                        review_entry(stage, 3, 69, "held for user", 3), release_entry(stage, 3)],
            "revision": [review_entry(stage, 1, 100, "passed", 0, items=[])],
            "passed": [review_entry(stage, 1, 100, "passed", 0, items=[])],
            "held": [review_entry(stage, 1, 69, "returned", 1), review_entry(stage, 2, 69, "returned", 2),
                     review_entry(stage, 3, 69, "held for user", 3)],
            "none": None,
        }[case]
        if log:
            put(root, ep + "/reviews/" + fname.replace(".md", "-review.md"), review_log(stage, log))
        # earlier stages passed, so the stage's gate check does not stop it
        for n in range(1, stage):
            put(root, ep + "/" + STAGES[n][0], stage_md(n))
        put(root, "series/SERIES.md", series_md(ticked=BOXES[:stage - 1] if case != "passed" else BOXES[:stage]))
    if state == "count-reset":
        put(root, "series/SERIES.md", series_md())
        put(root, ep + "/reviews/01-artist-review.md", review_log(1, [
            review_entry(1, 1, 62, "returned", 1), review_entry(1, 2, 62, "returned", 2), release_entry(1, 2)]))
    print("wrote fixtures for state %r (stage %d) under %s" % (state, stage, root))


if __name__ == "__main__":
    main(sys.argv)
