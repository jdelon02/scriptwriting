---
name: scriptwriting
description: Use when working in the scriptwriting profile-source repo — editing the six role instruction bundles, templates, knowledge, WORKFLOW.md, the okf docs bundle, or the Hermes profile installer and its tests.
---

# Scriptwriting Repo Skill

<skill name="scriptwriting" format="hybrid-xml-markdown">
  <purpose>
    Guide agents through safe, consistent work on the scriptwriting
    profile-source repository without breaking the production workflow it
    governs.
  </purpose>
</skill>

## When To Use

<triggers>

Use this skill when the task involves:

- Editing any `profiles/<role>/` bundle (`AGENTS.md`, `SOUL.md`, `STYLE.md`, `SKILLS.md`, `MEMORY.md`).
- Changing `WORKFLOW.md` or the lifecycle/assignment/PR rules it defines.
- Adding or modifying `templates/` or `knowledge/` material.
- Updating the okf bundle under `docs/knowledge/` or validation docs under `docs/validation/`.
- Changing `scripts/install_profiles.py`, `scripts/profiles.json`, or their tests.
- Installing or refreshing Hermes profiles from this repo.

Do NOT use this skill for episode content work; that follows `WORKFLOW.md` in the assigned content repository.

</triggers>

## Required Context

<context_checklist>

1. Read `AGENTS.md` for the command center and repo map.
2. Read `SOUL.md` for project judgment and boundaries.
3. Read `STYLE.md` before editing instruction files, templates, or scripts.
4. Read `MEMORY.md` for durable project facts.
5. For workflow-touching changes, read the relevant sections of `WORKFLOW.md`.
6. Use the graphs before file scanning: `code-review-graph` for blast radius, `codegraph_explore` (or `codegraph explore "..."`) for symbol-level questions in `scripts/`.
7. Use `okf search` / `okf show` against `docs/knowledge/` before re-deriving plan or spec context.

</context_checklist>

## Workflow Map

<workflow>

Typical change cycle:

```bash
# 1. Understand scope
codegraph explore "<symbol or question>"        # or codegraph_explore MCP tool
# code-review-graph: get_impact_radius_tool / get_architecture_overview_tool

# 2. Edit sources (profiles/, templates/, WORKFLOW.md, docs/, scripts/)

# 3. Validate
okf validate docs/                               # if docs/specs changed
python3 scripts/test_install_profiles.py         # if installer/bundles changed
python3 scripts/test_head_fixtures.py            # if Head fixtures changed

# 4. Install and spot-check (when profile bundles changed)
python3 scripts/install_profiles.py --dry-run
python3 scripts/install_profiles.py

# 5. Commit, then refresh indexes
codegraph sync && code-review-graph update
okf index docs/knowledge/                        # if bundle docs were added/moved
```

</workflow>

## Safety Pattern

<safety_pattern>

- Edit sources here; never hand-patch `~/.hermes/profiles/`.
- Keep the five-file bundle shape per role; the installer requires it.
- Preview with `--dry-run` before installing profiles.
- Never touch `~/.hermes/.env` or print its contents; the installer symlinks it.
- Never let a change split `WORKFLOW.md` and the profile bundles into disagreement.
- Preserve historical/retired material; mark it historical instead of deleting it.
- Keep runtime artifacts (`.codegraph/`, `.code-review-graph/`, `.kilo/`) out of commits.

</safety_pattern>

## Implementation Guidance

<implementation_guidance>

### Profile Bundles

- Match the role's voice and rule structure already in the bundle.
- Keep role boundaries explicit: workers never create issues, poll the board, or dispatch; Reviewer owns verdicts and merges; Head owns orchestration.
- Reference `WORKFLOW.md` for shared rules instead of restating them.
- Remember the installer renames `SKILLS.md` → `SKILL.md` and rewrites `profiles/<role>/` paths to profile homes; write source paths, not installed paths.

### WORKFLOW.md

- It is the single workflow authority. Changes here usually fan out to several bundles — use `code-review-graph` impact tools to find them.
- Keep the agent directory table (names, UUIDs, Hermes profiles) exact; UUIDs are used for assignment, names for user-facing text.
- Doneness rules, verdict comment formats, and metadata keys are contract; change them only deliberately and everywhere at once.

### Templates and Knowledge

- Field labels and headings in `templates/` are consumed by profiles; grep/graph for consumers before renaming anything.
- Creative-method sources in `knowledge/` inform the hats; keep them separate from operational rules.

### Installer and Tests

- Pure transforms (`split_sections`, `wrap_sections`, `rewrite_text`, `retitle`) should stay pure and tested.
- Never overwrite an existing installed `memories/MEMORY.md`.
- Any new installer flag or behavior gets a test in `scripts/test_install_profiles.py`.

</implementation_guidance>

## Verification

<verification>

Choose the lightest verification that proves the work:

- Instruction/doc-only changes: re-read the edited sections and confirm no contradiction with `WORKFLOW.md`; run `okf validate docs/` when the bundle changed.
- Installer/script changes: run `python3 scripts/test_install_profiles.py` (and `e2e_install_test.py` for end-to-end behavior).
- Profile bundle changes: `python3 scripts/install_profiles.py --dry-run`, then install and inspect one converted file in `~/.hermes/profiles/`.
- Workflow-rule changes: walk one affected transition in `WORKFLOW.md` end to end and confirm each named actor's bundle agrees.

</verification>

## Common Gotchas

<gotchas>

- Root `SKILL.md` (this file) is repo-level; role skills are `profiles/<role>/SKILLS.md` — plural in source, singular after install.
- Profile sources are pre-wrapped hybrid xml+markdown; the installer's `wrap_sections` is idempotent, but only when a section's tag exactly matches its heading-derived name (`tag_for`; `Who you are` → `identity` in SOUL files). A renamed heading with a stale tag will double-wrap.
- `Status: approved` in episode artifacts means creator wording approval, never issue completion — do not blur this when editing instructions.
- `PeeWee (Architect)` in the Multica workspace is not the scripting Architect; never rely on fuzzy name matching in examples or instructions.
- `docs/knowledge/` (okf bundle) and `knowledge/` (creative sources) are different trees with different rules.
- Nested worktrees may exist under `profiles/.kilo/`; exclude them from searches and never edit through them.

</gotchas>
