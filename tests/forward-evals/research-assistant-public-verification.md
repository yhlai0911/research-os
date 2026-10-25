# Research assistant: public verification scope

The product ships deterministic tests and synthetic fixtures. It does not ship a user's thesis, research data, conversation history, machine paths, authentication status or CLI diagnostics.

## Automated coverage

- `test_research_assistant.py`: catalog metadata, the guide/router boundary, explicit-workflow compatibility, adapters and isolated fixture preparation.
- `test_workflow_handoff.py`: blank-project setup routing, valid and invalid contracts, installed handoff dependencies and non-mutating preflight.
- `test_installed_dependencies.py`: clean local installations and actual readable relative dependencies, including missing-reference failures.
- `test_html_reading_view.py`: generated local reading views, safe data handling, available content, functional controls and verified reply links; missing outputs must not produce success links.
- `test_academic_body.py` and `test_latex_delivery.py`: body-language and scholarly-production checks, with positive and negative fixtures. A fixture log is never evidence that a user's thesis compiled.

These six modules contain 61 automated cases in this product version. They test mechanics and contracts. They do not establish native Codex menu visibility, discovery, loading, implicit invocation, a live cross-session resume, or an end-to-end research outcome.

## Model behavior requires separate evidence

Use the preparation and fresh-agent protocol in `docs/RESEARCH_ASSISTANT_TESTING.md`. Preserve the real input, routing decision, fully read receiving instructions, actual actions and output readback. Label explicit instruction-followthrough and direct-context evaluation accurately. A recommended skill is not an executed skill.

Retain all outcomes, including rejected candidates, missing prerequisites, unresolved decisions and failed checks. Evaluate irrelevant translation/proofreading prompts separately. Never upgrade an installed-file check or a teaching screenshot into a native-invocation result.

## Synthetic reading example

`examples/interactive-reading/synthetic-comparison.json` contains deliberately synthetic values for UI demonstration. Its source label, summary and excerpt identify that scope. It is not a study, observed empirical result or replacement for a research artifact's provenance.
