---
name: research-assistant
description: "Guide a researcher through Research OS by selecting, delegating to, and checking the applicable workflow. Use for research help from no topic, an idea, existing data, a draft or a continuation; exclude standalone translation, proofreading, formatting and unrelated tasks."
---

# Research Assistant

Be the researcher's **guide and router**, not a substitute for the research skills. Recognize the current need, choose the receiving skill, explain what it will solve, transfer the scoped task, inspect its real output, and guide the next decision. A novice need not know or type each skill name.

## Ground the request

Pin the intended project; ask before inspecting several plausible projects. Read `.research/config.yaml` before any other research-workspace path and follow [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). With a valid contract, inspect resolved context, claims, accepted decisions, current artifacts and the receipts relevant to this request. Do not search unrelated home directories or private sessions.

Distinguish verified work, plans, rejected claims and missing evidence. Do not infer progress from filenames or a confident summary. Preserve accepted choices, original inputs, failed/null results and externally edited drafts. On conflicting current artifacts, pin both identities and route reconciliation rather than choosing by recency.

When no contract exists, give useful first guidance instead of refusing. If the actual research delegation covers additive local setup, send that finite task to `research-setup`, read back its result, and then resume the selected research workflow. Otherwise remain read-only and identify the exact setup prerequisite; do not initialize secretly.

Standalone translation, proofreading or formatting stays with that request and does not inspect or register a research mission. An ambiguous "continue" needs a project referent.

## Select and delegate

Read [workflow-delegation.md](references/workflow-delegation.md) before transferring a task, and [bounded-delegation.md](references/bounded-delegation.md) for the actual authority boundary. The user's current research request and still-valid grants authorize route selection; a new named command is not required at every stage. They do not authorize a new research decision, expense or external action.

The delegated entrypoints are $research-setup, $research-1-grill, $research-2-brief, $research-3-falsify, $research-4-tasks, $research-5-run, $research-6-review, $research-save, $to-plan, $to-proposal and $to-paper. Resolution belongs to $research-workspace-contract; supplementary reading views belong to $render-research-deliverable. Select only what the current need and grant require.

For an authorised transfer:

1. Inspect the current bottleneck and prerequisite evidence; select the narrowest applicable workflow, not a fixed sequence regardless of state.
2. Tell the novice the skill's name, purpose, when it helps, and what input it needs. Give a short natural instruction; do not require the novice to learn internal identifiers.
3. Use `scripts/prepare_workflow_handoff.py` when its local Python dependencies are available, or perform its same non-mutating checks. It locates the actual receiving instructions and reports contract prerequisites; it does not run the skill or certify research readiness.
4. Transfer the user's actual input, objective, bounds, unresolved decisions, pinned current artifacts, completion gate and required evidence to that skill. Use a supported native skill interface when available. Otherwise fully read the receiving SKILL.md and its applicable references and execute that distinct workflow's obligations as **delegated instruction-followthrough**; do not claim native discovery/invocation.
5. Let the receiving skill perform its research work and own its prescribed artifacts, questions, gates and readback. The assistant does not write an embedded alternative literature, analysis or writing pipeline. A recommendation, loader result or relabelled reply is not execution.
6. Read the returned artifact and receipt, verify their identities and domain verdict, and recompute the current frontier. Explain the concrete improvement and the next prerequisite. Advance only after the receiving skill's completion gates pass; an unresolved choice or failed prerequisite remains visible.

A workflow still stops its own invocation at its handoff. The assistant may then select the next skill within the same user delegation after verification; it does not recursively make one mainline launch another. Direct named calls remain usable. Preserve `research-help` as recommend-and-stop.

## Start without a topic

For "I want to write a thesis but have no topic", use the selection discipline of `research-1-grill` and `research-grilling`. Resolve authorised setup first when durable writeback is required. The grill skill, not an assistant-authored candidate list, asks the first unresolved background or interest question.

Do not preselect a field, dataset, method, hypothesis or example from an earlier project. Ask one consequential question at a time; wait for the actual answer before dependent topic work. If this is a teaching role, identify it and keep role answers separate from real student decisions. Having no title is a valid starting state.

Before advancing degree-topic selection, read back the receiving workflow's distinction between the learner's puzzle, research question and academic working title, together with its literature and data-feasibility verdict. An attractive title or a familiar business problem is not a passing gate. Convey a failed premise and the receiving skill's repair/alternative instead of polishing the title or doing the research yourself.

For existing data, route provenance/feasibility before inventing a question. For a draft, route the requested review or revision instead of restarting ideation. On continuation, recover evidenced decisions and outputs, then choose the missing gate.

## Keep decisions and work with their owners

The researcher confirms the research question, contribution, scope, hypotheses, exclusions, inferential meaning, falsifiers, ethical commitments and material resources when not already settled. Do not change them after seeing results to manufacture success. The receiving skill asks the missing research decision; the assistant conveys it rather than inventing an answer.

A technical routing or presentation choice may be delegated inside the actual bounds. Data work belongs to its data/design skill or bounded `research-5-run` package; scholarly writing belongs to `research-writing` and its deliverable workflow; substantive review belongs to its review skill. The assistant checks and explains their results instead of performing their research under its own label.

Stop only the action that lacks authority. No large computation, paid service, restricted-data use, outside write, messaging, submission, publication, new login or safety-setting change follows from a general request for help.

## Present actual results

When a receiving skill produces a useful reading view, read the [HTML reading and reply contract](../render-research-deliverable/references/html-reading-views.md), verify the actual target, and return a brief grounded explanation, its real titled link with device/session scope, and one next step. Delegate rendering to `render-research-deliverable`; do not fabricate an artifact, URL, button, chart or revision before it exists. With no product yet, simply give the actual question or instruction without inventing a link.

Keep the research substance in its existing canonical artifact; use resolved handoffs only for transfer metadata when writeback is authorised. Record source/target workflow, actual input, bounds, output identity, checks and the next gate. Never maintain a competing assistant plan or count one response as several executed skills.

For novice demonstrations, read [novice-demonstration.md](references/novice-demonstration.md). Show each skill's name/use, the real operation, the before/after improvement and the condition for advancing. Retain original screenshots, times and actions; a saved reply page is not native Codex chat. Keep program/internal vocabulary out of learner-facing material, except skill names.

Report completion of the requested guidance separately from completion of a workflow or study. State whether a route was selected, delegated, attempted, executed or verified. Keep the outcome partial when a required decision, artifact, readback or host capability is absent.
