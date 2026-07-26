---
name: design-research-three-ways
description: "Generate and compare three genuinely different research designs under shared constraints. Use when the first design may be anchoring the project, when theory-first, identification-first, and data-first alternatives should be contrasted, or when a design choice needs independent parallel exploration."
---

# Design Research Three Ways

Create a **contrast**, not three cosmetic variants. Hold the question and constraints fixed while changing the design's organizing logic.

## Protect the workspace contract

- Read `.research/config.yaml` first. Resolve its canonical context, maps, and decisions paths, then read the domain, theory, construct, evidence, and feasibility artifacts needed for the question.
- Use an existing registered comparison; otherwise create `design-contrast-<topic-slug>.md` under the resolved maps directory (baseline `.research/maps/`) and register it in the resolved context.
- Record a selected design under the resolved decisions directory; keep all three candidates in the map.
- Register the comparison through one `## Artifact index` table in the resolved context with columns `Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes`; preserve superseded rows.
- Stop with `blocked: research_workspace_not_initialized` when the contract is absent.

## Fix the shared brief

Write a compact shared brief containing the research question, target inference, population, unit, time, ethical limits, available resources, hard data constraints, success criterion, and whether selection is in scope. Resolve consequential ambiguity before generating designs.

## Generate independently

Generate exactly three designs from the shared brief:

1. **Theory-first:** begin with the mechanism and discriminating predictions; choose measurement, data, and tests that expose the mechanism.
2. **Identification-first:** begin with the estimand and credible counterfactual; choose setting, data, and model around the identifying variation.
3. **Data-first:** begin with obtainable data and its real semantics; derive the strongest question and inference the data can support without overclaiming.

Use isolated agents when available and pass each only the shared brief and its lens. Otherwise draft each in a separate pass before comparing them. Do not show one design to another generator.

For every design, specify the question, mechanism, estimand or prediction, constructs and measurement, data, identification, analysis, assumptions, falsifiers, feasibility, ethics, expected contribution, and first tracer study.

Assign stable candidate IDs `<topic-slug>-theory-first`, `<topic-slug>-identification-first`, and `<topic-slug>-data-first` before invoking other skills. For a causal, treatment, transmission, or mechanism-effect target, invoke `$identification-design` separately for every retained candidate and require one identification brief per candidate ID. Reference its estimand, counterfactual, assumptions, and threat verdict; do not share one brief across candidates or treat a matrix score as identification.

Apply each verdict mechanically: keep `identified` eligible; keep `conditionally-identified` or `pilot-required` candidates `partial`; reject or explicitly recast `descriptive-only` candidates for a causal target; mark `blocked` candidates blocked and mark the comparison blocked when all three are blocked.

## Compare on one matrix

Compare all three on inferential strength, theory leverage, measurement validity, data obtainability, identification credibility, falsifiability, execution cost, ethics, time to first evidence, and contribution potential. Identify dominated designs and genuine trade-offs. Consider a hybrid only after the independent comparison.

Begin the comparison with `Status: complete|partial|blocked`, `Updated`, and the shared scope.

## Stop branches

- Regenerate a candidate when it differs only by model, algorithm, sample, or wording.
- Mark a candidate `blocked` rather than filling missing data or identification with assumptions.
- Mark the artifact `blocked` when all candidates fail a required identification or feasibility gate.
- Keep the outcome `partial` when no design dominates and the deciding evidence is unavailable; name the smallest test that would decide.
- Keep the outcome `partial` whenever selection is in scope and the user defers it, even when the comparison itself is finished.
- Do not silently select a design for the user.

## Complete only when

- Produce three designs with different organizing logics and complete fields.
- Apply the same constraints and comparison criteria to all three.
- Expose every hard dependency, fatal flaw, and trade-off.
- Verify a current identification artifact for every retained causal candidate.
- When selection is in scope, obtain an accepted design decision under the resolved decisions directory. When comparison alone is in scope, record selection as out of scope rather than deferred.
- Re-read the comparison and verify that the selected or pending state matches the resolved context.
- Set artifact status `complete` only after all preceding criteria pass; use `partial` whenever an in-scope design decision or nonfatal gate remains open.
