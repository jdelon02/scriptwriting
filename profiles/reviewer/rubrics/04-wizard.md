> SUPERSEDED — historical reference only. No active profile loads this rubric.
> Review the issue Doneness and actual PR under WORKFLOW.md; do not calculate scores.

# Rubric: Stage 4, Wizard

Output file: `series/episodes/<id>/04-wizard.md`. Review log: `reviews/04-wizard-review.md`. Earlier stages:
`03-writer.md`, `02-architect.md`, and `01-artist.md`. Also readable: `series/VOICE.md`, to resolve `V<n>`
sources.

Severities, constants, the generic checks (G1-G4), the comprehension categories, and the dedupe rule are in
`scoring.md`. This file adds what is specific to the Wizard's output.

When stage 4 passes, tick the `Wizard` box on the `Pipeline:` line **and** the `Scripted` box on the
episode's `Long-form` line (see `SKILLS.md`, skill `return-or-pass`).

## Required sections

Used by check G1. One item per missing section.

- `## Inputs`
- `## Final script`
- `## Edit log`
- `## Cues`
- `## Placeholders`
- `## Wizard answers`
- `## Review`
- `## Open threads`
- `## Final handoff`

## Final script subsections

Also used by check G1, but each missing subsection is **blocking**. Inside `## Final script`:

- `### Hook`
- `### Introduction`
- `### Summary`
- `### Call to action`
- a `### Loop <n>` section for every loop in the skeleton (`02-architect.md`, `## Loops`)

## Valid Phase values

Used by check G2.

`intake | simplify | gap-check | read-aloud | cues | final-check | in review | returned`

At submission, `Phase:` is `in review` and the `## Review` section's `Status:` is `in review`.

## Resolving cue sources

Each row in `## Cues` has an Origin and a `Sources or approval` cell.

- **`user-sourced`:** every source in the cell must resolve. `#N` resolves if entry N exists under
  `## Idea dump` in `01-artist.md`. `A<loop>.<n>` resolves if that ID is in `02-architect.md`. `V<n>` resolves
  if `series/VOICE.md` has it. `W<n>` resolves if `03-writer.md` has it under `## Writer answers`. A skeleton
  ID such as `L1.payoff` resolves if `02-architect.md` has that element. `Q<n>` resolves if `04-wizard.md`
  has it under `## Wizard answers`.
- **`wizard-suggested`:** the cell must read `approval: Q<n>`, and `Q<n>` must exist under
  `## Wizard answers`.

A cue whose sources or approval do not resolve counts as **one** item for that cue, not one per source.

Cue types are `CHAPTER`, `ON-SCREEN`, and `B-ROLL`. Inline cue markers have the forms
`[CHAPTER: <title> | C<n>]`, `[ON-SCREEN: <text> | C<n>]`, and `[B-ROLL: <note> | C<n>]`. Each marker must
match a row in `## Cues` with the same ID (check Z5).

## Checking integrity (Z2, Z3)

Run the integrity helper in `SKILLS.md` (skill `mechanical-check`, Wizard helpers). It prints every labeled
text line that differs between `03-writer.md` and `## Final script` (cue markers removed), and checks each
approved edit's before and after text.

## Mechanical checks

| ID | Check | Severity |
|---|---|---|
| Z1 | Every `## Edit log` row has an ID, section, type (`jargon`, `sentence`, `gap-timing`, `conversational`, or `placeholder`), before text, after text, reason, and status (`approved` or `rejected`). One item per row with a missing or invalid part. | Significant |
| Z2 | **Unlogged change.** After removing inline cue markers, each labeled text line in `## Final script` matches the corresponding line in `03-writer.md`, unless an `approved` edit accounts for the difference. One item per line that differs without one. | Blocking |
| Z3 | **Phantom edit.** Each `approved` edit's before text appears verbatim in `03-writer.md` in the named section, and its after text appears in the final script. One item per edit that fails either. | Blocking |
| Z4 | The set of sections and the order of loops in `## Final script` match `03-writer.md`. One item per mismatch. | Blocking |
| Z5 | Every cue is `user-sourced` with `Sources` that resolve, or `wizard-suggested` with an `approval: Q<n>` that resolves (see above). Missing or unresolved: one item per cue. Every inline cue marker has a row in `## Cues` and every row has a marker: one item per mismatch. | Significant for a cue's sources or approval. Minor for a marker mismatch. |
| Z6 | A `CHAPTER` cue exists for every loop in the skeleton. One item per loop without one. | Significant |
| Z7 | A `wizard-suggested` cue whose text contains a digit or a `%` sign. One item per cue: it may be a new claim. | Blocking |
| Z8 | Hook sentences in the final script have fewer than ten words. A sentence of ten or more is minor; report one item listing all of them. | Minor |
| Z9 | No section in `## Final script` has `Status: draft`. Each is `approved` or `open`. A `draft` section is one item. An `open` section is itself one item, because its content is incomplete. | Significant |
| Z10 | Every inline `[PLACEHOLDER P<n>: ...]` appears in `## Placeholders` and every listed placeholder appears inline: one minor item per mismatch. Each remaining `open` placeholder is an item: blocking in the Hook or in a loop's Payoff, significant elsewhere. Each open placeholder must also appear in `## Open threads`: one minor item if not. | Blocking, significant, or minor |

The generic checks G1-G4 also apply. G3 applies to `## Final handoff`.

## Comprehension focus

Read as the person filming and editing, who has `04-wizard.md`, the earlier stages' files, and
`series/VOICE.md`. Look hardest at:

- Cues that do not say what to show ("show the chart" with no chart identified).
- On-screen text that refers to nothing in the script ("the three" with no three named).
- B-roll notes with undefined referents ("the footage" with no footage identified).
- A script line that lost the meaning it needed after an edit, for example a cut that removed the antecedent
  of a later pronoun.
- Contradictions between a cue and the script.

A conversational cut, a short sentence, or a cue you would not have chosen is not an item if it is clear.
Never judge cue quality, and never rank, reorder, or rewrite anything.
