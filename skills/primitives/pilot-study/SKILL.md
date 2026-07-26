---
name: pilot-study
description: "Design the smallest end-to-end tracer study or interaction prototype that can expose feasibility, identification, representation, or usability failures. Use when a research idea needs a pilot, proof of concept, minimum viable dataset, preliminary estimation, questionnaire or coding-flow test, research-tool prototype, power reconnaissance, or go-no-go evidence before full execution."
---

# Pilot Study

Build a **tracer study**: preserve the full path from source to research verdict while shrinking volume, duration, and polish. The tracer may test an empirical pipeline or a research interaction, but it must answer one decision-changing question and remain throwaway.

## Load the research contract

1. Read only `.research/config.yaml` first. Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, reviews, pilots, workpackages, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry, followed by the active brief, identification design, data-feasibility review, methodology, falsification plan, workpackages, and ethics decisions at their resolved paths.
4. Name the single uncertainty the pilot must reduce. Stop when the pilot has no decision it can change or a required resolved path is missing; request workspace repair instead of inventing a parallel path.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry; keep pilot progress and `go`, `repair`, or `stop` verdicts in pilot artifacts rather than adding them as claim statuses.

## Select the tracer branch

Choose exactly one:

- **empirical tracer** — the uncertainty concerns data, measurement, estimation, identification, compute, or end-to-end feasibility; or
- **interaction prototype** — the uncertainty concerns a questionnaire or interview flow, annotation/coding schema, research software state model, analytic interface, decision aid, explanation, or other human interaction.

Do not force an interaction question through an empirical acquisition-to-estimation checklist. Do not call static prose an interaction prototype when no actor, action, state change, or observable verdict exists.

## Design the empirical tracer

1. Choose the smallest representative population, period, sample, and variable set that still crosses the hardest seam.
2. Preserve every load-bearing stage: lawful acquisition, validation, transformation, merge, measurement, estimation or computation, diagnostic, and verdict.
3. Remove scale and polish before removing a stage. Reject toy data when it cannot expose the real failure mode.
4. Freeze input identities, versions, timestamps, and environment assumptions.
5. Define one command or explicit sequence that can reproduce the tracer.
6. Define observable outputs and checks for every stage.
7. Predeclare `go`, `repair`, and `stop` thresholds for feasibility, data loss, timing, identification, signal, uncertainty, cost, and ethics.
8. Estimate time, access, compute, human effort, and paid-resource needs. Obtain explicit authority before any purchase, submission, participant contact, or irreversible action.

## Design the interaction prototype

1. Name one actor, task, context, and decision the prototype must inform.
2. Define the observable interaction: starting state, allowed actions, state transitions, visible output, failure state, and one verdict measure.
3. When representation is the uncertainty, build two or three materially different variants under the same content and evaluation conditions. Do not generate cosmetic variants.
4. Stub external writes, licensed systems, personal data, participant contact, and irreversible actions. Use synthetic or consented inputs whose limitations are explicit.
5. Make the smallest runnable path that exposes the hard interaction seam. Capture the exact launch command or protocol, version/hash, screenshots or traces when relevant, and user/evaluator observations.
6. Predeclare `go`, `repair`, and `stop` thresholds for comprehension, task success, error recovery, state visibility, bias, accessibility, time, cost, and ethics as applicable.
7. Treat scaffolding as quarantined under the pilot ID. Preserve decision evidence and the validated minimal core; do not promote the prototype as production research infrastructure.
8. If the verdict is `go`, create a separate bounded workpackage before integrating the validated core. Delete or archive misleading scaffolding only with explicit authority and a receipt.

## Execute only when authorized

When the user requests execution and all approvals exist, run the selected tracer against the frozen inputs. Capture commands or interaction protocol, environment, input hashes or stable source identifiers, outputs, observations, failures, and costs. Treat failed and zero-result runs as evidence; do not silently rerun with changed thresholds.

Delegate unresolved access to `$data-feasibility`, causal design to `$identification-design`, and ethics gates to `$ethics-reproducibility`.

## Write back

Reuse the current registered pilot ID for the same topic, or allocate a stable pilot ID and create `plan.md` under the resolved pilots directory (baseline `.research/pilots/<pilot-id>/plan.md`). Begin the plan with `Status: complete|partial|blocked`, `Updated`, and scope. When executed, add `result.md` beneath the same pilot identifier, give it the same status metadata, and preserve all output pointers there. Update affected entries in the resolved claims registry using only its declared statuses; record whether the result verifies, contests, or blocks each exact claim. Record any threshold-changing repair under the resolved decisions directory.

Register the current plan or executed result in the single `## Artifact index` table in the resolved context with columns `Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes`. Update the current row for the same kind and topic when its artifact ID is unchanged. When replacing an artifact, preserve the prior row as `superseded`, add the new current row, and name the prior ID in `Supersedes`.

For a design-only request, set the plan `complete` when it is executable without hidden assumptions; use `partial` for unresolved nonfatal design dependencies and `blocked` when a required authorization, ethics gate, access premise, or resolved path is unavailable. For an executed pilot, map `go` to `complete`, `repair` to `partial`, and `stop` to `complete` as a diagnostic outcome while marking the dependent study blocked; do not describe an unexecuted plan as an executed result.

## Stop conditions

- Stop when the pilot omits the seam most likely to fail.
- Stop before execution when authorization, licensing, ethics approval, or required access is absent.
- Stop when the sample cannot represent the feasibility question being tested.
- Stop and record the failure when a predeclared stop threshold is crossed.
- Never promote a pilot estimate to confirmatory evidence without a separate design.
- Never contact participants, deploy an interface, or promote prototype scaffolding without separate authority and ethics/access gates.

## Completion criteria

Finish the design only when the branch is explicit; every empirical stage or interaction state has an input, action, output, check, and owner; all decision thresholds are predeclared; scaffolding disposition is named; and `plan.md` is executable without hidden assumptions.

Finish an executed pilot only when the frozen plan, complete receipts, observed checks, result artifact, claim updates, and one `go`, `repair`, or `stop` verdict agree.

Re-read the saved plan and result when present, affected claim and decision records, execution receipts, and Artifact-index row. Verify their IDs, paths, frozen inputs, verdict, and status agree. Report the run `complete` only after that readback passes, otherwise `partial` or `blocked` according to the status rules above.
