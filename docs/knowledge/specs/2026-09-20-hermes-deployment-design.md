---
type: spec
title: "Hermes Deployment Design"
description: "How the five scriptwriting profiles are packaged as Hermes profiles: repo sources, a transform into Hermes format, an install script that creates and populates ~/.hermes/profiles/script-<name>, and how the agents run."
tags: [scriptwriting, hermes, deployment, spec]
---

# Hermes Deployment — Design

Date: 2026-09-20
Status: Draft, pending user review

## 1. Context

The five profile specs (Artist, Architect, Reviewer, Writer, Wizard) describe agents as folders of markdown
files. They do not say how those agents become real. This spec fixes that: the agents are **Hermes profiles**
(Hermes Agent v0.21.3), created in `~/.hermes/profiles/` with the `hermes` CLI. Paperclip AI, Multica, or
Hermes' own `kanban` are the orchestrators that run them, not the place they are created. The earlier specs
implied otherwise; they are corrected by small patches listed in the packaging plan.

The repo stays the source of truth, so the whole set can be recreated on another machine by running a script.

### What was verified on 2026-09-20

Read-only, plus one throwaway profile that was deleted afterwards:
- A Hermes profile is an isolated home at `~/.hermes/profiles/<name>/`. `hermes profile create <name>
  [--description ...] [--no-skills] [--no-alias] [--clone-from ...]` creates it. `hermes profile describe`
  sets the description that the kanban orchestrator uses to route tasks.
- The existing profiles (for example `project-planner`) keep `SOUL.md`, `AGENTS.md`, and `STYLE.md` at the
  root. `SKILL.md` at the root is a symlink to `skills/<name>/SKILL.md`, which has YAML frontmatter with
  `name` and `description`. `MEMORY.md` at the root is a symlink to `memories/MEMORY.md`. Sections are wrapped
  in XML-style tags such as `<identity>` and `<communication>`. `SOUL.md` contains a `<profile_context>` block
  that tells the agent to read `AGENTS.md`, `STYLE.md`, and `SKILL.md` from its home.
- A new profile starts with a `.env` that holds only a comment header (no variables) and a default
  `config.yaml`: no model and no keys until they are provided.
- `~/.hermes/.env` holds the LiteLLM keys and URL, and `~/.hermes/config.yaml` routes `model.default:
  smart-router` through `${LITELLM_BASE_URL}`. `ceo` has an identical `.env` but a different `config.yaml`, so
  `~/.hermes/` is the source to share, not `ceo`. Symlinked `.env` and `config.yaml` survived `hermes config
  set`, setting an env var, and `hermes config migrate` on a throwaway profile (scratch dummy files, not the
  real ones).
- **Copying files into a freshly created profile works.** Hermes then lists a profile-local skill in
  `hermes skills list`, and reports the `memories/MEMORY.md` content in `hermes prompt-size`.
- `AGENTS.md` in a profile's home is **not** auto-loaded (the prompt's context tier was 0 bytes). Only
  `SOUL.md` is native, which is why `SOUL.md` carries the `<profile_context>` block.
- `~/.agents/skills` is **not** scanned by default. No config on this machine sets `skills.external_dirs`.
  Setting it made Hermes list all 62 skills there. This design does not use it: skills are copied into each
  profile instead.
- `hermes profile create` makes a command alias by default: a one-line script in `~/.local/bin` named after
  the profile, running `hermes -p <name> "$@"`.
- A plain `hermes profile create` seeds Hermes' bundled skills (12 folders, 57 skills). A profile created with
  `--no-skills` can be brought in line with `hermes -p <name> skills opt-in --sync`, which removes the
  `.no-bundled-skills` marker and re-seeds them. On a throwaway profile the result matched a normally created
  one exactly. The bundled skills grow a profile's skills index from 0.4 KB to 5.5 KB (about 15 KB to 20 KB of
  system prompt).
- `hermes chat --in DIR` changes into DIR before starting, so a profile can run with this repo as its working
  directory.

## 2. Scope

**In scope**
- A manifest of the five profiles with their Hermes descriptions.
- A transform from plain-markdown sources to Hermes format.
- An install script that creates and populates the profiles, idempotently.
- Unit tests, and an end-to-end test against real Hermes with guaranteed cleanup.
- A short guide to running the walkthroughs against installed profiles.
- Patches to the five specs and five plans so they describe the Hermes deployment.

**Out of scope**
- The content of the profiles (their own specs and plans).
- Choosing the orchestrator (Paperclip AI, Multica, or kanban).
- Choosing the model or keys. They come from `~/.hermes` (§6).
- Hermes "distributions" (`hermes profile install`). A distribution carries `SOUL.md`, config, skills, cron,
  and MCP config, but not `AGENTS.md`, `STYLE.md`, or `MEMORY.md`, so it does not fit the five-file model.

