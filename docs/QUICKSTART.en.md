# Research OS: English quickstart

[English README](../README.en.md) · [繁體中文 README](../README.md) · [繁體中文使用教學](USAGE_GUIDE.zh-TW.md)

This guide installs the 43-skill generic core and walks through a first research session. The optional [finance-social-science profile](../profiles/finance-social-science/README.md) is a separately installed, explicit opt-in in the same repository. It is not a second repository or part of the default core installation.

Workflow examples below use Claude Code's `/skill-name` notation. In Codex, use `$skill-name` to explicitly invoke the same skill; for example, `$research-setup` and `$research-1-grill`.

## 1. Choose the source and installation scope

You need Git, [uv](https://docs.astral.sh/uv/), Python 3.11 or newer, and Codex or Claude Code.

Install the v2 six-step workflow from `main`. The installation receipt records the exact source commit so you can identify and reproduce your installed revision:

```bash
git clone --branch main https://github.com/yhlai0911/research-os.git
cd research-os
git branch --show-current
git rev-parse HEAD
uv sync --locked
```

If you already have a checkout, preserve uncommitted changes and deliberately select the intended branch or commit before installing. Do not blindly replace your working tree.

Research OS is a suite, not a root-level skill. Its installer reads the complete catalog and records a receipt. A single-skill installer pointed at the repository root is not equivalent, and no Claude plugin manifest is required.

If you are upgrading from v1.1, go to [Migration](#migration-from-v11) before running an installer against your existing skills directory.

## 2. Install for your harness

Choose one of the following. A dry-run is an inspection step: **run the installation only when it reports no conflicts**. The installer will also enforce the conflict check when run normally.

### Codex: personal installation

```bash
uv run python scripts/install_skills.py --dry-run
uv run python scripts/install_skills.py
uv run python scripts/verify_install.py
```

Target: `$CODEX_HOME/skills`, or `~/.codex/skills` if `CODEX_HOME` is unset. For a custom Codex skills directory, pass the same `--target /absolute/path/to/skills` on all three commands. New skills load on the next turn or task.

### Claude Code: personal installation

```bash
uv run python scripts/install_skills.py --harness claude-code --dry-run
uv run python scripts/install_skills.py --harness claude-code
uv run python scripts/verify_install.py --harness claude-code
```

Target: `~/.claude/skills`. The installer generates Claude Code invocation metadata from the catalog: 17 user-only skills (16 orchestrators plus one meta skill) and 26 model-only primitives. Copy mode is required and is the default.

### Claude Code: project-only installation

Replace the absolute project path below. Run from the Research OS checkout, not from the target project's skills directory:

```bash
uv run python scripts/install_skills.py \
  --harness claude-code --target /absolute/path/to/project/.claude/skills --dry-run
uv run python scripts/install_skills.py \
  --harness claude-code --target /absolute/path/to/project/.claude/skills
uv run python scripts/verify_install.py \
  --harness claude-code --target /absolute/path/to/project/.claude/skills
```

Use Claude Code's `/skills` to inspect the commands. If the top-level skills directory was created after your session started, restart Claude Code. See the [official skills documentation](https://code.claude.com/docs/en/skills) for discovery behavior.

### Check the result

Expect `INSTALL OK: 43 skills`. Read `.research-os-install.json` in the selected target directory and check its `source_commit`, `harness`, and recorded hashes. The verifier checks installed files against the current source checkout and receipt.

If the dry-run reports a conflict, inspect the exact path. Back up local customizations and resolve ownership or version conflicts deliberately, then rerun dry-run. The installer does not overwrite conflicting skills. A successful verification establishes installation integrity, not a guarantee of model behavior.

## 3. Set the language and research workspace

Open the research project where you want artifacts stored. Invoke:

```text
/research-setup

Initialize Research OS in this project directory. Preserve existing files.
Use English for our discussion and research artifacts.
```

Use an explicit project path if the active directory is unclear. Setup establishes `.research/config.yaml`, which points to the canonical context, decisions, claim registry, and research artifacts. It is not permission to write elsewhere or change external services.

You can instead request Traditional Chinese discussion and English deliverables. Explicit language choices take precedence; otherwise help and output follow the user's language. Skill names, command names, paths, claim IDs, and machine-readable statuses remain unchanged. See [LANGUAGE.md](LANGUAGE.md).

Unsure where to begin? Use `/research-help` with a short description of what you have. It recommends a route and stops; it does not launch the next workflow for you.

For guided progression, ask `$research-assistant` in ordinary language, including "I want to write a thesis but have no topic." It selects and delegates the applicable workflow, whose instructions own the actual research work, then checks the returned result before guiding the next step. You need not type each skill name; missing research decisions still require your answer. Native invocation and fully read delegated instruction-followthrough must be reported separately when the host has no native skill interface.

## 4. Work through the six-step mainline

Start with one bounded seed:

```text
/research-1-grill

I want to study whether structured peer feedback improves the clarity of
students' research questions. My intended output is a research plan for review.
I have no verified literature, dataset, or selected method yet. Help me decide
what is researchable, and keep unsupported factual claims explicitly unverified.
```

The workflow asks one dependent researcher decision at a time and investigates accessible facts itself. Each step checks its completion conditions, records the current result, names a next step, and stops. Invoke the next command only when you are ready:

1. `/research-1-grill`: bound the question, mechanism, evidence requirements, and failure conditions.
2. `/research-2-brief`: consolidate settled decisions and evidence into one research contract.
3. `/research-3-falsify`: predeclare falsifiers, rival explanations, and kill/repair/continue conditions before execution.
4. `/research-4-tasks`: create bounded, independently verifiable workpackages.
5. `/research-5-run`: execute one eligible workpackage within its allowed reads, writes, and stop conditions; leave a verified receipt. Repeat for other eligible tasks as needed.
6. `/research-6-review`: challenge the current work and identify unresolved or repairable weaknesses.

Use `/research-status` at any time to read progress and gaps. It does not advance or repair the project. If a stage is `blocked`, resolve the named missing evidence, access, or decision rather than skipping the gate and calling it complete.

After the relevant evidence and review gates, select `/to-plan`, `/to-proposal`, or `/to-paper`. A manuscript request cannot turn unexecuted work into empirical findings. With insufficient results, the honest output may be a blueprint, partial draft, or blocked state.

For adaptive end-to-end work, start `/research-auto` instead of manually walking every command. It selects narrow primitives around the live bottleneck and may establish the scoped workspace; it cannot silently launch another user-only workflow or acquire additional permissions.

## 5. Optionally add the finance-social-science profile

Skip this section for the generic core. After core verification succeeds:

```bash
uv run python scripts/install_skills.py --profile finance-social-science --dry-run
uv run python scripts/install_skills.py --profile finance-social-science
uv run python scripts/verify_install.py --profile finance-social-science
```

For Claude Code, add `--harness claude-code` to all three commands. If the core uses a custom target, pass that same `--target` to all profile commands.

The independent `/research-finance-social-science` entry point (`$research-finance-social-science` in Codex) adds opt-in domain guidance without changing the 43-skill core catalog. Installing it does not make every project use it. Follow the [profile's activation and scope instructions](../profiles/finance-social-science/README.md) ([繁體中文](../profiles/finance-social-science/README.zh-TW.md)).

## Migration from v1.1

Read [MIGRATION-v2.md](MIGRATION-v2.md) for the exact old-to-new name mapping. Of the 13 v1.1 orchestrators, 12 were renamed and `to-proposal` retained its name; three new orchestrators bring v2 to 16. The 25 primitives keep their names, and existing `.research/` workspaces remain compatible.

The installer does not remove old names. Back up customizations, identify the old directories from the mapping, and remove only those you intend to replace. Do not delete the research workspace. Same-name content changes can still cause installation conflicts and need deliberate resolution. Then rerun dry-run, installation, and verification for the correct harness and target.

## Permissions and evidence: what completion means

- Scope local work to the project and canonical paths you authorized. Preserve existing artifacts and reconcile conflicts.
- Human objectives, values, trade-offs, and consequential decisions remain with the researcher.
- Reading accessible evidence does not authorize paid access, new credentials, uploads, messages, publication, submission, issue creation, pushes, purchases, or other external state changes. Ask for explicit authorization before those actions.
- Unavailable tools, inaccessible sources, and incomplete evidence remain visible as limitations. A literature search that found nothing does not prove novelty.
- Quote and cite only what was actually verified. Keep planned analyses distinct from executed analyses and observed results.
- Repository validation, installation checks, and evaluation scenarios are different kinds of evidence. Their existence does not show that fresh-agent behavioral evaluations ran, nor that bilingual support or the optional profile improves research outcomes. No such efficacy is claimed here.

For technical validation, maintainers can run:

```bash
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

Continue with the [skill catalog](SKILL_CATALOG.md), [architecture](ARCHITECTURE.md), and [quality gates](QUALITY_GATES.md).
