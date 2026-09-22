> SUPERSEDED — historical reference only. No active profile loads this rubric.
> Review the issue Doneness and actual PR under WORKFLOW.md; do not calculate scores.

# Rubric: Stage 3, Writer

Output file: `series/episodes/<id>/03-writer.md`. Review log: `reviews/03-writer-review.md`. Earlier stages: `01-artist.md` and `02-architect.md`. Also readable: `series/VOICE.md`, to resolve `V<n>` sources.

Severities, constants, the generic checks (G1-G4), the comprehension categories, and the dedupe rule are in `scoring.md`. This file adds what is specific to the Writer's output.

## Required sections

Used by check G1. One item per missing section.

- `## Inputs`
- `## Draft`
- `## Placeholders`
- `## Skeleton coverage`
- `## Writer answers`
- `## Review`
- `## Open threads`
- `## Wizard handoff`

## Draft subsections

Also used by check G1, but each missing subsection is **blocking**. Inside `## Draft`:

- `### Hook`
- `### Introduction`
- `### Summary`
- `### Call to action`
- a `### Loop <n>` section for every loop in the skeleton (`02-architect.md`, `## Loops`)

## Valid Phase values

Used by check G2.

`intake | voice | body | frame | hook | completeness | in review | returned`

At submission, `Phase:` is `in review` and the `## Review` section's `Status:` is `in review`.

## Resolving sources

Each drafted section ends with a `Sources:` line. Every source in it must resolve:

- `L<n>.payoff`, `L<n>.setup`, `L<n>.tension` resolve if `### Loop <n>` in `02-architect.md` has a
  `- Payoff:`, `- Setup:`, or `- Tension:` line.
- `T<a>-<b>` resolves if `## Sequence` in `02-architect.md` has a transition `Loop <a> to Loop <b>`.
- `REHOOK` resolves if `## Sequence` has a `Mid-video re-hook:` line.
- `INTRO.promise` and `INTRO.roadmap` resolve if `### Introduction` under `## Framing` has a `- Promise:` or
  `- Roadmap` line. `SUMMARY` resolves if `### Summary` has a `- Takeaways` line. `CTA.link`, `CTA.gap`, and
  `CTA.promise` resolve if `### Call to action` has a `- Link`, `- Curiosity gap`, or `- Promise` line.
- `#N` resolves if entry N exists under `## Idea dump` in `01-artist.md`.
- `A<loop>.<n>` resolves if the `Answers:` list of Loop `<loop>` in `02-architect.md` has that ID.
- `V<n>` resolves if `series/VOICE.md` has a `V<n>` entry under `## In my own words`.
- `W<n>` resolves if `## Writer answers` in `03-writer.md` has that ID.

A section with any source that does not resolve counts as **one** item for that section, not one per source.

## Mechanical checks

| ID | Check | Severity |
|---|---|---|
| W1 | Each drafted section (Hook, Introduction, each Loop, each Transition, the Re-hook, Summary, Call to action) has a `Sources:` line. One item per section without one. | Significant |
| W2 | Every source resolves (see above). Unresolved on the Hook or a Loop section: blocking. Unresolved elsewhere: significant. One item per section. | Blocking or significant |
| W3 | Every skeleton element (each loop's setup, tension, and payoff; each transition; the re-hook; the intro promise and roadmap; the summary takeaways; each CTA part) appears in `## Skeleton coverage` as `drafted` or as `not used` with a reason. One item per element that does not. | Significant |
| W4 | Loops appear in the skeleton's `Order`, each transition sits between the two loops it joins, and the re-hook follows the loop the skeleton names. One item per mismatch. | Significant |
| W5 | No section has `Status: draft`. Each is `approved` or `open`. A `draft` section is one item. An `open` section is itself one item, because its content is incomplete. | Significant |
| W6 | Every inline `[PLACEHOLDER P<n>: ...]` appears in `## Placeholders`, and every listed placeholder appears inline: one minor item per mismatch. Each remaining `open` placeholder is an item: blocking in the Hook or in a loop's Payoff, significant elsewhere. Each open placeholder must also appear in `## Open threads`: one minor item if not. | Blocking, significant, or minor |
| W7 | The Hook has all three labeled parts: `Context lean-in`, `Scroll stop`, `Contrarian snapback`. A missing part is significant. A hook sentence with ten or more words is minor; report one item that lists all such sentences (the article says to keep them under ten words: fewer than ten words). | Significant or minor |
| W8 | The Introduction has `Validating language`, `Problem`, `Promise`, `Credibility`, and `Roadmap`. The Call to action has `Link`, `Curiosity gap`, and `Promise`. A missing labeled line is significant. More than one call to action is minor. | Significant or minor |

The generic checks G1-G4 also apply. G3 applies to `## Wizard handoff`.

## Comprehension focus

Read as the Wizard, who will edit this script and has `03-writer.md`, the earlier stages' files, and
`series/VOICE.md`. Look hardest at:

- Undefined referents inside the prose: a term, person, or event the files do not explain.
- A promise in the Introduction or the Call to action that does not say what the viewer will get.
- Contradictions between sections, for example the Promise and the payoffs.
- Text such as "as I said earlier" that refers to nothing in the draft.
- Text that depends on a placeholder to make sense.

A clumsy, wordy, or unpolished sentence that is clear is not an item. Polish is the Wizard's job (see
`scoring.md`, "Not items"). Never rank, reorder, or rewrite anything.
