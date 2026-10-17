---
name: research-help
description: Route a research task to the right Research OS workflow.
---

# Research Help

Use **route** as the leading concept. Diagnose the research state, recommend one entry point, record the accepted route, and stop. Do not perform the routed workflow.

## Workspace resolution

- Check whether `.research/config.yaml` exists before inspecting any other `.research/` path. Its absence is routing evidence, not automatically a blocker.
- When the config exists, resolve and bind every canonical key per [writeback-protocol.md](../../primitives/research-workspace-contract/references/writeback-protocol.md). Routing reads across all of them, so a missing or invalid key stops the route as `blocked`.

## Guardrails

- Follow the user's explicit language preference; otherwise match their current language (English or Traditional Chinese). Keep command names and machine-readable values unchanged.
- After successful path resolution, read `CONTEXT`, `CLAIMS`, and only the canonical artifacts relevant to the route.
- Investigate discoverable facts yourself. Ask the user only for objectives, priorities, risk tolerance, and other decisions.
- Never invoke another user-invoked skill. Name the recommended skill and yield control to the user.
- Treat the resolved canonical workspace as the sole durable source of truth. Never create a competing plan or status file elsewhere.

## Stage 1 — Locate the state

Identify the active research objective, the latest verified artifact, unresolved blockers, and the next uncertainty that prevents progress. Prefer artifact evidence over the conversation.

Classify the request:

- A topic, direction, equation, phenomenon, dataset, draft, or reviewer concern that the user wants developed end to end into a verdict, brief, plan, proposal, blueprint, or paper → `research-auto`
- Explicit request only to initialize the workspace contract → `research-setup`
- Missing workspace contract during an end-to-end request → still `research-auto`; that workflow is authorized to establish the contract
- Fuzzy but session-sized idea → `research-1-grill`
- Existing ideas needing a go/no-go judgment → `research-triage`
- Multi-session effort with unresolved decision dependencies → `research-map`
- Settled discussion needing a durable research contract → `research-2-brief`
- Verified brief needing an executable academic plan → `to-plan`
- Approved brief needing executable slices → `research-4-tasks`
- One eligible workpackage needing bounded execution → `research-5-run`
- Verified findings needing a manuscript → `to-paper`
- Credible design needing a grant, institutional, or project case → `to-proposal`
- Session or agent transition → `research-save`
- Narrow factual or analytical work → the matching model-invoked primitive

**Complete when:** one current bottleneck and the artifact state supporting it are explicit.

## Stage 2 — Recommend the route

Present one primary route, why it fits, the input it will consume, and the completion condition it should reach. Mention at most one alternative and state the condition that would make it preferable.

If a factual premise affects the route, verify it before recommending. If a value judgment affects the route, present the trade-off and wait for the user to choose.

**Complete when:** the user accepts a route or explicitly chooses an alternative.

## Stage 3 — Record and hand back

When a valid workspace exists, record the active route outcome in `CONTEXT` and its Artifact-index row with:

- objective and current bottleneck;
- accepted route and rationale;
- canonical input artifacts;
- unresolved facts and decisions;
- expected completion criterion for the next workflow.

Update the existing route outcome when one already represents the same objective. Do not duplicate it. Create an RDR in `DECISIONS` only when route selection itself passes the four admission tests in `$research-grilling`; ordinary workflow routing is reversible operational state, not a substantive research decision. When the workspace is absent, state that the selected workflow will establish it; do not create route state from the router.

**Complete when:** the accepted route is readable from the resolved canonical workspace, or—when no contract exists—the recommendation explicitly names the workflow that will establish it.

## Register and verify

For every terminal outcome reached with a readable workspace, write or update its canonical record through the resolved output path, then register it in `CONTEXT` and read it back per the writeback protocol.

A `no-op` must read back the already-current row instead of adding one. Keep this skill's `needs-decision` and `no-op` states in the canonical artifact; they never replace the three index statuses.

## Stop branches

- Stop as `blocked` when an existing workspace contract is invalid or required configured artifacts cannot be read.
- Stop as `needs-decision` when two routes remain materially different after factual investigation.
- Stop as `no-op` when the requested workflow is already complete in the canonical artifacts.
- Never claim a downstream workflow has run merely because it was recommended.
