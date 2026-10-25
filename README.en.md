# Research OS

**A research assistant that guides the workflow, from no topic to a manuscript.** `research-assistant` is included in the **43-skill core on `main`**, following [PR #6](https://github.com/yhlai0911/research-os/pull/6). It identifies the current need, selects and delegates to the applicable skill, then checks the returned artifacts and next gate. Receiving skills perform the research; novices need not memorize their names. See the [assistant guide](docs/RESEARCH_ASSISTANT.en.md). Existing installations still need an intentional update and source-commit verification.

**English** · [繁體中文](README.md) · [English quickstart](docs/QUICKSTART.en.md) · [繁體中文使用教學](docs/USAGE_GUIDE.zh-TW.md)

**Earlier public video example:** [Granger voiced v4 (7:57.93, Traditional Chinese)](https://github.com/yhlai0911/research-os/releases/download/granger-tutorial-voiced-v4/research-os-granger-follow-along-voiced-v4.mp4) · [walkthrough](docs/TUTORIAL_GRANGER.en.md) · [40 scenes and rebuild sources](jobs/research-os-granger-tutorial/v4/README.md). It illustrates an earlier Treasury-data workflow; follow the current documentation for skills and installation. It does not establish native invocation of the new assistant. The bank-thesis demonstration is being revoiced with ElevenLabs; no public new-video release or download is linked here (status: 2026-10-25).

Research OS is a composable set of Agent Skills for turning a topic, equation, dataset, draft, or reviewer concern into a falsifiable research brief and an evidence-led plan, proposal, or paper. It separates researcher decisions from discoverable facts, records uncertainty and provenance, and makes the conditions for completing or stopping each stage explicit.

Its design draws on [Matt Pocock's skills](https://github.com/mattpocock/skills), including narrow primitives, explicit completion criteria, progressive disclosure, and feedback loops. Research OS adds claim–evidence tracking, counterfactuals, falsification, data feasibility, ethics, reproducibility, and durable handoffs. These are design intentions, not a claim that the system has demonstrated better research outcomes.

**Version and installation:** this guide covers the v2 six-step workflow, bilingual operation, and optional domain profile. Installation commands use `main`; check the installation receipt's source commit to identify the version you actually installed. Existing v1.1 users should read the [migration guide](docs/MIGRATION-v2.md) first.

**One repository, distinct core and optional extension:** the default suite remains **43 generic core skills**. The independent [finance-social-science profile](profiles/finance-social-science/README.md) ([繁體中文](profiles/finance-social-science/README.zh-TW.md)) lives in this same repository. It is not a separate repository and is not installed by default. Explicit opt-in keeps domain-specific assumptions out of the generic workflow.

## Start with six steps

Examples display `/skill-name`, the Claude Code command form. In Codex, explicitly invoke the same skill with `$skill-name`. Names and workflow order are the same.

```text
One-time setup
  /research-setup        Create the project's .research/ workspace

Mainline
  /research-1-grill      Turn a fuzzy idea into a researchable question
  /research-2-brief      Consolidate decisions and evidence into a research contract
  /research-3-falsify    Declare what would defeat the claim before execution
  /research-4-tasks      Split the work into independently verifiable tasks
  /research-5-run        Execute one eligible task and seal its receipt
  /research-6-review     Challenge the work through independent review axes

At any point
  $research-assistant   Identify the stage, delegate a skill, inspect outputs and guide the next step
  /research-status      Read current progress, artifacts, gaps, and next step

Deliverables
  /to-plan   /to-proposal   /to-paper
```

Each mainline skill has checkable completion conditions and ends its own invocation at the handoff. Direct calls remain user-paced. In an assistant-guided mission, the assistant reads back the artifact, domain verdict and checks before delegating the next applicable workflow within the existing grant. Missing evidence, a consequential decision or missing authority remains a gate. Falsification precedes execution so failure conditions are recorded before results.

The agent may use 26 model-invoked research primitives as needed. You do not need to memorize their names. The six steps are the user-facing path; they do not force every topic through every possible method.

For a less manual route, `/research-auto` works adaptively on the current bottleneck using model-invoked primitives. It still respects researcher decisions, workspace scope, evidence limits, and external-action permissions. `/research-help` recommends an entry point and stops.

Start with `$research-assistant` in Codex, or ask naturally: “I want to write a thesis, but I have no topic. Where should I start?” The assistant selects `research-1-grill`; that receiving skill asks the first necessary background or interest question. Guidance, recommendations, explicitly delegated technical choices and authorized execution are distinct. The assistant routes and checks; data, analysis, writing and review stay with their respective skills. Consequential research decisions stay with the researcher. Standalone translation or proofreading should not launch a research mission. In Claude Code the assistant is model-invoked and does not have a slash-menu entry.

## English and Traditional Chinese

- Ask `/research-help` in English or Traditional Chinese.
- An explicit language request takes precedence; otherwise, responses follow the language you are using. Discussion and deliverable languages can differ: “Discuss this in Traditional Chinese and draft the paper in English.”
- Command names, paths, claim IDs, and machine-readable status values stay unchanged. Translation does not verify a source or strengthen its evidence status.
- Reusable skill instructions remain concise English. User-facing help and research output support both languages; not every historical technical document has a translated copy.

See the [language convention](docs/LANGUAGE.md). For a complete first session, use the [English quickstart](docs/QUICKSTART.en.md).

## Install the 43 core skills

Requirements: Git, [uv](https://docs.astral.sh/uv/), Python 3.11 or newer, and the agent harness you intend to use. Run these commands from a local checkout you are authorized to modify.

Research OS is a suite, not one skill at the repository root. Use its catalog-driven installer rather than passing the root URL to a single-skill GitHub installer. Neither supported installation requires `.claude-plugin/plugin.json`.

```bash
git clone --branch main https://github.com/yhlai0911/research-os.git
cd research-os
uv sync --locked
```

### Codex

For a project-only installation, add the same `--target /absolute/path/to/project/.agents/skills` to all three commands below. Commands without a target intentionally use the installer's personal default. The [quickstart](docs/QUICKSTART.en.md) gives Bash and PowerShell examples.

```bash
uv run python scripts/install_skills.py --dry-run
# Continue only if the dry-run reports no conflicts.
uv run python scripts/install_skills.py
uv run python scripts/verify_install.py
```

This installer's existing default is `$CODEX_HOME/skills`, or `~/.codex/skills` when unset. That is not a universal discovery guarantee for every current host. Prefer an explicit project `.agents/skills` target, open the correct project, and verify the host's actual skill inventory. Choose a personal location according to the installed host's documentation. A turn change does not prove loading. See [official Codex skills guidance](https://developers.openai.com/codex/build-skills).

### Claude Code

```bash
uv run python scripts/install_skills.py --harness claude-code --dry-run
# Continue only if the dry-run reports no conflicts.
uv run python scripts/install_skills.py --harness claude-code
uv run python scripts/verify_install.py --harness claude-code
```

The default is `~/.claude/skills`. To install only for a project, add `--target /absolute/path/to/project/.claude/skills` to all three commands. Use copy mode, the default; symlink mode is rejected because Claude Code's installed metadata differs from the canonical source.

The adapter generates `disable-model-invocation: true` for **17 user-only skills** (16 orchestrators and one meta skill), and `user-invocable: false` for **26 model-only primitives**. It does not modify the repository's canonical `SKILL.md` files. Use `/skills` to inspect the installed list. Restart Claude Code if its top-level skills directory was created after the session started. See the [installation research](docs/research/claude-code-skills-installation.md) and [official skills documentation](https://code.claude.com/docs/en/skills).

### Verify before starting

Core verification must report `INSTALL OK: 43 skills`. The installer writes `.research-os-install.json` in the selected skills directory, recording source commit, harness, and hashes. Verification reads back the installed files and receipt. It establishes installation integrity, not the quality of future model behavior.

The installer preflights the whole selection. If a destination has conflicting content, it stops without overwriting it. Inspect and back up your changes before resolving a conflict. Do not delete or force-overwrite unrelated skills to make an installation pass.

For v1.1 installations, read the [v2 migration guide](docs/MIGRATION-v2.md) first. Twelve old orchestrator names changed, `to-proposal` stayed the same, and three new orchestrators were added. Existing `.research/` workspaces remain compatible. Old renamed directories are not automatically removed.

## Reading views and scholarly delivery

The assistant can delegate to `render-research-deliverable` for self-contained HTML reading views of actual tables and passages: sorting, filtering, synchronized charts, highlights and a before/after comparison only where real inputs exist. A reply briefly explains the result, provides the real titled artifact link, then states the next step. Generate and verify the target first. Missing output or unavailable delivery must not produce a success link. Local files and localhost are not cross-device URLs.

`research-writing` and `to-paper` require connected disciplinary prose, verified literature, managed APA citations, numbered equations with defined symbols/units, uncertainty and counterevidence. Keep skill names, program notation and operation logs outside the academic body; disclose AI assistance under the applicable rules. Chinese writing adapts clarity and terminology consistency without claiming formal compliance with the English ASD-STE100 specification. Completeness is not a fixed word or reference quota.

A paper delivery includes editable `.tex`/`.bib`, permitted assets, a PDF **actually compiled from those sources with LaTeX**, genuine build records, citation/reference checks, first-delivery all-page visual QA and a rebuildable source package. HTML and Word-exported PDFs do not replace that gate. Skills do not bundle research tools: source access, numerical libraries, a TeX engine, Biber and suitable fonts depend on the task and actual authorization. See [deliverables and dependencies](docs/DELIVERABLES.en.md).

## Optional finance and social-science profile

Install and verify the core first. Then, only if you want the domain-specific guidance:

```bash
uv run python scripts/install_skills.py --profile finance-social-science --dry-run
# Continue only if the dry-run reports no conflicts.
uv run python scripts/install_skills.py --profile finance-social-science
uv run python scripts/verify_install.py --profile finance-social-science
```

For Claude Code, add `--harness claude-code` to all three commands. Use the same `--target` as the verified core if you selected a custom target.

The profile adds the independent `/research-finance-social-science` entry point (`$research-finance-social-science` in Codex). It does not alter the 43-skill core catalog and is not automatically activated merely because a topic mentions finance or social science. Read its [English guide](profiles/finance-social-science/README.md) or [繁體中文說明](profiles/finance-social-science/README.zh-TW.md) for activation, scope, and limitations.

## First session

In your research project, invoke `/research-setup` and identify the project directory you authorize the agent to use. After setup, start:

```text
/research-1-grill

I want to study whether structured peer feedback improves the clarity of
students' research questions. I need a reviewable research plan. I have an
initial topic, but no verified literature, dataset, or chosen method yet.
Please discuss the project and write the research artifacts in English.
```

The workflow resolves one consequential decision at a time. When the idea is researchable, it recommends `/research-2-brief` and stops. Use `/research-status` to inspect progress. Re-run `/research-5-run` only for another eligible workpackage; one invocation does not imply that the entire project has been executed.

| Situation | Entry point |
|---|---|
| Develop a seed adaptively end to end | `/research-auto` |
| Decide whether an idea deserves investment | `/research-triage` |
| Map unresolved decisions across sessions | `/research-map` |
| Save a verifiable handoff | `/research-save` |
| Choose the right workflow | `/research-help` |

## Scope and evidence boundaries

- The researcher owns objectives, trade-offs, and consequential decisions. The agent investigates accessible facts and identifies access gaps.
- `.research/config.yaml` resolves canonical artifact paths. Workspace setup is additive; existing conflicting artifacts must be preserved and reconciled.
- A scoped local workflow does not authorize publication, submission, messages, issue creation, remote pushes, uploads, purchases, paid data access, or other external changes. Those require explicit authorization.
- Missing or inaccessible evidence stays `unverified`, `partial`, `contested`, or `blocked` as applicable. An unsuccessful search is not proof that a contribution is the first of its kind.
- A paper or proposal may describe planned work honestly. It must not turn an unexecuted analysis into results or turn fluent prose into evidence.
- Catalog checks, unit tests, installation verification, and evaluation scenario files do not by themselves establish fresh-agent behavioral efficacy. Bilingual and profile behavior needs separately recorded evaluations; the project does not claim that efficacy has been demonstrated.

## Architecture and maintenance

The core contains **16 orchestrators, 26 primitives, and one meta skill**. [`skills/catalog.yaml`](skills/catalog.yaml) is the source of truth; it generates the [skill catalog](docs/SKILL_CATALOG.md) and Codex metadata. Claude Code adapters are generated at installation. Other harnesses are not claimed to enforce equivalent invocation policy without an adapter and verification.

```bash
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

See [architecture](docs/ARCHITECTURE.md), [quality gates](docs/QUALITY_GATES.md), [upstream analysis](docs/MATT_SKILLS_ANALYSIS.md), and [forward-evaluation materials](tests/forward-evals/). The [Traditional Chinese cookbook](docs/PROMPT_COOKBOOK.zh-TW.md), [troubleshooting guide](docs/TROUBLESHOOTING.zh-TW.md), and [worked financial-wave example](examples/financial-wave-diffusion/WALKTHROUGH.zh-TW.md) provide additional examples; the example is not a core domain requirement.

## License

MIT. Attribution and the pinned upstream source are documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). See [CHANGELOG.md](CHANGELOG.md) for version history.
