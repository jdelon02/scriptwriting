---
type: plan
title: "Hermes Packaging Implementation Plan"
description: "Task-by-task plan to package the five scriptwriting profiles as Hermes profiles: a manifest, a transform and install script with tests, an end-to-end test, a run guide, and patches to the earlier specs and plans."
tags: [scriptwriting, hermes, deployment, plan]
---

# Hermes Packaging Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Package the five scriptwriting profiles as Hermes profiles, so that running one script creates `~/.hermes/profiles/script-<name>` for each profile with the files in Hermes format, and the whole set can be recreated on any machine from this repo.

**Architecture:** The five profile plans keep producing plain-markdown sources in `profiles/<short>/`. A manifest and a standard-library Python installer transform those sources into Hermes format (XML-style section tags, a `SKILL.md` with frontmatter, a `<profile_context>` block in `SOUL.md`, rewritten paths), run `hermes profile create` when a profile is missing, copy the files and symlinks into the profile's home, share model and keys from `~/.hermes` (`.env` linked, `config.yaml` copied), and never overwrite learned memory. Unit tests use a stub `hermes`; an end-to-end test uses the real CLI and a throwaway profile that it always deletes.

**Tech Stack:** Python 3 (standard library only), the `hermes` CLI (v0.21.3 or later), shell `grep`.

**Spec:** `docs/knowledge/specs/2026-09-20-hermes-deployment-design.md`

## Execution order

Run this plan **first**. Then, for each profile plan (Artist, Architect, Reviewer, Writer, Wizard): build its sources, run `python3 scripts/install_profiles.py --only <short>`, and only then run that plan's walkthroughs, which now run against the installed profile (see `docs/validation/running-with-hermes.md`).

## Global Constraints

- **No git commits.** The user commits later. Do not run `git add` or `git commit`.
- Python 3 standard library only. No third-party packages.
- Aliases are created by default when a profile is created (`hermes profile create` default). `--no-alias` is opt-in.
- Profiles get Hermes' bundled skills: new ones are created without `--no-skills`, and one that still has the `.no-bundled-skills` marker is opted in with `hermes -p <name> skills opt-in --sync`. `--no-bundled-skills` opts out and never removes skills from an existing profile.
- The installer links `~/.hermes/.env` into new profiles and copies `~/.hermes/config.yaml` (spec §6). It never reads or modifies those two source files, never prints `.env` content, never writes through a symlink, never touches `auth.json`, and never modifies files under `profiles/`.
- Tests and the end-to-end test use dummy config files in a temp directory. They never touch the real `~/.hermes/.env` or `config.yaml`.
- The only profiles the tests may create or delete are those named with the prefix `zz-e2e-`. Never delete or alter any other Hermes profile.
- Profile names use the prefix `script-`: `script-artist`, `script-architect`, `script-writer`, `script-wizard`, `script-reviewer`. Short names: `artist`, `architect`, `writer`, `wizard`, `reviewer`.
- Learned memory is never overwritten: `memories/MEMORY.md` is created only if absent.
- Files inside the okf bundle `docs/knowledge/` need quoted YAML frontmatter, and generated `index.md` files are never edited by hand (regenerate with `okf index docs/knowledge`). Tasks 5 and 6 edit bundle files.
- All paths are relative to `/Users/jdelon02/Projects/scriptwriting`. Run all shell commands from that directory.

## Prerequisite check

```bash
python3 --version
hermes --version
test ! -e ~/.hermes/profiles/zz-e2e-artist || echo "PREREQUISITE: leftover zz-e2e-artist profile exists; delete it first"
```

Expected: a Python 3 version, a Hermes version line, and no `PREREQUISITE:` line.

## File Structure

```
scripts/profiles.json                          Task 1
scripts/test_install_profiles.py               Task 2
scripts/install_profiles.py                    Task 2
scripts/e2e_install_test.py                    Task 3
docs/validation/running-with-hermes.md         Task 4
docs/knowledge/specs/*.md (five specs)         Task 5 (modify)
docs/knowledge/plans/*.md (five plans)         Task 6 (modify)
docs/validation/*-walkthroughs.md              Task 6 (modify, only those that exist)
```

---

### Task 1: The manifest

**Files:**
- Create: `scripts/profiles.json`

**Interfaces:**
- Consumes: nothing.
- Produces: `scripts/profiles.json`, a list of five objects with keys `short`, `description` (the Hermes profile description, used by kanban routing), and `skill_description` (a one-line frontmatter description). `install_profiles.py` (Task 2) loads it by `short`.

- [ ] **Step 1: Write the check**

```bash
python3 - <<'PYEOF'
import json
m = json.load(open("scripts/profiles.json"))
assert [e["short"] for e in m] == ["artist", "architect", "writer", "wizard", "reviewer"], [e["short"] for e in m]
for e in m:
    assert e["description"].strip() and e["skill_description"].strip() and "\n" not in e["skill_description"]
print("manifest OK:", len(m), "profiles")
PYEOF
```

- [ ] **Step 2: Run it to verify it fails**

Expected: `FileNotFoundError: ... scripts/profiles.json`.

- [ ] **Step 3: Create `scripts/profiles.json`**

Create the `scripts/` directory if needed, then the file with exactly this content:

````json
[
  {
    "short": "artist",
    "description": "First hat of a four-hat YouTube scripting process. Interviews a creator through the idea dump and Grand Payoff for one episode by asking open questions; never authors ideas.",
    "skill_description": "Interview a creator through an episode's idea dump and Grand Payoff, recording only their own words, then submit for review."
  },
  {
    "short": "architect",
    "description": "Second hat of the scripting process. Builds a Setup-Tension-Payoff loop skeleton for an episode from the Artist's output, authoring structure only from the creator's material with provenance on every element.",
    "skill_description": "Build a sourced Setup-Tension-Payoff skeleton from the Artist's output: inputs, loops, sequence, framing, and flow check, with user approval for each loop."
  },
  {
    "short": "writer",
    "description": "Third hat of the scripting process. Drafts the script prose from an approved skeleton in the creator's own voice, only from sources, with placeholders for missing material and the hook written last.",
    "skill_description": "Draft script prose from an approved skeleton in the creator's own voice: voice intake, body, frame, hook last, and a completeness check."
  },
  {
    "short": "wizard",
    "description": "Fourth hat of the scripting process. Runs the retention edit on a drafted script with logged, user-approved changes, then adds visual cues (chapter markers, on-screen text, B-roll notes) the creator approves.",
    "skill_description": "Run the retention edit on a drafted script: simplify, curiosity-gap check, read-aloud cuts, and visual cues, logging every change for approval."
  },
  {
    "short": "reviewer",
    "description": "Independent gate for the scripting pipeline. Scores a stage's output by itemized deduction, passes it at 70% or returns it with a plain critique of what is unclear; never edits or judges idea quality.",
    "skill_description": "Score a pipeline stage's output by itemized deduction, then pass it at 70% or return it with a critique of what is unclear."
  }
]
````

- [ ] **Step 4: Run the check to verify it passes**

Run the check from Step 1.
Expected: `manifest OK: 5 profiles`.

---

### Task 2: The transform and installer, test first

**Files:**
- Create: `scripts/test_install_profiles.py`
- Create: `scripts/install_profiles.py`

