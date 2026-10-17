# Writeback protocol

Load this reference whenever a skill reads or writes the durable research workspace. It is the single source of the resolution procedure, the Artifact index contract, and the three index statuses. Skills state only what is specific to their own artifact; they never restate the rules below.

For the canonical path inventory and authority rules, see [workspace-contract.md](workspace-contract.md).

## Resolve before reading

### Language and stable identifiers

Follow the user's explicit output-language preference; otherwise match their current language (English or Traditional Chinese). Keep commands, paths, IDs, and schema/status values unchanged. Preserve original quotations and label translations. Bilingual explanations do not authorize duplicate canonical artifacts or competing current pointers.

1. Read only `.research/config.yaml` first. Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve every canonical key the current task needs from that file. Resolve relative values against the repository root; preserve absolute values.
3. Bind the resolved values and read and write only through those bindings.
4. Treat the setup baseline paths as defaults only, never as fallback targets. When a required key is missing, invalid, or has a file/directory type collision, stop as `blocked`. Never probe or write a default path, and never invent a parallel path.
5. Read the resolved context and claim registry first, then only the artifacts linked to the active branch.

A skill that lacks explicit local-setup authority must not initialize a missing workspace. Recommend the setup entry point and stop.

## Preserve what you did not author

Preserve the resolved claim registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses that registry already declares. Keep skill-specific verdicts out of the claim-status field and out of the index statuses; they belong in the canonical artifact.

## Register in the Artifact index

Register every created or updated current artifact or evidence-task outcome in the single `## Artifact index` table in the resolved context:

`| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |`

- Keep substantive content in its canonical artifact. The index carries only identity, current state, timestamp, and lineage.
- Upsert one current row per `Kind` and `Topic`.
- When an artifact ID changes, preserve the former row as `superseded` and name its ID in the replacement row's `Supersedes`.
- Never create a second index, and never leave two current rows for the same subject.
- A claim-only outcome uses its claim IDs in the artifact-or-claim-ID column.

## Index statuses

These three are the only index statuses. Domain verdicts stay in the artifact.

- `complete` — every completion gate of the skill passes, and both the artifact or outcome and its index row read back successfully.
- `partial` — a usable, read-back durable result exists but remains incomplete, or only the index update or its readback cannot be sealed.
- `blocked` — no usable current result can be produced because a load-bearing input, permission, resolved path, artifact write, or artifact readback fails.

## Read back before reporting

Re-read the written artifact and the resolved context, then verify the row's ID, status, timestamp, and lineage agree with what was written. Report a run `complete` only after that readback passes.

If the config or the resolved context cannot be read, report `blocked` and state that registration did not occur.
