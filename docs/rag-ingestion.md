---
type: reference
title: OKF to RAG ingestion
description: Configure and run the local OKF ingestion test through LiteLLM embeddings and litellm-pgvector.
tags: [scriptwriting, rag, okf, tooling]
---

# OKF to RAG ingestion

`scripts/push_to_rag.py` reads the concepts enumerated by `okf list
docs/knowledge`, then retrieves their full bodies and metadata with `okf show`.
This includes generated repository copies and curated bundle concepts; generated
navigation indexes are not uploaded as document content. Original Markdown is
not independently ingested a second time.

## Configuration

The local `.env` is ignored by Git. Start from `.env.example` in a new checkout.

```dotenv
primary_vector_store_id=vs-your-store
vector_stores='["vs-your-store", "vs-another-store"]'
rag_base_url=https://your-vector-service.example
rag_api_key=
```

`vector_stores` is a JSON array; `[]` means no additional configured IDs. Only
`primary_vector_store_id` is a write target. The script does not create stores.
An empty primary ID disables the pre-commit upload. Process environment values
override these four local settings. Dotenv values are read as data, never sourced
as shell code; use one assignment per line with optional surrounding quotes.

The embedding URL and credential come from `model.base_url` and `model.api_key`
in `~/.hermes/config.yml`, falling back to `~/.hermes/config.yaml`. An alternative
file can be selected with `--hermes-config`. `${NAME}`, `$NAME`, and `env:NAME`
references resolve from the process environment. Export the referenced variable
in the shell running Git if necessary; the script does not read or modify the
Hermes `.env` file. Credentials are neither printed nor saved in upload state.

The embedding request uses model `embedding-model`; returned vectors must contain
1,536 finite numbers. Configure the deployed vector service to use the same model
for search. `rag_base_url` is the litellm-pgvector service URL, which may differ
from the embedding proxy URL. Its key defaults to the resolved Hermes key; use
`rag_api_key` when the service has a different `SERVER_API_KEY`.

Dependencies are the existing `okf` CLI and Python 3.10+ with PyYAML:

```bash
python3 -m pip install -r scripts/requirements-rag.txt
python3 scripts/sync_knowledge.py
python3 scripts/push_to_rag.py --dry-run
python3 scripts/push_to_rag.py
```

Dry run only reads the existing OKF bundle, needs no credentials or configured
store, and performs no HTTP requests or state writes. Manual upload also consumes
the existing bundle; run the sync command first when sources changed.

## Chunking and API behavior

The script splits on Markdown headings outside fenced code blocks. Oversized
sections prefer paragraph boundaries, then newlines, with a default ceiling
of 3,000 characters (`--chunk-chars` overrides it). This is a character bound,
not an exact token count. Oversized sections, XML wrappers, and code fences can
span multiple chunks; section names are retained in metadata.

The paragraph-boundary preference follows the approach in the local
`~/.agents/skills/vectorizeme/ims_meili_index_docs.py` reference. That older script
targets Meilisearch; its upsert behavior is not available through this vector API.

Each chunk carries concept ID, title, type, tags, lifecycle/trust fields when
available, bundle path, filename, section, chunk index, and a content/metadata
hash. Text is embedded in batches of 16, then posted to
`/v1/vector_stores/{primary_vector_store_id}/embeddings/batch` as `content`,
`embedding`, and `metadata`. API IDs and creation timestamps are server-generated.
This prototype uses flat chunks, not the proposed parent-child database design.

## Git integration

The existing `.githooks/pre-commit` performs graph updates and conditional OKF
linting, then invokes `push_to_rag.py --hook`. There is no RAG pre-push hook. This checkout
already uses `core.hooksPath=.githooks`; new clones must enable it:

```bash
git config core.hooksPath .githooks
```

With a primary store configured, pre-commit requires Markdown changes to be fully
staged: it refuses unstaged edits, partial Markdown staging, and untracked Markdown
files that are not ignored. Stage or stash those documents first. Unrelated
unstaged non-Markdown edits are left alone.

It refreshes and validates the OKF bundle with `scripts/sync_knowledge.py`, then
stages only navigation `index.md` files changed or created by that refresh and
not ignored by Git. These indexes join the same commit; generated repository
copies remain ignored. It then uploads new chunks. No after-commit indexing step
is added, so the refresh does not leave tracked index changes outside the commit.
RAG errors stop the commit; refreshed indexes may remain staged after a failed
attempt. With an empty primary ID, the RAG step exits successfully without
refreshing OKF, loading credentials, or making network requests.

This runs **before** Git creates the commit. The RAG upload can succeed even if
a later hook rejects the commit or the commit is cancelled. It does not wait for
successful publication and does not introduce a GitHub Actions workflow.

## Repeat runs and prototype limitations

Confirmed chunk hashes are recorded in ignored `.rag/` JSON files, separately
for each vector endpoint, store ID, proxy endpoint, and embedding model. A local
lock prevents concurrent uploads. Repeated runs skip those confirmed chunks.
Preserve this state: another clone or a deleted state directory cannot identify
previously uploaded chunks and may duplicate them. Changing the model behind the
`embedding-model` alias requires a new/rebuilt store and matching search config.

The current backend only appends. Changed chunks are added; old versions and
deleted documents remain searchable. The script reports how many locally known
chunks are no longer current. This is **not** document replacement or full mirror
synchronization; server-side upsert/deletion is needed for that behavior.

Before each insert, a pending batch is saved. If the request times out or the
response is incomplete, subsequent runs stop because the server may have already
inserted it. Inspect the `pending` hashes against server records (stored as
`metadata.chunk_id`). After confirming outcomes, add accepted hashes to the
state's `uploaded` mapping with value `true` and remove `pending`. Only clear an
unaccepted batch after verifying the server did not insert it. Never blindly
delete state to retry an uncertain request. The script cannot guarantee exactly
once delivery against an append-only API.

## Verification

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_push_to_rag.py
python3 scripts/push_to_rag.py --dry-run
```

Tests use temporary OKF bundles and simulated API responses. They do not upload
documents or call the live embedding service. A successful live ingestion still
requires the target URL, existing store ID, and reachable services.
