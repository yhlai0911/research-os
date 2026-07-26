# Research OS 疑難排解

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

確認是否已有可讀取的真實結果、表格、程式執行 receipt 與資料 provenance。沒有結果時拒絕撰寫「結果章」是正確行為。完成 workpackages 或提供已執行成果後再使用 `/to-paper-draft`。

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

本版是 Codex-first distribution。先確認安裝位置與 `agents/openai.yaml` 存在，再明確呼叫：

```text
/develop-research
```

或在支援 `$skill-name` 的環境中：

```text
Use $develop-research to ...
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
