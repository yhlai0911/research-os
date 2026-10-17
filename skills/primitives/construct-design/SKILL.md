---
name: construct-design
description: "Define constructs and defensible measurement models. Use when abstract concepts must become variables, proxies, scales, indices, labels, or latent measures; when construct validity is at risk; or when measurement choices could create the finding."
---

# Construct Design

Treat **measurement** as a model linking an abstract construct to observations, not as a convenient column choice.

## Protect the workspace contract

- Resolve `.research/config.yaml` and its canonical context, maps, and decisions paths per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md), then read the relevant domain, theory, literature, data, decision, and evidence artifacts.
- Use an existing registered construct map; otherwise create `constructs-<topic-slug>.md` under the resolved maps directory and register it in the resolved context.
- Preserve canonical construct IDs from the domain model. Record consequential measurement choices under the resolved decisions directory.
- Stop with `blocked: research_workspace_not_initialized` when the contract is absent.

## Design each measurement model

1. Define the construct independently of available measures. State its content domain, exclusions, unit, level, timing, and expected variation.
2. Specify whether indicators are reflective, formative, direct observations, labels, proxies, indices, or latent measures. State the assumed link from construct to indicator.
3. Inventory candidate measures and record source, coverage, frequency, transformation, coding, missingness, accessibility, and provenance.
4. Map each candidate to the construct facet it captures and the facets it omits or contaminates.
5. Audit content, convergent, discriminant, criterion, temporal, and cross-context validity as applicable.
6. Audit reliability, invariance, label error, common-method bias, strategic reporting, post-treatment measurement, and measurement error correlated with treatment or outcome.
7. Compare alternatives and select a primary measure, robustness measures, and negative or placebo measures. Record the decision and why rejected measures failed.
8. State how each measurement failure would bias or reverse the target result.

## Write the construct map

Begin with `Status: complete|partial|blocked`, `Updated`, and scope. For every construct, record its ID, definition, measurement model, candidate and selected indicators, transformations, validity evidence, known threats, decision IDs, evidence claim IDs, and status. Keep raw dataset semantics in the data artifact; link rather than duplicate them.

## Stop branches

- Stop when the only available variable measures a different construct, level, or period.
- Mark the design `blocked` when validity depends on inaccessible labels, undocumented transformations, or untestable invariance.
- Mark it `contested` when reasonable measurement models imply different substantive conclusions.
- Do not choose a measure solely because it produces significance or predictive lift.
- Set artifact status `partial` for unresolved nonfatal validity threats and `blocked` when no measure supports the target construct.

## Complete only when

- Define every in-scope construct before naming its measures.
- Account for every selected indicator's mapping, provenance, transformation, missingness, and likely error.
- Test all material validity classes and specify robustness or falsification checks.
- Record the primary measurement decision and every unresolved threat.
- Re-read the map and verify all construct, decision, data, and evidence references.
- Set artifact status `complete` only after all preceding criteria pass.
