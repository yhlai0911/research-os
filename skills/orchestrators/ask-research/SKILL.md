---
name: ask-research
description: Route a research task to the right Research OS workflow.
---

# Ask Research

Use **route** as the leading concept. Diagnose the research state, recommend one entry point, record the accepted route, and stop. Do not perform the routed workflow.

## Workspace resolution

- Check whether `.research/config.yaml` exists before inspecting any other `.research/` path. Its absence is routing evidence, not automatically a blocker.
- When the config exists, resolve `canonical.context`, `canonical.decisions`, `canonical.claims`, `canonical.maps`, `canonical.briefs`, `canonical.plans`, `canonical.workpackages`, `canonical.papers`, `canonical.proposals`, `canonical.handoffs`, `canonical.reviews`, `canonical.pilots`, and `canonical.templates`. Resolve relative values against the repository root and preserve absolute values.
- Bind the resolved paths as `CONTEXT`, `DECISIONS`, `CLAIMS`, `MAPS`, `BRIEFS`, `PLANS`, `WORKPACKAGES`, `PAPERS`, `PROPOSALS`, `HANDOFFS`, `REVIEWS`, `PILOTS`, and `TEMPLATES`. Read and write only through these bindings.
- Treat the setup baseline paths as defaults only, never as fallback targets. If a required key is missing, invalid, or has a file/directory type collision, stop as `blocked`; do not probe or write a default path.

## Guardrails

- After successful path resolution, read `CONTEXT`, `CLAIMS`, and only the canonical artifacts relevant to the route.
- Investigate discoverable facts yourself. Ask the user only for objectives, priorities, risk tolerance, and other decisions.
- Never invoke another user-invoked skill. Name the recommended skill and yield control to the user.
- Treat the resolved canonical workspace as the sole durable source of truth. Never create a competing plan or status file elsewhere.

## Stage 1 — Locate the state

Identify the active research objective, the latest verified artifact, unresolved blockers, and the next uncertainty that prevents progress. Prefer artifact evidence over the conversation.

Classify the request:

- A topic, direction, equation, phenomenon, dataset, draft, or reviewer concern that the user wants developed end to end into a verdict, brief, plan, proposal, blueprint, or paper → `develop-research`
- Explicit request only to initialize the workspace contract → `setup-research-os`
- Missing workspace contract during an end-to-end request → still `develop-research`; that workflow is authorized to establish the contract
- Fuzzy but session-sized idea → `grill-research-idea`
- Existing ideas needing a go/no-go judgment → `idea-triage`
- Multi-session effort with unresolved decision dependencies → `research-wayfinder`
- Settled discussion needing a durable research contract → `to-research-brief`
- Verified brief needing an executable academic plan → `to-research-plan`
- Approved brief needing executable slices → `to-workpackages`
- One eligible workpackage needing bounded execution → `execute-workpackage`
- Verified findings needing a manuscript → `to-paper-draft`
- Credible design needing a grant, institutional, or project case → `to-proposal`
- Session or agent transition → `research-handoff`
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

For every terminal outcome reached with a readable workspace, write or update its canonical record through the resolved output path, then register every created or updated current artifact or outcome in the single `## Artifact index` table in `CONTEXT`:

`| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |`

Keep substantive content in its canonical artifact; the index contains only identity, current state, timestamp, and lineage. Upsert one current row per `Kind` and `Topic`. When an ID changes, preserve the former row as `superseded` and put its ID in the replacement row's `Supersedes`; never create a second index or two current rows for the same subject. A claim-only outcome uses its claim IDs in the artifact-or-claim-ID column.

Read back the resolved artifact or outcome and `CONTEXT`, then verify the row's ID, status, timestamp, and lineage. Use only these index statuses:

- `complete` only when every skill completion gate passes and both the artifact or outcome and its row read back successfully;
- `partial` when a usable, read-back durable result exists but remains incomplete, or only the index update or index readback cannot be sealed;
- `blocked` when no usable current result can be produced because a load-bearing input, permission, resolved path, artifact write, or artifact readback fails.

If the config or `CONTEXT` cannot be read, report `blocked` and state that registration did not occur. A `no-op` must read back the already-current row instead of adding one. Keep domain-specific states in the canonical artifact; they do not replace the three index statuses.

## Stop branches

- Stop as `blocked` when an existing workspace contract is invalid or required configured artifacts cannot be read.
- Stop as `needs-decision` when two routes remain materially different after factual investigation.
- Stop as `no-op` when the requested workflow is already complete in the canonical artifacts.
- Never claim a downstream workflow has run merely because it was recommended.