## 3. Repository layout

```
profiles/<short>/          <short> is artist, architect, reviewer, writer, or wizard
  SOUL.md
  AGENTS.md
  STYLE.md
  SKILLS.md                  source name; becomes SKILL.md when installed
  MEMORY.md                  the initial memory template
  rubrics/                   supporting material (the Reviewer only)
scripts/
  profiles.json              the manifest: short name, Hermes description, skill description
  install_profiles.py        the installer and transform (Python 3 standard library only)
  test_install_profiles.py   unit tests (stub hermes, temp dirs)
  e2e_install_test.py        end-to-end test against real Hermes
docs/validation/
  running-with-hermes.md     how to start an installed profile for the walkthroughs
```

The sources stay plain markdown, exactly as the five plans produce them. Shared project files stay in the
repo: `WORKFLOW.md`, `knowledge/`, `templates/`, `series/`.

## 4. Installed layout

For a profile named `script-<short>`, in `~/.hermes/profiles/script-<short>/`:

```
SOUL.md                              transformed, with <identity> and <profile_context>
AGENTS.md                            transformed
STYLE.md                             transformed
SKILL.md  ->  skills/script-<short>/SKILL.md      symlink
skills/script-<short>/SKILL.md       transformed, with frontmatter
MEMORY.md ->  memories/MEMORY.md                  symlink
memories/MEMORY.md                   the live memory; created once, never overwritten
rubrics/...                          supporting material, copied (Reviewer)
.env  ->  ~/.hermes/.env             symlink; keys are shared
config.yaml                          a copy of ~/.hermes/config.yaml, made once at creation
```

Profile names use the `script-` prefix: `script-artist`, `script-architect`, `script-writer`,
`script-wizard`, `script-reviewer`. The prefix groups them in `hermes profile list`, avoids clashing with the
existing role-named profiles, and keeps kanban routing unambiguous.

## 5. Transform rules

Applied to the installed copies only. The sources are never modified.

1. **Titles.** `# SOUL: The Artist` becomes `# The Artist`. `# AGENTS: The Artist` becomes
   `# The Artist operating contract`. `# STYLE: The Artist` becomes `# The Artist communication`.
   `# SKILLS: The Artist` becomes `# The Artist skills`.
2. **Tags.** Each level-2 section body is wrapped in a tag derived from its heading (`## Hard limits` becomes
   `<hard_limits>...</hard_limits>`), as the existing profiles do. Headings inside code fences are ignored,
   including nested fences of different lengths. A trailing horizontal rule at the end of a section is dropped.
   In `SOUL.md`, `## Who you are` maps to `<identity>`.
3. **Profile context.** A generated `## Profile context` section with a `<profile_context>` block is inserted
   after the identity section. It tells the agent to read `AGENTS.md`, `STYLE.md`, and `SKILL.md` from its
   home, to follow the load order in `AGENTS.md`, and to work from the scriptwriting project directory.
4. **Skill file.** `SKILLS.md` becomes `SKILL.md` with frontmatter (`name: script-<short>`, a one-line
   `description`), and a generated `<procedure>` block after the title.
5. **Paths.** `profiles/<short>/` in text becomes `~/.hermes/profiles/script-<short>/`, so per-profile
   references resolve from the profile's home. The bare name `SKILLS.md` becomes `SKILL.md`. Paths to shared
   files (`WORKFLOW.md`, `knowledge/`, `templates/`, `series/`) are left alone, because they resolve from the
   working directory.
6. **Supporting files.** Copied with the same path rewrite for `.md` files, and without tags.

## 6. Installer behavior (`scripts/install_profiles.py`)

`python3 scripts/install_profiles.py [--only a,b] [--clone-from PROFILE] [--no-alias] [--no-bundled-skills] [--config-from DIR]
[--no-config] [--refresh-config] [--dry-run]`, plus `--repo`, `--prefix`, `--profiles-dir`, and `--hermes` for
tests.

For each requested profile:
1. If `profiles/<short>/` does not exist, print `skipped` and continue. This lets profiles be installed as
   their plans are executed. If it exists but lacks `SOUL.md`, `AGENTS.md`, `STYLE.md`, or `SKILLS.md`, report
   an error and exit non-zero.
2. If `~/.hermes/profiles/script-<short>/` does not exist, run `hermes profile create script-<short>
   --description <text>`. With `--clone-from`, the flag is passed through (Hermes then copies model config,
   `.env`, and skills from that profile). Without it, Hermes seeds its bundled skills as for any profile (`--no-bundled-skills` passes `--no-skills`
   instead).
   **Aliases are created by default**, as for the existing profiles. `--no-alias` skips them.
