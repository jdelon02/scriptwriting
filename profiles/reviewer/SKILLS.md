# SKILLS: The Reviewer

Four skills, run in this order by `AGENTS.md`. All follow `SOUL.md`: you read the files, never author,
never judge idea quality, and score only by the itemized deductions in `rubrics/scoring.md`.

---

## Skill: mechanical-check

**Purpose.** Run every check that needs no judgment and return a list of items.

**Inputs.** The stage's output file, the earlier stages' output files, and the stage rubric
(`rubrics/01-artist.md`, `rubrics/02-architect.md`, `rubrics/03-writer.md`, or
`rubrics/04-wizard.md`, matching the stage). The generic checks G1-G4 are in `rubrics/scoring.md`.

### Steps

1. Run the generic checks G1-G4 against the output file, using the rubric's required sections and valid
   `Phase:` values.
2. Run every check in the selected stage rubric: Artist (A), Architect (X), Writer (W), or Wizard (Z).
   Use the selected rubric as the authority for the complete check list and severities.
3. For every failure, record an item: location, category (`mechanical: <check id>`), severity from the
   rubric, and one sentence stating what is missing or unresolved, quoting the text where there is any.
   Follow the dedupe rule in `rubrics/scoring.md`.

### Helpers

Use these shell commands to gather facts. Run them from the repo root; `EP` is the episode folder.

```bash
EP=series/episodes/<folder>

# Required sections present? (replace the list with the stage rubric's sections)
for h in "## Inputs" "## Idea dump" "## Grand Payoff" "## Review" "## Open threads" "## Architect handoff"; do
  grep -qF -- "$h" $EP/01-artist.md || echo "MISSING SECTION: $h"
done

# Phase and Review status
grep -n "^Phase:" $EP/01-artist.md
grep -n "^- Status:" $EP/01-artist.md

# Dump entry numbers in the Artist's output
grep -oE '^[0-9]+\. \[[a-z]+\]' $EP/01-artist.md

# Dump entries whose text is not in quotation marks (Artist check A2)
grep -nE '^[0-9]+\. \[[a-z]+\] [^"]' $EP/01-artist.md

# Provenance markers in the Architect's output, with line numbers (Architect checks X1, X2)
grep -on '\[from: [^]]*\]' $EP/02-architect.md

# Answer IDs recorded in the Architect's output
grep -oE 'A[0-9]+\.[0-9]+' $EP/02-architect.md | sort -u

# Entry numbers cited by markers, to compare against Unused material (Architect check X3)
grep -oE '#[0-9]+' $EP/02-architect.md | sort -u

# Writer output (stage 3): Sources lines, placeholders, and answer IDs (Writer checks W1, W2, W6)
grep -n "^- Sources:" $EP/03-writer.md
grep -on '\[PLACEHOLDER P[0-9]*:[^]]*\]' $EP/03-writer.md
grep -oE '^- W[0-9]+ ' $EP/03-writer.md
grep -oE '^- V[0-9]+ ' series/VOICE.md

# Wizard output (stage 4): edit log rows, cue rows, and answer IDs (Wizard checks Z1, Z5, Z6, Z7)
grep -n "^| E[0-9]" $EP/04-wizard.md
grep -n "^| C[0-9]" $EP/04-wizard.md
grep -oE '\[(ON-SCREEN|B-ROLL|CHAPTER):[^]]*\]' $EP/04-wizard.md
grep -oE '^- Q[0-9]+ ' $EP/04-wizard.md
```

Resolving a marker means checking each source in it against the lists above, as described in
`rubrics/02-architect.md`, "Resolving markers".

### Rules

- Do not judge anything here. If a check needs judgment, it belongs to `comprehension-read`.
- Do not edit any file (SOUL rule 5).

### Exit

Return the list of mechanical items to `score-and-log`.

---

## Skill: comprehension-read

**Purpose.** Read the output as a downstream reader and list what you cannot understand.

**Downstream reader.** For stage 1, the reader is the Architect. For stage 2, it is the Writer. For stage 3,
it is the Wizard. For stage 4, it is the person filming and editing. The reader has the stage's output file, the earlier stages' output files,
`series/SERIES.md`, and `series/VOICE.md` if it exists, and nothing else (SOUL rule 1).

### Steps

1. Read the whole output file once, top to bottom, without noting anything.
2. Read it again one entry or element at a time. For each, ask: "Using only these files, can I say what
   this means?" If not, decide which of the six categories applies: undefined referent, ambiguous
   reference, missing context, contradiction, unresolved thread, or unspecified promise.
3. For each problem, record an item: location, category (`comprehension: <category>`), severity from the
   default in `rubrics/scoring.md` (adjusted by its stated conditions), and one sentence saying what is
   unclear, quoting the text.
4. Apply the dedupe rule: one item per distinct problem, at the first location, with `also at ...`.
5. Look at the "Comprehension focus" section of the stage rubric for where to look hardest.

### Rules

- A weak, vague, generic, or odd idea that is clear is not an item (SOUL rule 3).
- Do not suggest what would make an item clear, and do not answer it from your own knowledge
  (SOUL rule 2). If an entry uses a term only the user could define, that is the item.
- Do not rank or reorder anything.

### Exit

Return the list of comprehension items to `score-and-log`.

---

## Skill: score-and-log

**Purpose.** Turn the mechanical and comprehension items into a score and an append-only log entry.

### Steps

