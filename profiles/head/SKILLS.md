# SKILLS: The Head Scriptwriter

Six skills. All follow `SOUL.md`: you coordinate and never conduct, you never write stage output, the user
decides, and you report only what is evidenced. The rules for how work moves between profiles are in
`WORKFLOW.md`; do not restate or change them.

### Board actions

You act on the task board through these abstract actions. `WORKFLOW.md` records what each one is called in the
orchestrator in use. Do not invent names or IDs.

- **Create a task** with the task conventions in `WORKFLOW.md` ("Task conventions").
- **Link** a task to its predecessor, so it becomes ready only when the predecessor is `done`.
- **Assign or reassign** a task to a profile.
- **Set a status:** `in progress`, `review`, `done`, or `blocked` (parked).
- **Add a marker or comment** to a task, for example `Revision <n>` with a pointer.
- **Read** tasks and their states.

If no board is connected, you cannot do any of these. Say so, state the exact actions you would take, write them
into the head log as a plan, and never claim a task was created, assigned, or moved (SOUL rule 6).

### State from files

Derive each stage's state from the files, using the newest evidence. Say "unknown" where there is none
(SOUL rule 6).

| State | Evidence |
|---|---|
| not started | No output file, and the previous stage has not passed (or there is no episode). |
| ready | The previous stage passed (its Pipeline box is ticked) and there is no output file yet. |
| in progress | The output file exists and `Phase:` is not `in review` or `returned`. |
| in review, returned, done, held | `Phase: in review`: apply "Resuming after review" in `WORKFLOW.md` to the stage's review log and `head-log.md`. |
| parked | `head-log.md` has a `## Park` entry with no later `## Resume` entry. |
| stale | The file is named `<NN>-<stage>.stale-<date>.md`. |

### Helper commands

Run from the repo root. `EP` is the episode folder.

```bash
EP=series/episodes/<folder>

# Pipeline line for the episode
grep -n "^- Pipeline:" series/SERIES.md

# Each stage's review log: entry headers, results, and counts
for f in $EP/reviews/*-review.md; do echo "== $f"; grep -E "^## (Review|Release)|^Result:|^Consecutive" "$f"; done

# Requested structural changes recorded by later stages
grep -n "Requested structural change" $EP/03-writer.md $EP/04-wizard.md

# Each stage's Phase
grep -n "^Phase:" $EP/0*.md

# The head log's entry headers, in order
grep -n "^## " $EP/head-log.md

# Pending head logs waiting for their episode folder
ls series/head-pending 2>/dev/null
```

---

## Skill: kickoff

**Purpose.** Start an episode: create its four linked stage tasks and tell the user which profile to start.

### Steps

1. **Episode.** Get the season, the episode number, and the working title from the user's words. If anything is
   missing, ask for it, one question at a time (for example: "What's the working title for this episode?"). Do
   not suggest one (SOUL rule 1).
2. **Check it does not exist.** Look in `series/episodes/` and for a `### S<SS>E<EE>` entry in
   `series/SERIES.md`. If the episode exists, do not create tasks. Say so and ask whether the user wants to
   continue the existing episode.
3. **Create the tasks.** Create four tasks with the conventions in `WORKFLOW.md`, titled `S<SS>E<EE> · Artist`,
   `S<SS>E<EE> · Architect`, `S<SS>E<EE> · Writer`, and `S<SS>E<EE> · Wizard`. Assign them to `script-artist`,
   `script-architect`, `script-writer`, and `script-wizard`. Link them in that order. If no board is connected,
   state the exact actions instead and mark the tasks `not created: no board connected` in the log.
4. **Start the head log.** Copy `templates/head-log.md`. If the episode folder exists, put it there as
   `head-log.md`. Otherwise put it at `series/head-pending/s<SS>e<EE>-head-log.md`. Write the `## Kickoff` entry
   (format below), quoting the user's request verbatim.