**Interfaces:**
- Consumes: `scripts/profiles.json` (Task 1).
- Produces: `scripts/install_profiles.py` with functions `split_sections`, `tag_for`, `wrap_sections`, `rewrite_text`, `retitle`, `render_soul(text, name, prefix)`, `render_agents(text, prefix)`, `render_style(text, prefix)`, `render_skill(text, name, description, prefix)`, `install_profile(entry, args)`, `load_manifest()`, `env_is_blank(path)`, `share_config(config_dir, home, created, refresh)`, `main(argv)`, and the constants `SHORTS`, `REQUIRED`, `FIVE`, `DEFAULT_REPO`. The end-to-end test (Task 3) imports it and `make_repo` from the test file.

- [ ] **Step 1: Write the failing test**

Create `scripts/test_install_profiles.py` with exactly this content:

````python
#!/usr/bin/env python3
"""Unit tests for install_profiles.py. They use a stub `hermes` and temp directories, and never touch the
real ~/.hermes. Run: python3 -m unittest scripts/test_install_profiles.py -v"""
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import install_profiles as ip  # noqa: E402

STUB = """#!/usr/bin/env python3
import json, os, pathlib, sys
args = sys.argv[1:]
with open(os.environ["STUB_LOG"], "a") as f:
    f.write(json.dumps(args) + "\\n")
if args[:2] == ["profile", "create"]:
    home = pathlib.Path(os.environ["STUB_PROFILES"]) / args[2]
    (home / "skills").mkdir(parents=True)
    (home / "memories").mkdir()
    (home / "SOUL.md").write_text("default soul")
    (home / ".env").write_text("# Per-profile secrets for this Hermes profile.\\n# Behavioral settings belong in config.yaml.\\n")
    (home / "config.yaml").write_text("default config")
    if "--no-skills" in args:
        (home / ".no-bundled-skills").write_text("")
if args[:1] == ["-p"] and args[2:4] == ["skills", "opt-in"]:
    home = pathlib.Path(os.environ["STUB_PROFILES"]) / args[1]
    marker = home / ".no-bundled-skills"
    if marker.exists():
        marker.unlink()
    (home / "skills" / "bundled-example").mkdir(parents=True, exist_ok=True)
"""

SOUL_SRC = """# SOUL: The Artist

## Who you are

You are the Artist.

## Hard limits

1. Never author content.

```markdown
## Not a heading (inside a fence)
```

## When you are unsure

Ask the user.
"""
AGENTS_SRC = "# AGENTS: The Artist\n\n## Load order\n\n1. Read `profiles/artist/SOUL.md` and `SKILLS.md`.\n"
STYLE_SRC = "# STYLE: The Artist\n\n## Voice\n\nWarm.\n"
SKILLS_SRC = "# SKILLS: The Artist\n\n## Skill: idea-dump\n\nAsk.\n\n---\n\n## Skill: grand-payoff\n\nChoose.\n"
MEMORY_SRC = "# MEMORY\n\n(none yet)\n"


def make_repo(root, shorts=("artist",)):
    for s in shorts:
        d = Path(root) / "profiles" / s
        d.mkdir(parents=True)
        (d / "SOUL.md").write_text(SOUL_SRC)
        (d / "AGENTS.md").write_text(AGENTS_SRC)
        (d / "STYLE.md").write_text(STYLE_SRC)
        (d / "SKILLS.md").write_text(SKILLS_SRC)
        (d / "MEMORY.md").write_text(MEMORY_SRC)
        (d / "rubrics").mkdir()
        (d / "rubrics" / "scoring.md").write_text("See `SKILLS.md` and `profiles/artist/SOUL.md`.\n")


