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
SHORTS = ("artist", "architect", "reviewer", "writer", "wizard", "head")
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
        r"profiles/(artist|architect|reviewer|writer|wizard|head)/",
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
