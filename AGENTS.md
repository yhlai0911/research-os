# Repository instructions

- Use Traditional Chinese for user-facing project reports; keep reusable skill instructions in concise English.
- Use `uv` for Python environments, dependencies, validation, tests, and packaging.
- Treat `skills/catalog.yaml` as the inventory and metadata source of truth.
- Initialize every new skill with the Codex `skill-creator` initializer before editing it.
- Keep `SKILL.md` frontmatter to `name` and `description`.
- Put deterministic mechanics in `scripts/`, conditional guidance in one-level `references/`, and copyable templates in `assets/`.
- Use `apply_patch` for source edits.
- Run `uv run python scripts/sync_catalog.py --check`, `uv run python scripts/validate_repository.py`, and `uv run pytest` before committing.
- Preserve user artifacts. Installers and workspace setup must not overwrite conflicts.
- Label unsupported research claims as unverified, contested, partial, or blocked.
- Do not publish, submit, send, purchase, or mutate external systems without explicit authorization.
