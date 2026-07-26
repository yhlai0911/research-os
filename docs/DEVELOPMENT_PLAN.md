# Development plan

## Phase 1 — Reference analysis

- Pin and clone the Matt Pocock Skills source.
- Read every `SKILL.md`, direct resource, invocation policy, plugin metadata, lifecycle bucket, installer, and release file.
- Record adopt, adapt, and reject decisions.

Acceptance: all 41 upstream skills are accounted for and the pinned commit is recorded.

## Phase 2 — Contract and catalog

- Define user orchestrators and model primitives.
- Assign one leading concept, invocation type, responsibility, and UI contract per skill.
- Establish `.research/` authority boundaries.

Acceptance: one catalog entry exists per intended skill, with no trigger collision or uncatalogued directory.

## Phase 3 — Implementation

- Initialize every skill through the official creator.
- Implement SKILL.md, references, scripts, and assets.
- Add catalog synchronization, non-destructive installation, workspace setup, and packaging.

Acceptance: zero initializer placeholders and zero unverified overwrite paths.

## Phase 4 — Verification

- Run structural validation and unit tests.
- Forward-test the router, research ideation flow, evidence path, equation path, review path, blocked behavior, and handoff.
- Repair at the smallest source-of-truth rule.

Acceptance: all automated and forward tests pass.

## Phase 5 — Delivery

- Commit the exact validated source.
- Push `main` to the private GitHub repository.
- Build the ZIP from that clean commit.
- Verify archive checksum and repository remote state.

Acceptance: remote commit, ZIP receipt, and local commit match.
