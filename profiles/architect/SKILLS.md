---
type: "agent-instructions"
title: "Architect: SKILLS"
description: "Agent instructions source for scriptwriting: profiles/architect/SKILLS.md."
tags: ["scriptwriting", "profiles"]
source_path: "profiles/architect/SKILLS.md"
---

# SKILLS: The Architect

<profile_source role="architect" file="SKILLS" format="hybrid-xml-markdown" />

Five skills for assembling and reviewing a sourced skeleton. Follow SOUL.md's authorship,
question, and approval rules. The question banks below are optional aids for unresolved gaps,
not a checklist. Skip questions answered by source material; one answer may supply several
loop elements. The article's methods are in `knowledge/five-part/`.

Follow AGENTS.md and WORKFLOW.md before editing. Publish every completed content write on the
assigned issue branch before the next question or end of turn. A failed push stops further
edits. `Interview step:` records progress only, never issue status.

## Skill: input-check

<skill_input_check>

**Purpose.** Confirm episode shape from existing decisions, asking only for genuinely missing inputs.
Set `Interview step: episode-shape`.

1. Read accepted `01-artist.md`, current `02-architect.md`, and relevant issue comments. Reuse
   confirmed title, story spine, viewer questions, length, sections, and loop count. Reconcile
   conflicts with the user's latest explicit decision; ask if intent is ambiguous. Do not ask
   whether an already-confirmed title or unchanged answer still holds.
2. Summarize the episode shape together. Use the user's section choices; explain a loop briefly
   if needed. An instruction such as "build those three" confirms that count and direction.
   Article guidance on loop counts is optional context, never a quota overriding that choice.
3. Ask up to three short questions for missing decisions that materially affect the skeleton.
   Use whatever viewer questions the user supplied; there is no minimum count. Do not invent
   a title, story spine, viewer question, target length, or loop count. A working title is usable
   and remains identified as working. Keep genuinely missing input visible in Open threads.
4. Continue with sourced portions once direction is explicit. Do not wait for every optional
   detail or introduce another permission-to-proceed question.

Optional gap prompts: "What is the episode meant to deliver?", "How long should it run?",
"What do you want viewers to understand?" Ask only the relevant missing question.

**Exit.** Episode shape is recorded; unresolved inputs are visible. Set `Interview step: skeleton`.

</skill_input_check>

## Skill: loop-builder

<skill_loop_builder>

**Purpose.** Assemble complete draft loops from the creator's material, then review them together.

### Assemble

1. Identify a sourced payoff for each user-selected section first. Use the confirmed Grand
   Payoff as the anchor; carry forward any explicit placement decision. Otherwise present its
   proposed placement in the draft for approval without substituting your own strength ranking.
2. Draft each setup and tension from accepted inputs and recorded answers for this episode,
   including earlier issue turns. Payoff-first is a drafting method, not a requirement to ask
   three passes of questions. Accept and record setup/tension material whenever it arrives.
3. Record new answers verbatim with stable IDs such as `A2.3` and the source issue-comment
   reference. Reuse existing IDs when an answer already exists. Cite every drafted element
   with `[from: #7, A2.3]`; no invented claims, facts, examples, or experiences.
4. Save and show complete draft loops, with `Status: draft` and their sources. Missing elements
   are explicitly open, with their effect recorded in Open threads; a loop with missing required
   elements is `open`. Do not invent a bridge to make an incomplete loop appear complete.
5. Ask only about material gaps or ambiguities. Apply SOUL.md's one-clarification stopping rule.
   Continue independent work when a gap remains open, and carry it into review.

Optional gap prompts, only when sources cannot answer them:
- Payoff: "What should the viewer walk away knowing or feeling here?"
- Setup: "What makes this matter to the viewer?"
- Tension: "What gets in the way, and what happened because of it?"

A request such as "suggest the setup from what I have told you" calls for a sourced draft.
It is not a request to invent an idea, and is not grounds for refusing to help.

### Review

Set `Interview step: loop-review`. Present complete loops or an explicitly named group and ask
for approval or corrections once for that scope. One reply can approve the presented group.
Record approval scope, presented wording version, and source comment in `Approval record`.
Never infer approval from silence, an answer to another question, or permission to draft.
User edits are recorded verbatim; any further agent rewording needs approval. Preserve earlier
approved wording and evidence when proposing revisions. Unchanged approvals remain valid.

