---
name: synthesize-research-brief
description: "Synthesize verified research state into one canonical Research Brief. Use when an adaptive research conversation has resolved enough question, evidence, contribution, theory, measurement, identification, data, method, and falsification state for downstream planning, proposal, or paper work."
---

# Synthesize Research Brief

Use **collapse** as the leading concept. Compress resolved research state into one audience-neutral contract without reopening settled choices or inventing missing ones.

This skill is the only writer of the canonical Research Brief. Renderers and destination wrappers may validate or consume it, but never create a competing brief.

## Resolve the workspace

Read only `.research/config.yaml` first. Resolve context, decisions, claims, maps, pilots, reviews, briefs, and templates. Read the resolved context and only current linked artifacts. Use `research-brief.md` from the resolved templates directory.

Stop with `blocked: research_workspace_not_initialized` when config or a required resolved path is absent. Call `$research-workspace-contract` only when the surrounding workflow carries explicit local-setup authority.

## Prove readiness

Build a source table mapping each prospective section to:

- verified evidence claim IDs;
- accepted decisions;
- current theory, construct, equation, identification, data, method, falsification, pilot, and review artifacts;
- explicit assumptions or unresolved blockers.

Detect contradictions, superseded decisions, unsupported novelty, missing data facts, causal language above the identification verdict, and planned work presented as completed.

**Complete when:** every load-bearing statement is classified as verified fact, accepted decision, explicit assumption, or blocker.

## Collapse the contract

Write one brief containing:

- problem, motivation, and intended decision or inference;
- bounded research question and contribution delta;
- closest literature and claim-chain pointers;
- mechanism, actors, rivals, and boundary conditions;
- constructs, measures, units, population, setting, and period;
- estimand or prediction target and hypotheses;
- data, access, timing, measurement, and alignment;
- identification or inferential strategy;
- methods, baselines, diagnostics, and evaluation;
- falsifiers and kill/repair/continue rules;
- ethics, reproducibility, outputs, scope, exclusions, dependencies, and open decisions.

Reference canonical artifacts instead of copying their full contents. Preserve exact uncertainty and evidence states.

**Complete when:** every section is internally coherent and traceable to its source.

## Resolve only load-bearing choices

When a user decision remains, invoke `$research-grilling` and ask exactly one prerequisite decision at a time with a recommendation and trade-off. Do not ask for discoverable facts or reopen accepted choices. Persist each answer before continuing.

**Complete when:** the user confirms the question, contribution, scope, inferential claim, failure criteria, and declared assumptions, or the brief clearly records why one remains blocked.

## Seal and register

Reuse the current registered brief or allocate one stable ID. Assign its domain status:

- `ready` when no blocker prevents planning or the requested downstream artifact;
- `conditional` when named conditions must pass before execution or stronger claims;
- `blocked` when a load-bearing fact, decision, or validity condition is unresolved.

Record version, updated time, inputs, claim and decision links, acceptance, and readiness rationale. Register the brief in the resolved context's single `## Artifact index`:

`| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |`

Map `ready` to index `complete`, `conditional` to `partial`, and `blocked` to `blocked`. Re-read the brief, changed claims or decisions, and index row. A complete run requires all pointers and statuses to agree.

## Stop branches

- Stop at a canonical conflict; do not choose the convenient artifact. Invoke `$artifact-reconciliation` to pin both intents, supersede the parents, invalidate stale downstream gates, and prove one current pointer before synthesis resumes.
- Keep novelty blocked when a boundary search is incomplete.
- Keep a causal section partial or blocked when identification does not support it.
- Never mark a brief ready because prose is complete.
- Do not render a plan, proposal, or paper here; return the canonical brief to the caller.