3. Write the transformed files and symlinks (§4).
4. Create `memories/MEMORY.md` from the source template **only if it does not exist**. A hand-written root
   `MEMORY.md` that is not a symlink is moved into `memories/`, not lost. Learned memory survives every
   re-install.
5. Copy supporting material.
6. Share model and keys from `--config-from` (default `~/.hermes`), unless `--no-config` or `--clone-from`
   is given. `.env` is symlinked, and only replaced if the profile's own `.env` has no variable assignments (a
   fresh Hermes profile has a comment header only). `config.yaml` is copied once, when the profile is created,
   and replaced later only with `--refresh-config`. Nothing is written through a symlink, and a missing source
   is a warning, not an error. The two source files are never read or modified.
7. If the profile has a `.no-bundled-skills` marker and `--no-bundled-skills` is not given, run
   `hermes -p script-<short> skills opt-in --sync`, so profiles created lean earlier get the bundled skills
   too. `--no-bundled-skills` never removes skills from an existing profile.
8. Run `hermes profile describe script-<short> --text <description>`, so the description stays in sync on
   every run.

The script never touches `auth.json` and never prints `.env` content. It ends by printing how to start a
profile and how to change its model (`<name> setup` or `--refresh-config`). `--dry-run` reports what would happen and changes
nothing. Exit codes: 0 success, 1 a profile failed, 2 an unknown profile name.

## 7. Running the agents

- Start a profile with the repo as its working directory: `hermes -p script-<short> chat --in <repo>`, or with
  the alias `script-<short> chat --in <repo>`. The shared files then resolve from the repo, and per-profile
  files resolve from the profile's home.
- A profile's live memory is `~/.hermes/profiles/script-<short>/memories/MEMORY.md`. Agents update that file.
  The repo's `profiles/<short>/MEMORY.md` is only the initial template.
- Editing a source file in the repo changes nothing until the installer runs again.
- For the walkthroughs, run the agent in a scratch copy of the repo (`--in "$SCRATCH/run"`), so real series
  files are untouched. The installed profile is the same one.

## 8. Orchestrators and routing

Paperclip AI, Multica, and Hermes `kanban` are all candidates for running these profiles. The specs stay
orchestrator-agnostic, and the `WORKFLOW.md` mapping table remains the one place to record real status names.
The profile descriptions in the manifest are the text the kanban orchestrator uses to route tasks by role.

## 9. Verification

- **Unit tests** (`scripts/test_install_profiles.py`): the transform, including nested fences; the installer
  against a stub `hermes` (create flags, aliases on by default, `--no-alias`, `--clone-from`, idempotence,
  memory preserved, dry run, missing and incomplete sources); the manifest; and, once sources exist, a render
  of every real source file with balanced tags and no leftover repo paths.
- **End-to-end test** (`scripts/e2e_install_test.py`): creates `zz-e2e-artist` from a fixture, installs,
  checks the files and symlinks, checks that Hermes lists the skill and reports memory, checks that
  re-installing keeps memory, and always deletes the profile and purges its identity.
- Both pass as written on 2026-09-20 (33 unit tests, 1 skipped until real sources exist; the end-to-end test
  uses dummy config files and never touches your real `.env` or `config.yaml`).

## 10. Open items

Decisions made during design:
- Repo as the source of truth, with an install script that creates then copies (not Hermes distributions).
- Skills copied into each profile, not shared through `~/.agents/skills`.
- Every profile also gets Hermes' bundled skills: new profiles are created normally, and lean ones are opted in
  with `skills opt-in --sync`.
- Names use the `script-` prefix.
- Aliases are created by default.
- The existing profiles' XML-tag format is matched in the installed copies only.
- Learned memory is never overwritten.
- `.env` is linked and `config.yaml` is copied from `~/.hermes`.

Open:
1. **Shared config.** A symlinked `.env` means a key change reaches every `script-*` profile. A copied
   `config.yaml` means a model change needs `--refresh-config` or an edit to each profile. Tuning one profile's
   copy (for example, removing the Reviewer's file-write tool) affects only that profile.
2. **The agent obeying `<profile_context>`.** The design relies on the agent reading `AGENTS.md`, `STYLE.md`,
   and `SKILL.md` at session start, as the existing profiles do. The walkthroughs are the test; no model call
   was made in this design.
3. **Aliases hard-code the path to `hermes`.** The wrapper is generated per machine by `hermes profile create`,
   so a second machine gets its own.
4. **Untested launch syntax.** `hermes -p <name> chat --in <dir>` follows the CLI help, but a full session was
   not run here because it needs a model.
5. **Trash.** Deleting a profile leaves a copy in `~/.hermes/profiles/.deleted/`. The end-to-end test leaves
   `zz-e2e-artist` there.
6. **Orchestrator choice** and its status mapping remain open (Paperclip AI, Multica, or kanban).
