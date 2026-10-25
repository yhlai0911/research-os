# Research OS 使用教學

這份教學回答一個實際問題：當你只有一句題目或方向時，如何讓 Research OS 協助你形成一份可反駁、可執行、可審查的研究計畫、企劃案或論文藍圖。

Research OS 不是「輸入題目，立刻吐出三十頁文字」的生成器。它先找出最會影響下游的未知事項，查證可以查證的事實，只把真正需要研究者判斷的選擇交還給你。沒有證據的內容會保留為 `unverified`、`partial` 或 `blocked`，而不是用流暢文字假裝完成。

## 1. 安裝與驗證

Research OS 是 43 個 skills 的套件，不是單一 skill。Codex 的單一 skill GitHub 安裝器不能只靠 repository 根網址安裝整套 Research OS；請先 clone repository，再使用本專案的 catalog-driven 安裝器。這個流程不使用 Claude plugin，也不需要 `.claude-plugin/plugin.json`。

直接把下面整段交給 Codex 即可：

```text
請從 https://github.com/yhlai0911/research-os 安裝完整 Research OS。
這是 43 個 skills 的集合，不是單一 skill。
請 clone repository，以 uv 執行 install_skills.py 的 dry-run 與正式安裝，
再執行 verify_install.py；遇到任何 conflict 必須停止，不得覆寫。
不要使用單一 skill GitHub 安裝器處理 repository 根網址，
也不要尋找或建立 .claude-plugin/plugin.json。
完成時必須回報 source commit 與 INSTALL OK: 43 skills。
```

若要在終端機手動安裝：

```bash
git clone https://github.com/yhlai0911/research-os.git
cd research-os
uv sync --locked
uv run python scripts/install_skills.py --dry-run
uv run python scripts/install_skills.py
uv run python scripts/verify_install.py
```

預設安裝目標是 `$CODEX_HOME/skills`；若未設定 `CODEX_HOME`，則是 `~/.codex/skills`。只有需要非預設位置時才明確指定：

```bash
uv run python scripts/install_skills.py \
  --target /absolute/path/to/skills \
  --dry-run
uv run python scripts/install_skills.py \
  --target /absolute/path/to/skills
uv run python scripts/verify_install.py \
  --target /absolute/path/to/skills
```

安裝器採 fail-closed：只要目標已有同名但內容不同的 skill，43 個 skills 整批停止，不覆寫既有資料，也不留下半套安裝。複製安裝會調整共享規範的相對連結並逐項讀取檢查。`INSTALL OK: 43 skills` 代表檔案與相依驗證通過，仍須在正確專案確認 Codex 是否發現、載入並實際呼叫技能，不能只憑此訊息宣稱實操成功。

**本地分支注意：**本分支已將 `research-assistant` 納入 43 個核心技能。上面的公開網址不代表公開主線已有這項更新；試作請用此 checkout，並明確指定乾淨測試專案的 `.agents/skills`，不安裝到全域或覆寫既有副本。

### Claude Code

Claude Code 個人 skills 的官方位置是 `~/.claude/skills/`，專案 skills 則是 `<project>/.claude/skills/`。請使用同一個安裝器的 Claude Code harness，讓 catalog 自動生成正確的 invocation metadata，不要直接複製未轉換的來源目錄：

```bash
git clone https://github.com/yhlai0911/research-os.git
cd research-os
uv sync --locked
uv run python scripts/install_skills.py --harness claude-code --dry-run
uv run python scripts/install_skills.py --harness claude-code
uv run python scripts/verify_install.py --harness claude-code
```

這會將完整 43 skills 安裝到 `~/.claude/skills/`。若只供一個專案使用，三個 install／verify commands 都加上：

```bash
--target /absolute/path/to/project/.claude/skills
```

