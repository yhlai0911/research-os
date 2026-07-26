---
name: methodology-designer
description: "Align research questions, estimands, constructs, data, models, assumptions, diagnostics, baselines, and evaluation. Use when designing an empirical or theoretical method, choosing among models, translating equations into estimable form, or checking that every hypothesis has an observable test."
---

# Methodology Designer

Use **alignment** as the gate: require an unbroken chain from question to observable evidence, not merely a fashionable method.

## Load the research contract

1. Read only `.research/config.yaml` first. Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, maps, reviews, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry, followed by the active brief, identification design, construct definitions, equations, data-feasibility review, falsification plan, and relevant decisions at their resolved paths.
4. Separate confirmatory questions from exploratory questions. Stop when the primary question, target claim, unit of analysis, or a required resolved path is missing; request workspace repair instead of inventing a parallel path.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry; keep methodology progress and alignment outcomes in the methodology artifact rather than adding them as claim statuses.

## Build the alignment matrix

Create one row per hypothesis, proposition, estimand, or model implication:

`question → claim → estimand or target → construct → observable → data → method → assumptions → diagnostic → baseline → evaluation rule`

Then:

1. Define what observation would support, weaken, or contradict each row.
2. Choose the simplest method that can answer the row under defensible assumptions.
3. Compare credible alternatives. Explain why the selected method dominates for this question and data.
4. Translate equations into estimable or computable objects without changing their semantics.
5. Specify preprocessing, sample construction, model fitting, uncertainty, validation, and sensitivity steps in dependency order.
6. Include naive and domain-relevant baselines. Prevent a complex model from winning only against a weak comparator.
7. Define diagnostics for every load-bearing assumption.
8. Define evaluation metrics, uncertainty intervals, multiplicity handling, and decision thresholds before seeing confirmatory outcomes.
9. Separate robustness checks from alternate research questions.

Delegate unresolved counterfactuals to `$identification-design`, measurement to `$construct-design`, equations to `$equation-builder`, data premises to `$data-feasibility`, and decisive failure tests to `$falsification-first`.

## Decide and write back

Reuse the current registered methodology artifact for the same topic, or create `<artifact-id>-methodology.md` under the resolved briefs directory (baseline `.research/briefs/`). Begin it with `Status: complete|partial|blocked`, `Updated`, and scope. Include the alignment matrix, method comparison, executable sequence, assumptions, diagnostics, baselines, and evaluation rules. Update the relevant entries in the resolved claims registry with their observable tests and methodology pointer. Record only hard-to-reverse method choices under the resolved decisions directory.

Register the outcome in the single `## Artifact index` table in the resolved context with columns `Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes`. Update the current row for the same kind and topic when its artifact ID is unchanged. When replacing an artifact, preserve the prior row as `superseded`, add the new current row, and name the prior ID in `Supersedes`.

Set artifact status `complete` only when every in-scope alignment row and required dependency passes; use `partial` for unresolved nonfatal diagnostics or choices, and `blocked` when the target or a load-bearing data, construct, identification, or path dependency is unavailable.

## Stop conditions

- Stop when a hypothesis has no observable implication.
- Stop when the chosen method requires data, variation, or measurement not yet verified.
- Stop when an estimator is selected before the estimand.
- Stop when exploratory tuning is being presented as confirmatory evidence.
- Return a dependency list instead of filling gaps with conventional defaults.

## Completion criteria

Finish only when:

- every in-scope claim has one complete alignment row;
- every load-bearing assumption has a diagnostic or explicit blocker;
- every model has meaningful baselines and a predeclared evaluation rule;
- confirmatory and exploratory analyses are visibly separated;
- all method choices preserve the declared estimand and construct semantics;
- the methodology artifact and affected claim entries cross-reference each other;
- no row contains an unresolved silent dependency;
- the saved methodology artifact, affected claim and decision records, and Artifact-index row are re-read and agree on IDs, paths, dependencies, and status; and
- the run is reported `complete` only after that readback passes, otherwise `partial` or `blocked` according to the status rule above.