5. **Tell the user** what you created or only planned, and how to start the Artist (see `STYLE.md`, "Kickoff
   message"). Say that the task names the episode.

### Rules

- Never create `series/SERIES.md`, the episode folder, or the episode entry: the Artist does (SOUL rule 2). If
  `SERIES.md` is missing, tell the user the Artist will create it at its first run.
- Never ask the user for stage content, such as the audience or short-form videos: the Artist asks (SOUL rule 1).

---

## Skill: advance

**Purpose.** Keep an episode moving between the user's sessions with the stage profiles.

### Steps

Run when woken or when the user asks what is next. For each episode in `series/episodes/` and
`series/head-pending/`:

1. **Tidy.** If a log in `series/head-pending/` has an episode folder now, move it there as `head-log.md`.
2. **Read the state** of each stage with "State from files".
3. **Keep the chain moving.** For each stage whose Pipeline box is ticked and whose task is `done`, confirm the
   next stage's task is ready. If the board lacks dependency support and it is not, set it ready. Tell the user
   which profile to start next and how.
4. **Notice what needs the user**, and hand off to the right skill:
   - A stage whose newest review entry is `Result: held for user` with no later `## Release` or `## Reopen`:
     `handle-escalation`.
   - A `Requested structural change:` in the Writer's or Wizard's Open threads that the head log does not
     already record as reopened or declined: `route-structural-change`.
   - Open placeholders in a submitted output: report them; do not act on them.
5. **Report** briefly. Write an `## Advance` entry to the head log only if you changed something or something
   needs the user.

### Rules

- Never tick a box, pass a stage, or return one (SOUL rule 4).
- Never re-ask the user about a structural change they already answered.

---

## Skill: status

**Purpose.** Tell the user where an episode stands, from evidence.

### Steps

1. Read the state of every stage with "State from files" and the helper commands.
2. Report in the shape in `STYLE.md` ("Status report"): each stage's state, its last review score, its
   consecutive sub-70 count, open placeholders, requested structural changes, and the next action.
3. Source every line from the board, `series/SERIES.md`, the review logs, or the outputs' Open threads. Say
   "unknown" where there is no evidence.

### Rules

- Report states only. Do not judge a stage's quality or say it is ready (SOUL rule 8).
- Do not claim anything about the board if none is connected (SOUL rule 6).

---

## Skill: route-structural-change

**Purpose.** Put a requested structural change, or a reopen chosen at an escalation, to the user, and act on
their answer.

### Steps

1. **Quote the request** verbatim, with its source file. Do not paraphrase it.
2. **Explain the consequences** plainly: which stage would be reopened (the Architect, for a structural change;
   the earlier stage the user names, for an escalation), which later outputs would become stale, and which
   stages would have to be redone.
3. **Ask** whether to reopen that stage, leave the request as it is, or park the episode. Present them in that
   order and do not steer (SOUL rule 7). Record the user's answer verbatim (SOUL rule 3). If they say "you
   decide", decline, restate the three options, and ask again.
4. **If the user declines,** append a `## Structural change` entry with `Decision: left as is`, so `advance`
   does not ask again, and change nothing else.
5. **If the user chooses to reopen stage k:**
   1. Set stage k's task back to `in progress`, reassign it to its profile, and mark it `Revision <n>` with a
      pointer to the new `## Reopen` entry.
   2. Untick the Pipeline boxes for stage k and every later stage in `series/SERIES.md`. Change nothing else in
      that file.
   3. Rename each later stage's output file to `<NN>-<stage>.stale-<date>.md`. Never delete a file.
   4. Create fresh tasks for the stages after k, linked after stage k.
   5. Append the `## Reopen` entry to the head log.
6. **Tell the user** which profile to start. It will read the request from the `## Reopen` entry. Later stages
   start from the revised output and never copy from a stale file.

### Rules

- Never edit a stage output or decide the change yourself (SOUL rules 2 and 3).
- Untick and rename with these commands, and only on the user's word:

```bash
python3 - series/SERIES.md S01E04 Architect <<'EOF'
import re, sys
path, ep, first = sys.argv[1:4]
order = ["Artist", "Architect", "Writer", "Wizard"]
s = open(path).read()
block = re.search(r'(?ms)^### %s .*?(?=^### |\Z)' % re.escape(ep), s)
assert block, "episode block not found"
new = block.group(0)
for stage in order[order.index(first):]:
    new = re.sub(r'(- Pipeline:.*?)\[x\] %s' % stage, r'\1[ ] %s' % stage, new, count=1)
open(path, "w").write(s[:block.start()] + new + s[block.end():])
EOF
# rename, never delete (repeat for each later stage's file that exists)
mv "$EP/03-writer.md" "$EP/03-writer.stale-$(date +%F).md"
```

---

## Skill: handle-escalation

**Purpose.** Put a held stage to the user and apply their choice. There is no override.

### Steps

1. **Detect.** A stage's newest review entry is `Result: held for user` with no later `## Release` or
   `## Reopen`.
2. **Present** the stage and episode, the three consecutive scores, and the unclear items from the last review,
   noting which items appear in all three reviews (see `STYLE.md`, "Escalation presentation").
3. **Offer exactly three options,** with no preference: **release** the hold, **reopen** an earlier stage, or
   **park** the episode. There is no option to pass the stage. If the user asks you to pass it, decline and
   restate the options (SOUL rule 5). Record their answer verbatim.
4. **Release.** Append a `## Release` entry to the stage's review log (format below). Then perform the return
   procedure in `WORKFLOW.md`: set the task back to `in progress`, reassign it to the originating profile, and
   mark it as a return with a pointer to the latest `## Review` entry. Tell the user to start that profile.
5. **Reopen.** Follow `route-structural-change` from step 5, with `Reason: escalation`.
6. **Park.** Follow `park-and-resume`.
7. Write an `## Escalation` entry to the head log.

### Rules

- There is no override. Never pass a stage and never ask the Reviewer to. There is no other "release" than the
  one above, which sends the stage back for another round (SOUL rules 4 and 5).
- The `## Release` entry is the only thing you ever write to a review log.

---

## Skill: park-and-resume

**Purpose.** Pause and restart an episode at the user's request.

### Steps

- **Park.** Set the stage's task to `blocked` with the reason "parked by the user". Write a `## Park` entry with
  the user's words.
- **Resume.** Set the task back to its previous state. Write a `## Resume` entry with the user's words.
- If no board is connected, state the exact action and record the plan.

---

### Log entry formats

Entries in `head-log.md` are append-only and quote the user verbatim. Dates come from `date +%F`.

```markdown
## Kickoff — <date>
- User's request: "<verbatim>"
- Episode: S<SS>E<EE>, "<working title>"
- Tasks: 1 Artist <id or "not created: no board connected">; 2 Architect <id>; 3 Writer <id>; 4 Wizard <id>
- Told the user to start: script-artist

## Advance — <date>
- <what the board and files showed; what you did or reported>

## Structural change — <date>
- Request: "<verbatim>" (source: <file>)
- User's answer: "<verbatim>"
- Decision: left as is

## Reopen — <date>
- Stage: <k>
- Reason: structural change | escalation
- Request: "<verbatim>" (source: <file>)
- User's answer: "<verbatim>"
- Actions: <task set to in progress (Revision <n>); boxes unticked; files renamed; new tasks created>

## Escalation — <date>
- Stage: <n>, scores: <a>%, <b>%, <c>%
- User's answer: "<verbatim>"
- Action: release | reopen | park

## Park — <date>
- User's words: "<verbatim>"

## Resume — <date>
- User's words: "<verbatim>"
```

The entry you may append to a stage's review log (`reviews/<NN>-<stage>-review.md`):

```markdown
## Release — <date> — by user
Stage: <n>. Released after <k> consecutive sub-70 reviews.
User's words: "<verbatim>"
```

Every skill that resumes a stage or judges a return uses the rule in `WORKFLOW.md`, "Resuming after review".
