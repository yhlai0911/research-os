# Engineering skills prompt-level port audit

> **Audit snapshot:** Research OS `1.0.0`, catalog lifecycle `stable`, reconciled against the current repository state on 2026-07-26 (Asia/Taipei). This file preserves upstream-to-target behavioral analysis. The central cross-audit resolution pointer is [`docs/PORT_REMEDIATION.md`](../PORT_REMEDIATION.md); where current prompt readback disagrees with that ledger, this audit calls out the drift instead of inheriting the older verdict.

## Audit contract

This audit compares all 17 promoted engineering skills in Matt Pocock's upstream repository with the current Research OS prompt architecture. The purpose is behavioral equivalence: what causes a skill to run, which concept organizes its reasoning, which steps must occur in which order, what makes the run complete, where it must stop, what durable state it leaves, and how it composes with adjacent skills.

- Upstream source: `/tmp/matt-skills-analysis.qMpo5S/repo/skills/engineering`
- Upstream commit: `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- Research OS source of truth: `skills/catalog.yaml`
- Research OS comparison root: `/Users/apple/Downloads/research-os/skills`
- Audit date: 2026-07-26, Asia/Taipei

All 17 upstream `SKILL.md` files were read completely. The audit also read every directly linked local reference and the directly named HITL script:

- `codebase-design/{DEEPENING.md,DESIGN-IT-TWICE.md}`
- `diagnosing-bugs/scripts/hitl-loop.template.sh`
- `domain-modeling/{CONTEXT-FORMAT.md,ADR-FORMAT.md}`
- `improve-codebase-architecture/HTML-REPORT.md`
- `prototype/{LOGIC.md,UI.md}`
- `setup-matt-pocock-skills/{issue-tracker-github.md,issue-tracker-gitlab.md,issue-tracker-local.md,triage-labels.md,domain.md}`
- `tdd/{tests.md,mocking.md}`
- `triage/{AGENT-BRIEF.md,OUT-OF-SCOPE.md}`

The `agents/openai.yaml` file for every upstream skill was also checked so the audit does not infer invocation policy from prose alone. The directly cited [Smart Zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone) page and [GitLab CLI](https://gitlab.com/gitlab-org/cli) project page were inspected as well. On the Research OS side, the exact target prompts, their catalog invocation metadata, and directly relevant contract scripts, references, and assets were read. Because Research OS was being refactored during this audit, target verdicts below use a final readback rather than the first observed file state.

### Classification

- **Direct-port**: the upstream behavioral nucleus, ordering, and stop topology remain recognizably one-to-one. Research OS may strengthen provenance, authorization, or readback without changing the core control flow.
- **Adapt**: an upstream mechanism is retained, but research semantics, authority, artifacts, or stage topology materially change.
- **Exclude**: the skill itself is intentionally outside the research core. Reused sub-mechanisms and any resulting gaps are still named.

“Missing” below means prompt behavior absent from the current Research OS target. It is not automatically a defect: deliberate domain exclusions are labeled as such, while correctness or continuity losses are promoted to the prioritized gap list.

## Coverage matrix

| # | Upstream skill | Upstream boundary | Leading concept | Classification | Exact Research OS target(s) |
|---|---|---|---|---|---|
| 1 | `ask-matt` | user-only | flow / router | Direct-port | `skills/orchestrators/research-help/SKILL.md`, plus every route it names |
| 2 | `code-review` | model-invoked | two independent review axes | Adapt | `skills/primitives/research-review/SKILL.md`, `skills/primitives/citation-audit/SKILL.md` |
| 3 | `codebase-design` | model-invoked | deep module | Exclude | partial mechanisms in `skills/primitives/design-research-three-ways/SKILL.md`, `skills/primitives/research-domain-modeling/SKILL.md`, and `skills/primitives/methodology-designer/SKILL.md` |
| 4 | `diagnosing-bugs` | model-invoked | tight red-capable feedback loop | Direct-port | `skills/primitives/research-diagnosis/SKILL.md` |
| 5 | `domain-modeling` | model-invoked | active canonical language | Adapt | `skills/primitives/research-domain-modeling/SKILL.md`, `skills/primitives/research-grilling/SKILL.md`, `skills/primitives/research-workspace-contract/SKILL.md` |
| 6 | `grill-with-docs` | user-only | composed interview with inline writeback | Direct-port | `skills/orchestrators/research-1-grill/SKILL.md`, invoking `research-grilling` and `research-domain-modeling` |
| 7 | `implement` | user-only | execute a ticket through test and review gates | Adapt | `skills/orchestrators/research-5-run/SKILL.md`, `skills/orchestrators/research-auto/SKILL.md`, `skills/orchestrators/research-4-tasks/SKILL.md`, `skills/primitives/research-review/SKILL.md` |
| 8 | `improve-codebase-architecture` | user-only | survey deepening opportunities before design | Exclude | partial mechanisms in `research-diagnosis`, `design-research-three-ways`, `research-grilling`, and `render-research-deliverable` |
| 9 | `prototype` | model-invoked | throwaway artifact answers one question | Adapt | `skills/primitives/pilot-study/SKILL.md`, with alternative generation in `design-research-three-ways` |
| 10 | `research` | model-invoked | background primary-source investigation | Direct-port | `skills/primitives/evidence-research/SKILL.md`; broader synthesis in `literature-landscape` |
| 11 | `resolving-merge-conflicts` | model-invoked | reconcile intent from primary sources | Exclude | retained research mechanism in `skills/primitives/artifact-reconciliation/SKILL.md`, with stop-and-route edges from `research-save`, `research-domain-modeling`, `research-grilling`, and `synthesize-research-brief` |
| 12 | `setup-matt-pocock-skills` | user-only | explore, confirm, then configure | Adapt | `skills/orchestrators/research-setup/SKILL.md` → `skills/primitives/research-workspace-contract/SKILL.md` |
| 13 | `tdd` | model-invoked | red → green vertical slice | Exclude | selected mechanics in `research-5-run`, `pilot-study`, `falsification-first`, and `research-4-tasks` |
| 14 | `to-spec` | user-only | synthesize settled context into a contract | Adapt | `skills/orchestrators/research-2-brief/SKILL.md` → `skills/primitives/synthesize-research-brief/SKILL.md`; execution-plan rendering in `to-plan` |
| 15 | `to-tickets` | user-only | tracer bullets with blocking edges | Direct-port | `skills/orchestrators/research-4-tasks/SKILL.md` |
| 16 | `triage` | user-only | verified state transition | Adapt | `skills/orchestrators/research-triage/SKILL.md` |
| 17 | `wayfinder` | user-only | destination, fog, and frontier | Direct-port | `skills/orchestrators/research-map/SKILL.md` |

## Per-skill behavioral equivalence

### 1. `ask-matt` — Direct-port

**Invocation boundary.** Upstream is explicitly user-only in both frontmatter and Codex metadata. It is a remembered entry point, not an implicit dispatcher. `research-help` preserves that boundary through catalog invocation `user` and the generated `allow_implicit_invocation: false` policy. It may name another user workflow but must yield rather than invoke it.

**Leading concept.** Upstream organizes the catalog as a **flow**: one main idea-to-ship path, three on-ramps, a code-health loop, vocabulary underneath, cross-session bridges, and standalone tools. The router’s work is state recognition, not task execution. Research OS names this concept **route**, which is behaviorally equivalent but more state-aware.

**Ordered upstream mechanics.**

1. Require repository setup before the first engineering flow.
2. For a session-sized idea, begin with `grill-with-docs`.
3. If conversation cannot settle a runnable question, hand off to a fresh prototype session and hand the answer back.
4. Branch on build size: a multi-session build goes `to-spec` → `to-tickets` → one fresh `implement` session per ticket; a small build goes straight to `implement` in the current context.
5. Inside implementation, use TDD slices, then independent code review, then commit.
6. Route raw incoming work through `triage`, hard failures through `diagnosing-bugs`, and genuinely foggy multi-session efforts through `wayfinder`.
7. Keep grilling through ticket decomposition in one unbroken context. If reasoning quality approaches the Smart Zone boundary, hand off instead of pushing through degraded context.

**Completion gates.** Upstream has no formal checklist; it is complete when it has named the one correct entry point and the user can see how that route joins the larger flow. Critical negative gates are part of correctness: do not triage tickets already produced by `to-tickets`; do not send a wayfinder map directly to implementation unless the effort proved truly small; do not compact mid-phase.

**Stop/failure branches.**

- Missing setup → route to setup.
- Question requires runnable evidence → detour through a prototype and explicit handoffs.
- Effort is larger than one context → route through a map or handoff.
- No codebase → use the stateless grilling variant, not repository writeback.
- Router never performs the selected workflow.

**Durable state/writeback.** The upstream router writes nothing. It depends on downstream issue, context, ADR, handoff, and code artifacts. Research OS strengthens this: `research-help` resolves canonical paths, writes the accepted route to `DECISIONS`, registers it in the single `CONTEXT` Artifact index, and requires readback before reporting complete.

**Composition edges.** Upstream reaches nearly the entire engineering graph: setup, grilling, domain modeling, prototype, handoff, spec, tickets, implementation, TDD, review, triage, diagnosis, architecture review, wayfinder, research, and teaching. Research OS routes to setup, grilling, idea triage, wayfinder, brief synthesis, research planning, workpackage decomposition, one-package execution, adaptive research development, deliverable rendering, handoff, and model primitives.

**Research OS equivalence and missing behavior.**

- Preserved: one user-only router; recommend one route; do not silently invoke a user workflow; distinguish session-sized ideation, multi-session fog, durable synthesis, decomposition, and handoff.
- Strengthened: route decisions are evidence-backed, canonical, registered, and read back; `blocked`, `needs-decision`, and `no-op` are explicit. The current route table now distinguishes a verified brief needing a plan, an approved brief needing workpackages, and one eligible package needing `research-5-run`; the former end-to-end routing break is closed.
- Missing: the router and executor bound work to one package, but neither explicitly requires a fresh context per package. Upstream makes that context-isolation rule part of the multi-session flow.
- Missing: the Smart Zone rule is present only as a repository-level context principle, not as an executable router branch with an observable threshold or handoff trigger.
- Closed during remediation: routine routing now stays in `CONTEXT` and its Artifact-index row. `research-help` creates an RDR only when route selection itself passes the four admission tests owned by `research-grilling`, so reversible workflow state no longer inflates substantive decision history.

### 2. `code-review` — Adapt

**Invocation boundary.** Upstream is model-invoked when a user asks to review a branch, PR, work-in-progress diff, or changes since a fixed point. Research OS `research-review` is model-invoked for peer review, red-team review, or artifact audit.

**Leading concept.** Upstream prevents halo effects with **two independent axes**: Standards and Spec. Research OS generalizes the same anti-masking rule into six independent skeptical-review axes and derives an overall verdict from the worst load-bearing axis.

**Ordered upstream mechanics.**

1. Pin and validate the user-supplied fixed point.
2. Capture one three-dot diff command and the commit list; fail before delegation if the ref is invalid or the diff is empty.
3. Find the originating spec in a fixed order: commit references, user path, matching repository spec, then user clarification.
4. Load repository standards and add the complete Fowler smell baseline, with repository rules overriding that heuristic baseline.
5. Spawn Standards and Spec subagents in parallel with explicit, isolated briefs and word limits.
6. Skip only the Spec agent when the user confirms that no spec exists.
7. Present reports under separate headings without merging or reranking; summarize counts and the worst finding within each axis, never across axes.

**Completion gates.** The fixed point resolves; the diff is non-empty; source material for each active axis is explicit; both subagents receive identical pinned diff context; every finding cites its governing standard or spec line; axes remain separate in the final report.

**Stop/failure branches.**

- Invalid ref or empty diff → fail before spawning agents.
- No spec found → ask; if none exists, explicitly skip only that axis.
- Repository standard contradicts a smell heuristic → repository standard wins.
- Tooling already enforces a rule → omit it from manual review.
- Baseline smells remain judgment calls, never hard violations.

**Durable state/writeback.** Upstream returns a report in conversation and does not prescribe a file. Research OS pins target identity, writes or updates one review in the resolved `REVIEWS` directory, updates affected claim states without rewriting the target, registers the artifact, and verifies all pointers by readback.

**Composition edges.** Upstream depends on setup’s issue-tracker adapter and may fetch the originating issue. Research OS delegates deeper checks to `citation-audit`, `identification-design`, `data-feasibility`, and `ethics-reproducibility`; manuscript and proposal renderers call it as a readiness gate.

**Research OS equivalence and missing behavior.**

- Preserved: immutable review target, isolated axes, explicit coverage, exact finding targets, no averaging, and negative findings that say what was checked.
- Strengthened: six domain-validity axes, worst-load-bearing-axis verdict, durable report, claim-ledger updates, version/hash pinning, and readback.
- Closed during remediation: review now selects `full-target` or `comparison` mode. Comparison pins immutable base and target hashes, builds one deterministic Markdown-aware packet containing changed sections, claim IDs, tables, and unified diff, passes that exact packet identity to every review axis and citation audit, and exits `no-op` when the hashes match. The renderer uses the same packet for revisions, so review, citation, and rendered-output readiness cannot silently inspect different deltas.
- Missing: axis isolation is recommended as separate contexts or parallel agents, but the prompt does not specify the complete independent agent briefs or require separate axis outputs before aggregation. A single agent could still let one axis contaminate another.
- Missing: the current target has no explicit “axis unavailable” policy analogous to the no-spec branch. One load-bearing missing source blocks the overall verdict, but a clearly non-applicable axis versus an unavailable axis is not normalized.

### 3. `codebase-design` — Exclude

**Invocation boundary.** Upstream is model-invoked whenever module shape, interface depth, seam placement, testability, or AI navigability is the problem. It also acts as a vocabulary authority underneath TDD and architecture review.

**Leading concept.** A **deep module** offers high leverage behind a small interface at a clean seam. The prompt fixes an exact vocabulary—module, interface, implementation, depth, seam, adapter, leverage, locality—and explicitly rejects common substitutes.

**Ordered upstream mechanics.**

1. Describe the candidate using the fixed vocabulary.
2. Minimize interface surface and hide complexity while preserving useful behavior.
3. Apply the deletion test, interface-as-test-surface rule, and “one adapter is hypothetical; two adapters make a real seam.”
4. Accept dependencies rather than constructing them and return results instead of forcing side effects.
5. When deepening a cluster, classify dependencies as in-process, local-substitutable, remote-owned, or true external.
6. Test through the deepened interface; replace obsolete shallow-module tests instead of layering both suites.
7. When alternatives are needed, frame constraints, show the frame to the user, then generate three or more radically different interfaces in isolated agents with distinct design pressures.
8. Present alternatives sequentially, compare depth/locality/seam placement, and make an opinionated recommendation or hybrid.

**Completion gates.** A proposed module earns its existence under the deletion test, has an interface callers and tests can share, exposes no internal seams merely for tests, and has justified adapters. Design-it-twice completes only after at least three genuinely different, fully specified interfaces have been compared.

**Stop/failure branches.**

- One real adapter only → do not invent a port.
- Tests must reach past the interface → module shape or seam is wrong.
- Old shallow tests duplicate new interface tests → replace them.
- Alternative designs differ cosmetically → regenerate.

**Durable state/writeback.** The base vocabulary skill writes nothing. A composed architecture session may later write domain terms or ADRs; design alternatives are presented, not automatically implemented.

**Composition edges.** Directly underpins `tdd` and `improve-codebase-architecture`; its design-it-twice branch uses parallel agents, its deepening branch supplies dependency and testing rules.

**Research OS target and exclusion rationale.** Deep-module architecture is intentionally not a research-core concern. Research OS reuses only:

- independent alternatives and fixed constraints in `design-research-three-ways`;
- canonical research vocabulary and typed relations in `research-domain-modeling`;
- interface-like question-to-observable alignment in `methodology-designer`;
- separate source contract and destination profile in `render-research-deliverable`.

**Missing behavior.**

- Deliberate exclusion: Research OS should not import module/interface/seam vocabulary into academic design where those words would distort the domain.
- Retained-mechanism gap: `design-research-three-ways` fixes exactly three lenses and compares them in one matrix, but does not require the upstream sequence “show the common problem frame first → run isolated generators → present candidates one at a time → give an opinionated recommendation/hybrid.” It has the shared brief and isolation, but not the same human absorption checkpoint.
- Retained-mechanism gap: Research OS has no single declared vocabulary authority for cross-skill terms such as claim, construct, estimand, mechanism, evidence state, and artifact status. Definitions are strong inside individual primitives, but collision resolution depends on `research-domain-modeling` rather than a shared controlled glossary.

### 4. `diagnosing-bugs` — Direct-port

**Invocation boundary.** Upstream is model-invoked for a hard bug, regression, flake, failure, or performance problem. Research OS `research-diagnosis` is model-invoked when a project stalls, results collapse, replication fails, code and theory disagree, or work stops reducing uncertainty.

**Leading concept.** Upstream’s non-negotiable core is a **tight red-capable feedback loop**. No loop means no hypothesis. Research OS translates this to a **bottleneck** diagnosed through one captured observable loop.

**Ordered upstream mechanics.**

1. Read the domain context and relevant ADRs.
2. Build a loop, trying in order: failing test, HTTP script, CLI snapshot, headless browser, captured trace replay, throwaway harness, property/fuzz loop, bisect harness, differential loop, then structured HITL script.
3. Tighten it for speed, specificity, determinism, and unattended execution. For flakes, raise the reproduction rate rather than demanding a perfect single repro.
4. Stop if no loop can be built; list attempts and request environment access, a captured artifact, or temporary instrumentation authority.
5. Run the exact symptom red, repeat it, capture it, and minimize one element at a time until every remaining element is load-bearing.
6. Generate three to five ranked falsifiable hypotheses, show them to the user, then test one variable at a time.
7. Instrument only to distinguish named predictions; prefer debugger/REPL, then targeted uniquely tagged logs. Performance work starts with measurement.
8. Write a regression test before the fix at the correct seam. If no correct seam exists, record the architectural finding rather than creating false confidence.
9. Apply the fix, watch the regression test pass, and rerun the original unminimized loop.
10. Remove instrumentation and throwaway harnesses, state the proven cause in durable change history, then recommend architecture work only if the post-mortem supports it.

**Completion gates.** Phase 1 requires one command already run with captured output that is exact-symptom-capable, deterministic or high-reproduction, fast, and agent-runnable. Later phases require exact reproduction, a load-bearing minimum case, falsifiable tested hypotheses, original-scenario verification, regression coverage or documented seam absence, cleanup, and a stated root cause.

**Stop/failure branches.**

- No red-capable loop → no hypothesis work.
- Nearby but different failure → stop; it is the wrong bug.
- No correct test seam → document architecture gap; do not write a misleading test.
- Performance regression → measure and bisect, not log indiscriminately.
- Human-only reproduction → structure it through the HITL script.

**Durable state/writeback.** The loop command, minimized repro, regression test, and commit/PR cause statement persist. Temporary instrumentation must not. Research OS writes a version-pinned diagnosis report, affected claim and decision records, a preserved regression command, and a verified Artifact-index row.

**Composition edges.** Upstream hands architectural seam failures to `improve-codebase-architecture`. Research OS delegates the discovered domain failure to the relevant primitive and only repairs when the user asked for repair.

**Research OS equivalence and missing behavior.**

- Preserved: loop before theory, exact symptom, at least one captured run, minimization, three-to-five falsifiable hypotheses, one-variable probes, root-cause separation, original-scenario rerun, optional repair boundary, cleanup accounting, and durable readback.
- Strengthened: immutable artifact/environment pinning, diagnosis-only completion, claim updates, explicit authorization before repair, and complete/partial/blocked semantics.
- Closed during remediation: Phase 1 now records exact-symptom red capability, deterministic or measured reproduction, bounded runtime, and agent-runnable or structured HITL execution as four independent gates. The prompt adds predeclared stochastic repetition/escalation, a reusable HITL receipt, a visible ranked-hypothesis checkpoint before probes, one unique instrumentation tag with zero-match cleanup proof, and a pre-repair red/post-repair green observation at the correct seam. A missing truthful seam stops as `blocked: regression_seam_missing` and routes to a bounded workpackage instead of accepting a misleading check.

### 5. `domain-modeling` — Adapt

**Invocation boundary.** Upstream is model-invoked only when the model is being changed: terminology, ubiquitous language, relationships, or a hard-to-reverse decision. Merely reading the glossary is explicitly not invocation. `research-domain-modeling` preserves this rich model-invoked boundary for ambiguous constructs, measures, mechanisms, units, estimands, or field terms.

**Leading concept.** Upstream leads with active **canonical domain language**. Research OS leads with the **construct as the unit of meaning**, separating what a study means from how it measures, identifies, or estimates it.

**Ordered upstream mechanics.**

1. Detect single-context versus multi-context layout and create files lazily.
2. Challenge any term that conflicts with the glossary immediately.
3. Replace fuzzy or overloaded language with one canonical term and explicit avoided aliases.
4. Invent concrete edge cases to stress boundaries.
5. Cross-check the user’s account against code and surface contradictions.
6. Write each resolved term to `CONTEXT.md` immediately, never batching and never mixing implementation details into the glossary.
7. Offer an ADR only when a decision is simultaneously hard to reverse, surprising without context, and the result of a genuine trade-off.
8. Use sequential ADR numbering and preserve concise rationale.

**Completion gates.** Every material resolved term has one tight definition and avoided aliases where needed; context selection is unambiguous; contradictions are resolved rather than hidden; ADRs satisfy all three admission tests.

**Stop/failure branches.**

- Multiple contexts and unclear ownership → ask which context.
- Term conflicts with glossary/code → surface the contradiction before continuing.
- General programming concept → do not add it to domain glossary.
- Any ADR admission condition absent → skip the ADR.
- Implementation detail → keep it out of `CONTEXT.md`.

**Durable state/writeback.** Canonical vocabulary goes to `CONTEXT.md`; consequential decisions go to append-only ADRs. Research OS separates a richer domain map in resolved `MAPS`, Research Decision Records in `DECISIONS`, evidence claim IDs in `CLAIMS`, and only current pointers/status in the `CONTEXT` Artifact index.

**Composition edges.** Upstream is driven by grilling, architecture review, TDD vocabulary consumers, and diagnosis. Research OS invokes `research-grilling` for consequential choices and is itself referenced by theory and equation work when semantics collide.

**Research OS equivalence and missing behavior.**

- Preserved: active collision detection, canonical definitions and avoided aliases, code/artifact cross-reference, typed relationships, separate decision records, supersession, and explicit contested/blocked states.
- Strengthened: stable IDs, construct/measure separation, provenance, direction/level/time on relations, claim links, canonical path resolution, readback, and downstream blocking on unresolved semantic collisions.
- Closed during remediation: `research-grilling` now requires all four RDR admission tests—costly reversal, surprising/unsafe without rationale, a genuine alternative trade-off, and downstream ambiguity if rationale is lost. `research-domain-modeling` references that exact gate; `research-help` keeps routine routes in `CONTEXT`; and `research-workspace-contract` applies all four tests while seeding state. Routine terminology, routing, formatting, and progress no longer enter `DECISIONS`.
- Missing: upstream requires immediate inline writeback at the moment a term crystallizes. Research OS requires re-read-before-write and durable output, but the build procedure can still batch an entire model before persisting intermediate accepted terms.
- Intentional change: a separate domain-map artifact replaces a glossary-only `CONTEXT.md`. This is appropriate because research relations, construct status, provenance, and measurement collisions are too rich for the context index.

### 6. `grill-with-docs` — Direct-port

**Invocation boundary.** Upstream is user-only. Its seven-line prompt is deliberately a thin wrapper: run the reusable grilling primitive while also running domain modeling. Research OS `research-1-grill` is likewise user-only and composes model-invoked interviewing and domain modeling without invoking another user workflow.

**Leading concept.** Upstream delegates its leading behavior to the **decision interview plus durable domain writeback**. Research OS makes the **decision tree** explicit and adds researchability as the terminal criterion.

**Ordered upstream mechanics.**

1. Enter the generic one-question-at-a-time grilling flow.
2. Keep domain-modeling active during the same exchange.
3. Persist glossary changes and qualifying ADRs as decisions crystallize.

**Completion gates and stops.** They are inherited: grilling must resolve the active decision tree, and domain modeling must leave no silently conflicting term. The wrapper itself adds no independent completion claim.

**Durable state/writeback.** Upstream writes `CONTEXT.md` and ADRs inline. Research OS writes `CONTEXT`, domain maps, `DECISIONS`, and `CLAIMS`, then registers and reads back the current artifacts.

**Composition edges.** Upstream composes `grilling` + `domain-modeling`. Research OS composes `research-grilling` + `research-domain-modeling` and may call evidence, literature, data, design, or falsification primitives for discoverable facts.

**Research OS equivalence and missing behavior.**

- Preserved: explicit user entry, one human decision at a time, agent-owned fact finding, inline durable state, and no automatic transition to a downstream user workflow.
- Strengthened: a fixed research decision order, researchability stress test, falsifier/kill criteria, canonical paths, artifact registration, readback, and `repair`/`needs-map`/`kill-candidate` branches.
- Structural divergence: upstream’s wrapper remains intentionally tiny so primitive rules have one authority. Research OS currently carries substantial orchestration logic in `research-1-grill` in addition to the two primitives. The extra domain sequence is useful, but overlapping “one question,” decision persistence, and completion rules create a drift surface that should be regression-tested.
- Missing: when the unresolved graph exceeds one session, the orchestrator recommends wayfinder, but it does not require a handoff manifest before yielding. The durable decision records reduce risk, yet live frontier context can still be lost.

### 7. `implement` — Adapt

**Invocation boundary.** Upstream is user-only because it is a mutation workflow: the user supplies a spec or ticket, and the skill edits, tests, reviews, and commits. Research OS now has two user-only boundaries: `research-auto` is the broader topic-to-deliverable loop, while `research-5-run` is the direct one-contract execution boundary and accepts exactly one eligible package.

**Leading concept.** Upstream has no named noun, but its control object is one **piece of work** governed by a spec/ticket. `research-5-run` uses **claim**: one immutable package envelope is selected, atomically owned, executed, tested, reviewed when load-bearing, sealed, and used to recompute the frontier. This is the research-domain equivalent of the upstream control object. `research-auto` remains the broader adaptive loop for work that has not yet reached package form.

**Ordered upstream mechanics.**

1. Load the work described by the supplied spec or ticket.
2. Implement with TDD where possible, only at pre-agreed seams.
3. Run typechecking and the active single test file repeatedly during development.
4. Run the full test suite once at the end.
5. Run `code-review` over the completed change.
6. Commit the reviewed work to the current branch.

**Completion gates.** The requested behavior exists; agreed seam tests pass; typecheck and focused tests have been exercised during work; the full suite passes; independent review is complete; the commit exists.

**Stop/failure branches.** The 15-line upstream prompt leaves these mostly implicit. Its composition nevertheless implies: do not invent work beyond the ticket; do not add tests at unagreed seams; do not commit before final suite and review. There is no explicit blocked/partial model.

**Durable state/writeback.** Source code, tests, and the Git commit are the durable state. The originating ticket/spec remains the behavioral contract. Upstream commits automatically as part of the explicitly invoked workflow.

**Composition edges.** `implement` consumes `to-spec`/`to-tickets`, drives `tdd`, then calls `code-review`. The router requires one fresh context per ticket for multi-session builds.

**Research OS target behavior.**

- `research-auto` establishes a mission, resolves one uncertainty frontier at a time, invokes the narrowest primitive, attacks and repairs the design, synthesizes a canonical Research Brief, and renders the requested downstream artifact.
- `research-4-tasks` creates the dependency graph and per-package acceptance/failure contract.
- `research-5-run` selects one eligible package, pins its file and input versions, claims it through the shared atomic compare-and-set helper, stays inside its read/write envelope, records operations and costs, runs package-local plus project-level gates, conditionally invokes independent review, seals a receipt, and recomputes the frontier.
- `pilot-study` remains the specialized empirical-pilot primitive that an executing package may use.
- `research-review` provides the independent post-work attack.

**Equivalence and missing behavior.**

- Preserved: explicit user entry; contract-driven work; narrow cycles; factual work before user questions; verification and review before completion; durable writeback; no external side effect without authority.
- Strengthened: `research-auto` adapts the route before decomposition, while `research-5-run` enforces exactly-one-package ownership, immutable inputs, explicit allowed writes, package and project checks, separate execution/domain verdicts, external-authority stops, sealed receipts, and readback. `research-help` now routes an eligible package to that executor.
- Correctly excluded: automatic Git commit. A research workflow invocation is not commit authorization, and commit is not the universal durable unit of academic work.
- Closed during this audit: the former load-bearing absence of a package executor. The ordered prompt now covers blocker readback, atomic claim, bounded execution, operation/input/output/cost provenance, local acceptance and falsifier, project integration/reproducibility, load-bearing review, receipt sealing, `complete|partial|blocked`, and a verified already-sealed `no-op`.
- Closed during the final claim-lifecycle revision: `research-4-tasks` now owns the explicit `proposed → ready` gate and makes every ready version immutable; claim IDs include package version and source-hash prefix; all package/index/claim/readback writes occur before seal; the helper rechecks the source hash and validates JSON receipt fields, identity, and result; safe owner release archives a receipt.
- Remaining: the upstream “fresh context for each ticket” boundary is not explicit. The executor limits one invocation to one package, but does not tell a caller to start that invocation in a fresh context.
- Remaining: the upstream red/green inner loop is only conditionally approximated. Computational work should establish an independent observable failure “when practical,” but the prompt does not require one minimal green change or a user-confirmed observation seam.
- Closed during the terminal-CAS revision: `seal` and `release` now publish one shared terminal JSON through an atomic no-replace hard-link compare-and-set. Exactly one terminal state wins; either command can re-enter after a partial finalize and complete its matching public receipt plus history archival. The claim ID’s attempt component makes a separately authorized retry a new identity.

### 8. `improve-codebase-architecture` — Exclude

**Invocation boundary.** Upstream is user-only. It is proactive maintenance, not a hidden refactor: the user asks for a survey, sees candidates, then chooses whether to explore one.

**Leading concept.** A **deepening opportunity** is a refactor that moves behavior behind a smaller interface at a better seam, improving locality, leverage, testability, and agent navigability.

**Ordered upstream mechanics.**

1. Scope the survey before scanning. Follow a user-named area; otherwise use a meaningful commit-history window to find hot spots and widen only when no concentration exists.
2. Read the domain glossary and relevant ADRs.
3. Use an exploration agent organically; note navigation friction, shallow modules, leaked seams, scattered testability, and low locality.
4. Apply the deletion test to each candidate.
5. Write a fresh self-contained HTML report in the OS temp directory, never the repository.
6. Give each candidate files, problem, solution, benefits, recommendation strength, dependency category, and a purpose-built before/after visual. End with one top recommendation.
7. Open the report and tell the user its absolute path.
8. Do **not** propose interfaces yet. Ask which candidate to explore.
9. Grill the selected candidate, update domain terms inline, offer an ADR only for a durable load-bearing rejection, and use design-it-twice when interface alternatives are needed.

**Completion gates.** The report is scoped to likely-change areas, uses exact design vocabulary, visualizes each candidate, calls out relevant ADR conflicts, ranks one top recommendation, and stops before interface design. Selection and design are a separate phase.

**Stop/failure branches.**

- User gives scope → do not infer another.
- No commit hot spot → widen scan.
- Candidate violates an ADR without enough real friction → suppress it.
- No candidate selected → stop after report.
- Rejection is temporary/self-evident → do not create an ADR.

**Durable state/writeback.** The survey report is intentionally ephemeral in the temp directory. Only selected, crystallized domain terms or qualifying ADRs enter the repository. No refactor is performed.

**Composition edges.** Uses `codebase-design`, `grilling`, and `domain-modeling`; diagnosis may hand it a missing-seam finding.

**Research OS target and exclusion rationale.** Research OS deliberately excludes a code-architecture maintenance skill. It reuses pieces in:

- `research-diagnosis` for reactive bottleneck/root-cause work;
- `design-research-three-ways` for independent alternatives;
- `research-grilling` and `research-domain-modeling` for selection and semantics;
- `render-research-deliverable` for destination-aware artifact rendering.

**Missing behavior.**

- Deliberate exclusion: an HTML/Tailwind/Mermaid architecture report and deep-module candidate scan do not belong in the academic core.
- Optional research-operations gap: no skill proactively surveys the **research system itself** for repeated friction—stale claim chains, duplicated artifacts, shallow workpackages, recurrent manual joins, or areas with high repair churn—before selecting one improvement. `research-diagnosis` triggers on a known failure, not opportunistic health maintenance.
- Retained-mechanism gap: no current Research OS flow enforces “survey several candidates first, select one, then design it” as a phase boundary. `research-auto` chooses the narrowest active primitive, which is adaptive but not a proactive candidate survey.

### 9. `prototype` — Adapt

**Invocation boundary.** Upstream is model-invoked when a design question needs a runnable answer: logic/state behavior or visual UI shape. Research OS `pilot-study` is model-invoked when one cheap end-to-end empirical tracer or interaction prototype can collapse feasibility, identification, representation, or usability uncertainty.

**Leading concept.** Upstream: **throwaway code answers one question**. Research OS: a **tracer** preserves the complete input/action/state/output-to-verdict path while shrinking scale, duration, and polish.

**Ordered upstream mechanics.**

1. Name the exact question and choose the logic or UI branch. If ambiguous and the user is absent, infer from surrounding code and record the assumption.
2. Mark code visibly as prototype, colocate it with the future use site, give it one run command, keep state in memory, skip polish/tests/abstractions, and surface complete state after every action or variant switch.
3. Logic branch: choose the project runtime; isolate portable pure logic; build the smallest full-frame TUI; hand the run command to the user.
4. UI branch: strongly prefer variants embedded in the real page; create a throwaway route only as a last resort. Generate three by default, at most five, structurally different variants.
5. Switch UI variants by a shareable/reload-stable `?variant=` parameter and floating keyboard-accessible bar hidden in production.
6. After the user learns the answer, fold only the validated decision into production.
7. Preserve the prototype as a primary source on a throwaway branch, linked from the implementation issue; keep losing variants and the TUI shell off main.

**Completion gates.** The prototype names one question, is runnable in one command, exposes relevant state, produces a user verdict, and preserves both the answer and the primary-source artifact without shipping prototype scaffolding.

**Stop/failure branches.**

- Logic versus appearance ambiguous → ask; if unreachable, choose from surrounding code and state the assumption.
- Existing page can host UI → do not invent a detached route.
- Variants differ only cosmetically → regenerate.
- Prototype needs production tests, persistence, mutations, generalized abstractions, or polished error handling → scope has drifted.
- Prototype has answered the question → capture and remove from main, do not keep iterating as product.

**Durable state/writeback.** A throwaway branch preserves the runnable primary source; the issue/commit records the question and verdict; production/main receives only the validated decision and rewritten production implementation.

**Research OS target behavior.** `pilot-study` first selects an empirical-tracer or interaction-prototype branch. Both freeze one uncertainty, smallest representative inputs, the hardest seam, one reproducible command/protocol, authority/cost gates, predeclared `go|repair|stop`, execution receipts, claim updates, and canonical `plan.md`/`result.md`. The interaction branch additionally defines actor, starting state, actions, transitions, visible and failure states, representation variants under fixed content, and evaluator observations.

**Equivalence and missing behavior.**

- Preserved: one question, smallest faithful artifact, hardest seam, no scale/polish inflation, observable state/result, explicit handoff, and a verdict that can kill rather than “succeed.”
- Strengthened: frozen versions and environment, legal/ethics/access authority, paid-resource gate, costs and failures as evidence, immutable thresholds, claim status updates, and readback.
- Intentional change: canonical pilot artifacts replace throwaway Git branches. In research, the protocol and even a failed run are durable evidence, not disposable scaffolding.
- Closed during remediation: a questionnaire/interview flow, coding schema, research-software state model, analytic interface, decision aid, or explanation can now use a dedicated interaction branch rather than being forced through acquisition→estimation stages. Scaffolding is quarantined under the pilot ID; only the validated minimal core may move forward through a separately authorized bounded workpackage, while archive/delete actions require explicit authority and a receipt.

### 10. `research` — Direct-port

**Invocation boundary.** Upstream is model-invoked for documentation/API/source research and explicitly delegates it to a background agent so the caller can continue working. Research OS `evidence-research` is model-invoked whenever an external premise must be verified rather than recalled.

**Leading concept.** Upstream leads with **primary-source reading**. Research OS sharpens this into a **claim chain** from one exact scoped claim to inspectable evidence and entailment.

**Ordered upstream mechanics.**

1. Spawn a background agent.
2. Investigate only through primary/first-party sources; use secondary writing to discover, never to own, a claim.
3. Trace every claim back to the owning source.
4. Write one cited Markdown findings file where the repository already keeps research notes, or choose and report a sensible location.

**Completion gates.** Every finding is tied to a primary source and a durable cited file exists in the repository.

**Stop/failure branches.** A secondary write-up cannot close a claim. If no note convention exists, choose one explicitly rather than leaving findings only in chat.

**Durable state/writeback.** One cited memo is the durable output. Research OS instead atomizes claims in the configured claims registry, records exact source locators, entailment, status, caveats, coverage, freshness, and task outcome, then registers and reads back claim IDs.

**Composition edges.** Upstream feeds grilling and wayfinder and can run in parallel with foreground work. Research OS feeds nearly every primitive and is invoked by gap, data, citation, review, and development flows.

**Research OS equivalence and missing behavior.**

- Preserved: primary-source ownership, direct inspection, durable cited output, and downstream reuse.
- Strengthened: atomic scopes, exact locators, disconfirming search, independent corroboration for high-stakes claims, version checks, controlled statuses, schema preservation, and fail-closed completion.
- Missing: `evidence-research` does not itself require background delegation. `research-map` permits parallel factual work, but standalone evidence tasks can still block the foreground session.
- Intentional change: the target does not require one free-form Markdown memo. The ledger is a better authority for claims, while literature maps and briefs own synthesis.
- Possible usability gap: when a source investigation produces important non-claim operational detail, the prompt offers no explicit companion memo rule; forcing all context into structured claim entries risks either bloated YAML or loss of reading notes.

### 11. `resolving-merge-conflicts` — Exclude

**Invocation boundary.** Upstream is model-invoked only for an already in-progress Git merge or rebase. It is not a general refactor or branch-comparison skill.

**Leading concept.** Resolve each conflict by recovering **both intents from primary sources**, then preserve both where compatible and choose according to the merge’s stated goal where they are not.

**Ordered upstream mechanics.**

1. Inspect merge/rebase state, history, and all conflicting files.
2. Recover why each side changed by reading commits, PRs, issues, and tickets.
3. Resolve every hunk; preserve both intents when possible, otherwise choose the goal-compatible intent and record the trade-off.
4. Do not invent a third behavior.
5. Discover and run project checks, normally typecheck → tests → format.
6. Stage and finish the merge; continue a rebase until every commit is rebased.

**Completion gates.** No conflict remains; both intents were traced; incompatible trade-offs are named; automated checks pass; Git operation is finished.

**Stop/failure branches.**

- Never abort.
- Never choose from syntax alone when intent sources are available.
- Never invent behavior not owned by either side.
- Incompatibility → choose against the stated merge goal and disclose the loss.

**Durable state/writeback.** The resolved tree, staged state, completed merge/rebase, commit history, and any trade-off note persist.

**Research OS target and exclusion rationale.** Finishing a Git merge/rebase remains outside the academic research core, but its durable intent-reconciliation mechanism now has a first-class research target:

- `artifact-reconciliation` pins both conflicting identities, hashes, lineages, decisions, claims, and downstream consumers;
- it classifies fact, human-choice, schema, execution, and concurrent-edit conflicts before resolving;
- it preserves compatible content and both provenances, sends facts to evidence authority and choices to one named human owner, and creates one superseding artifact rather than editing parents into agreement;
- it invalidates and reruns affected downstream gates, supersedes both parent rows, and reads back exactly one current pointer; and
- `research-save`, `synthesize-research-brief`, `research-domain-modeling`, and `research-grilling` stop and route conflicts to this primitive rather than choosing a winner.

**Equivalence and retained boundary.**

- Deliberate exclusion: Research OS should not promise to finish a Git merge/rebase as a core research skill.
- Closed during remediation: the canonical research path now performs the complete `conflict → verified current artifact` transition while retaining the safe stop boundary for missing lineage, evidence, decision authority, schema mapping, or unapproved mutation.

### 12. `setup-matt-pocock-skills` — Adapt

**Invocation boundary.** Upstream is user-only and intended to run once before the engineering suite. Research OS `research-setup` remains user-only and is now a thin wrapper over the model-invoked `research-workspace-contract` primitive. The primitive requires either explicit setup invocation or explicit local-setup authority from a calling workflow.

**Leading concept.** Upstream is **explore, present, confirm, then configure**. Research OS leads with a durable **workspace contract** whose paths, authority, and receipts are canonical.

**Ordered upstream mechanics.**

1. Explore remotes, instructions, existing agent-skill blocks, context/ADR layout, prior setup docs, local tracker signals, triage availability, and monorepo signals.
2. Present what exists and what is missing.
3. Ask sections in order, one answer each: issue tracker; triage labels only if triage exists; multi-context layout only if monorepo evidence exists. Lead with a recommended answer.
4. Show exact drafts of the instruction-file block and every `docs/agents/*.md` file; let the user edit before writing.
5. Select `CLAUDE.md` if present, otherwise `AGENTS.md`; if neither exists, ask. Update an existing block in place and preserve surrounding edits.
6. Materialize tracker, label, and domain consumer templates.
7. Report which skills now consume the configuration and how later edits work.

**Completion gates.** Starting state is known; every genuine choice is confirmed; exact draft content is approved; no alternate instruction file or duplicate section is created; all configured docs are written without overwriting unrelated content.

**Stop/failure branches.**

- Triage absent → omit label questions and artifacts.
- No monorepo signals → choose single context without asking.
- Neither instruction file exists → ask which to create.
- Existing block → update in place.
- Custom tracker → preserve the user’s described adapter rather than force a template.

**Durable state/writeback.** Upstream writes instruction-file pointers and `docs/agents/{issue-tracker,triage-labels,domain}.md`; tracker-specific references define native blocking, claims, and resolution. Research OS writes config, context, claims registry, canonical directories, and versioned templates; adapters live in config; every write receives a receipt and readback.

**Research OS equivalence and missing behavior.**

- Preserved: explicit boundary, inspect first, additive setup, adapter support, never create a second source of truth, preserve conflicts, seed domain knowledge lazily, and tell downstream skills where authority lives.
- Strengthened: config-first path resolution; deterministic `uv` initializer; dry-run/apply/check modes; canonical artifact authority; claim ledger; single Artifact index; authorization boundary; partial/blocked status; byte-preservation intent; readback.
- Improved architecture: the user wrapper is thin and the reusable contract mechanics now have one primitive authority.
- Missing: upstream requires the user to see and edit exact file drafts before any write. Research OS preflight reports path classifications, not the content of every proposed baseline file, and applying after preflight does not require a distinct confirmation checkpoint.
- Closed during the final preflight revision: dry-run, apply, and check now run the same stable-content validator before mutation. It verifies every required canonical key, baseline-versus-adapter values, the unique Artifact-index marker and exact header, claims schema/version/status vocabulary, registry marker, and required template markers. Existing regular files become `unchanged` only after those compatibility checks pass; content conflicts return before apply writes.
- Verified proof: `test_workspace_initializer_proves_contract_markers_pass_fail_pass` exercises missing `canonical.plans`, a missing required claim status, a missing template gate, repair, and acceptance of a user-maintained context body that preserves the contract markers. `test_workspace_initializer_refuses_nonbaseline_adapter_without_writes` proves a nonbaseline adapter receives `nonbaseline-adapter-requires-direct-verification` and produces no filesystem change. The additive/idempotent test separately proves dry-run non-mutation, byte preservation, and check readback.
- Remaining, non-P0: the initializer intentionally refuses rather than validates a nonbaseline adapter; the primitive’s direct path-by-path verification remains the authority, without an equivalent deterministic adapter receipt. Its lightweight config parser also validates canonical markers/values rather than strict YAML duplicate-key semantics. These limitations cannot silently initialize or overwrite an adapter, so they are capability/hardening gaps rather than the former safety-critical preflight gap.

### 13. `tdd` — Exclude

**Invocation boundary.** Upstream is model-invoked for test-first feature work, bug fixing, red-green-refactor, or integration tests. It can be called directly or driven internally by `implement`.

**Leading concept.** **Red → green**, one vertical behavioral slice at a time. Despite the familiar phrase “red-green-refactor,” upstream explicitly moves refactoring out of the cycle and into review.

**Ordered upstream mechanics.**

1. Read domain vocabulary and relevant ADRs.
2. Identify public interfaces and write down proposed test seams.
3. Confirm every seam with the user before writing any test.
4. Write one behavior-level test through one public seam.
5. Make it fail for the intended missing behavior.
6. Write only enough implementation to make it pass.
7. Repeat with the next tracer-bullet behavior; never write all tests first.
8. Leave refactoring to code review.

**Test-quality rules from direct references.**

- Tests describe caller/user behavior and use public interfaces.
- Expected values come from an independent source of truth, not the same calculation as the implementation.
- Verify observable outcomes through the interface, not database internals or call counts.
- Mock only true system boundaries; prefer test databases/local stand-ins where practical.
- Inject external dependencies and prefer operation-specific SDK-like ports over a generic conditional fetcher.

**Completion gates.** Every test seam was pre-agreed; each cycle visibly went red then green; tests survive internal refactors; no tautology, internal-collaborator mock, private-method test, or horizontal test-first batch remains.

**Stop/failure branches.**

- Seam not confirmed → do not write the test.
- Test requires internals or side-channel verification → redesign the seam/test.
- Expected value repeats implementation → replace it with an independent oracle.
- All tests before all implementation → stop and return to one vertical slice.
- Speculative future behavior → do not implement.

**Durable state/writeback.** Production behavior and regression tests persist. The prompt itself defines no separate receipt.

**Research OS target and exclusion rationale.** Universal TDD is intentionally excluded because open-ended research cannot always be specified before observation. Research OS retains selected mechanics in:

- `research-4-tasks`: vertical tracer studies and explicit acceptance/failure criteria;
- `pilot-study`: one reproducible source-to-verdict path with frozen inputs and predeclared thresholds;
- `falsification-first`: independent failure oracles and action rules set before outcomes;
- `research-5-run`: one claimed vertical slice, an independent observable failure before repair when practical, then package-local and project-level checks;
- `research-auto`: one bottleneck/frontier cycle at a time before or outside package execution.

**Missing behavior.**

- Deliberate exclusion: do not force exploratory literature, theory generation, construct discovery, or qualitative interpretation into code-style red-green tests.
- Partially closed for computational workpackages: `research-5-run` requires an independent observable failure before repair when practical and always requires package-local plus project integration/reproducibility checks. It still does not require a visible minimal red → minimal green sequence, so an implementation-heavy package may jump from failure observation to a broad repair.
- Real gap: “pre-agreed seam” becomes “predeclared observable/falsifier” only loosely. Workpackages record checks and thresholds, but the user does not explicitly approve the observation seam before implementation begins.

### 14. `to-spec` — Adapt

**Invocation boundary.** Upstream is user-only. It takes the current conversation and codebase understanding and synthesizes them; it explicitly does not restart interviewing. Research OS `research-2-brief` is user-only and now delegates the reusable synthesis mechanics to model-invoked `synthesize-research-brief`. `to-plan` separately renders an executable academic plan from the verified brief.

**Leading concept.** Upstream turns settled context into a **spec/PRD**. Research OS calls this **collapse**: one audience-neutral Research Brief is the canonical design contract, while a plan is a downstream destination-specific rendering.

**Ordered upstream mechanics.**

1. Explore the repository if needed; use glossary vocabulary and respect ADRs.
2. Sketch testing seams, preferring existing and highest possible seams; minimize seam count.
3. Confirm those seams with the user.
4. Synthesize, without a fresh interview, a problem statement, solution, extensive user stories, implementation decisions, testing decisions, scope exclusions, and notes.
5. Avoid file paths and code snippets because they stale; permit only a decision-rich prototype excerpt.
6. Publish to the configured issue tracker and mark ready for an agent.

**Completion gates.** The user confirms seams; the spec covers the complete feature and boundaries; implementation/testing decisions reflect prior discussion; the issue is durably published with readiness state.

**Stop/failure branches.**

- Missing tracker config → setup first.
- No current codebase understanding → explore before synthesis.
- Unsettled seam choice → ask only that decision.
- No paths/snippets except a prototype fragment that is more precise than prose.
- No new general interview.

**Durable state/writeback.** The tracker issue is the authoritative spec and receives `ready-for-agent`. Research OS writes one versioned brief in canonical `BRIEFS`, registers and reads it back, then optionally renders a plan in canonical `PLANS`.

**Research OS equivalence and missing behavior.**

- Preserved: synthesize existing state, do not reopen settled choices, source every section, keep one canonical contract, record scope/non-goals/testing or evaluation decisions, and emit a readiness state.
- Strengthened: verified claim and decision source table, contradiction/supersession detection, claim-strength ceiling, planned-versus-observed separation, causal identification gate, falsifiers, ethics, readiness mapping, canonical paths, and readback.
- Improved architecture: `research-2-brief` is now a thin user wrapper; `synthesize-research-brief` is the reusable primitive. `to-plan` correctly separates an audience-neutral research contract from an institutional/executable rendering.
- Closed writer authority: `synthesize-research-brief` is the only canonical brief writer. `render-research-deliverable` treats its Research Brief profile as validation-only and stops `blocked: canonical_writer_mismatch` instead of creating or repairing a brief.
- Missing: there is no direct analogue of an explicit pre-draft **test-seam approval**. The brief contains observables, methods, diagnostics, and falsifiers, but the user confirmation gate does not require approval of the highest reliable observation seam.
- Closed during remediation: `to-plan` now requires a current sufficiently ready canonical brief, stops with the exact missing prerequisite, recommends `research-auto` or `research-2-brief`, and explicitly forbids silent setup or synthesis under the plan wrapper.
- Intentional change: no issue-tracker publication or `ready-for-agent` label. Research OS writes locally and requires separate authorization for external mutation.

### 15. `to-tickets` — Direct-port

**Invocation boundary.** Upstream is user-only because it publishes issues or writes a local issue set. Research OS `research-4-tasks` is user-only and writes the canonical execution graph locally.

**Leading concept.** Upstream uses **tracer-bullet vertical slices with blocking edges**. Research OS directly translates this to a **tracer study** that crosses question → evidence/data → construct → method → result → falsifier → verdict.

**Ordered upstream mechanics.**

1. Consume current conversation or fetch a referenced spec/issue in full, including comments.
2. Explore code only if needed; use domain vocabulary, respect ADRs, and look for prefactoring that makes the change easy.
3. Draft narrow, complete, independently demoable vertical slices, each small enough for one fresh context.
4. Record every genuine blocker.
5. For a mechanical wide refactor, use expand → migration batches → contract; use an integration branch/final integration ticket only when individual batches cannot remain green.
6. Present numbered tickets with title, blockers, and delivered behavior.
7. Quiz the user on granularity, edge correctness, and merge/split changes until approved.
8. Publish one ticket per artifact in dependency order, using native blocking when available.
9. Work the unblocked frontier; never modify or close the parent issue.

**Completion gates.** Each ticket is end-to-end, independently verifiable, context-sized, and has explicit blockers; the user approves the graph; one artifact exists per ticket; the frontier is mechanically computable.

**Stop/failure branches.**

- Horizontal layer-only ticket → reslice vertically.
- Mechanical blast radius cannot stay green → use expand–migrate–contract.
- Blocker is merely convenient ordering → remove the edge.
- Breakdown not approved → iterate, do not publish.
- Parent issue → leave unchanged.

**Durable state/writeback.** Upstream uses one local Markdown file per ticket or one real tracker issue per ticket, with native/text dependency edges. Research OS writes one canonical package index plus one record per package in `WORKPACKAGES`, links obligations back to the brief, registers and reads back every artifact.

**Research OS equivalence and missing behavior.**

- Preserved: full-source intake, vertical slices, first tracer, context-sized units, real blocking edges, expand–migrate–contract exception, user graph approval, one artifact per package, and computable frontier.
- Strengthened: exact obligation coverage, stable IDs, claim/evidence inputs, failure thresholds, reproducibility, decision ownership, a per-package context envelope of immutable inputs and allowed reads/writes, cycle/orphan/duplication rejection, canonical lineage, and readback.
- Missing: upstream’s quiz explicitly asks whether tickets should merge or split. Research OS presents package granularity and asks approval, but does not require the three explicit questions; a terse approval could skip a deliberate merge/split check.
- Closed composition edge: decomposition still ends correctly without starting work, while the separately user-invoked `research-5-run` now consumes and seals exactly one eligible frontier package.
- Closed readiness handoff: Stage 5 now defines `proposed → ready → claimed externally → sealed receipt`, makes readiness conditional on complete blockers, immutable inputs, context envelope, checks, falsifier, and expected receipt, and requires superseding versions rather than edits. Claim/outcome state remains outside the immutable package, so the executor can compute eligibility from ready versions and exact-version sealed blocker receipts.

### 16. `triage` — Adapt

**Invocation boundary.** Upstream is user-only because it can label, comment on, and close external issues/PRs. It acts only on raw incoming requests, never tickets created by `to-tickets`. Research OS `research-triage` is user-only and applies evidence-backed verdicts to research ideas.

**Leading concept.** Upstream uses a strict **state machine**: exactly one category (`bug|enhancement`) and one state (`needs-triage|needs-info|ready-for-agent|ready-for-human|wontfix`). Research OS uses exactly one **verdict** (`kill|repair|pilot|advance`) with the human retaining final authority.

**Ordered upstream mechanics.**

1. For discovery, show three oldest-first buckets: unlabeled, needs-triage, and needs-info with new reporter activity. Include only external PRs when configured.
2. For one item, read full body/comments/labels/author/dates and PR diff; parse prior notes.
3. Search by domain concept for an existing implementation and inspect `.out-of-scope/` for a prior rejected concept.
4. Recommend category and state with codebase reasoning, then wait for maintainer direction.
5. Verify the claim before grilling: reproduce bug or check out/test PR.
6. Grill only if needed, updating domain state inline.
7. Apply the approved outcome: durable agent/human brief, actionable needs-info note, or reason-specific wontfix behavior.
8. For a rejected enhancement, update one concept-level `.out-of-scope/` record; never put already-implemented behavior there.
9. Support explicit quick overrides after previewing exact mutations.
10. On resume, read prior notes and new reporter activity; never repeat resolved questions.

**Completion gates.** Exactly one category and state; maintainer approval; claim verification status; every external comment starts with the AI disclaimer; `ready-for-agent` has a durable behavioral brief with testable acceptance and scope; rejected enhancements have deduplicated institutional memory.

**Stop/failure branches.**

- Conflicting state labels → ask before doing anything.
- Verification fails or detail is insufficient → recommend `needs-info`.
- Already implemented → point to implementation, close, and do not poison out-of-scope memory.
- Rejected bug → close without out-of-scope record.
- Rejected enhancement → record one concept-level rejection, comment, then close.
- Quick override → trust maintainer but preview role/comment/close actions first.

**Durable state/writeback.** Tracker roles, AI-labeled comments, agent briefs, needs-info history, issue closure, and `.out-of-scope/<concept>.md` form the state machine and institutional memory.

**Research OS target behavior.** `research-triage` supports one-item, discover, and resume modes; derives a concept signature and aliases; compares them with existing verdicts before allocating an ID; pins a `checked_at` evidence frontier; inventories load-bearing claims; verifies premises; recommends one verdict and a reason code; records the human decision and consequences; registers artifacts; and supports blocked/conflict/no-op.

**Equivalence and missing behavior.**

- Preserved: evidence before transition, one explicit outcome, recommendation before human decision, distinct repair/pilot paths, durable reasoning, no silent promotion, and no-op when current evidence has not changed.
- Strengthened: literature, contribution, theory, measurement, data, identification, falsification, ethics, execution cost, claim statuses, and readback all participate in the gate.
- Intentional change: external issue/PR mutation, AI comment disclaimer, reporter interaction, and tracker labels are outside the research core.
- Closed during remediation: discovery returns untriaged, resumed-evidence, human-decision, and no-op buckets without silently executing them; resume recomputes only changed frontiers; renamed concepts reuse prior lineage; and `already-established`, `out-of-scope`, `invalid`, `superseded`, `evidence-changed`, and `insufficient-evidence` remain distinct from the strategic `kill|repair|pilot|advance` verdict.

### 17. `wayfinder` — Direct-port

**Invocation boundary.** Upstream is user-only and reserved for work too foggy for one session. It has two explicit invocation modes: chart a new map from a loose idea, or work one decision on an existing map. Research OS `research-map` is also user-only for genuinely multi-session uncertainty.

**Leading concept.** Both use **destination → fog → frontier**. A map plans decisions, not deliverables; the frontier contains precise, open, unblocked, unclaimed decisions; fog contains in-scope unknowns not yet precise enough to ticket.

**Ordered upstream mechanics.**

1. Name and confirm the destination first; it defines scope.
2. Breadth-first map current decisions and first takeable steps.
3. If no fog remains and one session can finish, stop: no map is needed.
4. Create one canonical map issue containing destination, notes, concise decision pointers, not-yet-specified fog, and out-of-scope.
5. Create currently stateable child decision tickets, then wire blocking edges in a second pass.
6. Fire all research tickets in background agents and stop; charting resolves nothing else.
7. In work mode, load only the low-resolution map, choose a named or first-frontier ticket, and claim it by assignment **before any work**.
8. Resolve the ticket with the type-appropriate workflow: research AFK, prototype/grilling HITL, or an enabling task.
9. Post the answer, close the ticket, and append only a gist/link pointer to the map.
10. Promote newly precise fog, create-then-wire new tickets, recompute invalidated nodes, and move beyond-destination work to out-of-scope.
11. Never resolve more than one non-research ticket per session.

**Completion gates.** Destination is explicit; map and decision detail have separate authorities; every ticket is precise, typed, context-sized, and edge-wired; only the unclaimed frontier is takeable; each resolution is durable before recomputation; route is clear only when no decision remains before execution/specification.

**Stop/failure branches.**

- No meaningful fog → stop as too small for a map.
- Question cannot yet be stated precisely → keep it in fog, not a ticket.
- Work lies beyond destination → out-of-scope, never future fog.
- HITL ticket → agent never supplies the human side.
- Chart mode → stop after map/tickets/research dispatch.
- Work mode → one ticket per session, research parallelism excepted.
- Map clear → hand off to spec; do not build directly from low-resolution map.

**Durable state/writeback.** The tracker map is an index; child tickets own questions and resolution comments; native dependency/assignment state makes concurrency visible. Research OS uses canonical `MAPS` plus one record per decision in `DECISIONS`, updates claims/context, registers and reads back all current pointers, and uses the shared workspace-contract helper for atomic active claims, sealed receipts, and claim history.

**Research OS equivalence and missing behavior.**

- Preserved: destination, breadth-first fog, precise-question graduation, explicit blockers, separate map/index versus decision substance, one HITL decision per invocation, parallel factual work, out-of-scope boundary, too-small/blocked/route-clear endings, and no automatic next user workflow.
- Closed during this audit: explicit `chart` and `work` modes are selected before work; charting creates every stable decision record before wiring blockers, may dispatch only isolated factual tasks, and must stop as `chart-complete`; it cannot resolve a frontier node in the same invocation.
- Closed during this audit: work mode pins the decision-record hash and atomically claims a hash-versioned node before reading sources or asking the decision question. It proceeds only on read-back `claimed`, stops/reselects on `already-claimed`, verifies and recomputes on `already-sealed`, refuses time-only stale-claim theft, and retains interrupted work as claimed with continuation state.
- Closed during the final claim revision: the claimed question remains immutable; its answer lives in a separate resolution record; map, frontier, claims, context, index, and receipt all agree and read back before seal; the helper rechecks the source plus receipt identity/result/schema; no map or decision mutation follows seal; an acknowledged owner can archive a release with an explicit reason.
- Closed during the terminal-CAS revision: seal and release now compete for one no-replace terminal record, the losing intent receives a structured conflict, and the winning intent can re-enter to finish its public receipt and claim-history archival after interruption.
- Strengthened: canonical paths, claim/decision authority split, evidence primitives, stable IDs, current Artifact index, readback, strict complete/partial/blocked reporting, and a shared version/attempt-aware claim authority instead of tracker-assignment assumptions.
- Missing: the map can reach `route-clear` when no unresolved decision blocks a brief, but it does not explicitly require handing the linked decisions through `synthesize-research-brief` before development. The router may recommend the right next workflow, yet the map prompt itself only says recommend.

## Recommended target and mechanics ledger

This table is the implementation-facing port decision. “Retain” names behavior that should remain normative in the target. “Reject” names behavior that should not be copied into Research OS even if it is valid for software engineering.

| Upstream | Recommended Research OS target skill name(s) | Retain mechanics | Reject mechanics |
|---|---|---|---|
| `ask-matt` | `research-help` | one remembered user router; state-based route; never secretly run another user workflow; context/handoff boundary | hard-coded engineering main flow, fixed token count, routes to code-only tools |
| `code-review` | `research-review`, `citation-audit` | immutable target; isolated axes; exact evidence; no averaging/masking; explicit unavailable axis | Fowler smell catalog, code/spec-only axes, chat-only report |
| `codebase-design` | `design-research-three-ways`, `research-domain-modeling`, `methodology-designer` | shared constraints; independent alternatives; controlled vocabulary; opinionated comparison; delete dominated indirection | deep-module nouns as research ontology, adapter-count rule outside software, line-oriented interface design |
| `diagnosing-bugs` | `research-diagnosis` | exact-symptom loop before hypotheses; minimization; 3–5 falsifiable hypotheses; one-variable probes; regression/full-scenario verification; cleanup | mandatory code fix when diagnosis-only was requested, unapproved instrumentation, architecture refactor before cause |
| `domain-modeling` | `research-domain-modeling`, `research-grilling` | immediate collision challenge; canonical terms; edge-case scenarios; artifact cross-check; stringent decision-record admission | implementation details in context, one glossary for genuinely distinct contexts, routine choices as RDRs |
| `grill-with-docs` | `research-1-grill` | thin explicit wrapper; one decision per exchange; facts by agent; domain/decision writeback inline | stateless chat for repository research, automatic downstream execution |
| `implement` | `research-5-run`; `research-auto` before decomposition; `research-review` for load-bearing outputs | one scoped contract; atomic ownership; focused package checks; final integration gate; independent review; durable sealed receipt | implicit commit, ticket scope expansion, external writes without separate authority |
| `improve-codebase-architecture` | no core skill; optional future `improve-research-operations` | proactive hotspot survey; multiple candidates before design; selection boundary; durable reasons against repeat suggestions | HTML/Tailwind/Mermaid mandate, deep-module semantics, automatic refactor |
| `prototype` | `pilot-study`; optionally `design-research-three-ways` | one decision-changing uncertainty; smallest faithful end-to-end path; one command; visible state/result; capture answer and source artifact | shipping prototype scaffolding, toy data that cannot expose the seam, unapproved real mutations |
| `research` | `evidence-research`; `literature-landscape` for synthesis | background/parallel primary-source reading; claim ownership; cited durable output; source convention | secondary source as proof, uncited chat-only findings, one memo as claim authority |
| `resolving-merge-conflicts` | `artifact-reconciliation` | trace both intents/provenances; classify fact/choice/schema/execution conflicts; preserve compatible content; disclose incompatible choice; supersede; rerun invalidated gates; finish with one current authority | “never abort” for external/unsafe research mutations, Git staging/commit as universal completion |
| `setup-matt-pocock-skills` | `research-setup` → `research-workspace-contract` | inspect; preview; explicit boundary; additive writes; adapters; conflict preservation; exact receipt/readback | issue-tracker/label assumptions, creating alternate instruction files, destructive migration |
| `tdd` | conditional branch in `research-5-run`; `pilot-study`, `falsification-first` | independent oracle; predeclared observation seam; one vertical slice; red before repair for code; public behavior; final integration check | universal TDD for exploratory research, internal mocks, horizontal bulk tests, automatic refactor |
| `to-spec` | `research-2-brief` → `synthesize-research-brief`; `to-plan` for a plan | synthesize current state; source table; no reopened choices; readiness; explicit scope and verification decisions | exhaustive user-story format, issue publication, fileless prose without claim pointers |
| `to-tickets` | `research-4-tasks` | tracer slices; real blockers; graph approval; expand–migrate–contract; one artifact per package; computable frontier | horizontal discipline silos, stale file paths/code snippets, automatic parent mutation |
| `triage` | `research-triage` | evidence before verdict; exactly one current outcome; human final authority; resume/dedup memory; reason-specific negative outcomes | external tracker mutations, AI comment boilerplate, software bug/enhancement categories |
| `wayfinder` | `research-map` | destination; fog versus precise node; map as index; explicit blockers; claim-before-work; chart/work split; one HITL decision; recomputation | issue-tracker-native dependency requirement, bare IDs in human prose, direct build from map |

## Prioritized prompt gaps

Priority reflects loss of correctness, authority, or multi-session continuity—not how much upstream prose is absent. A gap can cite several upstream skills because the engineering repository often distributes one lifecycle contract across router, setup, decomposition, implementation, review, and handoff.

### Current-state reconciliation

This snapshot has **0 open P0, 0 open P1, and 5 open P2 findings**.

| Disposition | Exact findings | Current meaning |
|---|---|---|
| **Closed** | `ENG-P0-01`, `ENG-P0-02`, `ENG-P0-03`, `ENG-P1-01` through `ENG-P1-09` | Current prompts/helpers contain the required authority path, the central remediation ledger agrees, and the evidence boundary is stated below. |
| **Open — deliberate v1 fidelity limitation** | `ENG-P2-01`, `ENG-P2-02`, `ENG-P2-03`, `ENG-P2-04`, `ENG-P2-05` | The audit accepts these as non-core v1 deferrals; `ENG-P2-04` is also explicitly outside v1 in the central remediation ledger. |

### Closed during this audit

#### ENG-P0-01 — Closed: the workpackage graph now has a first-class executor

- **Upstream behavior recovered:** `ask-matt` routes spec → tickets → one fresh `implement` per ticket; `to-tickets` makes the frontier computable; `implement` consumes one contract, runs focused and final checks, reviews, and seals durable work.
- **Current Research OS path:** `research-help` routes “one eligible workpackage” to user-only `research-5-run`; `research-4-tasks` owns the approved `proposed → ready` transition and stops after writing immutable package versions. The executor verifies exact-version blocker receipts, pins and claims one package, executes only allowed procedure/writes, captures provenance and cost, runs local plus project gates, invokes load-bearing review, updates and reads back every dependent state, then seals a JSON receipt and computes the frontier without mutating the package.
- **Concurrency mechanism:** the shared `research-workspace-contract/scripts/atomic_claim.py` uses version/hash/attempt claim IDs, atomic claim creation plus one shared terminal compare-and-set, competing-owner rejection, claim-time and seal-time source-hash checks, terminal-version conflict, receipt schema/identity/result checks, idempotent exact-attempt terminal readback, and owner-release archival. Centralizing it under the workspace-contract primitive avoids two claim authorities.
- **Current proof:** the claim tests prove one successful owner, one competing `already-claimed`, successful validated seal, exact-version `already-sealed`, changed-version conflict, changed-source seal refusal, owner-release archival, and one terminal winner under concurrent seal/release. Prompt gates separately preserve `complete|partial|blocked` execution status, `continue|repair|kill|blocked` domain verdict, authority stops, and pre-seal readback.
- **Verdict:** the former P0 absence is closed. The executor is an **Adapt** of `implement`, not a direct copy: it replaces automatic commit with bounded research mutations, dual verdicts, provenance, and explicit external authority.

#### ENG-P0-02 — Closed: baseline workspace preflight now proves its compatibility boundary

- **Upstream behavior recovered:** setup inspects before mutation, preserves user content, refuses conflicts, and does not invent a second configuration authority.
- **Current deterministic path:** `init_research_workspace.py` validates canonical config keys and baseline values, the unique Artifact-index marker/header, claims schema and complete status vocabulary, claims registry marker, and required markers in every template before mutation. Baseline path type collisions remain explicit. A nonbaseline adapter fails closed as `nonbaseline-adapter-requires-direct-verification` rather than being treated as unchanged or migrated.
- **Current proof:** the initializer tests cover additive dry-run/apply/check idempotence and context byte preservation; pass → missing-config-key fail → repair; missing-claim-status fail → repair; mutable context with preserved markers pass; missing-template-marker fail; and nonbaseline-adapter refusal with an unchanged filesystem.
- **Verdict:** the former P0 mismatch—malformed content labeled unchanged followed by additive writes—is closed for the initializer’s declared baseline boundary. Exact draft-by-draft user approval, deterministic validation of an accepted nonbaseline adapter, and strict-YAML duplicate-key parsing remain non-P0 limitations; the adapter path fails closed and cannot be mistaken for completed setup.

#### ENG-P0-03 — Closed: wayfinder now separates charting from claimed node work

- **Upstream behavior recovered:** chart and work are explicit invocation modes; charting names the destination, creates child decisions before wiring blockers, optionally dispatches isolated factual work, and stops. Work mode claims one frontier decision before investigation or a human question.
- **Current Research OS path:** `research-map` requires mode selection before work and forbids chart plus resolution in one invocation. Chart mode implements create-then-wire and terminates as `chart-complete`. Work mode pins the decision-record SHA-256, claims `<map-id>-<decision-id>-<sha256-prefix>-a<attempt>` through the shared atomic helper, gates continuation on a read-back `claimed`, handles `already-claimed` and exact-attempt terminal readback, refuses elapsed-time-only claim theft, resolves at most one HITL node, reads back the complete recomputed state, and only then seals.
- **Concurrency evidence:** `atomic_claim.py` checks the pinned source hash, atomically creates one claim directory and exclusive claim record, discloses the current owner to competitors, permits only the owner to seal/release, rechecks immutable source and receipt identity/result/schema, detects terminal-version conflict, chooses one terminal outcome by no-replace CAS, and re-enters finalize to produce the matching receipt/history. Tests prove one-owner claim contention, idempotent exact-version sealed rerun, changed-version conflict, changed-source seal refusal, owner release archival, and exactly one public outcome under concurrent seal/release.
- **Verdict:** the P0 risks of double-working one frontier node and silently falling through from charting into resolution are closed at the prompt and shared-helper layers.

#### ENG-P1-09 — Closed: claim terminal finalization is now linearizable and re-entrant

- **Former gap:** seal and release independently inspected one active claim and could race or crash between terminal receipt creation and active-claim archival, leaving contradictory or one-sided evidence.
- **Current mechanism:** both commands publish `.terminals/<claim-id>.json` with a complete fsynced temporary JSON file and an atomic no-replace hard link. That record is the single terminal compare-and-set. A different losing intent returns `terminal-state-conflict`; the winning intent can be retried to idempotently publish its matching sealed/release receipt and archive the active claim. Claim IDs include version/hash and an attempt identity, so a new authorized attempt cannot masquerade as the former terminal.
- **Current proof:** `test_atomic_claim_seal_and_release_share_one_terminal_cas` launches seal and release concurrently for the same owner and claim, requires return codes `[0, 4]`, verifies exactly one terminal state, requires only that state’s public receipt, and proves the active claim is gone. Code readback proves both terminal-present branches resume finalization after an interrupted winner.
- **Verdict:** every ENG-P1-09 subfinding is closed: readiness, source immutability, version/attempt identity, receipt validation, source recheck, version conflict, owner release, pre-seal state convergence, one terminal CAS, and re-entrant finalize.

#### ENG-P1-06 — Closed: the Research Brief has one writer

- **Current mechanism:** `synthesize-research-brief` owns canonical brief creation/update and stops before downstream rendering. `render-research-deliverable` treats the brief profile as validation-only, returns `blocked: canonical_writer_mismatch` for a Brief destination, and writes only plans, proposals, or papers.
- **Evidence boundary:** prompt and catalog composition readback prove one writer; the no-results forward evaluation proves the renderer preserves source truth, though no dedicated Brief-destination negative test exists. That coverage improvement does not reopen writer authority.

#### ENG-P1-07 — Closed: plan-wrapper prerequisite authority is explicit

- **Current mechanism:** `to-plan` requires a current sufficiently ready canonical brief. Missing workspace or brief stops with the exact prerequisite and only recommends `research-auto` or `research-2-brief`; the wrapper explicitly forbids silent initialization or synthesis. Renderer independently blocks on `research_brief_missing`.
- **Current proof:** `test_brief_writer_and_plan_authority_are_unambiguous` checks the wrapper's no-initialize/no-synthesis boundary and the renderer's independent missing-brief stop.

#### ENG-P1-01 — Closed: diagnosis now proves a red-capable feedback loop before reasoning

- **Current mechanism:** `research-diagnosis` writes a Phase-1 receipt with independently checked exact-symptom, reproducibility, runtime, and agent/HITL gates. It predeclares stochastic repetitions, exposes ranked hypotheses before testing, gives temporary instrumentation one unique diagnosis tag, captures the correct seam red before repair and green after, and saves zero-match cleanup evidence.
- **Current proof:** the reusable feedback-loop receipt specifies the stochastic and HITL capture fields; `test_prompt_ports_keep_load_bearing_matt_mechanics` checks the load-bearing prompt markers. Missing truthful regression seams fail closed and route to a bounded seam-creation workpackage.

#### ENG-P1-02 — Closed: revision review has one deterministic comparison packet

- **Current mechanism:** `research-review` selects full-target or comparison mode. The shared `build_comparison_packet.py` pins base and target SHA-256 values and deterministically inventories changed Markdown sections, claim IDs, tables, and unified diff. Every review axis, `citation-audit`, and revision renderer consumes the same packet identity; identical inputs return a read-back `no-op`.
- **Current proof:** `test_comparison_packet_is_deterministic_markdown_aware_and_no_op` proves deterministic repeated output, Markdown-aware inventories, persisted-output equality, and empty-delta behavior. Prompt regression checks require the explicit modes and shared packet acknowledgement.

#### ENG-P1-03 — Closed: canonical conflicts have an owned recovery transition

- **Current mechanism:** the new `artifact-reconciliation` primitive pins both artifact identities, hashes, lineages, claims, decisions, and consumers; classifies fact, human-choice, schema, execution, and concurrent-edit conflicts; preserves compatible content and both provenances; creates one superseding artifact; invalidates and reruns downstream gates; and reads back exactly one current pointer.
- **Composition:** handoff, brief synthesis, domain modeling, and grilling stop and route both pinned sides to the primitive instead of choosing a convenient winner. The catalog graph makes those edges mechanically checkable.
- **Current proof:** repository validation covers the skill and exact composition graph; `test_prompt_ports_keep_load_bearing_matt_mechanics` checks all conflict classes and the one-current-pointer completion gate.

#### ENG-P1-04 — Closed: every RDR path now applies the four-part admission gate

- **Current mechanism:** `research-grilling` and `research-domain-modeling` apply costly reversal, surprising/unsafe without rationale, genuine trade-off, and downstream ambiguity. `research-help` keeps routine routing in `CONTEXT`; `research-workspace-contract` now applies the same four tests when seeding state and keeps routine routing, formatting, and progress in the owning artifact or run record.
- **Current proof:** prompt regression checks the four workspace-contract predicates. Final readback finds no remaining setup path that admits an RDR merely because a choice is generically “consequential.”

#### ENG-P1-05 — Closed: triage has concept-level queues and resumable memory

- **Current mechanism:** `research-triage` supports one-item, discover, and resume modes; derives concept signatures and aliases before allocating IDs; stores `checked_at` plus the load-bearing evidence frontier; recomputes only changed cases; and returns queue buckets without silently triaging them. Reason codes distinguish already established, out of scope, invalid, superseded, changed evidence, and insufficient evidence from the strategic verdict.
- **Current proof:** prompt regression checks discovery/resume, signature, frontier, and reason markers. An unchanged same-concept frontier is a verified `no-op` without a manufactured timestamp update.

#### ENG-P1-08 — Closed: pilots distinguish empirical and interaction uncertainty

- **Current mechanism:** `pilot-study` selects an empirical tracer or interaction prototype. The interaction branch pins actor, starting state, actions, transitions, visible/failure states, variants, observations, and predeclared verdict thresholds. Prototype scaffolding is quarantined under the pilot ID; moving the validated minimal core requires a separate bounded workpackage and authority.
- **Current proof:** prompt regression checks both branch names and the quarantine rule. Human-subject contact, deployment, deletion, and promotion remain separate authority gates.

### P0 — no open findings

All three findings that entered this audit as P0 are now in the closed ledger above. The remaining gaps affect fidelity or deterministic hardening, not the existence of a safe first-class research path.

### P1 — no open findings

All nine P1 findings are in the closed ledger above. Remaining P2 items are deliberate v1 fidelity or maintainability deferrals, not unresolved P1 authority paths.

### P2 — useful fidelity and maintainability improvements

#### ENG-P2-01 — OPEN: background evidence delegation remains a v1 harness-dependent limitation

- **Upstream behavior:** reading legwork is a background agent so the caller continues.
- **Affected targets:** `evidence-research`, `research-map`, `research-auto`.
- **Current state:** `research-map` may dispatch isolated factual nodes and `design-research-three-ways` uses isolated agents when available, but standalone `evidence-research` and `research-auto` do not require background execution. Correctness is preserved through scoped durable claim chains; foreground latency is not.
- **v1 deliberate limitation:** scheduling/background semantics remain harness-dependent. A future version should spawn independent evidence tasks with stable claim scopes and non-overlapping write targets when work exceeds a quick lookup, while retaining synchronous mode for tiny or dependency-critical checks.

#### ENG-P2-02 — OPEN: alternative-design presentation retains a v1 absorption limitation

- **Upstream behavior:** show the shared problem frame, immediately run three-plus isolated agents, present alternatives sequentially, then recommend or hybridize.
- **Affected target:** `design-research-three-ways`.
- **Current state:** the target now fixes and exposes one shared brief before generation, uses isolated agents when available or separate passes otherwise, prevents cross-candidate leakage, and delays hybrids until after a common matrix. It still does not require one-at-a-time presentation for user absorption or an explicit model recommendation before the human selection.
- **v1 deliberate limitation:** retain human-owned selection and the current matrix presentation for v1; future fidelity work may add sequential presentation plus a disclosed recommendation without silently selecting.

#### ENG-P2-03 — OPEN: wrapper equivalence lacks a complete v1 behavioral regression matrix

- **Upstream behavior:** very thin wrappers keep the primitive as the single rule authority.
- **Affected targets:** `research-1-grill`/`research-grilling`, `research-help`/`research-auto`, `research-2-brief`/`synthesize-research-brief`, `to-plan`/`render-research-deliverable`.
- **Current state:** `research-2-brief` and `to-plan` are thin argument/stop wrappers; the catalog composition graph is mechanically checked against every `$skill` reference; four fresh-agent receipts cover adaptive, existing-design, blocked-claims, and no-results behavior. `research-1-grill` still carries substantial domain orchestration, and no saved matrix runs the same success/near-miss/blocked case through each direct primitive and wrapper pair.
- **v1 deliberate limitation:** structural dependency drift is closed, but exhaustive wrapper behavioral equivalence is deferred. Add paired fresh-agent cases before claiming identical status/writeback semantics across every wrapper boundary.

#### ENG-P2-04 — OPEN: proactive research-operations automation is deliberately outside v1

- **Upstream behavior:** architecture review looks at recent hot spots, surfaces multiple deepening candidates, and stops for selection before design.
- **Affected target:** none; possible future `improve-research-operations`.
- **Current state:** the remediation ledger explicitly places recurring research-operation automation outside the v1 core.
- **v1 deliberate limitation:** only if operational pain justifies a later skill, survey artifact churn, duplicate authority, recurring manual joins, stale evidence, weak package seams, and repeated review failures; rank candidates and stop before repair. Do not port the HTML or deep-module ontology by default.

#### ENG-P2-05 — OPEN: package graph confirmation keeps a v1 prompt-fidelity shortcut

- **Upstream behavior:** asks separately about granularity, blocker truth, and merge/split options.
- **Affected target:** `research-4-tasks`.
- **Current state:** Stage 4 presents the frontier, granularity, critical path, parallelism, and highest-risk dependency; rejects cycles, orphans, duplicates, and activity-only packages; and obtains graph approval. It still does not separately ask the three upstream granularity, blocker-truth, and merge/split questions.
- **v1 deliberate limitation:** the stronger structural gates are accepted for v1, while the explicit three-question quiz remains a fidelity improvement.

## Overall verdict

The engineering port is conceptually strong: 6 skills are direct behavioral ports, 7 are research-domain adaptations, and 4 are intentionally excluded as software-specific. Research OS consistently improves source-of-truth discipline, claim entailment, external-write authority, canonical path resolution, negative outcomes, lineage, and readback.

All three P0 findings and all nine P1 findings are closed in the current repository and reconciled with [`docs/PORT_REMEDIATION.md`](../PORT_REMEDIATION.md). Research OS now proves its baseline workspace contract before mutation; routes an immutable ready package to a version/attempt-safe executor; separates wayfinder charting from claimed work; proves diagnosis-loop quality; shares one deterministic revision packet; reconciles conflicting artifacts to one current authority; applies one four-part RDR gate; preserves resumable concept-level triage memory; distinguishes empirical from interaction pilots; preserves one Research Brief writer; stops plan generation at missing prerequisites; and finalizes seal versus release through one re-entrant terminal compare-and-set.

The **exact open set is `ENG-P2-01`, `ENG-P2-02`, `ENG-P2-03`, `ENG-P2-04`, and `ENG-P2-05` only**. They are deliberate v1 fidelity or maintainability deferrals: harness-dependent background delegation, sequential alternative presentation plus disclosed recommendation, exhaustive wrapper-equivalence regression cases, proactive recurring research-operations automation, and the explicit three-question package-graph quiz.
