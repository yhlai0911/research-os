# Research skill design vocabulary

Load this reference when a skill’s behavior, invocation, or maintainability is unclear.

## Root virtue

**Predictability** means stable process, not identical output. A divergent ideation skill can be predictable when it reliably explores independent alternatives, records the decision, and stops at the same evidence gate.

## Invocation

**Model-invoked** skills are reusable disciplines the agent may select autonomously. Their descriptions carry distinct trigger branches and spend context.

**User-invoked** skills are explicit orchestration or mutation surfaces. They spend human memory instead of agent context. A router reduces that cognitive cost.

**Leading concept** is a compact pretrained idea that anchors invocation and execution, such as counterfactual, mechanism, entailment, tracer study, or fog. Repeating the concept is useful; repeating its full definition is drift.

## Information hierarchy

1. Put ordered actions and their gates in `SKILL.md`.
2. Keep small rules needed by every branch beside those actions.
3. Move branch-specific detail to a directly linked reference.
4. Put deterministic, repeated mechanics in a tested script.
5. Put copyable output formats in assets.

A context pointer must state when to load its target. A bare filename is a weak pointer.

## Completion

A completion criterion needs:

- **clarity:** the agent can observe pass or fail;
- **demand:** it accounts for every required artifact or rule;
- **truth:** the verdict follows current readback, not intent;
- **status:** unsupported work is partial or blocked.

## Authority

Keep facts discoverable by the agent and consequential choices with the researcher. Keep each durable meaning in one source of truth:

- vocabulary and current design in `.research/CONTEXT.md`;
- current artifact pointers and task outcomes in the one `## Artifact index` table in the resolved context;
- hard decisions in Research Decision Records;
- external claims in the evidence ledger;
- work contracts in briefs and workpackages;
- continuity in handoff manifests.

Workspace paths are adapters, not constants. Read `.research/config.yaml` before every other `.research/` path, resolve its canonical entries, and use literal baseline paths only as documented defaults.

## Common defects

- **Premature completion:** a vague gate lets attention move to later steps.
- **Duplication:** two places claim authority for one rule.
- **Sediment:** stale exceptions accumulate because deletion feels risky.
- **Sprawl:** live but branch-specific material crowds the primary path.
- **No-op:** an instruction does not change behavior from the model default.
- **Negation:** the prohibited behavior becomes the prompt’s strongest concept.
- **Trigger collision:** several skills compete for the same words and task.
- **Receipt gap:** a write is claimed without readback, identity, hash, or status.
