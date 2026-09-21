# Scoring

How every review is scored, for every stage. The pass threshold (70%) and the return procedure are
defined in `WORKFLOW.md`. Do not restate or change them here.

## Formula

Score = 100% minus the sum of the deductions for the items you found, floored at 0%.

Every deduction is a named item. Never adjust a score by feel, and never round to pass or to fail.

## Severities and constants

These constants are defined here and nowhere else.

```
BLOCKING = 15
SIGNIFICANT = 8
MINOR = 3
```

| Severity | Deduction | Meaning |
|---|---|---|
| Blocking | 15 | A downstream reader could not proceed or would likely misread. Examples: a missing required section; an unresolved provenance marker on a payoff, setup, or tension; a contradiction between entries; a central term used without any explanation. |
| Significant | 8 | Understandable only by guessing. Examples: an ambiguous reference; missing detail a claim depends on; an entry that relies on the conversation. |
| Minor | 3 | A small clarity issue that does not impede understanding. |

**Central** means the entry's or element's main claim cannot be understood without the thing in question.

## Rules

1. **One deduction per distinct problem.** If the same problem appears in several places (the same
   undefined term used in four entries), record one item at the first location and list the others as
   `also at <locations>`. The item takes the highest severity among its occurrences.
2. **Every item cites its location and quotes the text.** No unlocated deductions. A location is a file
   name plus a section, entry number, or loop.
3. **Category and severity come from the rubrics.** Use the stage rubric's check IDs and the categories
   below. Do not invent categories.
4. **Mechanical failures are items like any other.**
5. **Write the arithmetic out** in the log, so anyone can re-check it.
6. **Items the rubrics do not list are not items.** See "Not items".

## Generic mechanical checks

Apply to every stage. The stage rubric lists the required sections and valid `Phase:` values.

| ID | Check | Severity |
|---|---|---|
| G1 | Every required section from the stage rubric is present. One item per missing section. | Blocking |
| G2 | `Phase:` is one of the stage's valid values, and agrees with the `## Review` section. At submission, `Phase:` is `in review` and the Review `Status:` is `in review`. | Significant |
| G3 | The handoff block is present and not empty. | Blocking |
| G4 | Elements follow the stage's format. A missing entry number or missing quotation marks is significant. Any other format slip is minor. | Significant or minor |

## Comprehension categories

Use only these six. Read as a downstream reader with the pipeline files, not the conversation.

| Category | Meaning | Default severity |
|---|---|---|
| undefined referent | A term, person, or event used without an explanation the files can resolve. | Significant. Blocking if central. |
| ambiguous reference | A pronoun or phrase ("it", "that") with more than one plausible meaning. | Significant. Minor if the surrounding text makes one meaning clearly the most likely. |
| missing context | An entry that only makes sense with the conversation. | Significant. Blocking if the element cannot be used downstream without it. |
| contradiction | Two statements that cannot both hold. | Blocking |
| unresolved thread | An item in Open threads that an entry depends on and nothing resolves. | Significant if an entry depends on it. Minor otherwise. |
| unspecified promise | A payoff, promise, or rationale that names an outcome without saying what it is ("they'll get it"). | Blocking in the Grand Payoff rationale or an Architect payoff. Significant elsewhere. |

## Not items

Do not deduct for any of these. They are not comprehension defects.

- A weak, vague, generic, or off-topic idea that is nonetheless clear.
- Opinions about ordering, ranking, or which point is stronger.
- Wording style, length, or tone.
- Anything the rubrics do not list.

## Worked example

Items found on a stage:

| # | Severity | Points |
|---|---|---|
| 1 | Blocking | -15 |
| 2 | Blocking | -15 |
| 3 | Significant | -8 |

Arithmetic: 100 - 15 - 15 - 8 = 62. That is below 70%, so the task is returned (see `WORKFLOW.md`).

With one blocking, one significant, and one minor item: 100 - 15 - 8 - 3 = 74. That passes, and the minor
item is listed as a note for the next stage.
