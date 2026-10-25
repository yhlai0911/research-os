# Finance and Social Science profile (optional)

[繁體中文](README.zh-TW.md) · [Generic core](../../README.en.md)

This separately versioned **0.1.0** extension requires Research OS core **2.0.0** from this checkout. It adds one command, `research-finance-social-science`, for an empirical-design validity audit. Core remains 43 generic skills; this profile is not installed by default and does not fork or replace them.

## Install and verify

From the repository root, after `uv sync --locked` and a successful core installation:

```bash
uv run python scripts/install_skills.py --profile finance-social-science --dry-run
uv run python scripts/install_skills.py --profile finance-social-science
uv run python scripts/verify_install.py --profile finance-social-science
```

Use `--harness claude-code` on all three commands for Claude Code. If core uses a custom directory, use the same `--target /absolute/path/to/skills` on all commands. The installer requires a verified core in the same target and harness. The profile writes `.research-os-finance-social-science-install.json`, leaving `.research-os-install.json` untouched. Conflicting existing files stop installation without overwriting them.

## Use

Initialize the project using `research-setup`, then invoke `$research-finance-social-science` in Codex or `/research-finance-social-science` in Claude Code:

> Review my panel-data design in English. I want to study a policy's effect on firm investment. Distinguish the identifying assumptions from the estimator, and list which evidence is still missing. Do not invent results.

The audit adapts to finance, quantitative social science, or qualitative/mixed methods. It checks applicable risks such as point-in-time data, leakage, survivorship, identification, measurement, consent, and reproducibility. It writes into the core's canonical review location and recommends the next core step. It does not run the six-step pipeline automatically, create another brief, or provide investment advice.

## Same repository, separate scope

The independent [catalog](catalog.yaml), [skill](skills/orchestrators/research-finance-social-science/SKILL.md), and conditional references are confined to this directory. Both editions are maintained in this repository: the generic core serves any research domain, while this explicitly selected extension adds finance/social-science checks. It depends on the compatible core rather than copying it. Use the parent repository's installer; this directory is not a standalone distribution or a separate repository.

This is a design aid, not validated evidence of research quality. Structural tests and install checks do not prove empirical conclusions, regulatory compliance, or publication readiness. The repository's [MIT license](../../LICENSE) applies; this profile does not create exclusive rights over the generic core.
