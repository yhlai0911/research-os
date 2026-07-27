---
name: research-status
description: Show where the project stands on the mainline, what exists so far, and what the next action is.
---

# Research Status

> **Not a mainline step.** This reports position; it never advances the project.

Lead with **position**. Answer three questions and nothing else: where am I, what do I have, what is missing.

This skill is **read-only**. It never creates, updates, supersedes, or repairs an artifact, and it never asks the user a decision question. When it finds a defect, it names the defect and the skill that repairs it.

Resolve `.research/config.yaml` per [writeback-protocol.md](../../primitives/research-workspace-contract/references/writeback-protocol.md); apply only its resolution rules. Stop with `blocked: research_workspace_not_initialized` when the config is absent, and recommend `research-setup`.

## Read the current state

Read, at their resolved paths and in this order:

1. the context's single `## Artifact index` table — identity, status, and lineage of every current artifact;
2. the claim registry — counts per declared status;
3. the workpackage index and any claim or receipt state, when the workpackages directory is populated.

Read only these. Do not open every artifact to summarize its contents; the index is the authority on what is current.

## Locate the mainline position

Infer the furthest step whose output exists and reads back as `complete`:

| Step | Present when the index holds |
|---|---|
| 1 `research-1-grill` | a resolved-idea decision record |
| 2 `research-2-brief` | a current Research Brief |
| 3 `research-3-falsify` | a falsification plan covering the brief's central claims |
| 4 `research-4-tasks` | current workpackages |
| 5 `research-5-run` | at least one sealed workpackage receipt |
| 6 `research-6-review` | a current review report |

A step whose artifact is `partial` or `blocked` is the current position, not a completed one. When artifacts exist out of order, report the gap rather than the highest number.

## Report

Give the user, in this order and in their language:

1. **Position** — the current mainline step and whether it is complete, partial, or blocked.
2. **What exists** — one line per current artifact: kind, ID, status, updated. Name superseded artifacts only when a stale consumer still points at one.
3. **What is missing** — unresolved claims by status, blocked gates, workpackages that are ready but unclaimed, and any artifact whose status disagrees with an artifact that depends on it.
4. **Next action** — exactly one recommended skill invocation, with the reason it is the binding constraint.

Report `blocked` and say registration was not read when the config or the context cannot be read. Never infer progress from conversation history, file names, or effort; only the index and the registries count.
