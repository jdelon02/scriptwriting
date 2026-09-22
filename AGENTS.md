# Agent Instructions for scriptwriting

<entry_point>
  This repository utilizes a modular 5-tier context stack. Before taking any action or processing tasks, load the root context files in order:
  1. SOUL.md - Identity, boundaries, and non-negotiable authorship guardrails.
  2. STYLE.md - Markdown conventions, hybrid xml+markdown format, and profile-source style.
  3. SKILL.md - The repo-native skill: when and how to work on this repo safely.
  4. MEMORY.md - Durable project facts, decisions, and invariants.
  5. WORKFLOW.md - The `multica-pr-v1` operational contract for episode work (agents, stages, lifecycle, PR protocol).
</entry_point>

<capabilities_and_tools>

  <code_discovery_engines>
    **IMPORTANT: ALWAYS use CodeGraph or code-review-graph BEFORE Grep/Glob/Read to explore the codebase.**
    The graphs are faster, cheaper (fewer tokens), and provide structural context (callers, dependents, cross-file references, test coverage) that file scanning cannot. Fall back to Grep/Glob/Read **only** when the graphs do not cover what you need.

    <tool_selection_strategy>
      - **Macro Scope & Risk Analysis:** Reach for `code-review-graph` first to evaluate change blast radius across profile bundles, review structural layout, or score diff risk before touching instruction files or scripts.
      - **Micro Navigation & Dynamic Hops:** Reach for `CodeGraph` (`codegraph_explore`) to trace specific symbols in `scripts/` (installer transforms, fixtures, tests) or locate references across profile and template files.
    </tool_selection_strategy>

    <!-- CODEGRAPH_START -->
    ## CodeGraph

    In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

    - **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
    - **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.
    - **Maintenance**: after substantive commits, run `codegraph sync` to keep the index current.

    If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
    <!-- CODEGRAPH_END -->

    <!-- code-review-graph MCP tools -->
    ## code-review-graph Matrix
    In repositories indexed by code-review-graph (a `.code-review-graph/` directory exists at root):

    | Tool | Use when |
    | :--- | :--- |
    | `detect_changes_tool` | Reviewing code changes — gives risk-scored analysis |
    | `get_review_context_tool` | Need source snippets for review — token-efficient |
    | `get_impact_radius_tool` | Understanding blast radius of a change before modifying code |
    | `get_affected_flows_tool` | Finding which execution paths or references are impacted |
    | `query_graph_tool` | Tracing callers, callees, imports, and dependencies |
    | `semantic_search_nodes_tool` | Finding functions/classes by name or keyword |
    | `get_architecture_overview_tool` | Understanding high-level repo structure |
    | `refactor_tool` | Planning renames, finding dead code |

    Keep the graph fresh with `code-review-graph update` after committing changes.
    <!-- code-review-graph END -->
  </code_discovery_engines>

  <knowledge_engine tool="okf">
    - **Knowledge Bundle Location:** `docs/knowledge/`
    - **Discovery Rule:** Use the `okf` CLI (`okf search`, `okf show`, `okf backlinks`) to discover plans, specs, playbooks, and dataset context before reading raw documentation files.
    - **Validation Rule:** Run `okf validate docs/` after modifying documentation or specs to ensure schema compliance before committing.
    - **Reindex Rule:** Run `okf index docs/knowledge/` after adding or restructuring bundle documents.
  </knowledge_engine>

</capabilities_and_tools>

<agentic_instructions project="scriptwriting" format="hybrid-xml-markdown">
  <purpose>
    scriptwriting is the profile-source repository for a four-hat YouTube
    scripting workflow. It defines six Hermes/Multica agent roles (Artist,
    Architect, Writer, Wizard, Reviewer, Head Script Writer), the templates and
    knowledge they consume, the installer that publishes profiles into Hermes,
    and the `multica-pr-v1` workflow contract that governs episode production.
  </purpose>

  <instruction_files>
    - Read `SOUL.md` for project identity and judgment.
    - Read `SKILL.md` for the reusable repo-work skill.
    - Read `STYLE.md` for markdown, profile, and script style.
    - Read `MEMORY.md` for durable facts, decisions, and invariants.
    - Read `WORKFLOW.md` for the episode workflow contract (agent directory, stages, lifecycle, PR protocol).
    - Treat this `AGENTS.md` as the operational command center.
  </instruction_files>
</agentic_instructions>

## Project Overview

<repo_map>

### Instruction Bundles

