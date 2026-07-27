---
name: research-map
description: Map a multi-session research effort as decisions that progressively clear the fog.
---

# Map a Big Project

Use **fog** as the leading concept. Maintain a shared decision map for research too large or uncertain to resolve in one session. Clear one frontier decision at a time; plan the route without pretending to execute the study.

## Workspace resolution

- Resolve `.research/config.yaml` per [writeback-protocol.md](../../primitives/research-workspace-contract/references/writeback-protocol.md). If it is absent, stop and recommend that the user invoke `research-setup`; do not invoke it yourself.
- Before reading any other workspace artifact, resolve `canonical.context`, `canonical.decisions`, `canonical.claims`, `canonical.maps`, and `canonical.briefs` from the config. Resolve relative values against the repository root and preserve absolute values.
- Bind the resolved paths as `CONTEXT`, `DECISIONS`, `CLAIMS`, `MAPS`, and `BRIEFS`. Read and write only through these bindings.
- Treat the setup baseline paths as defaults only, never as fallback targets. If a required key is missing, invalid, or has a file/directory type collision, stop as `blocked`; do not probe or write a default path.

## Guardrails

- After path resolution, read `CONTEXT`, `CLAIMS`, and relevant records in `DECISIONS`, `MAPS`, and `BRIEFS`.
- Investigate factual questions through model-invoked primitives. Reserve value judgments, trade-offs, priorities, and commitments for the user.
- Never invoke another user-invoked skill.
- Keep each decision in one canonical record in `DECISIONS`. Let the map in `MAPS` index and link decisions; never restate their full contents.

Choose one mode before work:

- `chart` when no current map exists or the user explicitly wants to map the effort;
- `work` when the user wants to resolve one node on an existing map.

Never chart and resolve a decision in the same invocation. A chart is a low-resolution routing artifact; a decision record owns the question and answer.

## Stage 1 — Name the destination

Define the durable outcome the map must make possible, its scope, its non-goals, and the condition for declaring the route clear. Treat the destination as a user decision.

If the effort already has no meaningful fog, stop as `too-small-for-map`, record that finding, and recommend the appropriate next workflow.

**Complete when:** the user confirms one destination against which every prospective decision can be tested.

## Chart mode — Build and stop

Explore breadth-first and separate:

- discoverable facts that an agent can investigate;
- research decisions that require user judgment;
- external tasks or access dependencies;
- in-scope unknowns that cannot yet be stated precisely;
- work beyond the destination.

Promote an unknown into a decision only when its question can be stated precisely. Give every decision an identifier, type, status, and canonical record path. First create all decision records with stable IDs; only then wire blocking edges in a second pass. Keep unspecifiable unknowns in the map's fog section.

**Complete when:** every currently stateable decision is on the map, every blocking edge is explicit, and unstateable fog remains visibly distinct from out-of-scope work.

Register and read back the map and decision records. Independent factual nodes may be dispatched through isolated model-invoked research tasks when their scopes and write targets do not overlap. Then stop as `chart-complete`; do not resolve a frontier node in this invocation.

## Work mode — Claim one frontier node

Select an open, unblocked decision:

- Resolve factual nodes with the matching model-invoked evidence, literature, data, design, or review primitive.
- Resolve human-in-the-loop nodes through one-question-at-a-time research grilling.
- Never resolve a user decision from model priors.

Before reading sources or asking the decision question, pin the decision-record SHA-256 and atomically claim the node:

```bash
uv run --no-project python <research-workspace-contract>/scripts/atomic_claim.py claim \
  --state-root <resolved-maps-directory> \
  --claim-id <map-id>-<decision-id>-<sha256-prefix>-a<attempt> \
  --source <absolute-decision-record-path> \
  --expected-sha256 <pinned-sha256> \
  --owner <agent-or-task-id>
```

Continue only after a `claimed` receipt reads back. On `already-claimed`, stop or recompute another frontier node. On `already-sealed`, verify the receipt and recompute the map as a no-op. Never steal a stale claim based on elapsed time alone.

Resolve at most one human-in-the-loop decision per invocation. Parallel factual investigations require separate claims and non-overlapping write targets.

Keep the claimed question record immutable. Write the answer to a separate canonical resolution record and point the decision and map to it. Update affected claims and context, mark the map node resolved, recompute edges and frontier, register the outcome, and read every write back.

Create the required JSON resolution receipt with the versioned `claim_id`, owner, execution status, claimed source hash, domain verdict, outputs, checks, and readback pointers. Seal only after the resolution, recomputed map, claims, context, and Artifact-index row all agree. The shared helper verifies identity, source immutability, receipt schema, and result, then archives the active claim. Do not mutate the map or decision state after sealing.

A failed or interrupted resolution remains claimed with explicit continuation state. An acknowledged owner may use the helper's `release` command with an explicit reason; never silently return or steal it.

**Complete when:** one frontier decision has an evidence-backed resolution or a precise blocked state.

## Work mode — Recompute the map

After each resolution:

1. remove resolved fog that is now represented by decisions;
2. promote newly stateable questions;
3. recompute blockers and the frontier;
4. update a concise decision index;
5. assess whether the destination is now reachable without further research decisions.

**Complete when:** the map has no stale edges, duplicated decisions, or implied next step.

## Register and verify

For every terminal outcome reached with a readable workspace, write or update the canonical map in `MAPS` and any changed decision record in `DECISIONS`, then register every created or updated current artifact or outcome in `CONTEXT` per the writeback protocol.

Keep decision substance in `DECISIONS` and map structure in `MAPS`. Read back every changed map, decision, or claim outcome and `CONTEXT`; a claim-only outcome uses its claim IDs.

Resolve the index status against the route: `complete` when all changed artifacts or outcomes and their rows read back; `partial` when a usable result exists but the route remains incomplete; `blocked` when a load-bearing input, permission, path, or write fails. Domain-specific map and decision states stay in their canonical artifacts.

## Finish and stop branches

- Finish as `route-clear` only when no unresolved decision blocks a rigorous research brief.
- Stop as `blocked` when the frontier is empty but unresolved decisions remain; name the external dependency or missing user decision.
- Stop as `needs-destination` when scope cannot be judged.
- Stop as `too-small-for-map` when one session can settle the remaining work.
- Record every terminal state in the canonical map. Recommend the next user-invoked workflow, but never invoke it.
