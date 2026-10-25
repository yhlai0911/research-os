# Bank term-deposit marketing and contact priority

[繁體中文](README.zh-TW.md) · [Follow-along tutorial](../../docs/TUTORIAL_BANK.en.md) · [Public material release](https://github.com/yhlai0911/research-os/releases/tag/bank-term-deposit-tutorial-v1)

This bounded management/finance master's teaching example asks how information assumptions and validation procedures change model selection and priority contact lists in the UCI Bank Marketing data. It is an empirical replication and comparison, not a new algorithm, causal marketing estimate or school-approved thesis.

The release supplies the authorized **ivan-advanced / Eleven v4 standard** narrated walkthrough, a genuine 30-page XeLaTeX/Biber PDF, and a clean LaTeX/Bib/data/numerical source package. Large artifacts remain release assets; this directory contains only a light index, [study design](STUDY_DESIGN.md), [six focal results](focal-policy.csv) and authoritative [asset metadata](assets.json).

The 13-chapter film follows no-topic exploration, rejected candidates, a change of direction, design, prespecified falsification and tasks, analysis, review, academic writing and visible revision. Research-assistant selects and delegates; each receiving skill performs its part. It uses a teaching role and real browser artifact captures. It is not evidence of native Codex discovery or automatic invocation, and human listening/ASR certification is not claimed.

## Reproduce the numerical example

Download and extract the source ZIP listed in [assets.json](assets.json). It includes unchanged **41,188-record bank-additional-full.csv**, with the UCI DOI and CC BY 4.0 attribution; it excludes the older 45,211-record file. With an already available compatible Python environment:

```bash
python analysis/reproduce.py verify
python analysis/reproduce.py refit-primary --output fresh-primary-output
```

`verify` checks all saved policies, contrasts, bootstrap quantiles and numerical fixtures without retraining. `refit-primary` explicitly repeats the primary fit into a new directory. During public preparation it reproduced both original score vectors exactly. Full sensitivity-grid retraining was not repeated. Dependencies are documented in the archive; nothing is installed automatically.

For the manuscript, use its `manuscript/BUILD.md`: XeLaTeX → Biber → XeLaTeX → XeLaTeX, with legal CJK fonts. The original PDF used Microsoft JhengHei on Windows; fonts and TeX binaries are not redistributed. Another font may change pagination and PDF bytes. The video stops before the subsequent PDF compilation; the published PDF is that later completed typesetting output.

Use **PUBLIC_ASSETS_SHA256SUMS.txt** for the public ASCII filenames. GitHub removes Chinese filename characters, so complete English subject names are used for download assets while Chinese titles remain in the release. The older SHA256SUMS.txt retains local original Chinese filenames and is clearly distinguished on the release page.

No private conversations, credentials, account usage, voice model, installed toolchain or third-party paper full texts are included. Data rights and code/media scope are documented in the ZIP. This example remains separate from the [earlier Treasury/Granger tutorial](../../docs/TUTORIAL_GRANGER.en.md).
