# MEMORY.md

<memory project="scriptwriting" format="hybrid-xml-markdown">
  <purpose>
    Durable facts and decisions that future agents should carry forward across
    work sessions in this repository.
  </purpose>
</memory>

## Project Facts

<facts>

- Project ID: `scriptwriting`.
- Kind: agent-instruction source repository (profiles, templates, knowledge, workflow contract, installer).
- Primary goal: define and maintain the four-hat YouTube scripting workflow executed by Multica agents with Hermes profiles.
- Workflow version: `multica-pr-v1` (defined in `WORKFLOW.md`).
- Six roles: Artist, Architect, Writer, Wizard, Reviewer, Head Script Writer.
- Hermes profile names: `script-artist`, `script-architect`, `script-writer`, `script-wizard`, `script-reviewer`, `script-head`.
- Multica workspace: `Personal Stuff` (`aa1884cb-1770-444b-b66d-4a036cba7e82`), issue prefix `PERS`. Exact agent names and UUIDs live in the `WORKFLOW.md` agent directory table.
- Episode content lives in separate content repositories (e.g. `delongpa-channel` worktrees), never in this repo.
- Related projects: `hermes` (profile runtime), `multica` (issue lifecycle/orchestration), the content channel repos.
- GitHub identity: all agents operate as `jdelon02`; commits use author `Jeremy DeLong <chefjeremy@delongaz.com>`.

</facts>

## Tooling State

<tooling>

- `.codegraph/` exists — CodeGraph is indexed; use `codegraph_explore` / `codegraph explore` first for code questions and run `codegraph sync` after commits. `codegraph init` was run on 2026-09-22.
- `.code-review-graph/` exists — use its MCP tools for impact/blast-radius analysis and run `code-review-graph update` after commits.
- okf bundle lives at `docs/knowledge/` (`okf_version: 0.2`); `okf index docs/knowledge/` refreshes it, `okf validate docs/` checks schema compliance.
- Hermes installer: `python3 scripts/install_profiles.py` publishes `profiles/<role>/` into `~/.hermes/profiles/<prefix><role>/`; supports `--dry-run`, `--only`, `--refresh-config`.

</tooling>

## Durable Decisions

<decisions>

- Multica owns issue lifecycle and ownership; GitHub PR review and verified merges are the evidence of accepted work. Markdown fields never indicate completion.
- Numerical scoring, deductions, pass thresholds, and the separate acceptance-criteria framework are retired; Reviewer compares PR results against the issue's Doneness prose.
- Every issue gets a specific, nonempty Doneness section derived from the user's request; placeholders are insufficient.
- `original_assignee_id` records the delegated worker and is immutable through review cycles; returns go to that UUID, never to a fuzzy name match.
- Agent verdicts are PR comments (`Agent verdict: approved` / `Agent verdict: changes-requested`) under the shared `jdelon02` account — not GitHub review events; no self-approval via `gh pr review --approve`.
- One active content writer per issue; branch names are exact issue IDs; PRs titled `<ISSUE-ID> PR` into `main`; no automatic close-intent phrases in PR bodies.
- Post-merge revisions get a new linked issue/branch/PR; accepted history is immutable.
- Head owns a parent episode issue whose deliverable is the navigation index (`templates/episode-index.md`); it flows through Reviewer like any other PR.
- `templates/head-log.md` is retired; historical logs and rubrics are preserved as evidence only.
- The installer never overwrites an existing installed `memories/MEMORY.md` and never reads or prints `.env` content.
- Profile sources use the hybrid xml+markdown format (pre-wrapped sections plus a `<profile_source />` marker); `wrap_sections` was made idempotent on 2026-09-22 so installs stay single-wrapped. Each role's AGENTS/SOUL/STYLE/SKILLS carries codegraph, code-review-graph, and okf directives.

</decisions>

## Secrets And External State

<secrets>

- API keys live in `~/.hermes/.env`, shared into profiles by symlink; never commit or print them.
- `~/.hermes/config.yaml` is copied per profile at creation so each can be tuned; the installer never modifies the source.
- Deployment readiness and capability evidence are recorded in `docs/validation/multica-pr-workflow.md`; do not activate a partial instruction bundle.

</secrets>

## Repo Layout Memory

<layout>

- `profiles/<role>/`: five-file source bundles (`SOUL.md`, `AGENTS.md`, `STYLE.md`, `SKILLS.md`, `MEMORY.md`).
- `templates/`: stage artifacts `01-artist.md`–`04-wizard.md`, `SERIES.md`, `VOICE.md`, `episode-entry.md`, `episode-index.md`, `issue.md`.
- `knowledge/`: `four-hat-article.md`, `wizard-checklist.md`, `five-part/` (hook, intro, body, summary, cta).
- `docs/knowledge/`: okf bundle (plans, specs, playbooks, datasets, tables).
- `docs/validation/`: per-role walkthroughs plus `multica-pr-workflow.md` and `running-with-hermes.md`.
- `scripts/`: installer, manifest (`profiles.json`), fixtures, and tests.

</layout>

## Agent Reminders

<agent_reminders>

- Renaming a template heading or field label (`Interview step:`, `Status: approved`) is a workflow change with downstream consumers — trace them first.
- If `WORKFLOW.md` and a profile bundle disagree, that is a defect to reconcile, with `WORKFLOW.md` as the workflow authority.
- Verified agent renames update the name in the `WORKFLOW.md` directory, never the UUID.
- Role SKILLS.md files are renamed to SKILL.md at install time; write source-relative paths in bundles.
- After substantive commits: `codegraph sync && code-review-graph update`; after bundle doc changes: `okf index docs/knowledge/`.
- Never write episode content, series data, or creator material into this repo or into any MEMORY file.

</agent_reminders>
