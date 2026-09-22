---
type: playbook
title: Repository-wide OKF indexing
description: Keep canonical Markdown in place while generating searchable copies in the OKF bundle.
tags: [scriptwriting, okf, indexing]
---

# Repository-wide OKF indexing

Source Markdown stays in the root, profiles/, templates/, knowledge/, and docs/ folders.
Its YAML frontmatter is canonical: keep `type`, `title`, `description`, `tags`, and
`source_path` alongside the original content. Preserve existing skill `name` and
`description` fields. The Hermes renderer removes source metadata before rendering
profile instructions and emits its own skill frontmatter.

## Refresh and search

From the repository root:

```bash
python3 scripts/sync_knowledge.py
okf search docs/knowledge --text "Grand Payoff"
okf show docs/knowledge repository/profiles/artist/AGENTS
okf validate docs/knowledge
python3 scripts/sync_knowledge.py --check
```

The sync discovers tracked and non-ignored new Markdown through Git, skipping hidden
runtime directories and `docs/knowledge/` itself. It copies each source byte for byte
into `docs/knowledge/repository/<original-path>`, updates changed copies, and removes
copies of deleted sources recorded in its `.sources.json` manifest. Unmanaged files
are preserved. It then runs `okf index` and `okf validate` against the complete bundle.
`--check` detects stale copies without writing; it does not re-run OKF validation.

Generated copies are Git-ignored and rebuildable. Existing curated plans, specs, and
playbooks in the bundle remain versioned and searchable. After cloning or editing
source Markdown, run the sync before searching. `okf index` alone does not refresh
copies. New source documents must have OKF frontmatter; the sync reports missing
metadata instead of inventing it.

Always edit the original identified by `source_path`, never its generated copy.
Source files named `index.md` or `log.md` are copied as `index.source.md` or
`log.source.md`, because those names are reserved for OKF navigation and history.
Links to those reserved source names may need explicit adjustment in source documents.

## Why copies instead of directory links

A local probe of installed OKF 0.5.0 demonstrated that directory symlinks are skipped,
individual `.md` file symlinks are read, and Markdown without frontmatter is rejected.
Copies avoid depending on symlink traversal, keep generated navigation out of the
source trees, and let the bundle retain its existing layout.

OKF requires frontmatter with a `type` field for every concept document; see the
[OKF specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).
Adding metadata to originals also makes them directly usable by OKF-aware tools;
the generated bundle provides one place to search them together.
