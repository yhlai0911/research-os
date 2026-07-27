---
name: research-domain-modeling
description: "Build and sharpen a research domain model. Use when constructs, variables, mechanisms, units, estimands, or field-specific terms are ambiguous; when a decision should be recorded; or when another research workflow needs the project vocabulary and research context maintained."
---

# Research Domain Modeling

Use the **construct** as the unit of meaning. Separate what the study means from how it measures, identifies, or estimates it.

## Protect the workspace contract

- Resolve `.research/config.yaml` and its canonical context, maps, and decisions paths per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md), then read the resolved context and current topic artifacts.
- Use an existing registered domain map; otherwise create `domain-model-<topic-slug>.md` under the resolved maps directory and register it in the resolved context.
- Re-read before writing and preserve unrelated entries. Treat conversation text as a proposal until it is accepted and written to `.research/`.
- Stop with `blocked: research_workspace_not_initialized` when the contract files are absent.

## Build the model

1. Bound the model by research question, population, unit, level, context, and time.
2. Inventory every material term in scope. Classify each as construct, observable variable, measure or proxy, mechanism, actor, action, state, outcome, estimand, estimator, dataset field, or assumption.
3. Give each canonical item a stable ID and record:
   - one precise definition and explicit exclusions;
   - unit, level, time index, and admissible values where applicable;
   - aliases to accept and ambiguous labels to avoid;
   - provenance from evidence or a decision record;
   - status as accepted, proposed, contested, superseded, or blocked.
4. Type every material relation with a direction and scope. Distinguish causal, temporal, logical, measurement, moderation, mediation, identification, and aggregation relations.
5. Detect collisions: one label for multiple constructs, multiple labels for one construct, a proxy presented as the construct, a dataset field presented as an estimand, or a mechanism presented as an outcome.
6. Resolve consequential choices through `$research-grilling`. Reference an RDR from the map only when the choice passes that skill's hard-to-reverse, surprising-without-rationale, genuine-trade-off, and downstream-ambiguity admission tests; keep routine terminology edits in the map.

## Keep the map usable

Begin the artifact with `Status: complete|partial|blocked`, `Updated`, and the bounded scope. Organize it into canonical terms, typed relations, collisions, and open issues. Link to evidence claim IDs instead of duplicating source summaries. Update a definition in place only when its meaning has not changed; supersede it when the change would invalidate downstream work.

## Stop branches

- Mark an item `contested` when sources or collaborators use incompatible meanings.
- Mark it `blocked` when its unit, level, or referent cannot be determined.
- Stop downstream construct or equation work when a required term remains multiply defined; report the exact collision instead of selecting a convenient meaning.
- When two canonical artifacts encode incompatible accepted meanings, route their pinned identities to `$artifact-reconciliation`; do not repair the collision by silently editing the glossary or choosing the later artifact.
- Set artifact status `partial` for unresolved but non-blocking terms and `blocked` when a collision prevents downstream interpretation.

## Complete only when

- Account for every material term used by the in-scope question and artifacts.
- Define each accepted construct independently of its measurement.
- Type every material relation and specify its direction, level, and boundary.
- Resolve or supersede every load-bearing collision. If one remains `contested` or `blocked`, keep the artifact `partial` or `blocked` and do not complete.
- Re-read the map and verify that all referenced decision and evidence IDs exist.
- Set artifact status `complete` only after all preceding criteria pass and no load-bearing item is `proposed`, `contested`, or `blocked`.
