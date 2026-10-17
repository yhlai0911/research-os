# Research OS

**English** · [繁體中文](README.md) · [English quickstart](docs/QUICKSTART.en.md) · [繁體中文使用教學](docs/USAGE_GUIDE.zh-TW.md)

Research OS is a composable set of Agent Skills for turning a topic, equation, dataset, draft, or reviewer concern into a falsifiable research brief and an evidence-led plan, proposal, or paper. It separates researcher decisions from discoverable facts, records uncertainty and provenance, and makes the conditions for completing or stopping each stage explicit.

Its design draws on [Matt Pocock's skills](https://github.com/mattpocock/skills), including narrow primitives, explicit completion criteria, progressive disclosure, and feedback loops. Research OS adds claim–evidence tracking, counterfactuals, falsification, data feasibility, ethics, reproducibility, and durable handoffs. These are design intentions, not a claim that the system has demonstrated better research outcomes.

**Version and installation:** this guide covers the v2 six-step workflow, bilingual operation, and optional domain profile. Installation commands use `main`; check the installation receipt's source commit to identify the version you actually installed. Existing v1.1 users should read the [migration guide](docs/MIGRATION-v2.md) first.

**One repository, distinct core and optional extension:** the default suite remains **42 generic core skills**. The independent [finance-social-science profile](profiles/finance-social-science/README.md) ([繁體中文](profiles/finance-social-science/README.zh-TW.md)) lives in this same repository. It is not a separate repository and is not installed by default. Explicit opt-in keeps domain-specific assumptions out of the generic workflow.

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
  /research-status      Read current progress, artifacts, gaps, and next step

Deliverables
  /to-plan   /to-proposal   /to-paper
```

Each mainline step has checkable completion conditions. It names the next step and stops; a recommendation does not authorize launching another user-invoked skill. Falsification comes before task decomposition so the project records failure conditions before spending execution effort.

The agent may use 25 model-invoked research primitives as needed. You do not need to memorize their names. The six steps are the user-facing path; they do not force every topic through every possible method.

For a less manual route, `/research-auto` works adaptively on the current bottleneck using model-invoked primitives. It still respects researcher decisions, workspace scope, evidence limits, and external-action permissions. `/research-help` recommends an entry point and stops.

## English and Traditional Chinese

- Ask `/research-help` in English or Traditional Chinese.
- An explicit language request takes precedence; otherwise, responses follow the language you are using. Discussion and deliverable languages can differ: “Discuss this in Traditional Chinese and draft the paper in English.”
- Command names, paths, claim IDs, and machine-readable status values stay unchanged. Translation does not verify a source or strengthen its evidence status.
- Reusable skill instructions remain concise English. User-facing help and research output support both languages; not every historical technical document has a translated copy.

See the [language convention](docs/LANGUAGE.md). For a complete first session, use the [English quickstart](docs/QUICKSTART.en.md).

## Install the 42 core skills

Requirements: Git, [uv](https://docs.astral.sh/uv/), Python 3.11 or newer, and the agent harness you intend to use. Run these commands from a local checkout you are authorized to modify.

Research OS is a suite, not one skill at the repository root. Use its catalog-driven installer rather than passing the root URL to a single-skill GitHub installer. Neither supported installation requires `.claude-plugin/plugin.json`.

```bash
git clone --branch main https://github.com/yhlai0911/research-os.git
cd research-os
uv sync --locked
```

### Codex

```bash
uv run python scripts/install_skills.py --dry-run
# Continue only if the dry-run reports no conflicts.
uv run python scripts/install_skills.py
uv run python scripts/verify_install.py
```

The default target is `$CODEX_HOME/skills`, or `~/.codex/skills` if `CODEX_HOME` is unset. For another location, add the same `--target /absolute/path/to/skills` to all three commands. Newly installed skills load on the next Codex turn or task.

### Claude Code

```bash
uv run python scripts/install_skills.py --harness claude-code --dry-run
# Continue only if the dry-run reports no conflicts.
uv run python scripts/install_skills.py --harness claude-code
uv run python scripts/verify_install.py --harness claude-code
```

The default is `~/.claude/skills`. To install only for a project, add `--target /absolute/path/to/project/.claude/skills` to all three commands. Use copy mode, the default; symlink mode is rejected because Claude Code's installed metadata differs from the canonical source.

The adapter generates `disable-model-invocation: true` for **17 user-only skills** (16 orchestrators and one meta skill), and `user-invocable: false` for **25 model-only primitives**. It does not modify the repository's canonical `SKILL.md` files. Use `/skills` to inspect the installed list. Restart Claude Code if its top-level skills directory was created after the session started. See the [installation research](docs/research/claude-code-skills-installation.md) and [official skills documentation](https://code.claude.com/docs/en/skills).

### Verify before starting

Core verification must report `INSTALL OK: 42 skills`. The installer writes `.research-os-install.json` in the selected skills directory, recording source commit, harness, and hashes. Verification reads back the installed files and receipt. It establishes installation integrity, not the quality of future model behavior.

The installer preflights the whole selection. If a destination has conflicting content, it stops without overwriting it. Inspect and back up your changes before resolving a conflict. Do not delete or force-overwrite unrelated skills to make an installation pass.

For v1.1 installations, read the [v2 migration guide](docs/MIGRATION-v2.md) first. Twelve old orchestrator names changed, `to-proposal` stayed the same, and three new orchestrators were added. Existing `.research/` workspaces remain compatible. Old renamed directories are not automatically removed.

## Optional finance and social-science profile

Install and verify the core first. Then, only if you want the domain-specific guidance:

```bash
uv run python scripts/install_skills.py --profile finance-social-science --dry-run
# Continue only if the dry-run reports no conflicts.
uv run python scripts/install_skills.py --profile finance-social-science
uv run python scripts/verify_install.py --profile finance-social-science
```

For Claude Code, add `--harness claude-code` to all three commands. Use the same `--target` as the verified core if you selected a custom target.

The profile adds the independent `/research-finance-social-science` entry point (`$research-finance-social-science` in Codex). It does not alter the 42-skill core catalog and is not automatically activated merely because a topic mentions finance or social science. Read its [English guide](profiles/finance-social-science/README.md) or [繁體中文說明](profiles/finance-social-science/README.zh-TW.md) for activation, scope, and limitations.

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

## Video tutorial

**Concept overview and installation guide:** the [3m47s Traditional Chinese tutorial](jobs/research-os-tutorial/v3/paced/output/research-os-tutorial-v3-paced-zh-TW.mp4), based on `56159bb`, uses twelve newly recorded Eleven v4 narration sections with pitch-preserving pacing and synchronized subtitles. It covers verified installation replays, Codex/Claude invocation, the 42-skill general core, the optional finance/social-science skill, language selection, and the six-step workflow. See [chapters, examples, reproduction, and QA](jobs/research-os-tutorial/v3/README.md) and the [frame overview](jobs/research-os-tutorial/v3/paced/evidence/delivery-scenes-contact.jpg). The previous eight-section tutorial remains in its original folder.

**Hands-on walkthrough: in preparation; no playable video yet.** The [recording plan](jobs/research-os-tutorial/PRACTICAL_PLAN.md) covers an actual blank project, setup, question/answer exchange, Brief, domain review, revision, and status. Future tutorial videos will be listed in both READMEs with playback links, chapter times, applicable versions, and example files. Unfinished videos remain marked as planned.

## Architecture and maintenance

The core contains **16 orchestrators, 25 primitives, and one meta skill**. [`skills/catalog.yaml`](skills/catalog.yaml) is the source of truth; it generates the [skill catalog](docs/SKILL_CATALOG.md) and Codex metadata. Claude Code adapters are generated at installation. Other harnesses are not claimed to enforce equivalent invocation policy without an adapter and verification.

```bash
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

See [architecture](docs/ARCHITECTURE.md), [quality gates](docs/QUALITY_GATES.md), [upstream analysis](docs/MATT_SKILLS_ANALYSIS.md), and [forward-evaluation materials](tests/forward-evals/). The [Traditional Chinese cookbook](docs/PROMPT_COOKBOOK.zh-TW.md), [troubleshooting guide](docs/TROUBLESHOOTING.zh-TW.md), and [worked financial-wave example](examples/financial-wave-diffusion/WALKTHROUGH.zh-TW.md) provide additional examples; the example is not a core domain requirement.

## License

MIT. Attribution and the pinned upstream source are documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). See [CHANGELOG.md](CHANGELOG.md) for version history.