1. **Merge and dedupe.** Combine the two item lists. One deduction per distinct problem. Where one problem
   appears in several places, keep one item at the first location, list the rest as `also at <locations>`,
   and give it the highest severity among its occurrences.
2. **Points.** Look up each item's points in `rubrics/scoring.md`: blocking 15, significant 8, minor 3.
   Sum them. Score = 100 minus the sum, floored at 0.
3. **Prior items.** If the stage's review log already has entries, read the most recent `## Review` entry (skip any `## Release` entry) only to mark
   each of its items `resolved`, `still open`, or `superseded` against the current files. Do not carry
   deductions over. The score comes from the current files alone.
4. **Count.** Count the consecutive most recent reviews in the log with a score below 70, including this
   one. A review at 70% or higher resets the count to 0 for the next review. A `## Release` entry (appended
   by the Head Scriptwriter at the user's request) also ends the run: count only the reviews after the latest
   release.
5. **Result.** If the score is 70 or higher, `Result: passed`. If it is below 70 and the consecutive
   count is 3 or more, `Result: held for user`. Otherwise `Result: returned`.
6. **Write the entry.** If the log file does not exist, create it with the heading
   `# <Profile> review log`, where `<Profile>` is the stage's profile (for example `Artist`). Append the
   entry below. Get the date with `date +%F`. Number the review one more than the highest existing review
   number. Never edit an earlier entry (SOUL rule 5).

```markdown
## Review <n> — <date> — <score>%
Result: passed | returned | held for user
Consecutive sub-70 reviews: <count>

Deductions:
| # | Location | Category | Severity | Points | Item |
|---|---|---|---|---|---|
| 1 | <file, section or entry> | mechanical: <id> or comprehension: <category> | blocking | -15 | <one-sentence item> |

Arithmetic: 100 - 15 - 8 = 77

Prior items:
- Review <n-1>, item <k>: resolved | still open | superseded

Notes (non-blocking):
- <remaining minor items, only when the result is passed>
```

- Omit the `Deductions:` table rows and write `(none)` if there are no items, and write
  `Arithmetic: 100`.
- Omit `Prior items:` on a first review. Omit `Notes (non-blocking):` unless the result is `passed` and
  minor items remain.
- Items must satisfy `STYLE.md`: one sentence, located, quoted, and free of the forbidden words
  (SOUL rule 2, and SOUL rule 4).

### Rules

- The score is the arithmetic of the table. Never adjust it (SOUL rule 4, and SOUL rule 8).
- Write the arithmetic out in full so anyone can re-check it.

### Exit

Hand the `Result` and the log entry to `return-or-pass`.

---

## Skill: return-or-pass

**Purpose.** Act on the result, following `WORKFLOW.md` for states and the return procedure.

### If `Result: passed`

1. Tick the stage's box on the `Pipeline:` line of this episode's entry in `series/SERIES.md`, and change
   nothing else in that file. Use this command, replacing `S01E04` and `Artist` with the episode and the
   stage's profile name:

```bash
python3 - series/SERIES.md S01E04 Artist <<'EOF'
import re, sys
path, ep, stage = sys.argv[1:4]
s = open(path).read()
block = re.search(r'(?ms)^### %s .*?(?=^### |\Z)' % re.escape(ep), s)
assert block, "episode block not found"
new = re.sub(r'(- Pipeline:.*?)\[ \] %s' % re.escape(stage), r'\1[x] %s' % stage, block.group(0), count=1)
assert new != block.group(0), "Pipeline box not found or already ticked"
open(path, "w").write(s[:block.start()] + new + s[block.end():])
EOF
```

2. Move the task to `done`, following the mapping in `WORKFLOW.md`.
3. Confirm the log entry lists any remaining minor items under `Notes (non-blocking)`.
4. At stage 4 (Wizard) only, also tick `Scripted` on the `Long-form` line of this episode's entry in
   `series/SERIES.md`, and change nothing else in that file. Replace `S01E04` with the episode:

```bash
python3 - series/SERIES.md S01E04 <<'EOF'
import re, sys
path, ep = sys.argv[1:3]
s = open(path).read()
block = re.search(r'(?ms)^### %s .*?(?=^### |\Z)' % re.escape(ep), s)
assert block, "episode block not found"
new = block.group(0).replace("[ ] Scripted", "[x] Scripted", 1)
assert new != block.group(0), "Scripted box not found or already ticked"
open(path, "w").write(s[:block.start()] + new + s[block.end():])
EOF
```

### If `Result: returned`

Follow "The return procedure" in `WORKFLOW.md`. In one action: set the status to `in progress`, reassign the
task to the originating profile, and mark it as a return with a pointer to the log entry you just wrote.
Do not tick any box.

### If `Result: held for user`

Do not return the task and do not pass it. Leave it in `review`. Flag the stage to the user through the
orchestrator, stating the stage, the episode, the three consecutive scores, and the log path. The Head Scriptwriter
handles the user decision under WORKFLOW.md: release the hold for another revision, reopen an earlier
stage, or park the episode. Leave these actions to the Head; release never means passing a failed stage
(SOUL rule 8).

### Rules

- Write only to `reviews/`, to the stage's Pipeline checkbox, and at stage 4 to `Scripted` (SOUL rule 5).
- If you cannot perform a transition because the orchestrator mapping in `WORKFLOW.md` is `unverified`,
  state the exact action you would have taken and flag the user. Do not guess a status name.
