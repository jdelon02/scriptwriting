---
type: "documentation"
title: "scriptwriting — README"
description: "Project overview for scriptwriting: the profile-source repo for the four-hat YouTube scripting workflow."
tags: ["scriptwriting", "project"]
source_path: "README.md"
---

# scriptwriting

The profile-source repository for a four-hat YouTube scripting workflow. It defines six
`Hermes`/`Multica` agent roles, the templates and creative-method knowledge they consume, the
installer that publishes those roles into `Hermes`, and the `multica-pr-v1` workflow contract that
governs episode production.

## What this is

`scriptwriting` is the trust anchor for a small creative team made of agents. It does **not**
write scripts. It defines how six agent roles help a human creator write scripts — and it guards
the line between helping the creator and speaking for them. The creator's words stay the
creator's words: agents structure, prompt, and edit with approval; they never invent ideas, and
every accepted piece of work is proven through a reviewed, merged PR.

The six roles follow the "four hats" of YouTube scripting:

| Role | Hermes profile | Hat | What it does |
| --- | --- | --- | --- |
| **Artist** | `script-artist` | Idea dump | Interviews the creator, dumps all material, nominates the Grand Payoff |
| **Architect** | `script-architect` | Structure | Builds the skeleton from Setup-Tension-Payoff loops, writes payoffs first |
| **Writer** | `script-writer` | Draft | Connects setups and payoffs, writing for momentum over perfection |
| **Wizard** | `script-wizard` | Retention edit | Cuts jargon, checks curiosity-gap timing, adds visual cues |
| **Reviewer** | `script-reviewer` | Edit | Audits PRs against an issue's Doneness prose; evidence of accepted work |
| **Head Script Writer** | `script-head` | Orchestrator | Owns the parent episode issue and the navigation index; dispatches and reconciles |

`Reviewer` and `Head` fall outside the four creative hats — one audits, one coordinates.

## How work is organized

There are two kinds of work, kept strictly separate:

- **Profile-source work (this repo).** Editing instruction bundles, templates, knowledge, docs,
  or installer scripts. This is normal software/documentation work: edit, validate, test, commit,
  submit a PR.
- **Episode work (content repos).** Producing episode content as one of the six roles happens in a
  *separate* content repository under `Multica` issue assignment — never in this repo.

## Repository layout

```
profiles/<role>/                 Five-file instruction bundles (SOUL, AGENTS, STYLE, SKILLS, MEMORY)
                                  for artist, architect, writer, wizard, reviewer, head

WORKFLOW.md                      The multica-pr-v1 contract: agent directory, stage table,
                                  ownership transitions, branch/worktree protocol, PR protocol

templates/                       Stage artifacts (01-artist … 04-wizard) plus SERIES.md, VOICE.md,
                                  episode-entry.md, episode-index.md, issue.md

knowledge/                       Creative-method sources: four-hat-article.md, wizard-checklist.md,
                                  and the five-part/ framework (hook, intro, body, summary, cta)

docs/knowledge/                  The okf-indexed knowledge bundle (plans, specs, playbooks, datasets)
docs/validation/                 Deployment-readiness evidence: multica-pr-workflow.md, per-role
                                  walkthroughs, running-with-hermes.md, profile-deployment.md

scripts/                         install_profiles.py, profiles.json manifest, deploy/preflight tooling,
                                  RAG ingestion, knowledge sync, and their tests
```

Each root context file governs its concern: `SOUL.md` (identity and authorship guardrails),
`STYLE.md` (markdown conventions), `SKILL.md` (how to work in this repo safely), `MEMORY.md`
(durable facts and decisions), and `AGENTS.md` / `WORKFLOW.md` (the operational command center).

## Tooling

- **Installer** — `python3 scripts/install_profiles.py` converts `profiles/<role>/` sources into
  `Hermes` format and publishes them into `~/.hermes/profiles/`. Rename `SKILLS.md` → `SKILL.md`,
  wrap sections, rewrite paths. Supports `--dry-run`, `--only`, `--refresh-config`.
- **Deployment preflight** — `python3 -B scripts/deploy_multica_profiles.py --check` previews and
  verifies coherent `Hermes` + `Multica` deployment before dispatch.
- **Knowledge bundle** — `okf search`, `okf show`, `okf validate docs/knowledge/`, and
  `python3 scripts/sync_knowledge.py` to refresh the bundle after Markdown changes.
- **Code graphs** — `.codegraph/` and `.code-review-graph/` are indexed; query them before
  grepping or scanning, and refresh them after substantive commits.

## Commands

```bash
# Profiles
python3 scripts/install_profiles.py --dry-run
python3 scripts/install_profiles.py
python3 scripts/deploy_multica_profiles.py --check --channel-root /path/to/content-repo

# Tests
python3 scripts/test_install_profiles.py
python3 scripts/test_head_fixtures.py
python3 scripts/e2e_install_test.py

# Knowledge bundle
okf validate docs/knowledge/
python3 scripts/sync_knowledge.py

# Graphs
codegraph sync && code-review-graph update
```

## Non-negotiables

- No episode content is written in this repo — it belongs in the assigned content repo.
- Role authorship guardrails are never weakened when editing a profile bundle (e.g. the Artist
  role never authors ideas).
- `WORKFLOW.md` and the six profile bundles move together; lifecycle, assignment, or PR changes
  update all of them in one change.
- Secrets (`~/.hermes/.env`) are symlinked into profiles, never committed or printed.
- Accepted work is proven by a merged PR plus a Reviewer verdict — never by a markdown "done"
  field.

## Getting started

Read the five-tier context stack in order before any work: `SOUL.md`, `STYLE.md`, `SKILL.md`,
`MEMORY.md`, `WORKFLOW.md`. That stack *is* the operations manual for the team this repo supports.
