# Research OS

Research OS 是一套可組合的 Agent Skills，用來把一個主題、方向、方程式、現象、資料、草稿或審查意見，透過自適應對話推進成可反駁、可執行、可審查的研究計畫、企劃案或論文。它不把「寫出很多字」當作完成；它會主動查證文獻與資料、區分研究者決策和可查事實、模擬審查攻擊、修補根因，再把已驗證狀態封裝成單一 Research Brief，最後依目的轉譯成所需成果。

本專案深層研究了 [Matt Pocock Skills](https://github.com/mattpocock/skills) 的完整 skill 架構與提示詞設計，但沒有逐句移植。Research OS 保留其最有效的底層原則：router 與 primitive 分工、leading concept、可檢查的 completion criterion、progressive disclosure、single source of truth、真實 feedback loop；並補上學術研究需要的 claim-evidence ledger、counterfactual、falsification、資料可得性、倫理、重現性與交接 receipt。

## 主要入口

```text
使用者的任意起點
  → /develop-research
  → 找出目前最關鍵的不確定性
  → 查事實或一次詢問一個必要決策
  → 文獻／gap／理論／識別／資料／方法（只走需要的分支）
  → 反證與審查攻擊
  → 根因修補或誠實停止
  → canonical Research Brief
  → 研究計畫／企劃案／proposal／paper blueprint／論文草稿
```

`/develop-research` 是端到端主流程，不會強迫每個題目走同一份 checklist。它每輪只解決最會影響下游的 frontier，並保留使用者排除過的領域、方法與資料限制。只想選擇工作流時用 `/ask-research`；大型跨 session 計畫可用 `/research-wayfinder`；已拆解的實作工作可用 `/execute-workpackage` 原子認領並留下 receipt；canonical artifacts 衝突時由 `artifact-reconciliation` 保留雙方 lineage、建立 superseding artifact，並驗證唯一 current pointer；其餘 orchestrators 是明確的快捷入口。

## 快速開始

驗證 repository：

```bash
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

安裝到一個新的 Agent Skills 目錄：

```bash
uv run python scripts/install_skills.py \
  --target /absolute/path/to/skills \
  --dry-run

uv run python scripts/install_skills.py \
  --target /absolute/path/to/skills
```

安裝器會先完成全目標 preflight；任何既有 skill 內容不同時，整批停止、不覆寫、也不留下半套新安裝。

最簡單的使用方式：

```text
/develop-research

我有一個主題或方向，希望最後形成一份研究計畫／企劃案／論文。
```

若只想先建立持久工作區，可執行：

```text
/setup-research-os
```

端到端主流程也會在明確授權的專案範圍內自動建立這份 additive contract。`.research/` 包含研究脈絡、決策紀錄、claim ledger、研究 brief、研究計畫、workpackage、review、pilot、proposal、paper 與 handoff 的 canonical paths。

## Skill 組成

- user-invoked orchestrators：需要研究者明確啟動的長流程與產出。
- model-invoked primitives：Agent 可依任務自動取用的研究紀律。
- meta skill：維護 Research OS 本身的 skill engineering 規格。

v1.0 共 39 個 catalogued skills：13 個 orchestrators、25 個 primitives、1 個 meta skill。

完整清單由 [`skills/catalog.yaml`](skills/catalog.yaml) 單點管理，並自動生成 [`docs/SKILL_CATALOG.md`](docs/SKILL_CATALOG.md)。架構、invocation 與品質標準見 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) 與 [`docs/QUALITY_GATES.md`](docs/QUALITY_GATES.md)。

41 個 upstream skills 的逐檔 prompt 稽核、移植矩陣與修補紀錄見 [`docs/MATT_SKILLS_ANALYSIS.md`](docs/MATT_SKILLS_ANALYSIS.md)、[`docs/MATT_PORT_MAP.yaml`](docs/MATT_PORT_MAP.yaml) 與 [`docs/PORT_REMEDIATION.md`](docs/PORT_REMEDIATION.md)；fresh-agent 行為測試收在 [`tests/forward-evals/`](tests/forward-evals/)。

本版是 **Codex-first** distribution：`agents/openai.yaml` 的 user/model invocation policy 由 catalog 生成並機械驗證。核心 `SKILL.md` 可供其他 Agent harness 參考，但 Claude、Cursor 或其他平台在沒有對應 generated adapter 與驗證前，不宣稱具備相同的 invocation enforcement。

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
