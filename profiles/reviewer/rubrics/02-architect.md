# Rubric: Stage 2, Architect

Output file: `series/episodes/<id>/02-architect.md`. Review log: `reviews/02-architect-review.md`. Earlier
stage: `01-artist.md`, needed to resolve provenance markers.

Severities, constants, the generic checks (G1-G4), the comprehension categories, and the dedupe rule are
in `scoring.md`. This file adds what is specific to the Architect's output.

## Required sections

Used by check G1. One item per missing section.

- `## Inputs`
- `## Loops`
- `## Sequence`
- `## Framing`
- `## Viewer-question coverage`
- `## Unused material`
- `## Review`
- `## Open threads`
- `## Writer handoff`

## Valid Phase values

Used by check G2.

`intake | inputs | payoffs | setups | tension | sequence | framing | flow-check | in review | returned`

At submission, `Phase:` is `in review` and the `## Review` section's `Status:` is `in review`.

## Resolving markers

Architect elements end with a provenance marker such as `[from: #7, A1.1]`. Each source inside it must
resolve:

- `#N` resolves if entry number N exists under `## Idea dump` in `01-artist.md`.
- `A<loop>.<n>` (for example `A2.3`) resolves if the `Answers:` list of Loop `<loop>` in `02-architect.md`
  contains an item with that ID.

An element with a marker whose sources do not all resolve counts as **one** item for that element, not one
per source.

## Mechanical checks

| ID | Check | Severity |
|---|---|---|
| X1 | Every payoff, setup, and tension in `## Loops` has a `[from: ...]` marker. Missing on a payoff, setup, or tension: blocking. Missing on a transition or a framing element: significant. One item per element. | Blocking or significant |
| X2 | Every marker resolves (see above). Unresolved on a payoff, setup, or tension: blocking. Unresolved on a transition or a framing element: significant. One item per element. | Blocking or significant |
| X3 | Every entry in `01-artist.md` `## Idea dump` is either cited by a marker somewhere in `02-architect.md` or listed under `## Unused material`. One item per entry that is neither. | Significant |
| X4 | No loop has `Status: draft`. Each loop is `approved` or `open`. A `draft` loop is one item. Each `open` loop must also appear in `## Open threads` (one item if it does not), and an `open` loop is itself one item, because its missing content cannot be used downstream. | Significant |
| X5 | `Order` in `## Sequence` lists every loop exactly once. Otherwise one item. `User's ranking notes` present: if missing, one item. | Significant for order. Minor for ranking notes. |
| X6 | `## Sequence` records a mid-video re-hook position. | Significant |
| X7 | `## Framing` is complete: an introduction `Promise`; a `Roadmap` of 3-5 topics; `Takeaways` numbering 3-5; a call to action with `Link`, `Curiosity gap`, and `Promise`. A missing part is significant. A count outside the range, or more than one call to action, is minor. One item per problem. | Significant or minor |
| X8 | Every viewer question listed in `## Inputs` appears in `## Viewer-question coverage`. One item per question that does not. | Significant |

The generic checks G1-G4 also apply. G3 applies to `## Writer handoff`.

## Comprehension focus

Read as the Writer, who will draft from this file and `01-artist.md`. Look hardest at:

- Each payoff, setup, and tension: can you say what it means using the two files alone?
- Transitions: do they refer to content that exists in the two loops they join?
- Framing: does the promise name what the viewer will get, or only that they will "get it"?
- `## Open threads` and `open` loops: does anything depend on a thread nothing resolves?

A weak idea, an unusual ordering, or a loop you would rank differently costs nothing (see `scoring.md`,
"Not items"). Never rank or reorder loops.
