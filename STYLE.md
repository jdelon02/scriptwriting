---
type: "project-instructions"
title: "STYLE.md"
description: "Project instructions source for scriptwriting: STYLE.md."
tags: ["scriptwriting", "project"]
source_path: "STYLE.md"
---

# STYLE.md

<style_guide project="scriptwriting" format="hybrid-xml-markdown">
  <purpose>
    Keep instruction bundles, templates, docs, and scripts consistent with the
    repo's role as the source of truth for a production agent workflow.
  </purpose>
</style_guide>

## Hybrid XML+Markdown Format

<format>

- Root instruction files use Markdown headings for scanability and XML-style tags to mark durable instruction sections.
- Level-2 sections carry a single wrapping tag (`<rules>`, `<commands>`, `<facts>`, ...); keep tag names snake_case and stable.
- Profile sources in `profiles/<role>/` also use the hybrid format: each level-2 section is pre-wrapped in its heading-derived tag, and each file carries a `<profile_source role="..." file="..." format="hybrid-xml-markdown" />` marker after the H1. The installer's wrapping is idempotent, so pre-wrapped sources stay single-wrapped at install time.
- A pre-wrapped section's tag must exactly match its heading's snake_case tag name (`tag_for` in `scripts/install_profiles.py`, with `Who you are` → `identity` in SOUL files); a mismatched tag gets wrapped again.
- Keep XML tags balanced and outside code fences; the installer's fence-aware splitter depends on clean structure.
- Prefer exact filenames, command names, and role names over vague references.

</format>

## Instruction-Writing Style

<instructions>

- Write rules as observable behavior ("commit and push before the next question"), not aspiration ("be diligent").
- Name the actor for every rule: Head, Reviewer, worker, installer, or user.
- Distinguish evidence from claims: an instruction that accepts a claim ("worker says done") where evidence exists (merged PR) is a bug.
- One concept, one home: define a rule once (usually `WORKFLOW.md`) and reference it from profiles rather than restating it with drift.
- Preserve creator-authorship language verbatim when moving or editing profile text; the guardrails are load-bearing.
- Mark retired material as historical explicitly; never delete acceptance evidence.

</instructions>

## Markdown Style

<markdown>

- Use tables for directories and matrices (agent directory, stage table, transitions) as `WORKFLOW.md` does.
- Keep commands copy-pasteable in fenced `bash` blocks.
- Use backticks for filenames, branch names, statuses (`in_review`), and metadata keys (`original_assignee_id`).
- Keep line lengths comfortable for diff review; wrap prose paragraphs.
- Episode/status vocabulary is fixed: use the exact stage names, statuses, and verdict strings from `WORKFLOW.md`.

</markdown>

## Template Style

<templates>

- Templates in `templates/` use angle-bracket guidance text (`<What the user wants...>`) that must be replaced at use time; keep that convention.
- Template headings and field labels (e.g. `Interview step:`, `Status: approved`) are contract surface — renaming one is a workflow change, not a copy edit.
- Keep stage templates numbered and aligned with the stage table: `01-artist.md` … `04-wizard.md`.

</templates>

## Python Style

<python>

- Scripts live in `scripts/` with entrypoints under `main()` and `if __name__ == '__main__':`.
- Use `pathlib.Path` for file paths and the standard library where sufficient.
- Keep pure text transforms (section splitting, tag wrapping, path rewriting) separate from filesystem helpers, as `install_profiles.py` does.
- Installer behavior is contract: never overwrite an existing `memories/MEMORY.md`, never read or print `.env` content, support `--dry-run`.
- Update `scripts/test_install_profiles.py` alongside any installer behavior change.

</python>

## Documentation and Knowledge Style

<docs>

- Repository Markdown carries OKF frontmatter (`type`, `title`, `description`, `tags`); existing skill metadata is preserved. The bundle root index carries `okf_version: "0.2"`.
- Edit originals in place. `python3 scripts/sync_knowledge.py` copies source documents into `docs/knowledge/repository/`, then indexes and validates the complete bundle. Generated copies are ignored by Git; curated bundle documents remain versioned.
- The Hermes installer removes source metadata from rendered SOUL/AGENTS/STYLE/SKILL instructions and emits the normal Hermes skill metadata.
- Run `okf validate docs/knowledge/` after editing bundle documents; run `python3 scripts/sync_knowledge.py` after changing any repository Markdown.
- Validation evidence belongs in `docs/validation/`; do not mix aspirational design with verified capability there.
- Update `AGENTS.md`, `MEMORY.md`, or `WORKFLOW.md` when behavior changes; stale instruction files are defects.

</docs>

## Change Scope

<change_scope>

- Keep edits tightly related to the requested change; instruction files reward surgical diffs.
- A lifecycle/assignment/PR-rule change must land in `WORKFLOW.md` and all affected profile bundles together.
- Do not reformat or re-wrap files wholesale; noise hides substantive rule changes from review.
- Leave historical files (`templates/head-log.md`, retired rubrics, old logs) untouched unless the task is explicitly about them.
- After committing substantive changes, refresh the graphs: `codegraph sync && code-review-graph update`.

</change_scope>
