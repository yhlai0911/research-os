# Changelog

All notable changes to Research OS are recorded here.

## 2.0.0

Breaking: every user-invoked orchestrator was renamed. See [`docs/MIGRATION-v2.md`](docs/MIGRATION-v2.md) for the full mapping and upgrade steps. Workspace format is unchanged and existing `.research/` projects need no migration.

- Renamed all 16 orchestrators to a numbered mainline (`research-1-grill` through `research-6-review`) plus plain-language off-mainline names, so the pipeline order is visible in the skill list itself.
- Added `research-3-falsify`, an explicit entry point for falsification. Previously reachable only from inside the end-to-end orchestrator, it now runs before task decomposition so no cost is committed to an unfalsifiable claim.
- Added `research-6-review` as the user-invoked wrapper over the `research-review` primitive. The numbered name is required because installed skill directories are flat and `research-review` is already taken.
- Added `research-status`, a read-only report of mainline position, current artifacts, unresolved claims, and the next action. The Artifact index was previously readable only by the agent.
- Made every mainline skill hand off explicitly: on reaching its completion gate it names the next step and stops, instead of converging silently.
- Collapsed the workspace resolution procedure, the Artifact index contract, and the three index statuses into one owned reference, `research-workspace-contract/references/writeback-protocol.md`.
- Changed `validate_repository.py` to require a link to that protocol rather than the literal index header. The old string check was what copied the same bookkeeping into 33 files and would have kept doing so for every new skill.
- Rebuilt the tutorial video for v2: all eight narration takes re-recorded, the script rewritten around the six-step mainline, captions rewritten, and the timeline recomputed from the new take lengths (2m50s to 4m01s).
- Removed every spoken skill name from the narration. The v1 script said the former name aloud in line 3, which made the video wrong the instant the skill was renamed; naming only the step keeps it stable across future renames.
- Added `scripts/regen_voice.py` and `scripts/retime.py` so narration and timing stay reproducible. The first refuses to regenerate a single take when the voice ID changed, which would leave one take in a different voice; the second derives every `data-start` and `data-duration` from `audio_meta.json` rather than hand-editing.

## Unreleased

- Clarified that Research OS is a 39-skill Codex suite rather than one root skill, and added a copyable Codex installation workflow.
- Made the installer default to `$CODEX_HOME/skills` or `~/.codex/skills` and added final installed-tree hash readback.
- Added `scripts/verify_install.py` to verify every catalogued skill, Codex metadata file, content hash, and installation receipt.
- Added regression coverage for the default Codex target and incomplete-install detection.
- Added a catalog-generated Claude Code adapter for personal and project skills, preserving user/model invocation boundaries without changing canonical `SKILL.md` frontmatter.
- Added official-source Claude Code installation, discovery, live-reload, and troubleshooting guidance.

## 1.1.0 — 2026-07-26

- Added a complete Traditional Chinese usage guide covering installation, one-frontier interaction, deliverable selection, artifact readback, statuses, and a worked mini example.
- Added a copyable prompt cookbook for vague topics, equation-led research, data-first work, plan repair, proposals, papers, and handoffs.
- Added a troubleshooting guide for over-questioning, blocked outputs, novelty overclaims, artifact conflicts, exclusions, invocation, and validation.
- Added a step-by-step Traditional Chinese walkthrough of the Financial Wave–Diffusion example.
- Added a reproducible 1920×1080 HyperFrames tutorial project with storyboard, locked script, ElevenLabs narration, captions, QA snapshots, cost ledger, render receipt, and a 2m50s MP4.

## 1.0.0 — 2026-07-26

- Added 39 catalogued skills: 13 explicit orchestrators, 25 model-invoked research primitives, and one skill-engineering meta skill.
- Added `develop-research`, the adaptive flagship that turns a topic, direction, equation, dataset, draft, or review concern into a verified Research Brief and destination-specific deliverable.
- Added output contracts for academic research plans, grant and project proposals, paper blueprints, and evidence-gated manuscript drafts.
- Added concurrency-safe workpackage execution with atomic claim, sealed receipt, falsification, integration, and no-op behavior.
- Added artifact reconciliation that pins both lineages, separates fact, choice, schema, execution, and concurrent-edit conflicts, supersedes rather than overwrites, and proves one current pointer.
- Added deterministic Markdown-aware comparison packets so revision review, citation audit, and rendering share one base/target delta and stop on no-op.
- Added four-gate diagnosis receipts, stochastic and HITL capture branches, pre-repair red/post-repair green checks, and tagged instrumentation cleanup.
- Added concept-level idea deduplication, evidence-frontier resume queues, and an interaction-prototype branch for research pilots.
- Added the config-resolved `.research/` workspace contract, claim ledger, decision records, current-artifact index, templates, and additive initializer.
- Added catalog synchronization, collision-safe transactional installation, repository validation, tests, deterministic ZIP packaging, and GitHub Actions validation.
- Added a file-level analysis of all 41 skills in the pinned Matt Pocock Skills source.
- Added the Financial Wave–Diffusion worked example with explicit evidence states, identification threats, falsifiers, and blocked empirical work.
