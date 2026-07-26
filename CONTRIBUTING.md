# Contributing

Start with `$writing-research-skills`. Add or change the catalog entry first, then initialize a new skill through Codex’s official skill initializer.

Each contribution must preserve these invariants:

1. one distinct responsibility and leading concept;
2. correct user/model invocation boundary;
3. concrete trigger examples and near-misses;
4. observable completion, partial, and blocked states;
5. one authority for each durable meaning;
6. no initializer placeholders, empty resources, or skill-local README;
7. current `agents/openai.yaml` generated from the catalog;
8. passing structural tests and fresh-agent forward tests.

Run:

```bash
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py
uv run python scripts/validate_repository.py
uv run pytest
```

When deprecating a skill, identify its replacement, remove router and dependency references, and add a validation fixture proving no ghost reference remains.