- `profiles/<role>/`: source-of-truth instruction bundles per role — `AGENTS.md`, `SOUL.md`, `STYLE.md`, `SKILLS.md`, `MEMORY.md` for `artist`, `architect`, `writer`, `wizard`, `reviewer`, `head`.
- `WORKFLOW.md`: the `multica-pr-v1` contract — agent directory (Multica UUIDs, Hermes profile names), stage table, ownership transitions, branch/worktree protocol, PR submission and review protocol.

### Templates and Knowledge

- `templates/`: stage artifact templates (`01-artist.md` … `04-wizard.md`), `SERIES.md`, `VOICE.md`, `episode-entry.md`, `episode-index.md`, `issue.md`. `head-log.md` is retired but retained.
- `knowledge/`: creative method sources — `four-hat-article.md`, `wizard-checklist.md`, `five-part/` (hook, intro, body, summary, cta).
- `docs/knowledge/`: the okf bundle (plans, specs, playbooks, datasets, tables).
- `docs/validation/`: deployment-readiness evidence — `multica-pr-workflow.md`, per-role walkthroughs, `running-with-hermes.md`.

### Tooling

- `scripts/install_profiles.py`: converts `profiles/<role>/` sources to Hermes format and installs them into `~/.hermes/profiles/<prefix><role>/`. Renames `SKILLS.md` → `SKILL.md`, wraps level-2 sections in XML-style tags, rewrites paths.
- `scripts/profiles.json`: profile manifest (short names, descriptions, skill descriptions).
- `scripts/test_install_profiles.py`, `scripts/e2e_install_test.py`: installer tests.
- `scripts/make_head_fixtures.py`, `scripts/test_head_fixtures.py`: Head-role fixtures and tests.

</repo_map>

## Two Kinds of Work

<work_modes>

### Mode 1: Profile-source work (this repo)

Editing instruction bundles, templates, knowledge, docs, or installer scripts.
This is normal software/documentation work: edit, validate, test, commit, PR.
Root `SOUL.md`/`STYLE.md`/`SKILL.md`/`MEMORY.md` govern this mode.

### Mode 2: Episode work (content repos)

Producing episode content as one of the six roles happens in a **separate
content repository** under Multica issue assignment — never in this repo.
`WORKFLOW.md` and the installed profile bundle govern that mode. If you are
asked to do episode work while sitting in this repo, stop and route through
Head per `WORKFLOW.md`.

</work_modes>

## Non-Negotiable Rules

<rules priority="highest">

- Never do episode content work in this repository; it belongs in the assigned content repo under `WORKFLOW.md`.
- Never weaken a role's authorship guardrails (e.g. Artist never authors ideas) when editing profile bundles.
- Keep the five-file bundle shape (`SOUL.md`, `AGENTS.md`, `STYLE.md`, `SKILLS.md`, `MEMORY.md`) intact for every role in `profiles/`; the installer depends on it.
- When changing lifecycle, assignment, or PR rules, update `WORKFLOW.md` and every affected profile bundle in the same change — they must not drift apart.
- Do not activate a partial instruction bundle; deployment readiness is recorded in `docs/validation/multica-pr-workflow.md`.
- Never commit secrets, `~/.hermes` contents, or runtime files. The installer symlinks `.env`; keys stay outside the repo.
- Do not edit installed profiles under `~/.hermes/profiles/` by hand; edit sources here and re-run the installer.
- Preserve historical material (retired rubrics, head-log, old review logs) without reactivating it.
- If `.codegraph/` exists, use CodeGraph before grep/find/read when locating or understanding code.
- Run `okf validate docs/` before committing documentation/spec changes.

</rules>

## Common Commands

<commands>

### Install / update Hermes profiles

```bash
python3 scripts/install_profiles.py --dry-run
python3 scripts/install_profiles.py
python3 scripts/install_profiles.py --only artist,writer
```

### Tests

```bash
python3 scripts/test_install_profiles.py
python3 scripts/test_head_fixtures.py
python3 scripts/e2e_install_test.py
```

### Graph maintenance

```bash
codegraph sync && code-review-graph update
```

### Knowledge bundle

```bash
okf search "<concept>"
okf validate docs/
okf index docs/knowledge/
```

</commands>

## Debugging Guide

<debugging>

- If an installed profile misbehaves, diff the source bundle in `profiles/<role>/` against `~/.hermes/profiles/<prefix><role>/` and re-run the installer; never patch the installed copy.
- If a role's instructions conflict with `WORKFLOW.md`, `WORKFLOW.md` is the workflow authority; reconcile the bundle.
- If agent identity/assignment questions arise, the agent directory table in `WORKFLOW.md` (exact Multica names + UUIDs) is the source of truth.
- If okf results look stale, re-run `okf index docs/knowledge/`.
- If graph queries miss recent edits, run `codegraph sync` and `code-review-graph update`.

</debugging>
