---
name: research-finance-social-science
description: Review an empirical finance or social-science research design using domain-specific validity checks, when the user chooses this optional profile.
---

# Finance and Social Science Research

Apply a **validity audit** to the user's question or existing design. This optional extension supplements the generic Research OS core; it does not replace the six-step workflow or create another canonical brief. It is for academic research, not personalized investment advice or trading decisions.

## Scope and language

- Follow the user's explicit language preference; otherwise match their current language (English or Traditional Chinese). Keep commands, paths, IDs, and schema/status values unchanged. Label translations of quotations.
- Clarify only genuinely ambiguous scope: finance, quantitative social science, qualitative/mixed methods, or a combination. Do not impose causal inference on descriptive, interpretive, or predictive questions.
- Preserve the user's selected population, methods, exclusions, and data-access limits. A domain label is not permission to collect personal data, contact participants, trade, pay, or submit anything.

## Resolve and inspect

Read `.research/config.yaml` before other workspace paths. If it is absent or invalid, stop as `blocked: research_workspace_not_initialized`, recommend `research-setup` for an absent workspace or repair for an invalid one, and do not create or overwrite it. Otherwise use the installed core's `research-workspace-contract/references/writeback-protocol.md` to resolve canonical paths and register artifacts. Locate that reference in the sibling installed skill directory; in a repository checkout it is under `skills/primitives/research-workspace-contract/references/`. If unavailable, stop as `blocked: core_dependency_missing`.

Read the current brief, relevant claims, and existing design evidence. Read [validity-checks.md](references/validity-checks.md) only for the applicable methods. Record an audit under the resolved reviews path; update an existing audit for the same topic rather than creating competing current records.

## Audit the load-bearing assumptions

1. State the research question, claim type, unit, population, time horizon, and estimand or interpretive aim. Separate confirmed inputs from assumptions and missing evidence.
2. Select the applicable domain checks. For each material risk, name the affected claim, evidence available, test or design repair, decision owner, and stop condition. Prioritize validity failures over more sophisticated estimators.
3. Distinguish predeclared analyses from post hoc exploration. Do not retrospectively call a choice preregistered. Name practical and statistical uncertainty; never fabricate data, citations, effect sizes, ethics approval, or completed checks.
4. Give one next core entry point suited to the bottleneck: `research-1-grill` for an unclear question, `research-2-brief` for agreed scope, `research-3-falsify` for failure criteria, or `research-6-review` for review. Recommend it, do not invoke another user-only skill automatically.

## Finish or stop

The audit contains: scope; source/artifact IDs; claim type; prioritized risk/evidence/repair table; unresolved decisions; an explicit `advance`, `repair`, or `blocked` verdict with rationale; and the next step. Domain verdicts remain in the audit, never in claim registry or index status fields.

Use `blocked` when a missing load-bearing input, permission, or path prevents the requested assessment; `repair` when available evidence identifies a design weakness with a concrete remedy; and `advance` only when no unresolved load-bearing issue prevents the explicitly bounded next step. Explain residual limitations even when advancing.

Complete only when the audit and its index entry read back consistently and all unchecked assumptions are labeled. `advance` means the specified audit gate passed, not that findings are true or publication-ready. If a required source, permission, or canonical path is missing, record the blocker when possible and stop. Do not claim research effectiveness from structural skill tests.
