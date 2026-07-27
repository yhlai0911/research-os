---
name: literature-landscape
description: "Map a literature into theories, mechanisms, methods, data, findings, and disputes. Use when the user needs a literature landscape, research stream map, conceptual synthesis, boundary search, or an evidence-backed view of what a field already knows."
---

# Literature Landscape

Build a **map** of the field's structure, not a chronological list of papers.

## Protect the workspace contract

- Resolve `.research/config.yaml` and register every outcome per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). This skill needs the resolved context, claims, and maps paths.
- Use an existing registered landscape; otherwise create `literature-landscape-<topic-slug>.md` under the resolved maps directory.
- Read only the sources and claim entries needed for the current map branch. Add detailed source verification to the claim registry; keep synthesis in the map.

## Map the landscape

1. Declare the focal question, adjacent fields, populations, contexts, period, source types, and inclusion and exclusion rules.
2. Record a reproducible search protocol: databases or venues, queries, date searched, citation chaining, and coverage limits.
3. Locate seminal work, the closest recent work, major reviews, and credible counter-streams. Follow backward and forward citations from the closest sources.
4. Extract each included work into a common matrix:
   - theory and mechanism;
   - question and unit of analysis;
   - constructs and measurement;
   - method and identification;
   - data, setting, and period;
   - findings, limitations, and evidence claim IDs.
5. Cluster works by shared theory, mechanism, method, data, or dispute. Name streams by their substantive logic rather than by author.
6. Map consensus, live disputes, boundary conditions, incompatible definitions, method-dependent results, and genuinely untested combinations.
7. Test the synthesis against the strongest opposing stream. Revise claims that only hold inside one method, setting, or vocabulary.

## Write the map

Begin with `Status: complete|partial|blocked`, `Updated`, and scope. Include the search protocol, source matrix, stream map, consensus, disputes, boundary conditions, coverage gaps, and unresolved searches. Reference claim IDs from the resolved claims registry; do not copy entire claim chains.

## Stop branches

- Mark the map `partial` when access, language, database, or time limits leave a material stream unchecked.
- Mark it `blocked` when an unchecked stream prevents any defensible landscape verdict.
- Stop and repair the domain model when the literature uses the same term for incompatible constructs.
- Reject a gap conclusion based only on an empty query. Hand candidate gaps to `$gap-audit`.

## Complete only when

- Execute every declared search and inspect the primary sources behind every material synthesis claim.
- Characterize every included work with the same extraction fields.
- Include the strongest relevant counter-stream and state the map's coverage ceiling.
- Reach practical saturation: one additional backward/forward citation pass and one reformulated query add no new material stream, mechanism, method, or dispute.
- Re-read the landscape and verify every evidence claim ID against the resolved claims registry.
- Set artifact status `complete` only after all preceding criteria pass.
