---
name: writing-research-skills
description: Design, review, and maintain predictable Research OS skills.
---

# Writing Research Skills

Optimize for **predictability**: the skill should drive the same process across runs while allowing the research output to vary with evidence.

Read [design-vocabulary.md](references/design-vocabulary.md) when diagnosing structure, invocation, disclosure, or drift.

## Process

### 1. Ground the behavior

Collect at least three concrete user prompts that should trigger the skill and two near-misses that should not. For each true case, state the artifact, decision, or observable state the skill must produce.

**Complete when:** trigger boundaries and expected outcomes are concrete enough to forward-test without hidden context.

### 2. Choose the invocation boundary

Use model invocation only when the agent should autonomously reach the skill or another skill needs its discipline. Use user invocation for explicit orchestration, state changes, or long flows. Keep user-only skills behind `policy.allow_implicit_invocation: false`.

Give each model-invoked skill one distinct leading concept that also appears in its trigger description. Prefer one strong primitive over several synonymous skills.

**Complete when:** the invocation choice, leading concept, and unique responsibility differ from every catalogued skill.

### 3. Design the contract

Define:

- inputs and factual discovery policy;
- decisions reserved for the researcher;
- canonical reads and writes; for workspace skills, read only `.research/config.yaml` first, resolve its adapters, and never probe a baseline path before resolution;
- one current-artifact registry in the resolved context, with durable pointers and `complete`, `partial`, or `blocked` outcomes;
- ordered steps or flat reference rules;
- a checkable, exhaustive completion criterion for every step;
- blocked, partial, and stop branches;
- external side effects and their authorization gate.

State positive target behavior. Use prohibitions only for hard safety boundaries and pair them with the intended action.

**Complete when:** an agent can distinguish complete, partial, and blocked from artifacts and receipts rather than prose confidence.

### 4. Allocate context

Keep essential actions in `SKILL.md`. Move branch-specific detail to one-level `references/`, deterministic operations to `scripts/`, and copyable output material to `assets/`. Keep each meaning in one authoritative place.

Split only when a new skill deserves autonomous invocation or when a real context boundary must hide later steps to prevent premature completion.

**Complete when:** every line changes behavior, every pointer says when to load its target, and no reference is duplicated.

### 5. Initialize and implement

Add the skill to `skills/catalog.yaml`, then use Codex’s official `skill-creator` initializer. Replace all generated placeholders. Keep frontmatter to `name` and `description`; regenerate `agents/openai.yaml` from the catalog.

**Complete when:** no initializer marker, placeholder, stale name, or unowned shared rule remains.

### 6. Prove predictability

Run:

```bash
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

Forward-test realistic prompts in fresh agents. Pass the skill and raw task, not the intended answer. Include one success case, one near-miss trigger, and one blocked case. Repair the smallest source-of-truth rule that explains a failure, then rerun.

**Complete when:** structural checks pass and forward tests follow the intended process without leaked conclusions.

## Failure modes

- **Premature completion:** sharpen the current completion criterion before splitting the sequence.
- **Duplication:** choose one authority and replace copies with pointers.
- **Sediment:** remove stale instructions instead of adding exceptions.
- **Sprawl:** disclose branch-specific reference or split at a real boundary.
- **No-op:** delete instructions that do not change default model behavior.
- **Trigger collision:** merge synonyms or give each skill a genuinely distinct leading concept.
- **Truth drift:** generate inventories and metadata from the catalog; do not maintain parallel hand-written lists.