安裝器會為 user-only skills 生成 `disable-model-invocation: true`，為 model-only skills 生成 `user-invocable: false`，但不修改 repository 來源。驗證成功後，用 Claude Code 的 `/skills` 檢查清單；輸入 `/research-` 應看到主線六步依號碼排列。若頂層 skills 目錄在目前 session 啟動後才建立，需重啟 Claude Code；已存在的 skills 目錄則支援即時偵測。詳見 [Claude Code 官方 skills 文件](https://code.claude.com/docs/en/skills)。

維護者若要驗證 repository 本身，再執行：

```bash
uv sync --locked --all-groups
uv run python scripts/sync_catalog.py --check
uv run python scripts/validate_repository.py
uv run pytest
```

## 2. 先叫研究助理，再選主線節奏

在 Codex 開啟你的研究專案，輸入：

```text
$research-assistant
我是新手。請先讀目前的研究問題、資料和成果，
解釋卡在哪裡，建議下一步；目前先不要改檔。
```

它負責選擇與交接適用skill，由接收skill執行研究，再讀回產出帶你往下；不需要先知道每個技能名稱。完全沒題目也可以直接說「我想寫論文，但完全沒有題目，應該從哪裡開始？」。助理會帶到`research-1-grill`，由grill先釐清背景與興趣，不預選資料或方法。詳見[一頁新手說明](RESEARCH_ASSISTANT.zh-TW.md)。

**技能主線**——助理可以依研究委託與完成條件帶你銜接；若偏好自行呼叫，也保留以下入口：

```text
/research-setup        建立 .research/ 工作區（一次性）
/research-1-grill      逼問：把模糊想法問成可研究的問題
/research-2-brief      鎖定：把討論收斂成一份研究契約
/research-3-falsify    找碴：先講清楚什麼結果會推翻你
/research-4-tasks      拆解：切成可獨立驗證的研究任務
/research-5-run        執行：認領並跑一個任務
/research-6-review     審查：用審稿人的角度攻擊自己
```

任何時候都可以用 `/research-status` 查看自己在第幾步、已經有什麼、還缺什麼。

**逐步導引**——由助理辨認階段與前置，交接給接收skill完成工作；每次讀回真實產物後再決定下一步。重要研究選擇仍詢問你，沒有回答就不假裝通過。`research-auto`是可另行明確選用的整合流程，不是新手使用助理的必要前提。

## 3. 用一句完整任務啟動

不論走哪條路，最穩定的起點不是只寫一個名詞，而是同時交代「主題、目的、目前狀態」：

```text
/research-1-grill

我想研究「生成式 AI 是否改善大學生的財務素養」，
最後要形成一份可以交給校內審查的研究計畫。
目前只有題目，沒有文獻、資料或方法。
請使用繁體中文。
```

把 `/research-1-grill` 換成 `/research-auto`，同一段描述也適用於自動駕駛。

如果你已知限制，直接寫出來：

```text
不要使用付費資料，不做高頻資料，也不希望以問卷作為唯一證據。
樣本最好能由台灣公開資料取得。
```

Research OS 會保留這些排除條件，不會在後續悄悄把被排除的方法放回來。

## 4. 它接下來會做什麼？

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

## 5. 如何回答追問？

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

## 6. 如何選擇輸出？

### 學術研究計畫

```text
/to-plan

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
/to-paper

依目前 artifacts 產出論文。
若尚未執行實證，請只建立 paper blueprint、理論命題、
方法與預期表格，不得虛構結果。
```

`/to-paper` 不代表一定會得到一篇看似完成的 manuscript。若沒有已登錄的實證結果，正確輸出是 paper blueprint；這是證據防線，不是功能不足。

## 7. 如何讀取 `.research/`？

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

## 8. 一個完整的小型示範

### 使用者

```text
/research-auto

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

## 9. 使用原則

- 把 Research OS 當成研究共同設計者，不是代寫器。
- 讓 Agent 查事實；你負責價值判斷、範圍與不可逆承諾。
- 對「首次」「沒人做過」「資料一定可得」保持高度懷疑。
- 方法必須服務問題與識別，不能只因為複雜或新奇而加入。
- 研究計畫可以在證據不足時停止；停止比製造漂亮但不可執行的成果更有價值。

下一步可從 [`PROMPT_COOKBOOK.zh-TW.md`](PROMPT_COOKBOOK.zh-TW.md) 複製最符合你情境的啟動提示詞。
