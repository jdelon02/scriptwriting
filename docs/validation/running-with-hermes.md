# Running the profile walkthroughs with Hermes

The walkthrough documents in this folder test the five profiles (`script-artist`, `script-architect`,
`script-writer`, `script-wizard`, `script-reviewer`) as installed Hermes profiles. This guide covers the setup
and the launch command they refer to. Design: `docs/knowledge/specs/2026-09-20-hermes-deployment-design.md`.

## Set up a profile

1. **Install it from the repo sources.** Re-run this after any edit to a file under `profiles/<short>/`,
   because the installed copy does not change until you do:

   ```bash
   python3 scripts/install_profiles.py --only artist
   ```

   Use `--only writer,wizard` for several, or no `--only` for all five. The first run creates the Hermes
   profile (with a command alias, as your other profiles have). Later runs update the files and never
   overwrite the profile's learned memory in `memories/MEMORY.md`.
2. **Model and keys come from `~/.hermes`.** When the installer creates the profile it links the profile's
   `.env` to `~/.hermes/.env` (keys are shared) and copies `~/.hermes/config.yaml` (so each profile can be
   tuned). Later installs keep the profile's config. Add `--refresh-config` to re-copy it. Use `--no-config`
   to skip this step, or `--clone-from <profile>` to clone another profile instead.
3. **Skills.** Profiles are created with Hermes' bundled skills, and a profile that was created lean is
   opted in on the next install. Use `--no-bundled-skills` to create one without them.
4. **Confirm.**

   ```bash
   hermes profile list                       # script-artist appears, with an alias
   ls -l ~/.hermes/profiles/script-artist/.env    # a symlink to ~/.hermes/.env
   hermes -p script-artist skills list       # script-artist appears as a local skill
   ```

## Start a profile for a walkthrough

Each walkthrough makes a scratch copy of the repo and tells you to start the profile. Start it with the
scratch copy as the working directory, so the shared files (`WORKFLOW.md`, `knowledge/`, `templates/`,
`series/`) come from the copy and real series files are untouched:

```bash
hermes -p script-artist chat --in "$SCRATCH/run"
# or, with the alias:
script-artist chat --in "$SCRATCH/run"
```

Untested: this launch syntax follows the CLI help. A full session needs a model, and none was run when this
guide was written. If it fails, `hermes chat --help` shows the current flags.

## What the agent reads

- **From its own home** (`~/.hermes/profiles/script-<short>/`): `SOUL.md`, `AGENTS.md`, `STYLE.md`,
  `SKILL.md`, `memories/MEMORY.md`, and, for the Reviewer, `rubrics/`. `SOUL.md` tells it to read the others at
  session start.
- **From the working directory** (the scratch copy): `WORKFLOW.md`, `knowledge/`, `templates/`, `series/`.

## The Reviewer

Start `script-reviewer` the same way, then tell it, as a normal message, which stage's task has moved to
`review` and for which episode. There is no orchestrator in the walkthroughs, so the agent states the exact
status change it would make.

## When a walkthrough fails

The defect is in the profile source. Fix the file under `profiles/<short>/`, re-run the installer for that
profile, and re-run the walkthrough. Do not edit the installed copy in `~/.hermes/profiles/`: the next
install overwrites it.

## Where memory lives

A profile's live memory is `~/.hermes/profiles/script-<short>/memories/MEMORY.md`. The repo's
`profiles/<short>/MEMORY.md` is only the initial template.
