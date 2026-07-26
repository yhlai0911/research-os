# Quality gates

## Skill gate

Every skill must satisfy:

- official initializer provenance;
- exact catalog name and description;
- correct invocation policy;
- one distinct leading concept;
- checkable and exhaustive completion criteria;
- explicit partial, blocked, or stop branches;
- no TODO, empty resource directory, or local README;
- direct, conditional pointers to one-level references;
- config-first canonical-path resolution for every workspace skill;
- one resolved-context Artifact index for current pointers and task outcomes;
- a fresh-agent success case, near-miss, and blocked case.
- an entry in the pinned upstream port map when it implements a retained Matt mechanism.
- a deterministic shared packet when several review contexts must inspect the same revision;
- a recovery path, not only a stop state, when the skill claims to resolve canonical conflicts.

## Repository gate

Run:

```bash
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

The catalog, generated metadata, docs, project version, and discovered skill directories must agree exactly.

The Matt port map must name the pinned upstream commit, contain exactly the 41 upstream skills in that commit once each, point every retained mechanism to an existing Research OS skill, and give an explicit reason for every rejected domain-specific behavior.

## Research artifact gate

An artifact is complete only when:

1. its inputs and provenance are named;
2. decisions are distinguished from discovered facts;
3. unsupported claims carry a non-verified status;
4. completion follows current readback;
5. a falsifier, rival, or failure branch is recorded where applicable;
6. the artifact points to its source of truth instead of copying it.
7. the output profile does not upgrade planned work into executed results.

## Release gate

A release ZIP must be produced from a clean committed source tree. The archive is deterministic, contains `MANIFEST.sha256`, and has an external SHA-256 sidecar plus a receipt naming the source commit and file count.

Before release, forward evaluations run the public prompts against fresh agents in isolated workspaces. At minimum they cover a vague seed, an imported equation or method, an existing design, a blocked novelty or data premise, and a manuscript request without results.
