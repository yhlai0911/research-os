---
name: research-grilling
description: "Resolve a research decision tree through one-question-at-a-time interviewing. Use when a research question, plan, construct, mechanism, scope, or trade-off is ambiguous; when the user asks to be grilled; or when another research workflow needs human decisions separated from discoverable facts."
---

# Research Grilling

Resolve a **decision tree** one dependency at a time. Investigate facts; reserve questions for choices that require human judgment.

When selecting a degree-thesis topic, use [academic-topic-admission.md](references/academic-topic-admission.md) before asking for acceptance of the resolved idea. Do not confuse an interesting puzzle, a research question and a supported academic working title.

## Protect the workspace contract

- Resolve `.research/config.yaml` and its canonical context, decisions, and templates paths per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md), then read the resolved context and only the linked artifacts needed for the current branch.
- Treat `.research/` and any configured adapters as one source of truth. Re-read a target immediately before writing, preserve unrelated edits, and link new records from the resolved context.
- Stop with `blocked: research_workspace_not_initialized` when `config.yaml` or a required resolved path is missing. Ask the user to run `$research-setup`; do not create a parallel workspace.
- Report the interview outcome as `complete`, `partial`, or `blocked`. Keep that run outcome distinct from each decision record's lifecycle status. Never convert an unknown fact into a user decision.

## Work the decision tree

1. State the root decision, its scope, and the observable outcome it must enable.
2. Read the workspace and inspect available tools for facts that bear on the root. Resolve discoverable facts without asking the user.
3. Identify the unresolved decision whose answer is prerequisite to the most downstream branches.
4. Ask exactly one question in the exchange. Include:
   - the decision to make;
   - the recommended answer and why;
   - viable alternatives and their material trade-offs;
   - what the answer will unlock.
5. Wait for the answer. Record it before asking the next question, then recompute the tree from the new state.
6. Continue until no in-scope decision remains silently assumed.

## Persist each answer

Create a Research Decision Record only when all four admission tests pass:

1. the choice is hard or costly to reverse;
2. it would be surprising or unsafe without its rationale;
3. viable alternatives create a genuine trade-off; and
4. downstream research artifacts would become ambiguous or invalid if the rationale were lost.

For an admitted decision, write one record under the configured decisions directory. Read `decision-record.md` from the resolved templates directory and preserve its schema. Follow a configured naming rule when present; otherwise scan existing `RDR-NNNN` records and increment the highest number.

Use decision status `accepted` after user confirmation, `proposed` while a choice remains open, `blocked` when a required fact is unavailable, and `superseded` only with a replacement record. Put the question, evidence, and unresolved dependencies in **Context**; the chosen option and rationale in **Decision**; rejected options in **Alternatives**; downstream effects in **Consequences**; and observable reopening conditions in **Revisit when**. Preserve superseded records and point them to the replacement.

For a routine, reversible answer that fails admission, update the owning current artifact or run outcome and its Artifact-index row; do not inflate `DECISIONS` with routing, formatting, or progress preferences.

## Stop branches

- When two accepted decisions conflict, stop the ordinary interview and route both pinned records to `$artifact-reconciliation`. Resume only after it proves one superseding current decision; do not create a third answer without lineage.
- Pause and persist the unresolved frontier as `proposed` records when the user stops the interview; report the run as `partial`.
- Return control to the calling workflow after recording decisions. Do not implement a design, run a study, or make external changes from this skill.

## Complete only when

- Resolve every in-scope branch reachable from the root; leave no unstated choice or `proposed` record on the active frontier.
- Trace every load-bearing factual premise to verified workspace evidence. If one remains `blocked`, report the run `blocked` and do not complete.
- Obtain the user's confirmation of the decision summary.
- Re-read every decision record or owning artifact written in this run, verify template compatibility where applicable, verify that the resolved context points to the current state, and leave no active load-bearing record `proposed` or `blocked`.
