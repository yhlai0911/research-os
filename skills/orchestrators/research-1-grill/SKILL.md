---
name: research-1-grill
description: Interrogate a research idea one decision at a time until it is researchable.
---

# Step 1 - Grill the Idea

> **Mainline step 1 of 6.** Open the first response by telling the user where they are. Next step: `research-2-brief`.

Use a **decision tree** as the leading concept. Resolve one consequential branch at a time until the idea has a bounded question, a defensible mechanism, observable evidence, and a way to fail.

## Workspace resolution

Resolve `.research/config.yaml` per [writeback-protocol.md](../../primitives/research-workspace-contract/references/writeback-protocol.md), binding `canonical.context`, `canonical.decisions`, and `canonical.claims` as `CONTEXT`, `DECISIONS`, and `CLAIMS`. When the config is absent, stop and recommend that the user invoke `research-setup`; never invoke it yourself.

## Guardrails

- After path resolution, read `CONTEXT`, relevant records in `DECISIONS`, and `CLAIMS`.
- Investigate facts with the appropriate model-invoked research primitives. Do not ask the user to recall facts the agent can verify.
- Put choices, interpretations, priorities, and trade-offs to the user one at a time. Include a recommendation and its cost.
- Never invoke another user-invoked skill.
- Update `CONTEXT`, `DECISIONS`, and `CLAIMS` as understanding changes. Do not leave settled knowledge only in chat.

## Stage 1 — Fix the root

Establish the phenomenon, decision problem, target audience, desired contribution, and practical constraint that motivate the study. Separate the user's desired outcome from claims about the world.

**Complete when:** the user confirms one sentence describing what the study must explain, estimate, predict, design, or decide.

## Stage 2 — Walk the tree

Resolve dependent decisions in order:

1. research question and unit of analysis;
2. constructs, outcomes, treatments, mechanisms, or theoretical objects;
3. target population, setting, period, and boundary conditions;
4. estimand or prediction target;
5. contribution relative to the closest literature;
6. data obtainability and measurement;
7. identification or inferential logic;
8. discriminating predictions, falsifiers, and kill thresholds;
9. ethics, reproducibility, scope, and explicit non-goals.

Use `research-grilling` for the interview discipline and `research-domain-modeling` when terms or relations change. Resolve prerequisite branches before their dependents.

**Complete when:** every live branch is either resolved, backed by a named evidence task, or explicitly ruled out.

## Stage 3 — Stress-test researchability

Try to break the idea with the closest prior work, data constraints, rival mechanisms, identification threats, measurement failure, and ethical constraints. Convert each surviving uncertainty into a testable question rather than optimistic prose.

**Complete when:** the idea has at least one credible failure condition and no hidden assumption that would invalidate the whole design.

## Stage 4 — Write the resolved idea

Write or update one canonical decision record in `DECISIONS`. Record:

- confirmed research question and intended contribution;
- construct and mechanism definitions;
- unit, population, setting, and scope;
- required evidence and current claim-chain links;
- proposed design direction;
- falsifiers and kill thresholds;
- unresolved facts and user decisions;
- status: `researchable`, `blocked`, `repair`, or `needs-map`.

Write canonical terms to `CONTEXT` and factual claims to `CLAIMS`.

**Complete when:** the user confirms the record and a fresh researcher can understand why the idea is or is not researchable.

## Register and verify

For every terminal outcome reached with a readable workspace, write or update its canonical record through the resolved output path, then register it in `CONTEXT` and read it back per the writeback protocol. A claim-only outcome uses its claim IDs.

Keep this skill's `researchable`, `blocked`, `repair`, `needs-map`, and `kill-candidate` states in the decision record. They never replace the three index statuses.

## Stop branches

Every branch below is terminal. Name the branch, say what it means, and name the next step; never continue past a branch on your own initiative.

- Hand off as `researchable` once every stage gate passes: tell the user the idea now has a bounded question, a defensible mechanism, observable evidence, and a way to fail, then name `research-2-brief` as the next step and stop. Converging is not permission to run it.
- Stop as `blocked` when a load-bearing factual premise cannot be verified.
- Stop as `repair` when the idea can survive only after a named change.
- Stop as `needs-map` when the unresolved decision graph will not fit one session; recommend `research-map` and yield.
- Stop as `kill-candidate` when evidence makes the central claim infeasible, non-distinct, unethical, or unfalsifiable; record the reason and ask the user for the final decision.
