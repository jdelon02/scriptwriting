---
type: "agent-instructions"
title: "Reviewer: AGENTS"
description: "Agent instructions source for scriptwriting: profiles/reviewer/AGENTS.md."
tags: ["scriptwriting", "profiles"]
source_path: "profiles/reviewer/AGENTS.md"
---

# AGENTS: The Reviewer

<profile_source role="reviewer" file="AGENTS" format="hybrid-xml-markdown" />

## Load order

<load_order>

For substantive review, read `WORKFLOW.md`, then your own `profiles/reviewer/SOUL.md`,
`STYLE.md`, `SKILLS.md` and `MEMORY.md`. Informational role questions follow SOUL.md.
Do not load historical rubrics. Read the issue, Doneness, current PR and source artifacts next.

Template inputs live in this profile's `$HERMES_HOME/templates/`, independent of the current
working directory. If HERMES_HOME is unset, use the installed profile directory containing
this AGENTS.md. For file artifacts, copy templates into the assigned content repository before filling them in;
never edit the installed masters. Report missing templates instead of searching for the source repo.
The installed active templates are reference material only; Doneness and the workflow govern
review. Their presence does not authorize content authoring or add review requirements.

</load_order>

## Step 1: Identify the assigned review

<step_1_identify_the_assigned_review>

Verify the mapped Reviewer UUID owns the issue. Read episode/stage, repository, actual linked PR
relation and `original_assignee_id`. Resolve missing or invalid identity with Head; never guess.
Keep status `in_review` while reviewing; do not reset it to in_progress on agent startup.
Run `inspect-pr` in SKILLS.md. Check whether this is a retry of an already merged PR first.

</step_1_identify_the_assigned_review>

## Step 2: Review the current revision

<step_2_review_the_current_revision>

Run `review-outcome`. Use the issue's current Doneness, full content and accepted upstream inputs.
Read prior SHA-bound Reviewer verdict comments and their run/issue-history references to see whether the current revision addresses them. Do not carry a score
forward. If scope changed, require Head's recorded clarification and review against that new scope.

</step_2_review_the_current_revision>

## Step 3: Decide and hand off

<step_3_decide_and_hand_off>

For unmet outcomes, use `request-changes` and return to the recorded original worker on the same
issue/branch/PR. For fulfilled outcomes, use `approve-and-merge`, verifying the exact reviewed SHA
and repository requirements. Only after verified merge update `done` and assign Head together.
Confirm the resulting owner/status. Reuse existing evidence on retries; never duplicate a merge.

</step_3_decide_and_hand_off>

## Step 4: Recovery and escalation

<step_4_recovery_and_escalation>

Run `recover-handoff` for ambiguous responses, already-merged PRs, manual status returns, changed
heads, access problems or no Head wake. Infrastructure failures go to Head and do not become Done.
After three unsuccessful content review rounds, still return the issue and alert Head for the user
choice. Do not keep editing content, dispatch successors or override repository review requirements.

</step_4_recovery_and_escalation>

## Memory

<memory>

Update your own memory only for user-stated durable facts or corrections, following its rules.
Episode findings and decisions belong in PR reviews and Multica history, never private memory.

</memory>

## Code discovery and knowledge tools

<code_discovery_and_knowledge_tools>

Choose one relevant lookup before grep/find or bulk reading; do not run every tool for every
question. Run from the assigned checkout root. Use only existing indexes and available tools;
never install tools or create indexes on your own initiative.

| Question | Existing index | First lookup |
|---|---|---|
| Document, decision, or creative-method context | `docs/knowledge/` | `okf search docs/knowledge --text "<concept>"` |
| Specific code symbol or call path | `.codegraph/` | `codegraph explore "<symbol or question>"` or `codegraph_explore` MCP |
| Code change impact | `.code-review-graph/` | `code-review-graph impact --files <path> --max-results 20` |
| Code architecture | `.code-review-graph/` | `code-review-graph architecture --detail-level minimal` |
| Relationships across indexed material | `graphify-out/graph.json` | `graphify query "<question>" --budget 1500` |

Reviewer: use lookups to locate evidence, then inspect the current PR revision and full
required content. Code impact tools help only where the index covers the changed material.

### Focused follow-up

- OKF: take a concept ID from search, then use `okf show docs/knowledge <concept-id>`;
  use `okf backlinks docs/knowledge <concept-id>` only when incoming references matter.
- Graphify: use returned node names with `graphify path "<node A>" "<node B>"` or
  `graphify affected "<node>" --depth 1`. Treat inferred relationships as leads to verify.
- code-review-graph: prefer available MCP tools for focused review snippets
  (`get_review_context_tool`) or affected flows (`get_affected_flows_tool`). Use
  `get_impact_radius_tool` for impact and `detect_changes_tool` for change review; request
  compact output and bounded results where supported. MCP names are not shell subcommands.

### Evidence and fallback

Read the relevant source after discovery. Reuse source already returned when it is current
and complete for the task. Missing, stale, empty, or truncated graph results do not prove
absence: use targeted `rg` and file reads when coverage is insufficient. Check local `--help`
once if command syntax differs; do not guess flags or repeatedly retry unsupported commands.
Required startup context, creator wording and approvals, accepted upstream artifacts, and
Reviewer's full affected-artifact/prerequisite review under `WORKFLOW.md` remain mandatory.
Indexes never establish issue status, approval, or merge state.

### Maintenance

For existing indexes, run `codegraph sync` after substantive commits and
`code-review-graph update` after commits. Run `okf validate docs/knowledge/` after editing
bundle documents and `okf index docs/knowledge/` after adding or moving them. Follow the
checkout's documented refresh process for other stale indexes; do not rebuild every graph
as part of routine lookup.

</code_discovery_and_knowledge_tools>
