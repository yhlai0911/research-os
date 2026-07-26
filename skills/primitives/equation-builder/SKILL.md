---
name: equation-builder
description: "Derive and audit research equations so every symbol, operator, unit, assumption, boundary condition, and limiting case has economic meaning. Use for mathematical models, PDEs, stochastic processes, optimization, estimators, or when a borrowed equation risks being only an analogy."
---

# Equation Builder

Make **semantics** constrain the mathematics. Require every expression to represent a defined mechanism, estimand, decision, or measurement relation.

## Protect the workspace contract

- Read `.research/config.yaml` first. Resolve its canonical context and maps paths, then read the relevant domain, theory, construct, design, decision, and evidence artifacts.
- Use an existing registered equation map; otherwise create `equations-<topic-slug>.md` under the resolved maps directory (baseline `.research/maps/`) and register it in the resolved context.
- Register it through one `## Artifact index` table in the resolved context with columns `Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes`; preserve superseded rows.
- Preserve symbol meanings already accepted in the domain model. Route semantic conflicts to `$research-domain-modeling` before deriving further.
- Stop with `blocked: research_workspace_not_initialized` when the contract is absent.

## Derive from meaning

1. State in words what the equation must represent and which question, mechanism, or estimand it serves.
2. Define every primitive before use. Record symbol, meaning, type, domain, unit, index, timing, observability, and provenance in one symbol table.
3. State operators, objective, constraints, information set, stochastic assumptions, initial conditions, boundary conditions, and equilibrium or solution concept as applicable.
4. Derive each equation step by step. Name every added assumption and explain the semantic operation performed by each step.
5. Audit:
   - dimensional and unit consistency;
   - signs, ranges, normalization, and index alignment;
   - existence, uniqueness, identification, and regularity conditions where claimed;
   - special cases, limiting cases, and behavior at boundaries;
   - mapping from theoretical quantities to observables or estimable objects.
6. Compare the equation's comparative statics or predictions with the verbal mechanism. Repair either side when they disagree.
7. For borrowed equations, verify the primary source through the resolved claims registry and state exactly which semantics, assumptions, or boundary conditions changed.
8. Use symbolic, numerical, or unit checks when they can expose algebraic or dimensional errors; record the check and result.
9. Give every empirical estimand a stable ID. Route every equation used to identify a causal, treatment, transmission, structural, or mechanism effect through `$identification-design` using that ID; distinguish mathematical identification from empirical identification.

## Write the equation map

Begin with `Status: complete|partial|blocked`, `Updated`, and scope. Include purpose, symbol table, assumptions, derivation, equations, checks, limiting cases, empirical mapping, evidence IDs, and unresolved issues. Define each symbol once and reference that definition thereafter.

## Stop branches

- Stop at the first undefined symbol, incompatible unit, missing boundary condition, or unjustified operator.
- Reject a borrowed equation that functions only as an analogy without a one-to-one semantic mapping.
- Mark the map `blocked` when a required solution or identification condition cannot be established.
- Mark it `contested` when multiple semantic interpretations fit the same notation and no decision resolves them.
- Set artifact status `partial` for unresolved nonfatal checks and `blocked` when any failed check invalidates the target inference.
- Apply the empirical identification verdict mechanically: let `identified` pass; keep `conditionally-identified` or `pilot-required` `partial`; remove or recast causal interpretation for `descriptive-only`; set the map `blocked` for `blocked`.

## Complete only when

- Define every symbol, operator, index, unit, assumption, and condition exactly once.
- Verify dimensional consistency and at least one informative special or limiting case for every material equation.
- Trace the derivation from accepted semantics without hidden steps.
- Map every quantity used in a prediction or estimator to an observable or explicitly latent construct.
- Re-read the map and verify all domain, theory, construct, decision, and evidence references.
- Verify a current identification artifact for every retained empirical causal equation.
- Set artifact status `complete` only after all preceding criteria pass.
