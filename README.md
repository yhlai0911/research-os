# Research OS

Research OS 是一套可組合的 Agent Skills，用來把一個主題、方向、方程式、現象、資料、草稿或審查意見，透過自適應對話推進成可反駁、可執行、可審查的研究計畫、企劃案或論文。它不把「寫出很多字」當作完成；它會主動查證文獻與資料、區分研究者決策和可查事實、模擬審查攻擊、修補根因，再把已驗證狀態封裝成單一 Research Brief，最後依目的轉譯成所需成果。

本專案深層研究了 [Matt Pocock Skills](https://github.com/mattpocock/skills) 的完整 skill 架構與提示詞設計，但沒有逐句移植。Research OS 保留其最有效的底層原則：router 與 primitive 分工、leading concept、可檢查的 completion criterion、progressive disclosure、single source of truth、真實 feedback loop；並補上學術研究需要的 claim-evidence ledger、counterfactual、falsification、資料可得性、倫理、重現性與交接 receipt。

## 主線：六步，打 `/research-` 就照號碼排好

```text
一次性
  /research-setup        建立 .research/ 工作區

主線
  /research-1-grill      逼問：把模糊想法問成可研究的問題
  /research-2-brief      鎖定：把討論收斂成一份研究契約
  /research-3-falsify    找碴：先講清楚什麼結果會推翻你
  /research-4-tasks      拆解：切成可獨立驗證的研究任務
  /research-5-run        執行：認領並跑一個任務，留下 receipt
  /research-6-review     審查：用期刊審稿人的角度攻擊自己

隨時
  /research-status       我在第幾步、已經有什麼、還缺什麼

成果
  /to-plan   /to-proposal   /to-paper
```

**每一步都會主動交棒。** 跑完 `/research-1-grill`，它會告訴你這個想法已經「可研究」了、下一步是 `/research-2-brief`，然後停下來——它不會自己往下跑。收斂條件是可檢查的，不是靠你喊停：每個 stage 都有明確的 `Complete when:`，每個 stop branch 都會說明現在是什麼狀態、下一步該做什麼。

`/research-3-falsify` 刻意排在拆任務之前。理由跟 TDD 先寫失敗測試一樣：先講定什麼結果會殺死這個設計，才不會把成本投進一個無法被推翻的主張。事後才調閾值不算數。

**你只需要記住上面這幾個名字。** 另外 25 個 model-invoked primitives（文獻地圖、gap 稽核、識別設計、資料可行性、引用查核……）由 Agent 依當下瓶頸自動取用，不需要你記、也不需要你叫。

不想逐步走的話，`/research-auto` 是自動駕駛：它每輪只解決最影響下游的 frontier，並保留你排除過的領域、方法與資料限制。其餘入口見下方「其他入口」。

## 安裝到 Codex（完整 42 skills）

Research OS 是一套 **42 個 skills 的集合**，不是一個可由 repository 根網址當成單一 skill 安裝的 skill。不要對 `https://github.com/yhlai0911/research-os` 直接使用 Codex 的單一 skill GitHub 安裝器；它需要每個 skill 的內部路徑，也不具備本專案的整批 preflight 與 receipt。這條 Codex 安裝流程不需要 `.claude-plugin/plugin.json`。

### 直接交給 Codex 安裝

把下面整段貼給 Codex：

```text
請從 https://github.com/yhlai0911/research-os 安裝完整 Research OS。
這是 42 個 skills 的集合，不是單一 skill。
請 clone repository，使用 uv 執行：
1. uv sync --locked
2. uv run python scripts/install_skills.py --dry-run
3. dry-run 沒有 conflicts 才執行 uv run python scripts/install_skills.py
4. uv run python scripts/verify_install.py
不要使用單一 skill GitHub 安裝器處理 repository 根網址，
也不要尋找或建立 .claude-plugin/plugin.json。
最後讀回 .research-os-install.json，回報 source commit，
並確認結果為 INSTALL OK: 42 skills。
```

### 在終端機手動安裝

```bash
git clone https://github.com/yhlai0911/research-os.git
cd research-os
uv sync --locked
uv run python scripts/install_skills.py --dry-run
uv run python scripts/install_skills.py
uv run python scripts/verify_install.py
```

未提供 `--target` 時，安裝器會使用 `$CODEX_HOME/skills`；若未設定 `CODEX_HOME`，則使用 `~/.codex/skills`。只有刻意安裝到其他 Codex skills 目錄時才需加上 `--target /明確的/skills/路徑`。

安裝器會先完成 42 個目標的全批 preflight；任何同名 skill 內容不同時，整批停止、不覆寫，也不留下半套新安裝。成功後會寫入 `.research-os-install.json`，`verify_install.py` 會重新核對 catalog、42 個 skill 目錄、`SKILL.md`、`agents/openai.yaml`、內容 hash 與 receipt。新 skills 會在 Codex 的下一輪或新 task 載入。

第一次使用可接著閱讀 [`docs/USAGE_GUIDE.zh-TW.md`](docs/USAGE_GUIDE.zh-TW.md)。常用提示詞可直接複製自 [`docs/PROMPT_COOKBOOK.zh-TW.md`](docs/PROMPT_COOKBOOK.zh-TW.md)，遇到卡關則查閱 [`docs/TROUBLESHOOTING.zh-TW.md`](docs/TROUBLESHOOTING.zh-TW.md)。

## 安裝到 Claude Code（完整 42 skills）

Claude Code 官方支援個人 `~/.claude/skills/` 與專案 `.claude/skills/`。Research OS 會在安裝時從同一份 catalog 生成 Claude Code invocation adapter：14 個 user-only skills 加上 `disable-model-invocation: true`，25 個 model-only skills 加上 `user-invocable: false`；repository 內的 canonical `SKILL.md` 不會被改寫。這是純 skills 安裝，不需要 plugin manifest。[Claude Code 官方 skills 文件](https://code.claude.com/docs/en/skills#where-skills-live)

### 直接交給 Claude Code 安裝

把下面整段貼給 Claude Code：

```text
請從 https://github.com/yhlai0911/research-os 安裝完整 Research OS。
這是 42 個 skills 的集合，不是單一 skill。
請 clone repository，使用 uv 執行：
1. uv sync --locked
2. uv run python scripts/install_skills.py --harness claude-code --dry-run
3. dry-run 沒有 conflicts 才執行
   uv run python scripts/install_skills.py --harness claude-code
4. uv run python scripts/verify_install.py --harness claude-code
最後讀回 ~/.claude/skills/.research-os-install.json，
回報 source commit，並確認結果為 INSTALL OK: 42 skills。
```

### 在終端機安裝為個人 skills

```bash
git clone https://github.com/yhlai0911/research-os.git
cd research-os
uv sync --locked
uv run python scripts/install_skills.py --harness claude-code --dry-run
uv run python scripts/install_skills.py --harness claude-code
uv run python scripts/verify_install.py --harness claude-code
```

### 安裝到單一專案

在 Research OS repository 根目錄執行，並把目標 project 換成明確路徑：

```bash
uv run python scripts/install_skills.py \
  --harness claude-code \
  --target /absolute/path/to/project/.claude/skills \
  --dry-run
uv run python scripts/install_skills.py \
  --harness claude-code \
  --target /absolute/path/to/project/.claude/skills
uv run python scripts/verify_install.py \
  --harness claude-code \
  --target /absolute/path/to/project/.claude/skills
```

如果 `~/.claude/skills/` 或專案 `.claude/skills/` 在 Claude Code session 啟動時已存在，新增 skills 可被即時偵測；若頂層 skills 目錄是安裝時才建立，請重啟 Claude Code。可用 `/skills` 檢查清單；輸入 `/research-` 應看到主線六步依號碼排列。[Claude Code 官方 live change detection](https://code.claude.com/docs/en/skills#live-change-detection)

Claude Code 官方安裝規格、standalone skills 與 Marketplace plugin 的差異，整理於 [`docs/research/claude-code-skills-installation.md`](docs/research/claude-code-skills-installation.md)。

### 維護者驗證 repository

```bash
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

最簡單的使用方式，從主線第一步開始：

```text
/research-setup

（建立 .research/ 之後）

/research-1-grill

我想研究「生成式 AI 是否改善大學生的財務素養」，
最後要形成一份可以交給校內審查的研究計畫。
目前只有題目，沒有文獻、資料或方法。
```

它會一次問一個決策，收斂後告訴你下一步是 `/research-2-brief`。隨時可以用 `/research-status` 查看自己在第幾步。

不想逐步走的話，改用自動駕駛：

```text
/research-auto

（同樣的題目描述）
```

從 v1.1 升級請先讀 [`docs/MIGRATION-v2.md`](docs/MIGRATION-v2.md)：所有 orchestrator 都改了名稱，舊目錄需要手動移除。

端到端主流程也會在明確授權的專案範圍內自動建立這份 additive contract。`.research/` 包含研究脈絡、決策紀錄、claim ledger、研究 brief、研究計畫、workpackage、review、pilot、proposal、paper 與 handoff 的 canonical paths。

### 其他入口

主線之外的入口，都是為了特定情境而存在：

| 你的狀態 | 入口 | 會得到什麼 |
|---|---|---|
| 不想自己逐步走 | `/research-auto` | 自動駕駛：查證與追問後形成 Research Brief 及指定成果 |
| 想先判斷題目值不值得做 | `/research-triage` | `kill / repair / pilot / advance` 判決 |
| 題目大到一個 session 裝不下 | `/research-map` | 跨 session 的決策地圖，逐步散霧 |
| 要換 session 或交給別人接手 | `/research-save` | 可驗證的交接文件，不用倒轉錄檔 |
| 不知道該用哪個 | `/research-help` | 診斷現況、推薦一個入口，然後停下 |

<details>
<summary>25 個 model-invoked primitives（你不需要記，Agent 會自己取用）</summary>

文獻與定位：`literature-landscape`、`gap-audit`、`evidence-research`、`contribution-design`、`journal-fit`

理論與測量：`theory-builder`、`construct-design`、`equation-builder`、`research-domain-modeling`

設計與執行：`identification-design`、`methodology-designer`、`data-feasibility`、`design-research-three-ways`、`falsification-first`、`pilot-study`

品質與收尾：`research-review`、`research-diagnosis`、`citation-audit`、`research-writing`、`ethics-reproducibility`

系統層：`research-workspace-contract`、`artifact-reconciliation`、`research-grilling`、`synthesize-research-brief`、`render-research-deliverable`

完整說明見 [`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md)。

</details>

完整的「金融衝擊 Wave–Diffusion」案例導覽見 [`examples/financial-wave-diffusion/WALKTHROUGH.zh-TW.md`](examples/financial-wave-diffusion/WALKTHROUGH.zh-TW.md)。

### 影片教學

Repository 內附一支 4 分 01 秒的繁體中文 HyperFrames 教學影片，走完整條六步主線：從模糊題目、一次一個決策、預先反證、拆解與執行，到 Research Brief 與不同成果輸出：

- [觀看 MP4](jobs/research-os-tutorial/output/research-os-tutorial-zh-TW.mp4)
- [分鏡與重製說明](jobs/research-os-tutorial/README.md)
- [視覺 contact sheet](jobs/research-os-tutorial/snapshots/contact-sheet.jpg)

## Skill 組成

- user-invoked orchestrators：需要研究者明確啟動的長流程與產出。
- model-invoked primitives：Agent 可依任務自動取用的研究紀律。
- meta skill：維護 Research OS 本身的 skill engineering 規格。

v2.0 共 42 個 catalogued skills：16 個 orchestrators、25 個 primitives、1 個 meta skill。

完整清單由 [`skills/catalog.yaml`](skills/catalog.yaml) 單點管理，並自動生成 [`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md)。架構、invocation 與品質標準見 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) 與 [`docs/QUALITY_GATES.md`](docs/QUALITY_GATES.md)。

41 個 upstream skills 的逐檔 prompt 稽核、移植矩陣與修補紀錄見 [`docs/MATT_SKILLS_ANALYSIS.md`](docs/MATT_SKILLS_ANALYSIS.md)、[`docs/MATT_PORT_MAP.yaml`](docs/MATT_PORT_MAP.yaml) 與 [`docs/PORT_REMEDIATION.md`](docs/PORT_REMEDIATION.md)；fresh-agent 行為測試收在 [`tests/forward-evals/`](tests/forward-evals/)。

本版以 catalog 作為跨 harness source of truth：Codex 的 `agents/openai.yaml` 由 catalog 生成並機械驗證；Claude Code 則在安裝時生成對應的 `disable-model-invocation`／`user-invocable` frontmatter 並做 readback。其他 Agent harness 在沒有 generated adapter 與驗證前，不宣稱具備相同的 invocation enforcement。

從乾淨且已提交的來源建立 deterministic release：

```bash
uv run python scripts/package_release.py
```

ZIP 內含逐檔 `MANIFEST.sha256`；外部另產生 archive checksum 與指向來源 commit 的 release receipt。

## 設計邊界

- 研究者保留價值判斷與不可逆決策；Agent 自行查找可驗證事實。
- 每輪只問一個真正依賴前一答案的人類決策，並提供建議與代價；可查事實不丟回給使用者。
- 未直接查證的外部主張維持 `unverified`、`contested` 或 `blocked`。
- 找不到文獻只代表目前搜尋邊界內未找到，不等於證明「首次」或「沒人做過」。
- 公開投稿、寄信、建 issue、推送、付費資料或其他外部寫入，不會因研究流程自動獲得授權。
- 論文與 proposal 只能從已有 provenance 的研究 artifacts 草擬；缺證據不以流暢 prose 補齊。

## English summary

Research OS is a composable Agent Skill system that adaptively develops a topic, direction, equation, dataset, draft, or reviewer concern into a falsifiable Research Brief and a fit-for-purpose research plan, proposal, paper blueprint, or manuscript. It separates human decisions from discoverable facts, attacks the design before rendering it, and maintains a durable `.research/` contract for provenance and continuity.

## License and attribution

Research OS is released under the MIT License. Its design was informed by Matt Pocock’s MIT-licensed skills repository at a pinned source commit; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) and [`docs/MATT_SKILLS_ANALYSIS.md`](docs/MATT_SKILLS_ANALYSIS.md).

Version history is in [`CHANGELOG.md`](CHANGELOG.md).
