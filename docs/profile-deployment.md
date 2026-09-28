---
type: reference
title: Deploy and verify scripting profiles
description: Synchronize canonical role instructions into Hermes and Multica and verify runtime identity.
tags: [scriptwriting, deployment]
---

# Deploy and verify scripting profiles

Run from the scriptwriting source checkout. The existing Hermes installer updates local profiles;
the deployment command also updates Multica's existing agent instructions and assigned role skills.
It preserves unrelated skill assignments, model settings, credentials and learned memory.

```bash
python3 -B scripts/deploy_multica_profiles.py --channel-root /absolute/path/to/content-repo
python3 -B scripts/deploy_multica_profiles.py --apply --channel-root /absolute/path/to/content-repo
python3 -B scripts/deploy_multica_profiles.py --check --channel-root /absolute/path/to/content-repo
```

The default is a preview; `--check` exits nonzero on drift. The revision identifies rendered
instruction/template content, canonical workflow, deployer and guard, including uncommitted source
changes. It is a content hash, not a claim that a git commit was published.

## Deployment behavior

1. Resolve exact agent UUIDs from WORKFLOW.md. Require one matching local Hermes runtime and
   launch profile per role, with the correct explicit HERMES_HOME and executable wrapper.
2. Refuse unknown launch overrides, missing/disabled skills and active scripting runs.
   This is an idle check, not an atomic Multica scheduling lock; do not dispatch during deployment.
3. Save the previous non-secret configuration and touched local files in a private backup directory.
   The default is under /private/tmp; use `--backup-dir` for a durable operator-controlled location.
4. Mark all profiles pending, run the source installer without configuration refresh, synchronize
   the channel WORKFLOW.md contract while preserving its local preamble, and update existing
   Multica skill IDs and generated agent bootstraps. Do not modify episode artifacts or issues.
5. Verify each remote readback. Publish all six receipts and clear pending markers only after the
   complete bundle validates. Run the final source/deployment comparison.

An interrupted deployment retains pending markers. Correct the reported cause and rerun with a
new backup directory; do not manually remove markers to declare success. The original `before.json`
contains the previous prompts, runtime IDs, skill contents and affected files for operator recovery.
It is not a backup of model configuration, private memory, credentials or episode content.

## Startup and dispatch verification

The generated Multica prompt loads the installed role files instead of duplicating their procedure.
For content work it requires:

```bash
python3 "$HERMES_HOME/profile_guard.py" --channel-root /absolute/path/to/assigned-content-repo
```

Head checks the target role before dispatch:

```bash
python3 ~/.hermes/profiles/script-architect/profile_guard.py --preflight --channel-root /absolute/path/to/content-repo
```

The startup check validates the executing HERMES_HOME, live mapping, executable digest, remote
prompt/skill, local files, and channel workflow. `--preflight` checks the target configuration
without expecting the caller to be running that target role. Neither check reads private memory.
These are instruction-required checks, not a modification to Multica's server-side scheduler.
Ordinary informational role questions retain the installed SOUL exception.

Multica regenerates its workdir instructions when preparing a new run. Do not patch generated
AGENTS.md by hand. Existing conversations may contain historical instructions; the new bootstrap
explicitly directs the agent to the installed current role. Verify a fresh run before resuming work.

## Boundaries

The command updates the supplied channel checkout's WORKFLOW.md only. Publishing that change
to the channel's main branch and refreshing other worktrees remains a normal reviewed git change;
the guard blocks a checkout with a different contract. A passing deployment check does not
migrate legacy issue metadata, establish creator approval, or prove native PR linking/merge/wake
behavior. Those gates remain in the workflow validation runbook.
