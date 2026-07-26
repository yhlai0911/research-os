# Research OS 使用教學

這份教學回答一個實際問題：當你只有一句題目或方向時，如何讓 Research OS 協助你形成一份可反駁、可執行、可審查的研究計畫、企劃案或論文藍圖。

Research OS 不是「輸入題目，立刻吐出三十頁文字」的生成器。它先找出最會影響下游的未知事項，查證可以查證的事實，只把真正需要研究者判斷的選擇交還給你。沒有證據的內容會保留為 `unverified`、`partial` 或 `blocked`，而不是用流暢文字假裝完成。

## 1. 安裝與驗證

在 repository 根目錄執行：

```bash
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

先預覽安裝目標：

```bash
uv run python scripts/install_skills.py \
  --target /absolute/path/to/skills \
  --dry-run
```

確認後再安裝：

```bash
uv run python scripts/install_skills.py \
  --target /absolute/path/to/skills
```

安裝器採 fail-closed：只要目標已有同名但內容不同的 skill，整批停止，不覆寫既有資料，也不留下半套安裝。

## 2. 用一句完整任務啟動

最穩定的起點不是只寫一個名詞，而是同時交代「主題、目的、目前狀態」：

```text
/develop-research

我想研究「生成式 AI 是否改善大學生的財務素養」，
最後要形成一份可以交給校內審查的研究計畫。
目前只有題目，沒有文獻、資料或方法。
請使用繁體中文。
```

如果你已知限制，直接寫出來：

```text
不要使用付費資料，不做高頻資料，也不希望以問卷作為唯一證據。
樣本最好能由台灣公開資料取得。
```

Research OS 會保留這些排除條件，不會在後續悄悄把被排除的方法放回來。

## 3. 它接下來會做什麼？

主流程每輪只處理一個最關鍵的 frontier：

```text
任務與目的
  → 找出最關鍵的不確定性
  → 可查的事實由 Agent 查證
  → 需要價值判斷時，一次只問一個問題
  → 記錄決策並重新計算 frontier
  → 攻擊設計、修補根因或誠實停止
  → 封裝 Research Brief
  → 轉譯為指定成果
```

例如，Agent 可能問：

> 我建議先把「改善」限定為可觀察的學習成效，而不是自陳滿意度。你希望主要結果變數是知識測驗、決策品質，還是兩者並列？若兩者並列，研究範圍與樣本數需求都會增加。

這個問題需要研究者決策；「有哪些已驗證量表」「資料是否免費」「相近研究做過什麼」則應由 Agent 查證，不應全部丟回給你。

## 4. 如何回答追問？

不需要使用學術術語。只要表達真正的偏好與限制：

```text
主要結果用知識測驗，決策品質作為次要結果。
我接受範圍縮小，優先確保識別清楚。
```

如果你不確定，可以要求建議：

```text
我沒有偏好。請根據資料可得性與審查風險替我建議，
並說明代價後直接採用你的建議。
```

如果你要改方向，明確說明新增或取代：

```text
新增限制：研究期程只有六個月。
```

或：

```text
取代前面的決定：不再限定台灣資料，改成優先使用可重現的跨國公開資料。
```

## 5. 如何選擇輸出？

### 學術研究計畫

```text
/to-research-plan

把目前已驗證的 Research Brief 轉成學術研究計畫。
受眾是校內研究審查委員，請使用財經學術散文體，
保留所有尚未解除的資料與識別限制。
```

### 企劃案或補助 proposal

```text
/to-proposal

把目前研究設計轉成校級教學創新計畫。
受眾是跨領域審查委員；需要問題、受益者、方法、
里程碑、風險、預算假設與成效評估。
尚未核准的預算與合作承諾不得寫成既定事實。
```

### 論文

```text
/to-paper-draft

依目前 artifacts 產出論文。
若尚未執行實證，請只建立 paper blueprint、理論命題、
方法與預期表格，不得虛構結果。
```

`/to-paper-draft` 不代表一定會得到一篇看似完成的 manuscript。若沒有已登錄的實證結果，正確輸出是 paper blueprint；這是證據防線，不是功能不足。

## 6. 如何讀取 `.research/`？

`.research/` 是專案的單一研究狀態，不是聊天紀錄備份。

| 位置 | 用途 |
|---|---|
| `.research/CONTEXT.md` | 研究目的、限制、詞彙及 current artifact index |
| `.research/decisions/` | 研究者已接受或仍待決的決策 |
| `.research/evidence/claims.yaml` | 主張、來源、locator 與證據狀態 |
| `.research/briefs/` | audience-neutral 的 Research Brief |
| `.research/reviews/` | 審查攻擊、嚴重度與 disposition |
| `.research/pilots/` | 小型 tracer study 與 go/no-go 結果 |
| `.research/plans/` | 學術研究計畫 |
| `.research/proposals/` | grant 或 project proposal |
| `.research/papers/` | paper blueprint 或有證據支持的 manuscript |
| `.research/workpackages/` | 可認領、可驗證、具依賴關係的工作包 |
| `.research/handoffs/` | 跨 session 交接與 readback receipt |

判讀時先看 `CONTEXT.md` 的 current pointer，再開啟它指向的 artifact。不要因資料夾中存在多個舊版本，就自行挑一份看起來最新的檔案。

## 7. 一個完整的小型示範

### 使用者

```text
/develop-research

我想研究央行升息消息如何傳到不同產業 ETF。
資料要免費，最後要寫成財金期刊論文。
```

### Research OS 應做的事

1. 記錄目的地為 paper blueprint／manuscript，並確認是否已有結果。
2. 查明事件、ETF、頻率與公開資料的真實可得性。
3. 分開「衝擊傳播」「一般共同波動」與「時區或交易時間造成的機械落後」。
4. 找最接近的 spillover、event study、network diffusion 文獻，不能因搜尋不到就宣稱首次。
5. 若研究者把物理方程帶入金融，先檢查符號、單位、機制與可拒絕限制。
6. 以反證與 pilot 檢查 wave-like 和 ordinary lagged diffusion 是否真的能由資料區分。
7. 沒有執行結果時，產出 paper blueprint，而不是撰寫虛假的實證發現。

### 可接受的結果狀態

- `complete`：指定成果存在，所有必要 gates 均有 readback。
- `partial`：已形成可用成果，但仍有不影響核心用途的限制。
- `conditional`：可繼續，但某些核心主張依賴尚未完成的查證或 pilot。
- `blocked`：目前證據不足以支持指定成果。
- `kill`：題目在現有限制下不值得繼續；這也是有效研究結果。

## 8. 使用原則

- 把 Research OS 當成研究共同設計者，不是代寫器。
- 讓 Agent 查事實；你負責價值判斷、範圍與不可逆承諾。
- 對「首次」「沒人做過」「資料一定可得」保持高度懷疑。
- 方法必須服務問題與識別，不能只因為複雜或新奇而加入。
- 研究計畫可以在證據不足時停止；停止比製造漂亮但不可執行的成果更有價值。

下一步可從 [`PROMPT_COOKBOOK.zh-TW.md`](PROMPT_COOKBOOK.zh-TW.md) 複製最符合你情境的啟動提示詞。
