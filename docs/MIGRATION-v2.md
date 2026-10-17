# 從 v1.1 升級到 v2.0

v2.0 將 v1.1 原有 13 個 user-invoked orchestrators 中的 12 個重新命名，保留 `to-proposal`，並新增三個 orchestrators，合計 16 個。這是 **breaking change**：已改名的 12 個舊名稱不再提供，也沒有別名。

工作區格式沒有改變。既有的 `.research/` 目錄、`config.yaml`、claim registry、Artifact index 與所有既有 artifacts **完全相容**，不需要遷移。25 個 model-invoked primitives 的名稱也維持不變。

## 名稱對照

| v1.1 | v2.0 | 說明 |
|---|---|---|
| `setup-research-os` | `research-setup` | |
| `grill-research-idea` | `research-1-grill` | 主線第 1 步 |
| `to-research-brief` | `research-2-brief` | 主線第 2 步 |
| — | `research-3-falsify` | **新增**，主線第 3 步 |
| `to-workpackages` | `research-4-tasks` | 主線第 4 步 |
| `execute-workpackage` | `research-5-run` | 主線第 5 步 |
| — | `research-6-review` | **新增**，主線第 6 步 |
| — | `research-status` | **新增**，隨時檢視進度 |
| `to-research-plan` | `to-plan` | |
| `to-proposal` | `to-proposal` | 未變更 |
| `to-paper-draft` | `to-paper` | |
| `develop-research` | `research-auto` | |
| `idea-triage` | `research-triage` | |
| `research-wayfinder` | `research-map` | |
| `research-handoff` | `research-save` | |
| `ask-research` | `research-help` | |

## 新增的三個 skill

- **`research-3-falsify`** — `falsification-first` 的顯性入口。v1.1 只有在 `develop-research` 內部才會觸發反證，使用者無法單獨要求「先想清楚什麼會推翻我」。它刻意排在拆任務之前。
- **`research-6-review`** — `research-review` primitive 的 user-invoked wrapper。名稱帶編號是必要的：安裝後的 skill 目錄是扁平的，`research-review` 這個名字已由 primitive 佔用。
- **`research-status`** — 唯讀。讀取 Artifact index、claim registry 與 workpackage 索引，回報「在第幾步／已有什麼／缺什麼／下一步」。v1.1 的累積狀態只有 Agent 讀得到，使用者沒有入口。

## 升級步驟

安裝器**不會**自動移除舊名稱的目錄。舊 skill 會留在原地並繼續被 harness 載入，造成新舊並存。先刪除再安裝：

### Claude Code

```bash
cd /path/to/research-os
git pull
uv sync --locked

# 1. 移除 v1.1 已改名的 12 個舊 skill 目錄（先備份自訂內容）
cd ~/.claude/skills
rm -rf setup-research-os grill-research-idea to-research-brief \
       to-workpackages execute-workpackage to-research-plan \
       to-paper-draft develop-research idea-triage \
       research-wayfinder research-handoff ask-research

# 2. 安裝 v2.0
cd /path/to/research-os
uv run python scripts/install_skills.py --harness claude-code --dry-run
uv run python scripts/install_skills.py --harness claude-code
uv run python scripts/verify_install.py --harness claude-code
```

### Codex

同上，但目標目錄是 `$CODEX_HOME/skills` 或 `~/.codex/skills`，且三個指令都不加 `--harness`。

驗證結果應為 `INSTALL OK: 42 skills`。

`.research-os-install.json` 會被 v2.0 的 receipt 覆寫；若 dry-run 回報 conflicts，先處理 conflicts 再安裝，不要強制覆寫。

## 其他變更

- **簿記契約收攏為單一來源**：workspace resolution 程序、Artifact index 契約與三個 index 狀態，現在只定義在 `skills/primitives/research-workspace-contract/references/writeback-protocol.md`。其他 skill 以連結引用，不再各自複述。
- **驗證器規則變更**：`validate_repository.py` 從「每個 SKILL.md 內文必須含 Artifact index 表頭字串」改為「必須連結至 writeback protocol」。撰寫新 skill 時請加上該連結，不要複製表頭。
- **主線 skill 會主動交棒**：達成完成條件時，會明確告知下一步 skill 名稱後停止；它們仍然不會自行呼叫另一個 user-invoked skill。

## 教學影片

`jobs/research-os-tutorial/` 已完整重製為 v2：八段旁白全部重錄、腳本改以六步主線敘事、字幕重寫、時間軸依新音長重算（2 分 50 秒 → 4 分 01 秒）。

旁白刻意不再唸出任何 skill 名稱。v1 第三段直接唸「develop research」，skill 一改名影片就錯了；只講「第幾步」可以撐過往後的改名。

重製流程是可重現的，兩個腳本各自守住一個容易犯的錯：

```bash
cd jobs/research-os-tutorial
uv run python scripts/regen_voice.py --all   # 換 voice 時拒絕只重錄單段
uv run python scripts/retime.py              # 由 audio_meta.json 推算全部時間軸
npm run check && npm run render
```

需要 `.env` 內的 `ELEVENLABS_API_KEY`（必須具備 `text_to_speech` 權限）與 `ELEVENLABS_VOICE_ID`。輸出格式固定 `mp3_44100_128` 再本地解碼；`pcm_44100` 需要 Pro 方案，而 22 kHz／24 kHz 格式會被迫上採樣。
