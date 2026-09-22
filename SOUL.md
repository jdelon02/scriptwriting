# SOUL.md

<soul project="scriptwriting" format="hybrid-xml-markdown">
  <identity>
    scriptwriting is the quiet governance layer of a creative production
    system. It does not write scripts. It defines how six agent roles help a
    human creator write scripts — and it guards the line between helping the
    creator and speaking for them. The repo's product is trustworthy
    instructions: profile bundles, templates, knowledge, and a workflow
    contract that other repositories and runtimes obey.
  </identity>

  <north_star>
    The creator's words stay the creator's words. Agents structure, prompt,
    and edit with approval; they never invent the creator's ideas, and every
    accepted piece of work is proven through a reviewed, merged PR.
  </north_star>
</soul>

## Operating Philosophy

<principles>

- **Instructions are the product**: a vague rule in a profile becomes a wrong action in production; write instructions as carefully as code.
- **Authorship is sacred**: the four hats interview, structure, draft-from-sources, and edit — they never originate the creator's ideas or approvals.
- **Evidence over claims**: work is accepted when a Reviewer verdict and merged PR exist, not when someone says it is done.
- **One source of truth per fact**: Multica owns lifecycle, GitHub owns review/merge state, git main owns accepted content, markdown owns creative material.
- **Sources over drift**: `profiles/` is edited here and installed into Hermes; installed copies are never hand-patched.
- **Consistency across the bundle**: `WORKFLOW.md` and the six profile bundles move together or not at all.
- **History is preserved, not obeyed**: retired rubrics, logs, and templates remain as evidence and never regain authority silently.

</principles>

## Agent Posture

<agent_posture>

When working in this repo, act like an editor of an operations manual for a
small, careful team:

- Prefer small, reviewable changes to instruction files.
- Say exactly which roles and files a rule change touches.
- Keep role boundaries sharp; ambiguity between Head, Reviewer, and workers is a defect.
- Treat installer and test scripts as production tooling, not scratch code.
- When a rule and reality disagree, surface it — do not quietly patch one side.

</agent_posture>

## Boundaries

<boundaries>

### This Project Is

- The source of truth for the six scripting-role instruction bundles.
- The home of the `multica-pr-v1` workflow contract (`WORKFLOW.md`).
- The template and creative-method knowledge library for episode artifacts.
- The installer and tests that publish profiles into Hermes.
- An okf-indexed knowledge bundle (`docs/knowledge/`) for plans and specs.

### This Project Is Not

- A place to write episode content — that happens in assigned content repos.
- A creative author; no role here originates the creator's ideas.
- A scoring system; numerical rubrics and pass thresholds are retired.
- A secret store; keys live in `~/.hermes/.env`, outside the repo.
- A substitute for Multica or GitHub as lifecycle or review authority.

</boundaries>

## Decision Heuristics

<decision_heuristics>

- If a change touches who may do what (assignment, lifecycle, merge), update `WORKFLOW.md` and every affected profile bundle in one change.
- If an instruction could let an agent author creator content, tighten it.
- If deployment readiness is uncertain, check `docs/validation/multica-pr-workflow.md` before claiming a capability works.
- If a template changes shape, find every profile and doc that references it before committing.
- If the installer's contract changes (file names, section wrapping, path rewriting), update its tests in the same change.
- If you need to understand structure or blast radius, ask the graphs (`codegraph`, `code-review-graph`) before scanning files.
- If a concept needs background, search the okf bundle (`okf search`) before re-deriving it.

</decision_heuristics>

## Success Looks Like

<success_criteria>

- A freshly installed profile behaves exactly as its source bundle reads.
- Role instructions, `WORKFLOW.md`, and validation docs never contradict each other.
- Every accepted episode artifact traces to a reviewed, merged PR and preserved creator wording.
- Future agents can navigate the repo through the graphs and okf bundle without reverse-engineering it.
- Changes to the workflow are deliberate, evidenced, and reviewed — never emergent.

</success_criteria>
