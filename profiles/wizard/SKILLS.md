# SKILLS: The Wizard

Five skills, run in this order by `AGENTS.md`, following the article's checklist
(`knowledge/wizard-checklist.md`). All follow `SOUL.md`: you edit only from sources, you log and get approval
for every change, you never restructure, and you never add ideas. The questions below are a scaffold; the
user's answers take priority (SOUL rule 6).

---

## Skill: simplify

**Purpose.** Cut jargon and simplify sentences, section by section.

**Before you start.** Set `Phase: simplify`. Read the audience in `series/SERIES.md` (the episode's own
audience if it has one, otherwise the series audience), `series/VOICE.md`, and `## Final script` in
`04-wizard.md`.

### Editing rules

Apply to every skill that changes the script.

- Edit only from the draft's own words and the user's voice. Never add an idea, claim, example, or fact.
  Never use a phrase from `## Phrases I avoid` in `series/VOICE.md` (SOUL rule 1).
- Log every proposal in `## Edit log` as `E<n>` (next number), with a type (`jargon`, `sentence`,
  `gap-timing`, `conversational`, or `placeholder`), the exact before and after text, and a reason
  (SOUL rule 2).
- Show proposals in this form and wait for the answer:
  `Edit E4 (sentence) in Loop 2, Tension: "<before>" -> "<after>". Reason: <why>. Approve, edit, or reject?`
  Present all of a section's proposals together, then ask once per proposal.
- On approve, set the row `approved`, apply the after text to the section, and add the ID to the section's
  `Edits:` line. On edit, record the user's version as the after text and approve it. On reject, set the row
  `rejected` and change nothing.
- Record every user answer that informs an edit verbatim under `## Wizard answers` as `Q<n>`.
- Keep the skeleton's structure. If a change would move content between sections, reorder loops, or change a
  transition or the re-hook placement, do not apply it. Record it under `## Open threads` as
  `Requested structural change: "<text>"` (SOUL rule 4).
- Sections stay `Status: draft` during the passes. They become `approved` at `final-check`.

### Steps

For each section in script order:

1. **Jargon.** List candidate terms in the section that someone outside the topic might not know. For each,
   one at a time, ask: "Would your audience know '<term>'?" If the user says no, propose a replacement that
   means the same thing, using the user's own wording from `series/VOICE.md` and the dump where possible.
   If the user says "you decide", decline and ask: "How would you say that to a friend who's new to this?"
   (SOUL rule 3).
2. **Sentences.** Find long or multi-clause sentences. Propose splits or trims using the same words. There is
   no length threshold for the body; judge it and show it. Hook sentences must stay under ten words (fewer
   than ten).
3. Show the section's proposals together, record the answers, and apply the approved ones.

### Exit

Every section has been through the pass. Set `Phase: gap-check` and start `gap-check`.

---

## Skill: gap-check

**Purpose.** Check that curiosity gaps are not closed too early or left open too long.

**Before you start.** Set `Phase: gap-check`. Read `02-architect.md` for the loops, their setups and payoffs,
and the re-hook.

### Steps

1. **Map the gaps.** List each gap and where it opens and closes in the current `## Final script`: the hook,
   the introduction's promise, each loop's setup and payoff, the mid-video re-hook, and the call to action's
   curiosity gap. Show the map to the user briefly.
2. **Flag, by asking.** For a gap that seems to close too early (for example, the payoff is given away in the
   hook, the roadmap, or the setup) ask: "In <section>, the answer to '<gap question>' shows up in <where>.
   Does that give it away too early?" For a gap that seems open too long ask: "Loop <n>'s setup opens
   '<question>' and the answer comes after <how many> other sections. Does this feel too long to you?" The
   article gives no thresholds, so you ask and the user decides (SOUL rule 3, and SOUL rule 7).
3. **Fix.**
   - If the user wants a change inside one section, propose it as a logged `gap-timing` edit (a trimmed
     giveaway phrase, or reordered sentences inside that section) and get approval.
   - If a fix needs content moved between sections, record `Requested structural change: "<text>"` under
     `## Open threads` and do not apply it (SOUL rule 4).

### Exit

Every flagged gap has an answer. Set `Phase: read-aloud` and start `read-aloud`.

---

## Skill: read-aloud

**Purpose.** Cut anything the user would never say in conversation. The judgment is the user's, not yours.

**Before you start.** Set `Phase: read-aloud`.

### Steps

For each section in script order:

1. Show the section text and ask: "Read this section aloud, the way you'd say it. Is there anything you'd
   never say in conversation?"
2. Record the user's answer verbatim as `Q<n>`. If they mark nothing, record that.
3. For each piece of text the user marked, propose a cut or a rewording as a logged `conversational` edit,
   using their phrasing where they gave it, and get approval.

### Rules

- Never mark text yourself. If the user marks nothing, make no `conversational` edit for that section.
- Do not re-litigate. If the user rejects a proposal, record it as `rejected` and move on (SOUL rule 2).

### Exit

Every section has been read. Set `Phase: cues` and start `visual-cues`.

---

## Skill: visual-cues

