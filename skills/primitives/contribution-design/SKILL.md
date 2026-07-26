---
name: contribution-design
description: "Design a defensible contribution delta against the closest literature. Use when a research idea needs theoretical, empirical, measurement, identification, data, or predictive contribution claims; when novelty exists but significance is unclear; or when a reviewer asks what the paper changes."
---

# Contribution Design

Express each contribution as a **delta**: the closest literature establishes a baseline, this project changes it, and the change alters a material inference.

## Protect the workspace contract

- Read `.research/config.yaml` first. Resolve its canonical context, claims, and briefs paths, then read the relevant gap audit, landscape, design, theory, and claim entries.
- Use an existing registered brief; otherwise create `contribution-design-<topic-slug>.md` under the resolved briefs directory (baseline `.research/briefs/`) and register it in the resolved context.
- Register it through one `## Artifact index` table in the resolved context with columns `Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes`; preserve superseded rows.
- Reference evidence, map, review, and decision IDs instead of duplicating their contents.
- Stop with `blocked: research_workspace_not_initialized` when the workspace contract is absent.

## Design the delta

1. Select the closest literature baseline, not a broad field-level straw man.
2. State one candidate delta at a time:
   - **Baseline:** what the closest work already establishes.
   - **Change:** what this project adds, revises, distinguishes, or overturns.
   - **Consequence:** which belief, estimate, mechanism, boundary, prediction, measure, or decision changes.
   - **Proof:** which result and evidence standard would demonstrate the change.
3. Classify the delta as theoretical, empirical, measurement, identification, data, methodological, or predictive. Separate independent deltas; do not inflate one change into a contribution list.
4. Test necessity: remove the delta and state whether the paper's conclusion becomes identical to prior work.
5. Test defensibility against the closest reviewer attack, including "new setting only," "new data only," "better performance only," "relabeling," and "method without changed inference."
6. Match the wording to the actual design. Reserve causal, structural, mechanism, and generalization claims for evidence capable of supporting them.

## Rank and write

Rank candidate deltas by materiality, evidentiary feasibility, and dependence on unresolved assumptions. Designate one primary delta and only genuinely distinct secondary deltas.

Begin the brief with `Status: complete|partial|blocked`, `Updated`, and scope. For each retained delta, record the closest neighbors, exact difference, consequence, required result, falsifier, scope boundary, evidence claim IDs, dependencies, and status. Preserve rejected deltas with the reason they failed.

## Stop branches

- Stop with `blocked: gap_not_audited` when no current gap verdict exists.
- Reject or recast the delta when the gap audit is `fails` or `blocked`.
- Mark the brief `partial` when the consequence is material but the design cannot yet prove it.
- Route every retained causal, treatment, transmission, or mechanism-effect delta through `$identification-design`; keep the brief `partial` until a current identification artifact supports its claim strength.
- Apply the identification verdict mechanically: let `identified` pass; keep `conditionally-identified` or `pilot-required` `partial`; recast `descriptive-only` as a noncausal delta before completion; set the contribution `blocked` when its primary delta is `blocked`.
- Remove promotional adjectives that cannot be replaced by a comparison or test.

## Complete only when

- Tie every retained delta to the closest literature and a surviving audited gap.
- State a changed inference and a discriminating result for every retained delta.
- Align every claim with the theory, measurement, design, and available evidence.
- Record the strongest dismissal and a concrete answer or unresolved dependency.
- Re-read the brief and verify that every referenced artifact and claim ID exists.
- Set artifact status `complete` only after all preceding criteria pass.
