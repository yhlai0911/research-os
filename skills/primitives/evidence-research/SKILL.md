---
name: evidence-research
description: "Trace research claims to high-trust primary sources and record an auditable claim chain. Use when a literature fact, dataset property, method claim, novelty claim, citation, or external factual premise must be verified rather than recalled."
---

# Evidence Research

Build a **claim chain** from the exact claim to inspectable primary evidence. Treat recall, snippets, and citation reputation as discovery aids rather than proof.

## Protect the workspace contract

- Read `.research/config.yaml` first. Resolve its canonical context and claims paths, then read the resolved files before searching; use `.research/evidence/claims.yaml` only as the baseline claim-registry path.
- Preserve `schema_version`, `statuses`, existing claim IDs, and unrelated entries. Use only the configured statuses: `unverified`, `verified`, `contested`, `superseded`, and `blocked`.
- Re-read the resolved claims registry immediately before writing. Link new material claims from the relevant map, brief, review, or paper instead of duplicating the chain.
- Record the evidence-task outcome and affected claim IDs in the resolved context; do not add an unregistered top-level status field to the claims registry.
- Record that outcome in one `## Artifact index` table with columns `Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes`; use the claim IDs as the current evidence pointer and preserve superseded rows.
- Stop with `blocked: research_workspace_not_initialized` when `config.yaml` or a required resolved path is absent.

## Trace the claim

1. Atomize the request into claims that can each be true or false. Fix the population, unit, place, period, version, comparison, and degree of certainty. Mark each claim as informational or load-bearing for a downstream inference.
2. Search for the closest primary source: original paper, official dataset documentation, standard, statute, registry, protocol, source code, or first-party release. Use secondary sources only to discover or contextualize primary evidence.
3. Inspect the source itself. Verify authorship, title, date, version, identifier, and the exact table, figure, section, page, code line, or data field that bears on the claim.
4. Compare the source's actual scope and result with the claim. Record whether it supports, qualifies, contradicts, or cannot resolve the claim.
5. Seek an independent primary source when the claim is high-stakes, disputed, surprising, or foundational to novelty.
6. Search deliberately for disconfirming evidence and newer versions before assigning a verdict.

## Write the chain

Preserve the registry schema. For each claim, record at least:

- `id`, exact `text`, and structured `scope`;
- `status`;
- `sources` with source type, citation, URL or DOI, version, locator, access date, and evidentiary role;
- `entailment` describing the source-to-claim inference and its result;
- `caveats`, search coverage, and `checked_at`.

Set `verified` only when inspectable evidence entails the scoped claim. Set `contested` when credible evidence conflicts or supports only a materially narrower claim. Set `blocked` when required evidence cannot be inspected. Use `superseded` only with a replacement claim ID.

## Stop branches

- Stop at the inaccessible source and record attempted routes; do not verify from an abstract, snippet, or another paper's citation.
- Narrow or split an overbroad claim instead of averaging incompatible evidence.
- Keep novelty `unverified` or `blocked` when a search merely finds nothing; route novelty to `$gap-audit`.
- Report a citation mismatch immediately when the named source does not entail the claim.
- Report the task as `blocked` when a load-bearing claim cannot be inspected, and `partial` when a required claim remains `unverified` or a load-bearing claim remains `contested`.

## Complete only when

- Give every material subclaim a registry entry and allowed status.
- Trace every `verified` claim to at least one inspectable primary source and exact locator.
- Record disconfirming search coverage, version checks, and material caveats.
- Verify that every cited identifier and URL resolves to the recorded source.
- Re-read the resolved claims registry and confirm that no existing schema, status list, claim ID, or unrelated entry changed.
- Report `complete` only when every load-bearing claim is `verified`, every remaining `contested` claim is explicitly non-load-bearing, and no required claim remains `unverified` or `blocked`.