class TransformTests(unittest.TestCase):
    def test_tag_for(self):
        self.assertEqual(ip.tag_for("## Hard limits"), "hard_limits")
        self.assertEqual(ip.tag_for("## Skill: idea-dump"), "skill_idea_dump")
        self.assertEqual(ip.tag_for("## Who you are", {"Who you are": "identity"}), "identity")

    def test_wrap_ignores_headings_inside_fences(self):
        out = ip.wrap_sections("# T\n\n## A\n\n```md\n## Not\n```\n\n## B\n\nx\n")
        self.assertIn("<a>", out)
        self.assertIn("<b>", out)
        self.assertNotIn("<not>", out)
        self.assertIn("## Not", out)

    def test_wrap_handles_four_backtick_fences(self):
        out = ip.wrap_sections("# T\n\n## A\n\n````md\n```\n## Inner\n```\n````\n\n## B\n\nx\n")
        self.assertNotIn("<inner>", out)
        self.assertEqual(out.count("<a>"), 1)

    def test_wrap_strips_trailing_hr(self):
        out = ip.wrap_sections("# T\n\n## A\n\ntext\n\n---\n\n## B\n\nmore\n")
        self.assertNotIn("\n---\n", out)
        self.assertIn("text\n\n</a>", out)

    def test_rewrite_text(self):
        t = ip.rewrite_text("`profiles/reviewer/rubrics/x.md` and `SKILLS.md`", "script-")
        self.assertIn("~/.hermes/profiles/script-reviewer/rubrics/x.md", t)
        self.assertIn("SKILL.md", t)
        self.assertNotIn("SKILLS.md", t)
        self.assertNotIn("`profiles/", t)

    def test_render_soul(self):
        out = ip.render_soul(SOUL_SRC, "script-artist", "script-")
        self.assertTrue(out.startswith("# The Artist"))
        self.assertIn("<identity>", out)
        self.assertIn("<profile_context>", out)
        self.assertIn("~/.hermes/profiles/script-artist", out)
        self.assertLess(out.index("</identity>"), out.index("<profile_context>"))
        self.assertIn("<hard_limits>", out)
        self.assertIn("## Not a heading (inside a fence)", out)

    def test_render_agents_and_style_titles(self):
        self.assertTrue(ip.render_agents(AGENTS_SRC, "script-").startswith("# The Artist operating contract"))
        self.assertTrue(ip.render_style(STYLE_SRC, "script-").startswith("# The Artist communication"))
        self.assertIn("~/.hermes/profiles/script-artist/SOUL.md", ip.render_agents(AGENTS_SRC, "script-"))

    def test_render_skill(self):
        out = ip.render_skill(SKILLS_SRC, "script-artist", 'Do "it": now', "script-")
        self.assertTrue(out.startswith("---\nname: script-artist\ndescription: "))
        self.assertIn(json.dumps('Do "it": now'), out)
        self.assertIn("<procedure>", out)
        self.assertIn("<skill_idea_dump>", out)
        self.assertIn("# The Artist skills", out)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.repo = base / "repo"
        self.profiles = base / "profiles"
        self.profiles.mkdir()
        self.log = base / "calls.log"
        self.cfg = base / "shared"
        self.cfg.mkdir()
        (self.cfg / ".env").write_text("DUMMY_KEY=not-a-real-secret\n")
        (self.cfg / "config.yaml").write_text("model: smart-router\n")
        stub = base / "hermes"
        stub.write_text(STUB)
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
        self.stub = str(stub)
        os.environ["STUB_LOG"] = str(self.log)
        os.environ["STUB_PROFILES"] = str(self.profiles)

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, *extra, shorts=("artist",)):
        if not self.repo.exists():
            make_repo(self.repo, shorts)
        argv = ["--repo", str(self.repo), "--profiles-dir", str(self.profiles), "--hermes", self.stub,
                "--config-from", str(self.cfg), "--only", ",".join(shorts)] + list(extra)
        return ip.main(argv)

    def calls(self):
        if not self.log.exists():
            return []
        return [json.loads(l) for l in self.log.read_text().splitlines()]

    def test_creates_and_copies(self):
        self.assertEqual(self.run_main(), 0)
        home = self.profiles / "script-artist"
        for f in ("SOUL.md", "AGENTS.md", "STYLE.md"):
            self.assertTrue((home / f).is_file(), f)
        self.assertTrue((home / "skills/script-artist/SKILL.md").is_file())
        self.assertEqual(os.readlink(home / "SKILL.md"), "skills/script-artist/SKILL.md")
        self.assertEqual(os.readlink(home / "MEMORY.md"), "memories/MEMORY.md")
        self.assertIn("(none yet)", (home / "memories/MEMORY.md").read_text())
        rub = (home / "rubrics/scoring.md").read_text()
        self.assertIn("SKILL.md", rub)
        self.assertNotIn("`profiles/", rub)
        self.assertIn("<profile_context>", (home / "SOUL.md").read_text())

    def test_create_command_defaults(self):
        self.run_main()
        create = [c for c in self.calls() if c[:2] == ["profile", "create"]][0]
        self.assertEqual(create[2], "script-artist")
        self.assertNotIn("--no-skills", create)  # default: Hermes seeds its bundled skills
        self.assertIn("--description", create)
        self.assertNotIn("--no-alias", create)  # aliases are on by default
        self.assertNotIn("--clone-from", create)
        describe = [c for c in self.calls() if c[:2] == ["profile", "describe"]]
        self.assertEqual(len(describe), 1)

    def test_no_alias_flag(self):
        self.run_main("--no-alias")
        create = [c for c in self.calls() if c[:2] == ["profile", "create"]][0]
        self.assertIn("--no-alias", create)

    def test_clone_from(self):
        self.run_main("--clone-from", "project-planner")
        create = [c for c in self.calls() if c[:2] == ["profile", "create"]][0]
        self.assertEqual(create[create.index("--clone-from") + 1], "project-planner")
        self.assertNotIn("--no-skills", create)

    def test_reinstall_preserves_memory_and_updates_sources(self):
        self.run_main()
        home = self.profiles / "script-artist"
        (home / "memories/MEMORY.md").write_text("LEARNED FACT\n")
        (self.repo / "profiles/artist/STYLE.md").write_text("# STYLE: The Artist\n\n## Voice\n\nNew voice.\n")
        self.assertEqual(self.run_main(), 0)
        self.assertEqual((home / "memories/MEMORY.md").read_text(), "LEARNED FACT\n")
        self.assertIn("New voice.", (home / "STYLE.md").read_text())
        creates = [c for c in self.calls() if c[:2] == ["profile", "create"]]
        self.assertEqual(len(creates), 1)  # not created twice

    def test_missing_sources_skipped(self):
        self.repo.mkdir()
        (self.repo / "profiles").mkdir()
        self.assertEqual(self.run_main(shorts=("artist",)), 0)
        self.assertEqual(self.calls(), [])

    def test_incomplete_sources_error(self):
        make_repo(self.repo)
        (self.repo / "profiles/artist/STYLE.md").unlink()
        self.assertEqual(self.run_main(), 1)
        self.assertEqual(self.calls(), [])

    def test_dry_run_changes_nothing(self):
        self.assertEqual(self.run_main("--dry-run"), 0)
        self.assertEqual(self.calls(), [])
        self.assertEqual(list(self.profiles.iterdir()), [])

    def test_unknown_profile(self):
        self.repo.mkdir()
        self.assertEqual(ip.main(["--repo", str(self.repo), "--only", "nope"]), 2)

    def test_env_linked_and_config_copied_on_create(self):
        self.run_main()
        home = self.profiles / "script-artist"
        self.assertTrue((home / ".env").is_symlink())
        self.assertEqual(os.readlink(home / ".env"), str(self.cfg / ".env"))
        self.assertFalse((home / "config.yaml").is_symlink())
        self.assertEqual((home / "config.yaml").read_text(), "model: smart-router\n")

    def test_config_kept_on_reinstall_and_refreshed_on_request(self):
        self.run_main()
        home = self.profiles / "script-artist"
        (home / "config.yaml").write_text("tuned: true\n")
        self.run_main()
        self.assertEqual((home / "config.yaml").read_text(), "tuned: true\n")
        self.run_main("--refresh-config")
        self.assertEqual((home / "config.yaml").read_text(), "model: smart-router\n")

    def test_nonempty_env_is_not_replaced(self):
        self.run_main("--no-config")
        home = self.profiles / "script-artist"
        (home / ".env").write_text("OWN=1\n")
        self.run_main()
        self.assertFalse((home / ".env").is_symlink())
        self.assertEqual((home / ".env").read_text(), "OWN=1\n")

    def test_symlinked_config_is_never_written_through(self):
        self.run_main("--no-config")
        home = self.profiles / "script-artist"
        target = Path(self.tmp.name) / "shared.yaml"
        target.write_text("shared\n")
        (home / "config.yaml").unlink()
        (home / "config.yaml").symlink_to(target)
        self.run_main("--refresh-config")
        self.assertEqual(target.read_text(), "shared\n")
        self.assertTrue((home / "config.yaml").is_symlink())

    def test_missing_config_source_warns_but_succeeds(self):
        empty = Path(self.tmp.name) / "empty"
        empty.mkdir()
        self.assertEqual(self.run_main("--config-from", str(empty)), 0)
        home = self.profiles / "script-artist"
        self.assertFalse((home / ".env").is_symlink())
        self.assertEqual((home / "config.yaml").read_text(), "default config")

    def test_no_config_flag(self):
        self.run_main("--no-config")
        home = self.profiles / "script-artist"
        self.assertFalse((home / ".env").is_symlink())
        self.assertEqual((home / "config.yaml").read_text(), "default config")

    def test_clone_from_skips_config_sharing(self):
        self.run_main("--clone-from", "project-planner")
        home = self.profiles / "script-artist"
        self.assertFalse((home / ".env").is_symlink())
        self.assertEqual((home / "config.yaml").read_text(), "default config")

    def test_source_config_files_are_never_modified(self):
        before = ((self.cfg / ".env").read_text(), (self.cfg / "config.yaml").read_text())
        self.run_main()
        self.run_main("--refresh-config")
        after = ((self.cfg / ".env").read_text(), (self.cfg / "config.yaml").read_text())
        self.assertEqual(before, after)

    def test_default_create_seeds_bundled_skills(self):
        self.run_main()
        home = self.profiles / "script-artist"
        self.assertFalse((home / ".no-bundled-skills").exists())
        self.assertEqual([c for c in self.calls() if "opt-in" in c], [])

    def test_no_bundled_skills_flag_creates_lean_profile(self):
        self.run_main("--no-bundled-skills")
        home = self.profiles / "script-artist"
        create = [c for c in self.calls() if c[:2] == ["profile", "create"]][0]
        self.assertIn("--no-skills", create)
        self.assertTrue((home / ".no-bundled-skills").exists())
        self.assertEqual([c for c in self.calls() if "opt-in" in c], [])

    def test_existing_lean_profile_is_opted_in(self):
        self.run_main("--no-bundled-skills")
        self.run_main()
        home = self.profiles / "script-artist"
        opt_in = [c for c in self.calls() if "opt-in" in c]
        self.assertEqual(opt_in, [["-p", "script-artist", "skills", "opt-in", "--sync"]])
        self.assertFalse((home / ".no-bundled-skills").exists())
        self.assertTrue((home / "skills" / "bundled-example").is_dir())

    def test_no_bundled_skills_flag_does_not_opt_in_or_remove(self):
        self.run_main("--no-bundled-skills")
        self.run_main("--no-bundled-skills")
        home = self.profiles / "script-artist"
        self.assertEqual([c for c in self.calls() if "opt-in" in c], [])
        self.assertTrue((home / ".no-bundled-skills").exists())

    def test_existing_root_memory_is_moved_not_lost(self):
        self.run_main()
        home = self.profiles / "script-artist"
        (home / "MEMORY.md").unlink()
        (home / "memories/MEMORY.md").unlink()
        (home / "MEMORY.md").write_text("HAND WRITTEN\n")
        self.run_main()
        self.assertEqual((home / "memories/MEMORY.md").read_text(), "HAND WRITTEN\n")
        self.assertTrue((home / "MEMORY.md").is_symlink())


