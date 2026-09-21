# Rubric: Stage 1, Artist

Output file: `series/episodes/<id>/01-artist.md`. Review log: `reviews/01-artist-review.md`.

Severities, constants, the generic checks (G1-G4), the comprehension categories, and the dedupe rule are
in `scoring.md`. This file adds what is specific to the Artist's output.

## Required sections

Used by check G1. One item per missing section.

- `## Inputs`
- `## Idea dump`
- `## Grand Payoff`
- `## Review`
- `## Open threads`
- `## Architect handoff`

## Valid Phase values

Used by check G2.

`intake | dump | payoff | in review | returned`

At submission, `Phase:` is `in review` and the `## Review` section's `Status:` is `in review`.

## Mechanical checks

| ID | Check | Severity |
|---|---|---|
| A1 | `## Inputs` has `Title`, `Story spine`, and `Audience`, each either verbatim or `not provided`. One item per missing field. | Significant |
| A2 | Each dump entry is numbered sequentially, has a `[lens]` tag from the allowed list (`points`, `examples`, `anecdotes`, `visuals`, `surprises`, `mistakes`, `numbers`, `objections`, `misconceptions`, `hindsight`), and its text is in quotation marks. A missing number or missing quotation marks is significant. A missing or unlisted lens tag is minor. One item per entry. | Significant or minor |
| A3 | `## Grand Payoff` has a `Chosen` payoff and a `Why it justifies the click` rationale. One item per missing part. | Blocking |
| A4 | `## Grand Payoff` has a `Title test` that is either the user's answer or `skipped` with a reason. | Significant |
| A5 | Every entry number in `Candidates nominated` exists in `## Idea dump`, and at most three are listed. | Minor |
| A6 | Every input recorded as `not provided` appears in `## Open threads`. One item per missing mention. | Minor |

The generic checks G1-G4 also apply. G3 applies to `## Architect handoff`.

## Comprehension focus

Read as the Architect, who will build a skeleton from this file. Look hardest at:

- Each dump entry: can you say what it means without the conversation?
- The Grand Payoff `Chosen` and its rationale: is the outcome the viewer gets stated, or only implied?
- `## Open threads`: does any entry depend on a thread that nothing resolves?
- `## Inputs`: are the title and spine, where given, understandable on their own?

A weak or generic idea that is clear costs nothing (see `scoring.md`, "Not items").
