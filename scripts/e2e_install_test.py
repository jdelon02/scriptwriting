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
