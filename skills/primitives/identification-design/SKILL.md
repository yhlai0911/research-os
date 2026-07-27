---
name: identification-design
description: "Design identification around an estimand and credible counterfactual. Use when a study makes causal, mechanism, transmission, treatment, policy, or structural claims; when endogeneity, selection, simultaneity, measurement error, or non-synchronous timing threatens inference; or when predictive evidence is being confused with causal evidence."
---

# Identification Design

Treat the **counterfactual** as the organizing object. Require every causal claim to name what would have happened to the same target under the relevant alternative.

## Load the research contract

1. Resolve `.research/config.yaml` per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, reviews, papers, proposals, workpackages, decisions, and templates paths from that file. Treat paths such as `.research/CONTEXT.md` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry, followed by the active brief, proposal, paper, workpackage, review, and relevant decisions.
4. Identify every causal, mechanism, transmission, treatment, policy, and structural claim in scope. Stop when a required resolved path is absent; ask the user to run or repair the setup workflow instead of inventing a parallel schema.

Use one stable target ID per estimand. Reuse the registered claim, candidate, equation, or estimand ID that triggered this skill. When none exists, allocate `estimand-<topic-slug>-NN` using the next unused two-digit suffix and register it in the resolved context before analysis. Never use a title or mutable wording as the identifier.

## Design the identification

1. Classify each claim as descriptive, predictive, associational, causal, or structural. Downgrade language that exceeds the available design.
2. Define one estimand at a time: target population, unit, treatment or exposure, outcome, horizon, aggregation, and intervention contrast.
3. State the counterfactual in plain language and formal notation when useful. Name the comparison that makes it observable.
4. Draw the timing: assignment or exposure, covariates, outcome, data release, and any revision dates. Expose look-ahead and non-synchronous timing.
5. State the assignment or variation source. Separate design-based variation from functional-form identification.
6. Enumerate all material threats: selection, omitted causes, simultaneity, reverse causality, measurement error, attrition, interference, anticipation, spillovers, and post-treatment conditioning. Mark non-applicable threats explicitly.
7. Map every applicable threat to a design response, diagnostic, sensitivity analysis, or unresolved blocker.
8. Compare at least one credible alternative design. Prefer the weakest assumptions that still identify the estimand.

Delegate construct ambiguity to `$construct-design`, data semantics to `$data-feasibility`, and kill tests to `$falsification-first`. Do not reproduce their detailed workflows here.

## Decide and write back

Assign one verdict per estimand: `identified`, `conditionally-identified`, `pilot-required`, `descriptive-only`, or `blocked`.

Write one design per target ID under the resolved briefs directory as `<target-id>-identification.md`. Do not combine candidates that have different target IDs into one verdict. Update the resolved claims registry with the estimand, identification status, assumptions, threats, and artifact pointer, but never rewrite an existing claim's `id`, `text`, `scope`, provenance, or status history in place. If identification requires a materially narrower or different claim, allocate a new claim ID, preserve the original entry, and record the recast or supersession relation explicitly.

Record a hard-to-reverse design choice with `decision-record.md` from the resolved templates directory. Follow a configured naming rule when present; otherwise scan the resolved decisions directory for `RDR-NNNN` records and increment the highest number. Never invent a second decision filename convention.

Register the brief in the resolved context per the writeback protocol. Map verdicts mechanically:

| Identification verdict | Identification brief | Dependent causal candidate, contribution, or equation |
|---|---|---|
| `identified` | `complete` | eligible for `complete` if every other gate passes |
| `conditionally-identified` | `partial` | `partial` |
| `pilot-required` | `partial` | `partial` |
| `descriptive-only` | `complete` as a diagnostic verdict | `blocked` in causal form; after an explicit noncausal recast, eligible for reassessment |
| `blocked` | `blocked` | `blocked` |

Do not let the mere existence of an identification file satisfy a downstream gate. Downstream skills must read its verdict and current Artifact-index status.

## Stop conditions

- Stop and request a sharper claim when no intervention contrast can be stated.
- Stop at `descriptive-only` when the evidence cannot support a causal counterfactual.
- Stop at `blocked` when treatment timing, outcome timing, assignment, or target population is unknown.
- Stop before selecting an estimator when data feasibility or measurement validity remains unresolved.
- Never present an assumption as verified merely because it is conventional.

## Completion criteria

Finish only when:

- every in-scope causal or structural claim has exactly one estimand and verdict;
- every estimand has a counterfactual, timing model, variation source, and target population;
- every applicable threat has a response or explicit blocker;
- predictive and causal language are separated everywhere reviewed;
- the identification brief and all affected claim entries point to each other; and
- no unresolved issue is described as identified.
