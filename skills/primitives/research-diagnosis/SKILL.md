---
name: research-diagnosis
description: "Diagnose a stalled, contradictory, or failing research project through a tight feedback loop. Use when results collapse, code and theory disagree, a reviewer attack cannot be repaired, a design keeps changing, a replication fails, or the team is doing more work without reducing uncertainty."
---

# Research Diagnosis

Find the **bottleneck** that prevents the next unit of work from reducing uncertainty. Require a tight observable loop before prescribing a repair.

Read [feedback-loop-receipt.md](references/feedback-loop-receipt.md) when the symptom is stochastic, requires human observation, or the initial probe cannot satisfy all four loop gates.

## Load the research contract

1. Read only `.research/config.yaml` first. Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, workpackages, pilots, reviews, papers, proposals, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry, followed by the active brief, workpackage, pilot, review, paper or proposal, decisions, and execution evidence connected to the reported failure.
4. State expected behavior, observed behavior, and the decision currently blocked. Pin the failing artifact versions and environment. Stop when a required resolved path is missing; request workspace repair instead of inventing a parallel path.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry; keep probe and diagnosis outcomes in the diagnosis report rather than adding them as claim statuses.

## Build the feedback loop

1. Define one probe that can reproduce or discriminate the exact symptom.
2. Prefer a deterministic test, minimal dataset, analysis command, trace replay, equation check, or side-by-side old/new comparison.
3. Tighten the loop by reducing irrelevant data and stages while preserving the failure.
4. Run the exact invocation at least once and write a Phase-1 loop receipt containing the command or observation protocol, pinned inputs, raw output locator, verdict, duration, and these four independently checked gates:
   - **exact-symptom red-capable** — a failing result is the reported symptom, not a nearby proxy;
   - **reproducible** — deterministic, or measured with an explicit reproduction count and rate;
   - **fast enough** — seconds-scale when possible, otherwise the smallest faithful bounded proxy with its runtime;
   - **agent-runnable** — unattended by the agent, or a structured HITL capture with a named human action and machine-readable observation.
5. For stochastic failures, predeclare a run count, measure the reproduction rate, and increase repetitions only to distinguish the named hypotheses or until a declared cost/time stop. Never call one lucky pass a fix.
6. For irreducibly long analyses, use the smallest faithful proxy for diagnosis and reserve the full run for final confirmation.

Stop here when any of the four gates cannot be evidenced. Record attempted probes and request the missing data, environment, source artifact, or a structured human capture. Do not turn guesses into a diagnosis.

## Isolate the cause

1. Minimize the failure until every remaining element is load-bearing.
2. Generate three to five ranked, falsifiable hypotheses across theory, construct, data, identification, method, code, environment, and workflow.
3. State one prediction per hypothesis.
4. Show the ranked hypotheses, predictions, and planned first discriminator to the user before testing. This is a non-blocking domain-correction checkpoint unless the user identifies a material error.
5. Test one variable at a time with the tight loop.
6. Tag temporary instrumentation with one unique diagnosis ID; record every file, field, log label, or tracing flag it changes.
7. Identify the earliest stage where expected and observed behavior diverge.
8. Distinguish root cause, contributing condition, and downstream symptom.

Delegate a discovered domain failure to the corresponding primitive instead of expanding this skill into a redesign.

## Repair and write back

Apply a repair only when the user requested one and the cause is supported. Before changing the target, create or identify a regression observation at the correct public seam and capture it red against the pinned pre-repair version. If no truthful seam exists, stop with `blocked: regression_seam_missing`, record the architectural gap, and recommend a bounded workpackage to create that seam instead of adding a misleading check.

After repair, capture the same regression observation green, re-run the minimized loop, and then re-run the original full scenario. Search for the unique diagnosis tag, remove every temporary instrument, and save the zero-match cleanup evidence. A repair is not verified by the new output alone.

Reuse the current registered diagnosis for the same symptom, or create `<diagnosis-id>-diagnosis.md` under the resolved reviews directory (baseline `.research/reviews/`). Begin it with `Status: complete|partial|blocked`, `Updated`, pinned failing artifact identity, and scope. Include the symptom, pinned inputs, loop, hypotheses, probes, root-cause evidence, repair or blocker, and verification. Update affected entries in the resolved claims registry; record any hard-to-reverse repair under the resolved decisions directory.

Register the outcome in the single `## Artifact index` table in the resolved context with columns `Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes`. Update the current row for the same kind and topic when its artifact ID is unchanged. When replacing an artifact, preserve the prior row as `superseded`, add the new current row, and name the prior ID in `Supersedes`.

Set artifact status `complete` when the supported root cause and requested repair outcome are fully verified, or when a diagnosis-only request reaches a supported root cause without claiming a repair. Use `partial` while nonfatal alternatives or full-scenario verification remain open, and `blocked` when no discriminating observation, pinned input, or required resolved path is available.

## Stop conditions

- Stop when the probe reproduces a different failure than the reported symptom.
- Stop when required inputs or environment cannot be pinned.
- Stop before redesigning theory or method from an unsupported hypothesis.
- Stop and report `blocked` when no discriminating observation is available.
- Stop repair when no truthful pre-repair regression seam exists.
- Never label correlation in logs as root-cause evidence.

## Completion criteria

Finish only when:

- the Phase-1 receipt independently passes exact-symptom, reproducibility, runtime, and agent/HITL gates;
- one captured loop detects the exact symptom and any stochastic reproduction rate is reported;
- every tested hypothesis has a prediction and observed result;
- ranked hypotheses were shown before probes and material user corrections were incorporated;
- root cause is separated from symptoms and alternatives;
- when repair is in scope, the same regression observation is captured red before repair and green after repair, and the original scenario is fixed or the repair is explicitly blocked;
- when diagnosis alone is in scope, the supported root cause and unresolved repair boundary are explicit;
- the regression check when applicable, diagnosis report, and affected claim entries agree;
- the unique instrumentation tag has a saved zero-match cleanup check and all diagnostic variants are accounted for;
- the saved diagnosis, affected claim and decision records, and Artifact-index row are re-read and agree on IDs, paths, observations, repair outcome, and status; and
- the run is reported `complete` only after that readback passes, otherwise `partial` or `blocked` according to the status rule above.
