# Running the six profile walkthroughs

The source bundle defines `multica-pr-v1`. Live deployment is gated by
[multica-pr-workflow.md](multica-pr-workflow.md). Do not mix new profiles with the old content workflow.

## Offline preparation

Run packaging and fixture tests from this source repository:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

Generate a scenario in a **new empty directory** (the generator refuses existing content):

```sh
python3 scripts/make_head_fixtures.py /private/tmp/script-workflow-example submission --stage 1
```

The generated directory is an **operator fixture package**, not the agent workspace. Create a
separate scratch content workspace and copy only series/ and test-data/ from the package, then the
shared WORKFLOW.md, knowledge/, templates/ and needed deployment context. Do not copy operator-only/
or these walkthrough answer tables into any path the test agent can access. The generator's `test-data/` contains synthetic observations, not full API responses or live lifecycle
state. Expected actions live separately in `operator-only/expected.md`. Supply the test directory
substitution explicitly and use the actor named in scenario.json; never call live tools with test IDs. Use the role walkthrough
with remote tools disabled, and keep actual observations separate from expected actions.

For profile rendering without installing, import scripts/install_profiles.py and use render_soul,
render_agents, render_style and render_skill with scripts/profiles.json. Compare the result against
installed files; do not compare raw source bytes because headings, tags and paths change on install.
`SKILLS.md` renders to `skills/script-<role>/SKILL.md`, with a root SKILL.md symlink.

## Controlled live installation

Only after the runbook's gates pass and a coherent bundle revision is approved, back up each profile's
managed instructions and supporting files. Preserve learned memory, config.yaml, .env and unrelated
skills. Use the same reviewed revision for all six profiles:

```sh
python3 scripts/install_profiles.py --no-config --no-bundled-skills
```

Do not use --refresh-config. The installer seeds memories/MEMORY.md only if missing; root MEMORY.md
links to it. A learned-memory difference from the source template is intentional, not stale deployment.
Retired rubric files may remain as historical references but no active role loads them.

Updating Hermes alone is insufficient. Update the six Multica embedded instruction and attached skill
copies from the same rendered revision, and verify their selected runtime/profile. Deliver WORKFLOW.md,
templates/, knowledge/ and the required validation runbook to the **content repository** through its
own reviewed PR. The profile-source repository need not exist in an episode worktree.

## Runtime context

An agent reads SOUL.md, AGENTS.md, STYLE.md, SKILL.md and its own learned memory from HERMES_HOME.
Shared workflow/content comes from the assigned content repository's runtime-supplied worktree.
Never start a second Hermes session to substitute for a Multica issue assignment, create a parallel
checkout system, or use a profile name as the assignee. Missing context goes to Head.

The live pilot must use actual Multica assignments in separate supplied worktrees. A standalone
`hermes -p script-artist chat --in <scratch-content>` session can exercise interview behavior but
cannot prove native PR association, wake delivery, cleanup, concurrency or cross-worktree visibility.
Confirm launch flags with `hermes chat --help`; no live session has been executed by this migration.

## Recording results

All six role walkthroughs distinguish not-run cases from observed passes/failures. Keep issue URLs,
PR URLs, reviewed head/merge SHAs, push confirmations and owner/status readbacks in the migration
issue/PR. A green installer suite is packaging evidence only, not orchestration validation.
Fix profile source when a walkthrough fails and regenerate the coherent bundle. Never patch installed
instructions alone and leave the source or Multica copies behind.