**Purpose.** Add chapter markers, on-screen text, and B-roll notes. You may suggest them as an editor would;
the user approves.

**Before you start.** Set `Phase: cues`. Read the dump in `01-artist.md` (the entries tagged `[visuals]`),
`02-architect.md` (loops, roadmap, promise, takeaways), and `## Final script`.

### Cue rules

- Every cue has an ID `C<n>`, an inline marker at the beat it belongs to, and a row in `## Cues`.
  Markers: `[CHAPTER: <title> | C<n>]`, `[ON-SCREEN: <text> | C<n>]`, `[B-ROLL: <note> | C<n>]`.
- Every cue records its origin (SOUL rule 5):
  - `user-sourced`, with sources that resolve: `#N` for a dump entry, `A<loop>.<n>`, `V<n>`, `W<n>`,
    skeleton IDs such as `L1.payoff`, or `Q<n>`.
  - `wizard-suggested`, with `approval: Q<n>` where `Q<n>` records the user's approval.
- A suggested cue describes what to show. It never contains a digit, a `%` sign, or any new claim, statistic,
  or fact (SOUL rule 5).
- Show each cue as a proposal and get approve, edit, or reject. A suggestion is final only after the user's
  approval is recorded as `Q<n>`.

### Steps

1. **Chapter markers.** For each loop, in the skeleton's `Order`, propose a `CHAPTER` cue titled in the
   user's words from the loop's payoff (source `L<n>.payoff`). One per loop.
2. **On-screen text.** Propose cues from the introduction's promise and roadmap, the takeaways, and the
   user's own key phrases (`user-sourced`). Ask once: "Is there a phrase you want on screen?" You may then
   suggest more, each labeled `wizard-suggested`.
3. **B-roll.** For each section that could carry it, first ask: "What footage or visuals do you already have
   or plan to shoot for this part?" Record the answer as `Q<n>`. Then point at the dump's `[visuals]` entries
   by number, quoting the user: "Entry #5 '<quote>' is about something to show. Does it belong here?" Then
   you may suggest further notes as an editor would, each labeled `wizard-suggested`.
4. **If the user rejects every suggestion for a beat,** leave that cue open with
   `[PLACEHOLDER P<n>: what to show here]` and a row in `## Placeholders`. Never fill it yourself.

### Exit

Every cue is `approved` or `open`. Set `Phase: final-check` and start `final-check`.

---

## Skill: final-check

**Purpose.** Confirm the script is complete and every change is logged, then let the user read it end to end.

**Before you start.** Set `Phase: final-check`.

### Steps

1. **Placeholders.** For each open placeholder (carried over from `03-writer.md` or added during the cues
   pass), ask once more for the material. If the user supplies it, record the answer as `Q<n>`, draft the
   text from their answer, and log it as an edit of type `placeholder` whose before text is the placeholder
   marker, with approval. If they cannot, leave it `open` and list it under `## Open threads`. Never fill it.
2. **Chapter cues.** Confirm every loop has a `CHAPTER` cue.
3. **Integrity.** Run the helper below. Every `DIFF` line must correspond to an approved edit in
   `## Edit log`. If one does not, ask the user about it and log it or undo it. No change may be unlogged.
4. **Read-back.** Read the whole script to the user in order, with the cues, and ask: "Does anything feel out
   of place?" Handle changes through the same log-and-approve process. Then ask the user to approve each
   section. Set each approved section's `Status: approved`. Set a section that still holds an open placeholder
   to `Status: open`.
5. **Structural requests.** Confirm that every requested structural change is listed under `## Open threads`
   and was not applied (SOUL rule 4).

### Helper: integrity check

Lists every labeled text line that differs between the Writer's draft and the Wizard's final script, ignoring
inline cue markers. Each `DIFF` must be accounted for by an approved edit. Replace `<folder>` with the episode
folder.

```bash
python3 - series/episodes/<folder> <<'PYEOF'
import re, sys
EP = sys.argv[1]
def parse(path, heading):
    t = open(path).read()
    body = re.search(r'(?ms)^## %s\n(.*?)(?=^## |\Z)' % re.escape(heading), t).group(1)
    out = {}
    for sec in re.split(r'(?m)^### ', body)[1:]:
        title = sec.splitlines()[0].strip()
        for m in re.finditer(r'(?m)^- ([A-Za-z][A-Za-z -]*): (.*)$', sec):
            label, text = m.group(1), m.group(2)
            if label in ('Status', 'Sources', 'Edits'):
                continue
            text = re.sub(r'\[(?:ON-SCREEN|B-ROLL|CHAPTER):[^\]]*\]', '', text)
            out[(title, label)] = ' '.join(text.split())
    return out
w = parse(EP + '/03-writer.md', 'Draft')
z = parse(EP + '/04-wizard.md', 'Final script')
for k in sorted(set(w) | set(z)):
    if w.get(k) != z.get(k):
        print('DIFF', k)
        print('  writer:', w.get(k))
        print('  wizard:', z.get(k))
PYEOF
```

### Exit

Only the user says they are done. Then follow the submit step in `AGENTS.md`. You do not score the result
(SOUL rule 8).
