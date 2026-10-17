---
name: research-workspace-contract
description: "Establish, resolve, and verify the durable Research OS workspace contract without overwriting existing work. Use when an explicitly authorized research workflow needs canonical context, decisions, evidence, briefs, outputs, handoffs, templates, or adapter paths initialized or repaired."
---

# Research Workspace Contract

Treat the workspace as a durable **contract**, not a folder convention. Establish one source of truth for research state, preserve existing work, and prove every write by readback.

Read [workspace-contract.md](references/workspace-contract.md) when adapting an existing project, resolving a nonstandard path, or deciding which artifact owns a piece of state.

This skill owns [writeback-protocol.md](references/writeback-protocol.md), the single definition of the resolution procedure, the Artifact index contract, and the three index statuses that every other skill follows. Changing that file changes the contract for the whole suite.

## Confirm the mutation boundary

Proceed only when the user explicitly invoked setup or an explicitly authorized research workflow called this skill. That authority covers additive local contract files inside the scoped project; it does not cover overwriting, migration, deletion, publication, or other external writes.

Resolve the repository root and read its instructions. Inspect any existing `.research/config.yaml` before every other `.research/` path. If it exists, resolve all canonical entries from it and use those paths; never create a second baseline tree as a fallback.

**Complete when:** the root, calling authority, and existing contract state are known.

## Preflight

For a new baseline contract, run:

```bash
uv run --no-project python <this-skill>/scripts/init_research_workspace.py \
  --root <repository-root> \
  --dry-run
```

Classify every target as `created`, `unchanged`, or `conflict`. Show material conflicts before applying. For an established nonstandard workspace, design an adapter in `config.yaml`; do not migrate files unless the user separately accepts an exact path map.

**Complete when:** the preview accounts for every directory and baseline file and no conflict is being silently overwritten.

## Establish or repair

Run the initializer without `--dry-run` only after preflight. It creates the baseline contract additively:

- canonical path registry;
- research context and current-artifact index;
- decision, evidence, map, brief, workpackage, pilot, review, paper, proposal, and handoff locations;
- versioned copyable templates.

Preserve every existing file byte-for-byte. A file or directory collision stops that target. When a configured contract already exists, repair only missing paths that the configuration actually resolves; do not replace the adapter with defaults.

**Complete when:** every authorized write has a `created` receipt, every existing target is `unchanged`, and conflicts remain untouched.

## Seed verified state

Write only conversation facts and inspected project facts into the resolved context. Keep unknowns explicit. Create one Research Decision Record per choice only when all four admission tests pass: the choice is costly to reverse, surprising or unsafe without its rationale, a genuine trade-off among viable alternatives, and necessary to keep downstream artifacts unambiguous. Put routine routing, formatting, and progress state in the owning artifact or run record, not `DECISIONS`. Put externally checkable propositions in the resolved claims registry with a declared evidence status.

Maintain exactly one `## Artifact index` in the resolved context, in the shape the writeback protocol defines. Register seeded artifacts and the setup outcome there, preserve superseded rows, and never duplicate claim evidence or decision substance into the index.

**Complete when:** known scope is durable, unresolved decisions remain visible, and every seeded artifact has one current pointer.

## Prove the contract

For a baseline contract, run:

```bash
uv run --no-project python <this-skill>/scripts/init_research_workspace.py \
  --root <repository-root> \
  --check
```

For an adapter, verify every resolved path directly. Re-read config, context, claims, templates, and every artifact written in this run. Report exact created, unchanged, conflicting, and missing paths plus the next unresolved research decision.

Use `complete` only when all required paths and index rows read back. Use `partial` when useful additive state exists but a non-load-bearing path or seed remains open. Use `blocked` when config, a required canonical path, an authorized write, or readback fails.

## Stop branches

- Stop with `blocked: authorization_missing` when no explicit workflow authorizes local setup.
- Stop with `blocked: root_ambiguous` when the project root is unresolved.
- Stop at a type or content conflict; never overwrite it.
- Stop before migration, deletion, remote writes, or publication.
- Report a missing required adapter key instead of probing the baseline path.
