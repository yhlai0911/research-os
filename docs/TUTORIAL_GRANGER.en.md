# From installation to a research draft: Treasury example

[Watch/download voiced v4](https://github.com/yhlai0911/research-os/releases/download/granger-tutorial-voiced-v4/research-os-granger-follow-along-voiced-v4.mp4) · [Release and checksum](https://github.com/yhlai0911/research-os/releases/tag/granger-tutorial-voiced-v4) · [繁體中文](TUTORIAL_GRANGER.zh-TW.md)

This Traditional Chinese tutorial has 40 scenes and runs for 7:57.93. Using 2015–2024 US two-year and ten-year Treasury yields, it follows installation, the six research steps, a diagnostic revision, analysis, and delivery of a bounded first draft.

The interface reconstructs selected teaching text and illustrates actions such as selecting a folder, sending a request, waiting, opening files, and resuming in a new conversation. It is not a live recording of the native Codex or Claude interface. Interruptions and the original diagnostic failure remain visible.

## Start your own project

Install and sign in to Codex or Claude Code, confirm that you can chat, and create a fresh research folder. Follow the tool-specific instructions in the [English README](../README.en.md) to install and verify the 42 general-purpose core skills. The optional finance and social-science profile was not installed in this example. Resolve conflicts without overwriting existing artifacts.

Verification should report `INSTALL OK: 42 skills`. Retain the source commit from your installation receipt. The example started at `4f7c162`, then adopted the public writing guidance at `a9174de` and reverified the core. These identify the example's sources, not a permanently fixed `main` branch.

In the next turn, set up the same research folder and specify the language you want:

```text
$research-setup Prepare this research folder. Discuss the project and write the draft in English.
```

Codex uses `$skill-name`; Claude Code uses `/skill-name` and requires `--harness claude-code` for installation and verification. Skill names and paths do not change with the discussion language.

| Step | What to check | Artifact to open |
|---|---|---|
| `research-1-grill` | Objectives, period, both directions, and prediction target | Research decisions |
| `research-2-brief` | Saved scope, method, and unresolved rules | Research Brief |
| `research-3-falsify` | Conditions requiring a stop or withdrawal | Falsification plan |
| `research-4-tasks` | Deliverables and acceptance conditions | Workpackage index and specifications |
| `research-5-run` | Actual outputs and data/model diagnostics | Analysis report and results |
| `research-6-review` | Failure explanations, bounded revisions, and limitations | Independent review |

Open the artifact links after each step. Ask for explanations when needed. A completed file, completed work, and a model eligible for inference are separate judgments. Resume in the same folder by reading the existing research record first.

After a diagnostic stop and an accepted revision, this example used `research-auto` to continue analysis, drafting, and comparative review. A single `research-5-run` invocation executes one eligible workpackage, not the whole project.

## Reading the result

Granger tests address additional predictive information within a specified model; they do not establish economic causality. Neither direction met the specified threshold in the main tests or fixed sensitivity analyses. This is insufficient evidence under the stated design, not proof that a predictive relationship does not exist or that trading profits follow.

The original stop is retained. The revision changes the treatment of heteroskedasticity in the residual diagnostic while preserving the data, model selection, and main equation. Non-rejection does not prove model correctness. The delivered first draft retains limitations involving leverage, finite-sample approximation, prior model selection, and the later diagnostic revision. It is not certified as submission-ready.

## Sources and earlier version

The [v4 source package](../jobs/research-os-granger-tutorial/v4/README.md) includes narration, the 40-scene timeline, HyperFrames visual source, retained audio, offline rebuild code, and hashes. Rebuilding needs no speech-service login or paid call. Full private conversations, installation receipts, private research workspaces, and private skills are excluded; only teaching excerpts already used in the film remain.

The [original 4:01 overview and sources](../jobs/research-os-tutorial/README.md) remain available. This publication reuses the completed MP4 without regenerating the film or narration.