class RealSourcesTests(unittest.TestCase):
    """Render the real profile sources in this repo, when they exist."""

    def test_real_sources_render_cleanly(self):
        import re
        repo = ip.DEFAULT_REPO
        found = [s for s in ip.SHORTS if (repo / "profiles" / s).is_dir()]
        if not found:
            self.skipTest("no profile sources in %s yet" % repo)
        for short in found:
            src = repo / "profiles" / short
            missing = [f for f in ip.REQUIRED if not (src / f).is_file()]
            self.assertEqual(missing, [], "%s is missing %s" % (short, missing))
            name = "script-" + short
            outs = {
                "SOUL": ip.render_soul((src / "SOUL.md").read_text(), name, "script-"),
                "AGENTS": ip.render_agents((src / "AGENTS.md").read_text(), "script-"),
                "STYLE": ip.render_style((src / "STYLE.md").read_text(), "script-"),
                "SKILL": ip.render_skill((src / "SKILLS.md").read_text(), name, "d", "script-"),
            }
            for kind, out in outs.items():
                opens = re.findall(r"(?m)^<([a-z0-9_]+)>$", out)
                closes = re.findall(r"(?m)^</([a-z0-9_]+)>$", out)
                self.assertEqual(opens, closes, "%s %s: unbalanced tags" % (short, kind))
                self.assertNotIn("`profiles/", out, "%s %s: repo path left in text" % (short, kind))
                self.assertNotIn("SKILLS.md", out, "%s %s: SKILLS.md left in text" % (short, kind))
            self.assertIn("<identity>", outs["SOUL"], short)
            self.assertIn("<profile_context>", outs["SOUL"], short)


class ManifestTests(unittest.TestCase):
    def test_manifest_covers_all_five(self):
        m = ip.load_manifest()
        self.assertEqual(set(m), set(ip.SHORTS))
        for e in m.values():
            self.assertTrue(e["description"].strip())
            self.assertTrue(e["skill_description"].strip())
            self.assertNotIn("\n", e["skill_description"])


if __name__ == "__main__":
    unittest.main()
