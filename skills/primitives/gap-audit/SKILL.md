---
name: gap-audit
description: "Audit whether a claimed research gap is real, material, and defensible. Use when a topic is said to be novel, underexplored, first, missing, or different; when a reviewer could dismiss the gap as relabeling; or before writing a contribution claim."
---

# Gap Audit

Test the claimed **difference** against the closest prior work. Require both novelty and consequence; a difference without stakes is not a research gap.

## Protect the workspace contract

- Resolve `.research/config.yaml` and its canonical context, claims, maps, and reviews paths per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md), then read the relevant resolved artifacts.
- Use an existing registered audit; otherwise create `gap-audit-<topic-slug>.md` under the resolved reviews directory and register it in the resolved context.
- Verify missing or stale literature claims through `$evidence-research` or `$literature-landscape` before judging the gap.
- Stop with `blocked: research_workspace_not_initialized` when the contract is absent.

## Audit the difference

1. Rewrite the proposed gap as a falsifiable statement about what the closest literature does not establish.
2. Identify the nearest substantive neighbors, including work that uses different terminology for the same construct.
3. Compare the proposal and each neighbor on question, construct, mechanism, population, context, period, data, measurement, identification, method, outcome, and prediction.
4. Classify every claimed difference as:
   - already present;
   - a relabeling;
   - a scope extension;
   - a method or data substitution;
   - a measurement improvement;
   - a new identification result;
   - a new mechanism or discriminating prediction;
   - unresolved by available evidence.
5. Test materiality. State what belief, estimate, mechanism, decision, or boundary changes if the difference is real.
6. Search for the strongest reviewer dismissal and answer it with evidence rather than adjectives.

## Write the verdict

Begin with `Status: complete|partial|blocked`, `Updated`, and scope. Record the claimed gap, search boundary, closest-neighbor matrix, surviving differences, failed differences, materiality test, reviewer attack, evidence claim IDs, and one verdict: `survives`, `narrows`, `fails`, or `blocked`.

Use `survives` only when the exact difference is absent from the searched neighborhood, is not terminological, and changes a material inference. Use `narrows` when only a scoped version survives. Preserve failed claims so downstream work does not revive them.

## Stop branches

- Return `fails` when the closest work already contains the claimed delta or terminology alone creates it.
- Return `blocked` when a material neighbor or primary source cannot be inspected.
- Return `narrows` and rewrite the claim when novelty holds only for a population, period, method, or measurement boundary.
- Use artifact status `partial` while a material comparison remains unresolved; assign no final verdict yet.
- Do not draft a contribution from a failed or blocked gap.

## Complete only when

- Compare every material axis against every closest neighbor.
- Trace every novelty premise to `claims.yaml`, including contrary evidence.
- State why each surviving difference matters and what evidence could still defeat it.
- Assign exactly one verdict and propagate it to the resolved context.
- Re-read the audit and verify that no unsupported "first", "novel", "missing", or "underexplored" claim remains.
- Set artifact status `complete` for `survives`, `narrows`, or `fails`; use `blocked` for a blocked verdict.
