---
name: develop-research
description: Develop a topic, direction, problem, source, or partial idea through adaptive interviewing, evidence research, reviewer attack, and repair until it becomes a verified Research Brief and the requested research plan, proposal, project brief, paper blueprint, or manuscript draft.
---

# Develop Research

Run an **adaptive loop**, not a fixed academic checklist. Start from whatever the user actually has, reduce the most load-bearing uncertainty, preserve their constraints, and continue until the requested research artifact is defensible.

Read [adaptive-routing.md](references/adaptive-routing.md) when selecting the next research primitive, handling a route change, or deciding whether alternative designs are needed.

## Establish the mission

Extract the seed, desired destination, audience, intended use or decision, constraints, exclusions, available evidence, current stage, language, required template or format, and preferred export path. A seed may be a phenomenon, equation, theory, dataset, policy, draft, reviewer comment, or vague interest. Do not re-ask fields already supplied.

If the destination is explicit, record it. Otherwise ask exactly one decision question: what must this become—topic verdict, Research Brief, academic research plan, grant or project proposal, paper blueprint, or manuscript draft? Recommend the most appropriate destination and its trade-off.

Invoke `$research-workspace-contract` to establish or resolve durable state under the explicitly authorized project. Record the mission and destination without turning the user's hopes into factual claims.

**Complete when:** the destination, audience and use, acceptance standard, hard constraints, available source material, output requirements, and current artifact state are explicit.

## Work one frontier at a time

At the start of every cycle:

1. read config, resolved context, current Artifact index, decisions, claims, and only artifacts linked to the active branch;
2. identify the single uncertainty or decision that blocks the most downstream work;
3. choose the narrowest research primitive that can resolve it;
4. execute discoverable factual work without asking the user;
5. ask at most one prerequisite human decision, with a recommendation and material trade-off;
6. write and read back the result before recomputing the frontier.

Preserve user exclusions. Do not resurrect a rejected domain, method, dataset, population, or output unless new evidence makes the trade-off materially different and the user accepts reopening it.

If the user answers several live branches at once, persist all resolved decisions and do not ask them again. Batch questions only when the branches are demonstrably independent; never batch a later choice whose options depend on an earlier answer.

Use `$research-grilling` for decisions and `$research-domain-modeling` for canonical terms. Use evidence, literature, gap, contribution, theory, construct, equation, identification, data, methodology, falsification, pilot, review, diagnosis, citation, journal, writing, and ethics primitives only when their trigger is present.

**Complete when:** each live branch is resolved, assigned to a named evidence task, or explicitly blocked; no consequential assumption remains hidden.

## Convert possibility into a research design

Clarify what the study will explain, estimate, predict, design, or decide. Require a bounded unit, population, setting, period, construct, estimand or prediction target, mechanism or inferential logic, observable evidence, and failure condition.

Do not force three designs. Invoke `$design-research-three-ways` only when the first design is anchoring the project, alternatives have materially different assumptions, or theory-first, identification-first, and data-first routes could change the answer. Otherwise repair the current design directly.

Actively verify literature, data, and method premises. Treat “nothing found” as search coverage, never proof of novelty. Keep causal, predictive, descriptive, and structural claims distinct.

**Complete when:** one current design is economically or substantively meaningful, empirically or logically distinguishable from serious rivals, feasible enough for its next step, and capable of being rejected.

## Attack and repair

Invoke `$falsification-first` before expensive work. Use `$pilot-study` when a small end-to-end tracer can expose feasibility or identification failure.

Invoke `$research-review` on the current design or brief. Keep contribution, theory, identification, measurement/data, evidence, and execution axes independent. Let the worst load-bearing axis control the verdict.

For each major or fatal finding:

1. diagnose the root cause;
2. identify the smallest repair that changes the failed inference;
3. ask the user only when repair changes the question, scope, contribution, commitment, or risk;
4. supersede affected artifacts and rerun the failed gate.

Kill or reframe a design that remains non-distinct, infeasible, unsupported, unethical, or unfalsifiable. Do not accumulate rhetorical patches around a failed core.

**Complete when:** every blocking reviewer finding is repaired, accepted as a scope limit, or recorded as a blocker; no rejection reason is hidden by writing quality.

## Seal the Research Brief

Invoke `$synthesize-research-brief`. The Research Brief is the one audience-neutral contract for the research question, evidence, contribution, theory, constructs, identification, data, methods, falsifiers, ethics, scope, decisions, and readiness.

When the brief is `conditional` or `blocked`, do not upgrade it in a downstream artifact. Ask whether the user wants the strongest honest partial output or wants to resolve the named gate first.

**Complete when:** the brief and its Artifact-index row read back, and the user has accepted its question, contribution, inferential strength, scope, and failure criteria.

## Produce the requested artifact

If the destination is the Research Brief or a topic verdict, stop with that accepted artifact and next action. Otherwise invoke `$render-research-deliverable` with the recorded destination, audience, intended use, language, format, export preference, and institutional constraints.

Use a paper blueprint when results do not exist. Use a manuscript draft only when executed results, uncertainty, provenance, and citations are registered. Use a grant or project proposal only within verified call or stakeholder constraints; leave budget and commitments unresolved unless authorized.

Re-read the final artifact, Research Brief, claims, decisions, reviews, and Artifact-index row. Report `complete`, `partial`, or `blocked` from current evidence, not effort.

## Finish only when

- the requested artifact exists at its canonical path and passes its output profile;
- every material factual claim has an inspectable claim-chain pointer;
- the design's contribution, inference, data, method, and failure conditions agree across artifacts;
- reviewer findings and dispositions remain visible;
- planned work is never presented as observed results;
- all writes and pointers read back; and
- the user receives the artifact, status, limitations, and next authorized action.

Never submit, publish, email, upload, purchase, promise third-party participation, or make an institutional commitment without separate explicit authorization.
