---
type: reference
title: OKF to RAG ingestion
description: Configure and run the local OKF ingestion test through direct NanoGPT embeddings and litellm-pgvector.
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
primary_vector_store_name=delongpa_channel
vector_stores='["delongpa_channel", "another_store"]'
rag_base_url=https://your-vector-service.example
rag_api_key=
NANOGPT_API_KEY=
```

`vector_stores` is a JSON array; `[]` means no additional configured names. Only
`primary_vector_store_name` is a write target. The script does not create stores. Names are exact and case-sensitive.
It looks up the primary name using `GET /v1/vector_stores?limit=100`, requires
exactly one match, and uses the returned ID for uploads and local state. Missing
or duplicate names stop the upload. The current backend has inconsistent cursor
ordering, so lookup rejects incomplete listings (more than 100 stores) until that
backend pagination is fixed. It never silently picks the first matching name.
A nonempty legacy `primary_vector_store_id` setting produces a migration error;
replace it with `primary_vector_store_name`, and change list entries to names.
The API itself still uses IDs in its URLs; this script handles the translation.
An empty primary name disables the pre-commit upload. Process environment values
override matching local settings. Dotenv values are read as data, never sourced
as shell code; use one assignment per line with optional surrounding quotes.

Embedding requests now go directly to `https://nano-gpt.com/api/v1/embeddings`,
using `NANOGPT_API_KEY` from the project `.env` (or a process environment override).
They use the script's `MODEL`, currently `text-embedding-ada-002`, without a
LiteLLM provider prefix. Returned vectors must contain 1,536 finite numbers.
The deployed vector service must use the same embedding model for search.

`rag_base_url` and `rag_api_key` still configure the litellm-pgvector service.
When `rag_api_key` is blank, only the vector-service key falls back to
`model.api_key` in `~/.hermes/config.yml` or `~/.hermes/config.yaml` (override with
`--hermes-config`). An explicit vector key removes the need for Hermes config.
The NanoGPT key is never used as the vector-service fallback. `${NAME}`, `$NAME`,
and `env:NAME` key references resolve from the process environment. The script
does not read or modify Hermes `.env` or save credentials in upload state.

Dependencies are the existing `okf` CLI and Python 3.10+ with PyYAML and requests:

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
hash. Text is embedded in configurable synchronous batches (default 16), then posted to
`/v1/vector_stores/{resolved_store_id}/embeddings/batch` as `content`,
`embedding`, and `metadata`. API IDs and creation timestamps are server-generated.
This prototype uses flat chunks, not the proposed parent-child database design.

### Batch requests and debugging

Following [NanoGPT's batch embedding guide](https://docs.nano-gpt.com/api-reference/embeddings#batch-processing),
the HTTP transport uses the documented `requests.post(url, headers=headers, json=data)`
form from the [direct API example](https://docs.nano-gpt.com/api-reference/embeddings#direct-api-usage).
Each embedding request sends an `input` array of texts and requests
`encoding_format: "float"`. Calls go directly to NanoGPT at
`https://nano-gpt.com/api/v1/embeddings`. These are synchronous requests,
not background `/batches` jobs.

Set `rag_batch_size=32` in the repository `.env` for the commit hook, or override
it for a manual run:

```bash
RAG_DEBUG=1 python3 scripts/push_to_rag.py --batch-size 32
```

Batch size must be 1–2048. Precedence is CLI, process environment, repository
`.env`, then 16. The provider's model/token limits still apply; the maximum
text count is not a guarantee that a request of that size fits those limits.
Batch size does not change chunk hashes or confirmed-upload state.

Progress reports the batch number, text count, model, and `usage.total_tokens`
when returned. Returned indexes associate vectors with their original chunks;
count, index, dimension, and finite-number checks run before storage.
Embedding HTTP 429, 500, 502, 503, and 504 errors get at most three retries after
1, 2, and 4 seconds. Other errors, including HTTP 400, stop immediately.
Vector-store inserts are never automatically retried because they may already
have committed. Confirmed chunks are skipped on later runs; unconfirmed vectors
are not cached across runs.

`RAG_DEBUG=1` in the process environment prints request URLs, headers, and full
embedding request bodies, with the request API key redacted. HTTP error bodies
are shown with the same key redaction. Debug output includes the document text.

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
attempt. With an empty primary name, the RAG step exits successfully without
refreshing OKF, loading credentials, or making network requests.

This runs **before** Git creates the commit. The RAG upload can succeed even if
a later hook rejects the commit or the commit is cancelled. It does not wait for
successful publication and does not introduce a GitHub Actions workflow.

## Repeat runs and prototype limitations

Confirmed chunk hashes are recorded in ignored `.rag/` JSON files, separately
for each vector endpoint, store ID, embedding endpoint, and embedding model. A local
lock prevents concurrent uploads. Repeated runs skip those confirmed chunks.
Preserve this state: another clone or a deleted state directory cannot identify
previously uploaded chunks and may duplicate them. Switching embedding endpoints
also uses separate local state. Changing the embedding model requires a new/rebuilt
store and matching search config.

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
requires the target URL, existing store name, and reachable services.
