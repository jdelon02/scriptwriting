## Review Cannot Proceed

**Issue:** The Artist stage output file does not exist.

Per `AGENTS.md` Step 2, the Reviewer must read the stage's output file at `series/episodes/<folder>/<NN>-<stage>.md`. For S01E01, this should be `series/episodes/s01e01-<slug>/01-artist.md`.

**Current state:**
- The file `series/episodes/s01e01-<slug>/01-artist.md` does not exist
- No episode folder exists under `series/episodes/`
- No review log exists at `series/episodes/<folder>/reviews/01-artist-review.md`
- Git status shows no untracked files

**What the comment history claims:**
The Artist profile stated in comment `01a0c764-49ca-7b33-afb1-b48606e1c594` that the Artist stage was submitted for review, with the file created and issue status changed to `in_review`. However, there is no evidence in the repository that the file was ever created.

**Required action:**
The Artist stage output file must be created before the Reviewer can proceed. Either:
1. Run the Artist profile to create the file properly, or
2. Provide the file content directly

The task remains in `review` status, but the Reviewer cannot perform the review without the output file.