````

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest scripts/test_install_profiles.py 2>&1 | tail -6`
Expected: `ModuleNotFoundError: No module named 'install_profiles'`.

- [ ] **Step 3: Write the implementation**

Create `scripts/install_profiles.py` with exactly this content:

````python
#!/usr/bin/env python3
"""Install the scriptwriting profiles into Hermes.

Sources live in <repo>/profiles/<short>/. For each profile this script creates the Hermes profile if it is
missing, converts the sources to Hermes format, and copies them into ~/.hermes/profiles/<prefix><short>/.
Re-running updates the source-controlled files. It never overwrites an existing memories/MEMORY.md.

Model and keys: each new profile gets ~/.hermes/.env as a symlink (keys are shared) and a copy of
~/.hermes/config.yaml (so each profile can be tuned). The installer never reads or modifies those two source
files, and never prints any .env content.

Usage:
    python3 scripts/install_profiles.py [--only artist,writer] [--clone-from PROFILE] [--no-alias] [--no-bundled-skills]
        [--config-from DIR] [--no-config] [--refresh-config] [--dry-run]
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_REPO = HERE.parent
MANIFEST = HERE / "profiles.json"
SHORTS = ("artist", "architect", "reviewer", "writer", "wizard")
REQUIRED = ("SOUL.md", "AGENTS.md", "STYLE.md", "SKILLS.md")
FIVE = ("SOUL.md", "AGENTS.md", "STYLE.md", "SKILLS.md", "MEMORY.md")
DEFAULT_MEMORY = "# Durable knowledge\n\nNo verified cross-session facts recorded yet.\n"

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")

PROFILE_CONTEXT = """## Profile context

<profile_context>

At session start, before substantive work, read AGENTS.md, STYLE.md, and SKILL.md from this profile's
HERMES_HOME, normally ~/.hermes/profiles/{name}, and follow the load order in AGENTS.md. Work from the
scriptwriting project directory: WORKFLOW.md, knowledge/, templates/, and series/ are read from the current
working directory, so start this profile with --in <path to the scriptwriting repo>. Report missing context
honestly.

</profile_context>"""

PROCEDURE = """<procedure>

Read AGENTS.md for the session procedure and SOUL.md for the hard limits. Run the skills below in the order
AGENTS.md names them.

</procedure>"""


# ---------------------------------------------------------------- pure transforms

def split_sections(text):
    """Split markdown on level-2 headings that are outside code fences.

    Returns (preamble_lines, [[heading_line, body_lines], ...]).
    """
    pre, secs, cur, fence = [], [], None, None
    for line in text.splitlines():
        in_fence = fence is not None
        if not in_fence:
            m = FENCE_RE.match(line)
            if m:
                fence = (m.group(1)[0], len(m.group(1)))
        elif re.fullmatch(r"\s*%s{%d,}\s*" % (re.escape(fence[0]), fence[1]), line):
            fence = None
        if not in_fence and line.startswith("## "):
            cur = [line, []]
            secs.append(cur)
        elif cur is None:
            pre.append(line)
        else:
            cur[1].append(line)
    return pre, secs


def tag_for(heading, special=None):
    """Turn a '## Heading' line into a snake_case tag name."""
    title = heading[3:].strip()
    if special and title in special:
        return special[title]
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_") or "section"


def wrap_sections(text, special=None):
    """Wrap the body of each level-2 section in an XML-style tag, as the existing Hermes profiles do."""
    pre, secs = split_sections(text)
    out = list(pre)
    while out and out[-1].strip() == "":
        out.pop()
    for heading, body in secs:
        body = list(body)
        while body and body[0].strip() == "":
            body.pop(0)
        while body and body[-1].strip() in ("", "---"):
            body.pop()
        tag = tag_for(heading, special)
        out += ["", heading, "", "<%s>" % tag, ""] + body + ["", "</%s>" % tag]
    return "\n".join(out) + "\n"


def rewrite_text(text, prefix):
    """Point per-profile paths at the profile home and rename SKILLS.md to SKILL.md."""
    text = re.sub(
        r"profiles/(artist|architect|reviewer|writer|wizard)/",
        lambda m: "~/.hermes/profiles/%s%s/" % (prefix, m.group(1)),
        text,
    )
    return text.replace("SKILLS.md", "SKILL.md")


def retitle(text, kind):
    """Rewrite the H1 to match the existing profiles ('# Project Planner operating contract')."""
    if kind == "SOUL":
        return re.sub(r"^# SOUL: ", "# ", text, count=1, flags=re.M)
    suffix = {"AGENTS": "operating contract", "STYLE": "communication", "SKILLS": "skills"}[kind]
    return re.sub(r"^# %s: (.*)$" % kind, r"# \1 " + suffix, text, count=1, flags=re.M)


def render_soul(text, name, prefix):
    text = retitle(rewrite_text(text, prefix), "SOUL")
    wrapped = wrap_sections(text, {"Who you are": "identity"})
    ctx = PROFILE_CONTEXT.format(name=name)
    end = wrapped.find("</identity>")
    if end == -1:
        return wrapped.rstrip("\n") + "\n\n" + ctx + "\n"
    end += len("</identity>")
    return wrapped[:end] + "\n\n" + ctx + wrapped[end:]


def render_agents(text, prefix):
    return wrap_sections(retitle(rewrite_text(text, prefix), "AGENTS"))


def render_style(text, prefix):
    return wrap_sections(retitle(rewrite_text(text, prefix), "STYLE"))


def render_skill(text, name, description, prefix):
    wrapped = wrap_sections(retitle(rewrite_text(text, prefix), "SKILLS"))
    lines = wrapped.splitlines()
    head = 1 if lines and lines[0].startswith("# ") else 0
    lines[head:head] = ["", PROCEDURE]
    frontmatter = "---\nname: %s\ndescription: %s\n---\n\n" % (name, json.dumps(description))
    return frontmatter + "\n".join(lines).rstrip("\n") + "\n"


# ---------------------------------------------------------------- filesystem helpers

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def link(path, target):
    """Create path -> target (relative). Replace a wrong symlink; leave a real file alone."""
    if path.is_symlink():
        if os.readlink(path) == target:
            return
        path.unlink()
    elif path.exists():
        return
    path.symlink_to(target)


def copy_supporting(src, home, prefix):
    """Copy everything in src except the five source files, rewriting text paths in .md files."""
    for item in sorted(src.iterdir()):
        if item.name in FIVE:
            continue
        dest = home / item.name
        if item.is_dir():
            for f in sorted(p for p in item.rglob("*") if p.is_file()):
                target = dest / f.relative_to(item)
                target.parent.mkdir(parents=True, exist_ok=True)
                if f.suffix == ".md":
                    target.write_text(rewrite_text(f.read_text(), prefix))
                else:
                    shutil.copy2(f, target)
        elif item.suffix == ".md":
            write(dest, rewrite_text(item.read_text(), prefix))
        else:
            shutil.copy2(item, dest)


def env_is_blank(path):
    """True if the file has no variable assignments: only blank lines and comments."""
    return all(not line.strip() or line.lstrip().startswith("#") for line in path.read_text().splitlines())


def share_config(config_dir, home, created, refresh):
    """Link .env and copy config.yaml from config_dir (normally ~/.hermes) into the profile.

    .env is symlinked so a key change reaches every profile. config.yaml is copied once, when the profile is
    created (or with --refresh-config), so each profile can be tuned on its own. Neither source file is read
    or modified, and nothing is ever written through a symlink. The profile's own .env is inspected only to see
    whether it holds any variable assignments (a fresh Hermes profile has just a comment header), and its
    contents are never printed. Returns human-readable notes.
    """
    config_dir = Path(os.path.abspath(os.path.expanduser(str(config_dir))))
    env_src, cfg_src = config_dir / ".env", config_dir / "config.yaml"
    env, cfg = home / ".env", home / "config.yaml"
    notes = []

    if not env_src.is_file():
        notes.append("no %s; .env not linked" % env_src)
    elif env.is_symlink():
        if os.readlink(env) != str(env_src):
            notes.append(".env is a symlink to somewhere else; left alone")
    elif env.exists() and not env_is_blank(env):
        notes.append(".env already has variables; left alone")
    else:
        if env.exists():
            env.unlink()
        env.symlink_to(env_src)
        notes.append("linked .env -> %s" % env_src)

    if not cfg_src.is_file():
        notes.append("no %s; config.yaml not copied" % cfg_src)
    elif cfg.is_symlink():
        notes.append("config.yaml is a symlink; left alone")
    elif created or refresh:
        shutil.copyfile(cfg_src, cfg)
        notes.append("copied config.yaml from %s" % cfg_src)
    return notes


def install_memory(src, home):
    """Create memories/MEMORY.md from the source template only if it does not exist."""
    mem = home / "memories" / "MEMORY.md"
    root = home / "MEMORY.md"
    if not mem.exists():
        if root.exists() and not root.is_symlink():
            mem.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(root), str(mem))
        else:
            template = src / "MEMORY.md"
            write(mem, template.read_text() if template.exists() else DEFAULT_MEMORY)
    link(root, "memories/MEMORY.md")


# ---------------------------------------------------------------- installation

def hermes(args, *cmd):
    return subprocess.run([args.hermes, *cmd], check=True, capture_output=True, text=True)


def install_profile(entry, args):
    short, name = entry["short"], args.prefix + entry["short"]
    src = Path(args.repo) / "profiles" / short
    home = Path(args.profiles_dir) / name
    if not src.is_dir():
        print("skipped %s: no sources at %s" % (short, src))
        return True
    missing = [f for f in REQUIRED if not (src / f).is_file()]
    if missing:
        print("ERROR %s: missing source files: %s" % (short, ", ".join(missing)), file=sys.stderr)
        return False
    if args.dry_run:
        print("dry-run %s: would %s and install into %s" % (
            short, "reuse existing profile" if home.exists() else "create profile " + name, home))
        return True

    created = not home.exists()
    if created:
        cmd = ["profile", "create", name, "--description", entry["description"]]
        if args.clone_from:
            cmd += ["--clone-from", args.clone_from]
        elif args.no_bundled_skills:
            cmd.append("--no-skills")
        if args.no_alias:
            cmd.append("--no-alias")
        hermes(args, *cmd)
        print("created profile %s" % name)
    else:
        print("profile %s exists; updating files" % name)

    read = lambda f: (src / f).read_text()
    write(home / "SOUL.md", render_soul(read("SOUL.md"), name, args.prefix))
    write(home / "AGENTS.md", render_agents(read("AGENTS.md"), args.prefix))
    write(home / "STYLE.md", render_style(read("STYLE.md"), args.prefix))
    skill_rel = "skills/%s/SKILL.md" % name
    write(home / skill_rel, render_skill(read("SKILLS.md"), name, entry["skill_description"], args.prefix))
    link(home / "SKILL.md", skill_rel)
    install_memory(src, home)
    copy_supporting(src, home, args.prefix)
    if not args.no_config and not args.clone_from:
        for note in share_config(args.config_from, home, created, args.refresh_config):
            print("  " + note)
    if not args.no_bundled_skills and (home / ".no-bundled-skills").exists():
        hermes(args, "-p", name, "skills", "opt-in", "--sync")
        print("  opted in to Hermes' bundled skills")
    hermes(args, "profile", "describe", name, "--text", entry["description"])
    print("installed %s -> %s" % (short, home))
    return True


def load_manifest():
    entries = json.loads(MANIFEST.read_text())
    return {e["short"]: e for e in entries}


def parse_args(argv):
    p = argparse.ArgumentParser(description="Install the scriptwriting profiles into Hermes.")
    p.add_argument("--only", help="comma-separated short names (%s)" % ", ".join(SHORTS))
    p.add_argument("--repo", default=str(DEFAULT_REPO), help="repo root that contains profiles/")
    p.add_argument("--prefix", default="script-", help="Hermes profile name prefix (default: script-)")
    p.add_argument("--profiles-dir", default=str(Path.home() / ".hermes" / "profiles"))
    p.add_argument("--hermes", default="hermes", help="hermes executable")
    p.add_argument("--clone-from", help="copy model config from this existing profile (e.g. project-planner)")
    p.add_argument("--no-alias", action="store_true", help="do not create the command alias wrapper")
    p.add_argument("--no-bundled-skills", action="store_true",
                   help="create new profiles without Hermes' bundled skills (never removes skills from existing ones)")
    p.add_argument("--config-from", default=str(Path.home() / ".hermes"),
                   help="directory holding the .env and config.yaml to share (default: ~/.hermes)")
    p.add_argument("--no-config", action="store_true", help="do not link .env or copy config.yaml")
    p.add_argument("--refresh-config", action="store_true",
                   help="re-copy config.yaml over existing profiles (overwrites their config)")
    p.add_argument("--dry-run", action="store_true", help="show what would happen; change nothing")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    manifest = load_manifest()
    shorts = [s.strip() for s in args.only.split(",")] if args.only else list(SHORTS)
    unknown = [s for s in shorts if s not in manifest]
    if unknown:
        print("unknown profile(s): %s" % ", ".join(unknown), file=sys.stderr)
        return 2
    ok = True
    for short in shorts:
        try:
            ok = install_profile(manifest[short], args) and ok
        except subprocess.CalledProcessError as e:
            print("ERROR %s: hermes %s failed: %s" % (short, " ".join(e.cmd[1:3]), (e.stderr or "").strip()),
                  file=sys.stderr)
            ok = False
    if ok and not args.dry_run:
        print("\nNext: start a profile with: hermes -p script-<name> chat --in <this repo>. Model and keys come "
              "from ~/.hermes (.env linked, config.yaml copied); use `<name> setup` or --refresh-config to change.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
````

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest scripts/test_install_profiles.py -v 2>&1 | grep -E "^(Ran|OK|FAIL|ERROR)"`
Expected: `Ran 32 tests` and `OK (skipped=1)`. The skip is `test_real_sources_render_cleanly`, which runs for real once any `profiles/<short>/` sources exist; then it must pass with no skip.