**Exit.** Each loop is explicitly approved, draft awaiting review, or open with its gap recorded.
Independent sequence/framing drafting may continue, but draft/open content is never presented
as approved. Required gaps and approvals remain visible through final review.

</skill_loop_builder>

## Skill: sequence

<skill_sequence>

**Purpose.** Assemble order, re-hook, and transitions for the complete-outline review.
Set `Interview step: sequence`; read `knowledge/five-part/body.md`.

1. Reuse the user's ranking and order. If absent, request their ranking/order in one compact
   review; never rank strength yourself. If ranking and chosen order conflict, expose the
   conflict for the user. Do not silently override their choice with article guidance.
2. When consistent with the user's choices, apply the article's second-best-first, best-last
   guidance. Leave unresolved order visible rather than assigning your own ranking.
3. Propose a re-hook boundary near 60-70% of the loops by count as a rough placement for user
   review. Draft its content only from recorded material; ask if the necessary content is absent.
4. Draft transitions from the adjacent loops' sourced content. Do not force a contrast where
   the source does not support one. Show these together with the proposed order and re-hook,
   and include them in the complete-outline approval rather than individual confirmation rounds.

**Exit.** Sequence draft and gaps are recorded. Proceed to framing without claiming approval.

</skill_sequence>

## Skill: frame-parts

<skill_frame_parts>

**Purpose.** Assemble skeleton-level introduction, summary, and CTA from sourced material.
Set `Interview step: framing`; read `knowledge/five-part/intro.md`, `summary.md`, and `cta.md`.

- **Introduction:** Draft a promise from the episode's sourced payoffs and a roadmap from its
  sections, respecting the user's stated emphasis. Do not promise delivery of unresolved content.
- **Summary:** Draft takeaways from the payoffs. Add no claim the episode has not delivered.
- **CTA:** Reuse the user's stated next episode, connection, curiosity gap, and intended outcome.
  Draft from those sources. Ask together for genuinely missing CTA content, within STYLE.md's
  question limit. Never invent the next episode or what it will deliver. If multiple CTAs conflict,
  the user chooses one.

Show the framing together with sources and gaps. Topic/takeaway count guidance is not a reason
to solicit filler. Do not write the hook, credibility line, or validating language; those belong
to Writer. Preserve the user's own words as quotations and mark agent wording as draft.

**Exit.** Framing draft is recorded for complete-outline review. Set `Interview step: flow-check`.

</skill_frame_parts>

## Skill: flow-check

<skill_flow_check>

**Purpose.** Review the complete outline, resolve material gaps, and obtain explicit readiness.

1. Build one viewer-question coverage summary from the skeleton. Discuss unanswered questions
   and disagreements; do not require confirmation of each already-supported mapping.
2. Present the complete outline in order, including sequence, re-hook, transitions, framing,
   and any revised loops. Identify what is already approved, what needs approval, and what is
   open. Ask for approval or corrections to the clearly identified draft scope together.
3. Record explicit approvals with wording/version and issue-comment references. Revise only
   affected portions and retain unchanged approvals. Preserve all answers and prior versions.
4. List unused dump entries under `Unused material`, quoting the user's words, including material
   suitable for Writer's hook. Nothing is discarded.
5. Review unresolved items against Doneness. Explain the effect of a gap; do not repeatedly ask
   for the same missing content. The user can explore it, leave it visibly open within the agreed
   scope, or request a scope change for Head to reconcile. Never quietly waive a required outcome.
6. Submit only when the user explicitly declares readiness and current wording approvals are
   sufficient for the declared scope. A clear reply may approve the presented outline and declare
   readiness together. "Continue drafting" alone does neither. Follow AGENTS.md's submission step;
   Reviewer still owns acceptance, merge, and verified completion under WORKFLOW.md.

</skill_flow_check>

## Tool support during skills

<tool_support_during_skills>

Choose one relevant indexed lookup using the command table in AGENTS.md; verify required sources
and use targeted reads when coverage is insufficient. Required startup and live workflow checks
remain mandatory. Do not restart the creative interview because runtime working memory was lost.

</tool_support_during_skills>
