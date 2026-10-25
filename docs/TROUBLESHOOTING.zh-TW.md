# Research OS 疑難排解

## 把 GitHub repository 網址交給 Codex，但安裝失敗

Research OS 是 43 個 skills 的集合，不是單一 skill。Codex 的單一 skill GitHub 安裝器收到 repository 根網址時會缺少內部 `--path`，不能代表整套安裝流程。

不要補建 `.claude-plugin/plugin.json`，也不要改用 Claude plugin 規則。請 clone repository 後執行：

```bash
uv sync --locked
uv run python scripts/install_skills.py --dry-run
uv run python scripts/install_skills.py
uv run python scripts/verify_install.py
```

預設目標是 `$CODEX_HOME/skills` 或 `~/.codex/skills`。只有 `verify_install.py` 回報 `INSTALL OK: 43 skills`，才能宣稱完整安裝。

## 看起來只安裝了一部分 skills

先執行：

```bash
uv run python scripts/verify_install.py
```

驗證器會逐一核對 catalog、43 個目錄、`SKILL.md`、`agents/openai.yaml`、內容 hash 與 `.research-os-install.json`。若出現 `INSTALL FAILED`，保留錯誤輸出；不要以手動補檔或建立 Claude plugin manifest 代替完整重裝。若目標有同名但不同內容的 skill，安裝器會列在 `conflicts` 並在寫入前整批停止。

## Claude Code 看不到 Research OS

先確認使用的是 Claude Code harness，而不是把 Codex 版本直接複製到 `~/.claude/skills/`：

```bash
uv run python scripts/verify_install.py --harness claude-code
```

個人安裝的目標應是 `~/.claude/skills/<skill-name>/SKILL.md`；專案安裝則是 `<project>/.claude/skills/<skill-name>/SKILL.md`。不要多包一層 `research-os/skills/`。

在 Claude Code 內執行 `/skills` 檢查 discovery。若頂層 `~/.claude/skills/` 或 `.claude/skills/` 是 session 啟動後才建立，請重啟 Claude Code；若目錄原本就存在，其中的 skill 檔案變更可即時偵測。user-only 入口請用 `/research-auto` 測試。

若驗證器指出 invocation metadata 錯誤，重新執行：

```bash
uv run python scripts/install_skills.py --harness claude-code
```

安裝器遇到既有不同內容會 fail closed，不會覆寫；請先判斷該 skill 是舊版 Research OS 還是使用者自有內容，不要直接刪除。

## Agent 一直問問題，沒有開始寫

先判斷問題是不是人類決策。如果資料來源、文獻或方法規格可以查證，可回覆：

```text
這是可查證事實，請自行查證並記錄來源；
只有會改變研究目的、範圍或承諾的選擇才交給我。
```

若問題確實會改變研究問題，回答它比直接要求長文更省時間。

## Agent 一次問很多題

要求回到 decision-tree discipline：

```text
請重新找出最會影響下游的一個問題，每次只問一題。
後續選項若依賴這一題，不要提前詢問。
```

## 產出被標示為 conditional 或 blocked

先看 artifact 中的 named gate。`blocked` 不是失敗文字，而是缺少哪一項證據的明確狀態。可選擇：

```text
先完成 named gate，再產出成果。
```

或：

```text
接受目前限制，產出最強的 honest partial output，
並在摘要與限制中保留 blocker。
```

## 想直接得到完整論文，但系統只給 paper blueprint

確認是否已有可讀取的真實結果、表格、程式執行 receipt 與資料 provenance。沒有結果時拒絕撰寫「結果章」是正確行為。完成 workpackages 或提供已執行成果後再使用 `/to-paper`。

## 系統宣稱題目是首次

要求執行 `$gap-audit`，並把主張改成可稽核形式：

```text
不得以「目前沒找到」推論「首次」。
請列出搜尋邊界、closest work、資料庫、查詢式、日期與未覆蓋範圍。
```

## `.research/` 有兩份互相矛盾的 artifact

不要手動刪除其中一份。使用：

```text
請使用 $artifact-reconciliation，
保留兩份 lineage，建立 superseding artifact，
並驗證 Artifact index 只有一個 current pointer。
```

## 修改後又出現被排除的方法

指出這是既有決策，不是新偏好：

```text
這違反已記錄的 exclusion。請讀回相關 decision record，
移除受影響內容，並重新計算 frontier。
```

## Skill 沒有被觸發

若使用 Codex，先執行 `uv run python scripts/verify_install.py`；若使用 Claude Code，則執行 `uv run python scripts/verify_install.py --harness claude-code`。確認完整安裝後，再明確呼叫：

```text
/research-auto
```

或在支援 `$skill-name` 的環境中：

```text
Use $research-auto to ...
```

不同 Agent harness 若沒有對應 adapter，不能假設具備相同的 implicit/user invocation enforcement。

## Repository 驗證失敗

依序執行：

```bash
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

先修第一個失敗 gate，再重跑全部 gates。不要只修改輸出的錯誤文字或略過驗證。

## Codex 看不到研究助理，但安裝顯示成功

先以同一 source checkout、harness、target 驗證，核對 receipt 的來源 commit，再確認目前開的是該研究專案。專案技能應在其 `.agents/skills/<name>/SKILL.md`，不是多包一層 repo；多份同名技能先查來源，不一律刪除。依宿主支援方式重整清單／重新開任務。`INSTALL OK`、完整規範讀取、原生 discovery/loading/invocation 是不同層次，不能互相代替，也不能僅憑選單缺項猜原因。[官方位置說明](https://developers.openai.com/codex/build-skills)

## 研究助理只報技能名稱，沒有推進

先確認委託範圍與前置。要求助理說明選路理由，將真實輸入交給適用 skill，由該 skill 完成義務，再讀回產物、判斷與下一門檻。缺必要研究決策就先問；不是每步都要求新手背名稱，也不能把一句推薦重標成執行。見[研究助理入門](RESEARCH_ASSISTANT.zh-TW.md)。

## HTML 連結打不開，或論文只有 HTML／Word PDF

核對產物是否生成、連結是否指向同版檔案，以及它是本機還是跨裝置交付。不要編造網址或用後製按鈕假裝點擊。正式論文仍需可編輯 LaTeX、Bib、實際編譯 PDF 與當版 QA；缺引擎、Biber 或字型要回報缺項，不能把來源稿或 Word 轉檔稱為通過。見[交付與依賴](DELIVERABLES.zh-TW.md)。

## Windows 的 symlink／release 測試失敗

一般使用選預設 copy 安裝。symlink 權限與 release 所需 POSIX 安全原語是不同問題；不要為測試全綠調整 ACL、關閉保護或略過檢查。Windows 失敗與支援平台 CI 分開回報；release 限制見[品質關卡](QUALITY_GATES.md)。