- [ ] **Step 5: Dry-run the installer**

Run: `python3 scripts/install_profiles.py --dry-run`
Expected: one `skipped <short>: no sources at ...` line per profile whose sources do not exist yet, and one `dry-run <short>: would ...` line for each that does. Exit code 0. Nothing changes.

---

### Task 3: The end-to-end test

**Files:**
- Create: `scripts/e2e_install_test.py`

**Interfaces:**
- Consumes: `install_profiles.main`, `make_repo` from `scripts/test_install_profiles.py`, and the real `hermes` CLI.
- Produces: an end-to-end check that always deletes its throwaway profile `zz-e2e-artist`.

- [ ] **Step 1: Write the check**

```bash
test -f scripts/e2e_install_test.py && python3 -c "import ast,sys; ast.parse(open('scripts/e2e_install_test.py').read()); print('parses')"
```

- [ ] **Step 2: Run it to verify it fails**

Expected: no output (the file does not exist yet).

- [ ] **Step 3: Create `scripts/e2e_install_test.py`**

Create it with exactly this content:

````python
#!/usr/bin/env python3
"""End-to-end check against the real Hermes CLI.

Creates a throwaway profile (zz-e2e-artist) from a tiny fixture repo, installs into it, verifies what Hermes
sees, checks that re-installing keeps memory, and ALWAYS deletes the profile afterwards.
Run: python3 scripts/e2e_install_test.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import install_profiles as ip  # noqa: E402
from test_install_profiles import make_repo  # noqa: E402

PREFIX = "zz-e2e-"
NAME = PREFIX + "artist"
HOME = Path.home() / ".hermes" / "profiles" / NAME


def hermes(*args, check=True):
    return subprocess.run(["hermes", *args], capture_output=True, text=True, check=check)


def check(cond, msg):
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        raise AssertionError(msg)


def main():
    if HOME.exists():
        print("refusing to run: %s already exists (delete it first)" % HOME)
        return 2
    tmp = tempfile.TemporaryDirectory()
    repo = Path(tmp.name) / "repo"
    make_repo(repo)
    shared = Path(tmp.name) / "shared"  # dummy files: the test never touches the real ~/.hermes/.env or config.yaml
    shared.mkdir()
    (shared / ".env").write_text("DUMMY_KEY=not-a-real-secret\n")
    (shared / "config.yaml").write_text("model:\n  default: smart-router\n")
    common = ["--repo", str(repo), "--only", "artist", "--prefix", PREFIX, "--no-alias", "--config-from", str(shared)]
    try:
        check(ip.main(common + ["--no-bundled-skills"]) == 0, "installer exits 0 (profile created without bundled skills)")
        check((HOME / ".no-bundled-skills").exists(), "--no-bundled-skills leaves the opt-out marker")
        check(ip.main(common) == 0, "re-install opts in to bundled skills")
        check(not (HOME / ".no-bundled-skills").exists() and len([p for p in (HOME / "skills").iterdir() if p.is_dir()]) > 3,
              "opt-in seeded Hermes' bundled skills")
        check((HOME / "skills" / NAME / "SKILL.md").is_file(), "our own skill survived the opt-in")
        check(HOME.is_dir(), "profile directory created by hermes")
        for f in ("SOUL.md", "AGENTS.md", "STYLE.md", "SKILL.md", "MEMORY.md"):
            check((HOME / f).exists(), "root file present: " + f)
        check((HOME / "SKILL.md").is_symlink() and (HOME / "MEMORY.md").is_symlink(), "SKILL.md and MEMORY.md are symlinks")
        check((HOME / "rubrics" / "scoring.md").is_file(), "supporting material copied")
        check((HOME / ".env").is_symlink() and (HOME / ".env").resolve() == (shared / ".env").resolve(), ".env is linked to the shared file")
        check((HOME / "config.yaml").is_file() and not (HOME / "config.yaml").is_symlink()
              and (HOME / "config.yaml").read_text() == (shared / "config.yaml").read_text(), "config.yaml is a copy, not a link")
        listing = hermes("-p", NAME, "skills", "list").stdout
        check(NAME in listing, "hermes lists the profile's skill")
        size = hermes("-p", NAME, "prompt-size").stdout
        check("memory" in size, "prompt-size reports a memory block")
        show = hermes("profile", "list").stdout
        check(NAME in show, "hermes profile list shows the profile")
        (HOME / "memories" / "MEMORY.md").write_text("LEARNED FACT\n")
        check(ip.main(common) == 0, "re-install exits 0")
        check((HOME / "memories" / "MEMORY.md").read_text() == "LEARNED FACT\n", "re-install kept learned memory")
        (HOME / "config.yaml").write_text("tuned: true\n")
        check(ip.main(common) == 0 and (HOME / "config.yaml").read_text() == "tuned: true\n", "re-install kept the tuned config.yaml")
        check((shared / ".env").read_text() == "DUMMY_KEY=not-a-real-secret\n", "shared .env was not modified")
        print("\nALL E2E CHECKS PASSED")
        return 0
    except AssertionError:
        return 1
    finally:
        hermes("profile", "delete", NAME, "-y", check=False)
        hermes("profile", "purge-identity", NAME, check=False)
        tmp.cleanup()
        print("cleanup: %s %s" % (NAME, "still exists!" if HOME.exists() else "removed"))


if __name__ == "__main__":
    sys.exit(main())
````

- [ ] **Step 4: Run the end-to-end test against real Hermes**

Run: `python3 scripts/e2e_install_test.py 2>&1 | grep -vE "^(created|installed|profile |Next:|$)"`
Expected: a `PASS` line for each of the twenty-two checks, then `ALL E2E CHECKS PASSED` and `cleanup: zz-e2e-artist removed`. It uses `--no-alias`, so it adds nothing to `~/.local/bin`. If any check fails the test still deletes the profile.

- [ ] **Step 5: Confirm nothing was left behind**

```bash
ls ~/.hermes/profiles | grep -c "zz-e2e" ; cat ~/.hermes/active_profile
```
Expected: `0`, and your usual active profile unchanged.

---

### Task 4: The run guide

**Files:**
- Create: `docs/validation/running-with-hermes.md`

**Interfaces:**
- Consumes: the installer (Task 2).
- Produces: `docs/validation/running-with-hermes.md`, referenced from every walkthrough's intro after Task 6.

- [ ] **Step 1: Write the check**

```bash
f=docs/validation/running-with-hermes.md
for h in "# Running the profile walkthroughs with Hermes" "install_profiles.py" "hermes -p script-" "chat --in" "setup" "--clone-from" "re-run" "scratch" "Untested" "memories/MEMORY.md"; do
  grep -qF -- "$h" "$f" || echo "MISSING: $h"
done
```

- [ ] **Step 2: Run it to verify it fails**

Expected: `No such file or directory` and `MISSING:` lines.

- [ ] **Step 3: Create `docs/validation/running-with-hermes.md`**

````markdown
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
````

- [ ] **Step 4: Run the check to verify it passes**

Run the check from Step 1.
Expected: no output.

---

### Task 5: Patch the five specs

The earlier specs say agents run in "Paperclip AI or Multica" and that files have no frontmatter. Correct both.

**Files:**
- Modify: the five specs in `docs/knowledge/specs/` (Artist, Architect, Reviewer, Writer, Wizard)

**Interfaces:**
- Consumes: the exact assumption wording in each spec.
- Produces: specs whose assumptions say the agents are Hermes profiles and point at the deployment spec.

- [ ] **Step 1: Write the check**

```bash
n=$(grep -lF "Agents are Hermes profiles" docs/knowledge/specs/2026-09-20-{artist,architect,reviewer,writer,wizard}-profile-design.md 2>/dev/null | wc -l | tr -d ' ')
test "$n" = 5 || echo "NOT PATCHED: $n of 5 specs updated"
m=$(grep -lF "Source files are plain markdown" docs/knowledge/specs/2026-09-20-{artist,architect,reviewer,writer,wizard}-profile-design.md 2>/dev/null | wc -l | tr -d ' ')
test "$m" = 5 || echo "NOT PATCHED: $m of 5 specs updated (frontmatter bullet)"
```

- [ ] **Step 2: Run it to verify it fails**

Expected: `NOT PATCHED: 0 of 5 specs updated` twice.

- [ ] **Step 3: Apply the patches**

Each replacement asserts that the old text occurs exactly once in its file. If an assertion fails, stop and reconcile that spec by hand.

```bash
python3 - <<'PYEOF'
D = "docs/knowledge/specs/2026-09-20-%s-profile-design.md"
HERMES = ("- Agents are Hermes profiles (`script-<name>`) installed from this repo (see the Hermes deployment\n"
          "  spec) and run as tasks/issues in an orchestrator (Paperclip AI, Multica, or Hermes kanban). ")
FM_NEW = ("- Source files are plain markdown with no framework-specific frontmatter. The packaging layer converts\n"
          "  them to Hermes format when installing.")
FM_NEW_OKF = ("- Source files are plain markdown with no framework-specific frontmatter (outside the okf bundle). The\n"
              "  packaging layer converts them to Hermes format when installing.")
FM_OLD = "- Files are plain markdown with no framework-specific frontmatter."
FM_OLD_OKF = "- Files are plain markdown with no framework-specific frontmatter (outside the okf bundle)."

patches = {
  "artist": [
    ("- Agents run as tasks/issues in an orchestrator (Paperclip AI or Multica). This spec relies only on two",
     HERMES + "This spec relies only on two"),
    (FM_OLD, FM_NEW)],
  "architect": [
    ("- Agents run as tasks/issues in Paperclip AI or Multica. Only the abstract states `in progress`,",
     HERMES + "Only the abstract states `in progress`,"),
    (FM_OLD, FM_NEW)],
  "reviewer": [
    ("- Agents run as tasks/issues in Paperclip AI or Multica. Concrete status names, how the Reviewer is woken",
     HERMES + "Concrete status names, how the Reviewer is woken"),
    (FM_OLD, FM_NEW)],
  "writer": [
    ("- Agents run as tasks/issues in Paperclip AI or Multica. Only the abstract states `in progress`, `review`",
     HERMES + "Only the abstract states `in progress`, `review`"),
    (FM_OLD_OKF, FM_NEW_OKF)],
  "wizard": [
    ("- Agents run as tasks/issues in Paperclip AI or Multica. Only the abstract states `in progress`, `review`",
     HERMES + "Only the abstract states `in progress`, `review`"),
    (FM_OLD_OKF, FM_NEW_OKF)],
}
for name, reps in patches.items():
    path = D % name
    s = open(path).read()
    for old, new in reps:
        assert s.count(old) == 1, "expected exactly one match in %s: %r (found %d)" % (path, old[:70], s.count(old))
        s = s.replace(old, new)
    open(path, "w").write(s)
    print("patched:", path)
PYEOF
```

- [ ] **Step 4: Run the check to verify it passes**

Run the check from Step 1.
Expected: no output.

- [ ] **Step 5: Refresh the okf bundle**

```bash
okf validate docs/knowledge
okf lint docs/knowledge
okf index docs/knowledge
```

Expected: `validate` and `lint` report `"errors": 0` and `"warnings": 0`, and `index` lists the regenerated `index.md` files.

---

### Task 6: Patch the walkthrough intros

Each profile plan says to "load the profile" from repo paths. Point them at the installed Hermes profile instead. The same text lives in each plan and, if that plan has been executed, in its built validation doc.

**Files:**
- Modify: the five plans in `docs/knowledge/plans/` (Artist, Architect, Reviewer, Writer, Wizard)
- Modify: `docs/validation/artist-walkthroughs.md`, `architect-walkthroughs.md`, `reviewer-walkthroughs.md`, `writer-walkthroughs.md`, `wizard-walkthroughs.md` (each only if it exists)

**Interfaces:**
- Consumes: `docs/validation/running-with-hermes.md` (Task 4).
- Produces: walkthrough intros that tell the reader to install and start the Hermes profile.

- [ ] **Step 1: Write the check**

```bash
n=$(grep -lF "running-with-hermes.md" docs/knowledge/plans/2026-09-20-{artist,architect,reviewer,writer,wizard}-profile.md 2>/dev/null | wc -l | tr -d ' ')
test "$n" = 5 || echo "NOT PATCHED: $n of 5 plans updated"
for f in docs/validation/{artist,architect,reviewer,writer,wizard}-walkthroughs.md; do
  if test -f "$f"; then grep -qF "running-with-hermes.md" "$f" || echo "NOT PATCHED: $f"; fi
done
```

- [ ] **Step 2: Run it to verify it fails**

Expected: `NOT PATCHED: 0 of 5 plans updated` (and a line for each built validation doc that exists).

- [ ] **Step 3: Apply the patches**

Each replacement asserts the old text occurs exactly once in each file it targets. Files that do not exist are skipped. If an assertion fails, stop and reconcile that file by hand.

```bash
python3 - <<'PYEOF'
import os

artist_old = r"""Load the Artist profile in your agent (load order is in `profiles/artist/AGENTS.md`). Where a walkthrough
starts from a state built by an earlier one, the "Setup" line says so."""
artist_new = r"""Install and start the Artist profile as described in `docs/validation/running-with-hermes.md`
(`hermes -p script-artist chat --in "$SCRATCH/run"`). Where a walkthrough starts from a state built by an
earlier one, the "Setup" line says so."""

architect_old = r"""Create the two fixtures below in the scratch copy, then load the Architect profile (load order is in
`profiles/architect/AGENTS.md`). Unless a walkthrough says otherwise"""
architect_new = r"""Create the two fixtures below in the scratch copy, then install and start the Architect profile as
described in `docs/validation/running-with-hermes.md`. Unless a walkthrough says otherwise"""

reviewer_old = r"""Create the fixtures below in the scratch copy. Load the Reviewer profile (load order is in
`profiles/reviewer/AGENTS.md`) and tell the agent the task has moved"""
reviewer_new = r"""Create the fixtures below in the scratch copy. Install and start the Reviewer profile as described in
`docs/validation/running-with-hermes.md` and tell the agent the task has moved"""

writer_old = r"""Create the fixtures below in the scratch copy. For the Writer walkthroughs, load the Writer profile (load
order is in `profiles/writer/AGENTS.md`). For Walkthroughs 12-13, load the Reviewer profile
(`profiles/reviewer/AGENTS.md`) and tell it the task for stage 3 has moved to `review`."""
writer_new = r"""Create the fixtures below in the scratch copy. For the Writer walkthroughs, install and start the Writer
profile as described in `docs/validation/running-with-hermes.md`. For Walkthroughs 12-13, start the Reviewer
profile the same way and tell it the task for stage 3 has moved to `review`."""

wizard_old = r"""Load the Wizard profile (load order is in `profiles/wizard/AGENTS.md`) for Walkthroughs 1-11.
For Walkthroughs 12-13, load the Reviewer profile (`profiles/reviewer/AGENTS.md`) and tell it the task for
stage 4 has moved to `review`."""
wizard_new = r"""Install and start the Wizard profile as described in `docs/validation/running-with-hermes.md` for
Walkthroughs 1-11. For Walkthroughs 12-13, start the Reviewer profile the same way and tell it the task for
stage 4 has moved to `review`."""

pairs = {
  "artist": (artist_old, artist_new), "architect": (architect_old, architect_new),
  "reviewer": (reviewer_old, reviewer_new), "writer": (writer_old, writer_new), "wizard": (wizard_old, wizard_new),
}
for name, (old, new) in pairs.items():
    for path in ("docs/knowledge/plans/2026-09-20-%s-profile.md" % name, "docs/validation/%s-walkthroughs.md" % name):
        if not os.path.exists(path):
            print("skipped (does not exist):", path)
            continue
        s = open(path).read()
        assert s.count(old) == 1, "expected exactly one match in %s (found %d)" % (path, s.count(old))
        open(path, "w").write(s.replace(old, new))
        print("patched:", path)
PYEOF
```

- [ ] **Step 4: Run the check to verify it passes**

Run the check from Step 1.
Expected: no output.

- [ ] **Step 5: Refresh the okf bundle**

```bash
okf validate docs/knowledge
okf lint docs/knowledge
okf index docs/knowledge
```

Expected: `validate` and `lint` report `"errors": 0` and `"warnings": 0`.

---

### Task 7: Final verification

**Files:** none created. Read-only verification, plus running the tests once more.

- [ ] **Step 1: Unit and end-to-end tests still pass**

```bash
python3 -m unittest scripts/test_install_profiles.py 2>&1 | grep -E "^(Ran|OK|FAIL|ERROR)"
python3 scripts/e2e_install_test.py 2>&1 | grep -E "ALL E2E|FAIL|cleanup"
```
Expected: `Ran 32 tests` with `OK` (with `skipped=1` until real sources exist; no skip and no failure afterward), then `ALL E2E CHECKS PASSED` and `cleanup: zz-e2e-artist removed`.

- [ ] **Step 2: The constraints hold**

```bash
grep -c "auth.json" scripts/install_profiles.py
grep -c "no-alias" scripts/install_profiles.py
ls ~/.hermes/profiles | grep -c "zz-e2e"
stat -f '%Sm' ~/.hermes/.env ~/.hermes/config.yaml
```
Expected: `0` (the installer never mentions `auth.json`), a nonzero count (the opt-out flag exists), `0`, and modification times for your real `.env` and `config.yaml` that match what they were before you ran the tests. The unit test `test_source_config_files_are_never_modified` covers the same guarantee.

- [ ] **Step 3: Spec coverage read-through**

Read `docs/knowledge/specs/2026-09-20-hermes-deployment-design.md` and confirm the file that implements each section:
- §3 layout: matches the File Structure list above.
- §4 installed layout and §5 transform rules: `install_profiles.py` (`render_*`, `install_profile`), and the unit tests.
- §6 installer behavior: `install_profile`, `share_config`, `main`, and the unit tests (flags, aliases on by default, idempotence, memory, `.env` link, `config.yaml` copy).
- §7 running: `docs/validation/running-with-hermes.md`.
- §9 verification: the two test files.
- §2 patches to the earlier specs and plans: Tasks 5 and 6.

- [ ] **Step 4: Install as each profile is built**

This step happens over time, not now. After each profile plan's sources exist, run `python3 scripts/install_profiles.py --only <short>` (add `--clone-from <existing profile>` on the first install if you want model config copied), then follow `docs/validation/running-with-hermes.md`. When every source exists, `python3 scripts/install_profiles.py` installs all five, and the skipped unit test (`test_real_sources_render_cleanly`) runs for real. Do not commit anything.
