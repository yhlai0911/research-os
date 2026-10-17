---
name: theory-builder
description: "Build a theory from mechanisms, actors, incentives, frictions, boundary conditions, and discriminating predictions. Use when a paper needs a conceptual framework, propositions, causal chain, competing mechanisms, or economic meaning before equations or methods are chosen."
---

# Theory Builder

Build the **mechanism** before choosing equations or methods. Explain who does what, why, through which link, and under which boundary.

## Protect the workspace contract

- Resolve `.research/config.yaml` and its canonical context and maps paths per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md), then read the relevant domain model, literature map, gap audit, decisions, and evidence claims.
- Use an existing registered theory map; otherwise create `theory-<topic-slug>.md` under the resolved maps directory and register it in the resolved context.
- Reference construct, decision, and evidence IDs. Route undefined terms to `$research-domain-modeling`.
- Stop with `blocked: research_workspace_not_initialized` when the contract is absent.

## Build the mechanism chain

1. State the outcome to explain and the baseline state without the proposed mechanism.
2. Identify actors, information, resources, objectives, actions, constraints, and frictions.
3. Build a directed chain from initiating condition to outcome. For every link, state:
   - the actor or process producing the transition;
   - the incentive, physical law, institutional rule, or information update that makes it occur;
   - the assumption and scope required;
   - the evidence claim or decision supporting it;
   - an observation that could break the link.
4. State moderators, mediators, feedback, timing, aggregation, and equilibrium effects where they materially alter the chain.
5. Derive boundary conditions by changing one necessary condition at a time.
6. Build the strongest rival mechanism that predicts the same headline association.
7. Derive discriminating predictions. Give each prediction a direction or ordering, unit, timing, boundary, observable implication, and result that separates it from the rival.

## Keep theory distinct

Separate assumptions from mechanisms, mechanisms from outcomes, and explanation from relabeling. Avoid circular chains in which the outcome appears in a premise. Delay formal equations until the verbal semantics and causal order are complete; hand them to `$equation-builder`.

Begin the map with `Status: complete|partial|blocked`, `Updated`, and scope. Give every empirical causal prediction a stable prediction or estimand ID, then route any proposed causal test or mechanism-effect estimate to `$identification-design`; theory alone does not identify an effect.

Apply the verdict mechanically when an empirical causal claim is in scope: let `identified` pass; keep `conditionally-identified` or `pilot-required` `partial`; relabel `descriptive-only` as an associational prediction; set the map `blocked` when its target inference is `blocked`.

## Stop branches

- Mark a link `blocked` when no actor, rule, incentive, or process can produce the transition.
- Mark the map `contested` when credible theories imply incompatible links or boundaries.
- Reject predictions that merely restate the mechanism or cannot differ across rivals.
- Return to construct design when a prediction has no defensible observable.
- Set artifact status `partial` for unresolved nonfatal links and `blocked` when no defensible mechanism chain can reach the outcome.

## Complete only when

- Connect the initiating condition to the outcome through an unbroken directed chain.
- Give every material link an assumption, scope, provenance, and falsifier.
- State at least one boundary condition and one credible rival mechanism.
- Derive predictions that distinguish the focal mechanism from the rival.
- Re-read the map and verify every construct, decision, and evidence reference.
- Set artifact status `complete` only after all preceding criteria pass.
