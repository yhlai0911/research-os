# Reading views, scholarly manuscripts and tool requirements

[繁體中文](DELIVERABLES.zh-TW.md) · [Assistant guide](RESEARCH_ASSISTANT.en.md) · [Quickstart](QUICKSTART.en.md)

## Research and presentation have different owners

`research-assistant` selects the next skill and checks its returned evidence. Data, methods, execution, writing and review remain with their applicable skills. `render-research-deliverable` presents those canonical artifacts; it does not invent results or replace the underlying research. `to-paper` coordinates the destination contract with writing, review, citation and production requirements.

## HTML reading views and the actual reply

Use a reading view when a real table, chart, passage or revision is easier to inspect in a browser. Prepare the renderer input from the current source, preserving raw values, units, sources, missing cells and display precision. Optional views appear only when their data exist. A revision requires two actual versions; an empty table is not fabricated into a result.

The reply contract has three parts: a short grounded explanation, the real titled output link, and the next research action. Generate the artifact first and check the target. A failure, missing file or unavailable delivery surface must be reported without a placeholder success link. Summary truth still needs source review; the helper checks artifact identity, not scientific validity.

The self-contained page supports sorting/filtering, a synchronized chart, passage highlights, revision comparison and return navigation as applicable. Controls need real targets/handlers. Browser acceptance means actually clicking the reply link and controls, inspecting empty/missing-data states and checking readable desktop/narrow layouts. A screenshot or timed cursor animation cannot prove a click. A saved reply page is not native chat.

The renderer uses Python's standard library and bundled HTML/CSS/JavaScript, without remote resource dependencies. It escapes data, rejects unsafe sources/nonfinite numeric inputs and refuses overwriting output files. Do not weaken those rules to display an artifact.

### Reproducible synthetic reading example

From the repository root, choose output names that do not already exist:

```bash
uv run python skills/primitives/render-research-deliverable/scripts/render_reading_view.py --input examples/interactive-reading/synthetic-comparison.json --output reading-demo.html
uv run python skills/primitives/render-research-deliverable/scripts/build_reading_reply.py --artifact reading-demo.html --next-step "Inspect the synthetic comparison, then return to the actual research question." --output reading-demo-reply.md --response-html reading-demo-reply.html
```

This [input](../examples/interactive-reading/synthetic-comparison.json) is explicitly synthetic UI data, not an empirical study. Open the resulting page with a supported local browser surface. `build_reading_reply.py` can also verify an already authorized loopback preview by fetching its exact bytes; it does not start a server or publish anything. See the [full renderer contract](../skills/primitives/render-research-deliverable/references/html-reading-views.md).

Local files and `127.0.0.1` are not accessible from another device. Use the host's real file-link format for local delivery, or an authorized supported attachment route for cross-device delivery. Do not turn a Windows path into a public URL or invent a download address.

## Academic manuscripts

The writing contract requires connected disciplinary prose: problem, closest verified literature, unresolved issue, rationale/mechanism, question, design, estimates with uncertainty, competing explanations and warranted conclusion. Develop the links between them. Lists, polished sentences, a word quota or a reference quota do not establish academic completeness.

Keep skill names, program variables/functions, file paths and operation logs out of the academic body. Preserve substantive data-processing and statistical detail in scholarly language; move reproducibility code to a technical appendix. Disclose AI assistance under the applicable institutional/venue rules. Use a verified template when supplied; do not claim unspecified school compliance or degree approval.

Chinese prose can adapt clear referents, precise wording and consistent terms. ASD-STE100 is a controlled-English technical-documentation specification; applying relevant clarity principles does not certify Chinese academic writing. Preserve necessary nuance and argument.

Number and label substantive equations, refer to them in the prose, define symbols/indices/units/assumptions near first use, and explain their derivation or verified source and model-selection rationale. Keep falsifiers, null/adverse results, failed checks and inference boundaries.

Use managed `.bib` references, normally APA 7 via BibLaTeX/Biber and `biblatex-apa`. Verify author/order/year/title/venue/DOI against authoritative records and source support separately. A resolving DOI is not proof of entailment; abstract-only access is not full-text reading. Reconcile citation keys, Bib entries and generated references. See [the scholarly-delivery contract](../skills/primitives/research-writing/references/scholarly-delivery.md).

## Genuine LaTeX delivery

Deliver editable `.tex`, `.bib` and permitted supporting assets with the PDF actually compiled from those sources. Retain real engine/backend commands, versions, exit codes, source/PDF hashes and final logs. Complete bibliography/cross-reference reruns; resolve undefined citations/references, missing glyphs, duplicate labels and outstanding rerun diagnostics. Inspect every rendered page on first delivery, then changed pages and pagination effects after repair. Package current inputs, build instructions, dependency/font versions and current academic/citation/visual reviews.

HTML is a reading companion. Word conversion or a directly drawn PDF does not substitute for a LaTeX build. Without an authorized compiler/backend/font, preserve sources and report a partial or blocked production gate instead of claiming PDF completion. Academic reviewers, citation checks and mechanical provenance checks provide different evidence; compilation does not certify scholarly or degree readiness.

## Tools and platform scope

| Work | Required capability | What Research OS supplies |
|---|---|---|
| Install/validate skills | Git, uv, Python 3.11+, supported harness | Catalog, installer, adapters, conflict checks and receipts |
| Literature/data access | Authorized browser/search/connectors or local sources | Source-verification discipline; no paid access or credentials |
| Data analysis | Actual suitable numerical/statistical tools | Method and execution contracts; no universal bundled analysis runtime |
| Reading views | Python standard library; browser for interaction QA | Self-contained renderer, assets and verified-reply helper |
| Chinese LaTeX paper | Suitable TeX engine such as XeLaTeX/LuaLaTeX, packages, permitted CJK fonts; managed APA backend | Writing/production gates, not a TeX/font installation |
| Tutorial capture | Formally supported capture surface | Evidence rules; no promise of desktop capture merely because a browser works |
| Release ZIP creation | POSIX safety primitives required by the packager | Fail-closed deterministic packaging; Windows copy installation is a separate capability |

Do not install tools, pay, log in, publish or change security settings merely because a skill needs them. Identify the exact missing dependency and use the authority actually granted. Default copy installation is the portable path; Windows symlink privileges and POSIX release tests have additional limits. See [quality gates](QUALITY_GATES.md) and [troubleshooting](TROUBLESHOOTING.zh-TW.md).
