# Research assistant verification

The catalog is authoritative. `research-assistant` is a model-invoked guide/controller; native mainline discovery stays explicit, while user-authorised workflow delegation is allowed without forcing a novice to name each entry. The receiving skill owns the research work. Official initializer provenance: Codex `skill-creator/scripts/init_skill.py research-assistant --path skills/primitives`, followed by catalog generation and `quick_validate.py`.

`tests/test_workflow_handoff.py` runs the non-mutating transfer helper against a blank project, a real initializer-created contract, an invalid contract and clean installed packages. These prove preflight/packaging behavior, not model routing or native invocation. A separate real no-topic followthrough must retain the natural input, assistant selection, receiving-skill operations and actual first question; an unanswered role question stops dependent topic work. Keep environment-specific execution records outside the public product tree; publish only sanitized product verification material.

## Structural and unit checks

```text
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

`tests/test_research_assistant.py` checks discovery metadata, the shared contract dependency, preservation of user-only workflows, source byte preservation, LF/CRLF Claude adapters, and exclusive local evaluation preparation. `tests/test_installed_dependencies.py` installs the catalog into clean projects, independently opens relative Markdown dependencies, and verifies that missing source/installed dependencies fail without overwriting user files. These are distribution/fixture checks, not model evaluations. On Windows, release/symlink/POSIX tests may fail independently; compare against the unchanged source commit before attributing regressions. Do not weaken packaging protections to make a Windows run green.

## Fresh-agent protocol

The raw prompts and separate observation rubric are in `tests/fixtures/research-assistant/cases.yaml`. Prepare one new disposable directory per case:

```text
uv run python scripts/prepare_assistant_eval.py natural-data --output <new-local-evaluation-directory>
```

Preparation installs only into that directory's `.agents/skills`, creates synthetic fixtures, and does not call a model. Existing directories are refused. No global installation or credentials are needed for preparation.

Run a new agent rooted in the prepared directory using only `prompt.txt` as the user request. For a real invocation test, let the harness discover the installed skills; do not mention the skill name or force-load it. Record CLI/harness version, effective skill inventory, selected skill, tool trace, reads/writes, result, and resource usage if exposed. Snapshot fixture files before/after; reject unauthorized mutations. Stop if the harness requires login, extra paid usage, or unsupported access; do not modify credentials to proceed.

Use the observation rubric only after the agent finishes. Judge actual actions and artifact contents, not keyword matches in the answer. Translation/proofreading must not load the companion or read research state. The adapter-path fixture contains a decoy baseline context; reading it is a config-resolution failure. Multiple projects require a target choice before reading their contents. A complete review with a `major-revision` verdict cannot pass manuscript readiness.

A fresh agent given the candidate description and skill location can test the behavioral contract and a simulated selection decision. Label this **direct-context forward testing**; it does not prove live harness implicit invocation. A forced explicit-skill evaluation likewise cannot prove natural selection. Cross-session fixtures test reconstruction from durable state, not a live multi-turn resume implementation.

The `authorized-local-check` case permits an actual small check and canonical writeback. Inspect the check result, changed files and readback, verify preserved inputs and workpackage state, and distinguish this finite execution from a proposed mainline handoff. A written recommendation alone cannot pass this case. The two-row synthetic fixture supports checking mechanics only, never a real study's feasibility or findings.

Save successful, failed, blocked and untested observations separately. A recommendation, handoff, fixture-preparation success, or static pass is not evidence that a research workflow executed.

The [public verification scope](../tests/forward-evals/research-assistant-public-verification.md) separates automated distribution checks from model behavior and native invocation. Personal CLI diagnostics, research-case outputs and private execution logs are not shipped with the product.
