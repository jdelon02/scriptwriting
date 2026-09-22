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

    def test_wrap_is_idempotent_on_prewrapped_sources(self):
        once = ip.wrap_sections("# T\n\n## A\n\ntext\n\n## Who you are\n\nyou\n", {"Who you are": "identity"})
        twice = ip.wrap_sections(once, {"Who you are": "identity"})
        self.assertEqual(once, twice)
        self.assertEqual(twice.count("<a>"), 1)
        self.assertEqual(twice.count("<identity>"), 1)

    def test_rewrite_text(self):
        t = ip.rewrite_text("`profiles/reviewer/rubrics/x.md` and `SKILLS.md`", "script-")
        self.assertIn("~/.hermes/profiles/script-reviewer/rubrics/x.md", t)
        self.assertIn("SKILL.md", t)
        self.assertNotIn("SKILLS.md", t)
        self.assertNotIn("`profiles/", t)

    def test_rewrite_text_handles_head(self):
        t = ip.rewrite_text("`profiles/head/SOUL.md`", "script-")
        self.assertIn("~/.hermes/profiles/script-head/SOUL.md", t)
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

    def test_rendered_context_uses_assigned_content_repository(self):
        out = ip.render_soul(SOUL_SRC, "script-artist", "script-")
        self.assertIn("assigned content repository", out)
        self.assertIn("runtime-supplied worktree", out)
        self.assertNotIn("--in <path to the scriptwriting repo>", out)

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

    def test_no_config_install_reports_runtime_handoff_without_claiming_config_copy(self):
        import contextlib
        import io
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(self.run_main("--no-config", "--no-bundled-skills"), 0)
        text = output.getvalue()
        self.assertIn("runtime-supplied content worktree", text)
        self.assertNotIn("--in <this repo>", text)
        self.assertNotIn("config.yaml copied", text)

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
    def test_manifest_covers_all_profiles(self):
        m = ip.load_manifest()
        self.assertEqual(set(m), set(ip.SHORTS))
        for e in m.values():
            self.assertTrue(e["description"].strip())
            self.assertTrue(e["skill_description"].strip())
            self.assertNotIn("\n", e["skill_description"])


if __name__ == "__main__":
    unittest.main()
