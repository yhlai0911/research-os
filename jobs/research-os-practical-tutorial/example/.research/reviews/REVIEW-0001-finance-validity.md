# Research Review: 財金領域效度檢查（0050 日內幅度 × 成交股數）

- ID: REVIEW-0001
- Status: complete（審查本身完成；domain verdict 見 Verdict）
- Updated: 2026-10-17
- Target artifact and version: BRIEF-0001 v0.1（sha256 前 16 碼 ceead8c84bd9fc49）
- Sources: RDR-0001, C-001, C-002, C-003, .research/CONTEXT.md, .research/config.yaml
- Reviewer lenses: research-finance-social-science › validity-checks.md「Finance and market data」「Quantitative social science（只用描述性 vs 因果的區分）」「Reproducibility」
- 限制：本回合只審查現有材料，沒有新的外部資料收集，沒有跑任何統計。

## Material reviewed

- **範圍**：問題是 0050 在 2024Q1 日內幅度代理與同日成交股數的單調關聯。
- **主張類型**：描述性關聯，不是預測，也不是因果。
- **分析單位**：交易日。
- **母體**：0050 單一證券。
- **期間**：2024-01 到 2024-03，候選 N=56。
- **目標**：描述 Spearman 等級相關（尚未執行）。
- **已確認的輸入**：C-001、C-002、RDR-0001 的決定。
- **未知**：C-003、ET-2、ET-3，以及下文 F2、F3。

## Contribution and theory

不宣稱貢獻，也不檢定機制，與 Brief 一致。沒有發現新穎性的過度宣稱。

## Identification

描述性設計，不要求因果識別。Brief 已排除因果、預測和投資用語，沒有發現超出識別能力的用語。

## Measurement and data

1. **命名**：「日內幅度代理」的命名恰當，也避開了「波動率」。不過 (H−L)/C 量到的是當日最高、最低成交價形成的區間。它是否只反映一般盤，取決於 F2。
2. **口徑錯配（F2，未知）**：
   - 官方 notes 說成交量統計含一般、零股、盤後定價、鉅額交易（C-002）。
   - 但 OHLC 是否同樣包含零股、盤後、鉅額的成交價，**未查證**。
   - 若價格只來自一般盤、量卻是合併口徑，兩邊的口徑就不一致。
3. **公司行動（F1，未知）**：
   - 註記欄全空，依 notes 只表示沒有「變更面額或分割、反分割恢復買賣」的標記。
   - **不能推出沒有除息**，C-003 維持 unverified。
   - 推論（未驗證）：同日的 (H−L)/C 不使用前一日價格，除息造成的跳空對它的機械影響可能有限。但除息日的成交量仍可能異常，所以必須核對。
4. **單位（F4）**：
   - 欄位名是「成交股數」，單位推定是股。
   - 原始值是帶千分位逗號的字串，需要明訂轉換規則。
   - 價格是未調整原始值（C-001）。
   - 若之後重新擷取時官方回溯調整歷史值，資料就會不同。這點未查證，所以需要快照（F5）。
5. **特殊日（F3）**：
   - 已知：2 月只有 13 個交易日（C-001 的計數）。
   - 未知：農曆年前後的封關、開紅盤，以及任何非正常交易日，ET-3 未核對。
   - 可能的影響：這些日子的量與價格區間可能結構性偏離其他日子。

## Evidence and citations

Brief 沒有引用任何文獻，符合要求。ET-2 仍未完成，完成前不得補上引用。

## Execution and reproducibility

- **F5**：原始 JSON 沒有快照與雜湊，只記錄了端點和擷取日期。重新擷取時不能保證得到相同資料。
- **F6（推論邊界）**：
  - N=56，是單一證券、單一季，兩個序列都可能有自我相關。
  - 若報告 Spearman 的 p 值，「獨立觀測」的假設可能不成立。
  - Brief 沒有預先決定是否報告顯著性。
  - 結論只能是這段樣本的描述，不能推廣到其他期間。

## Verdict

**repair**。

- 設計方向健全，用語邊界正確。
- 但 F1、F2、F5 有具體補救方法，必須在執行前完成。
- F6 需要使用者事前決定。
- 這不代表任何發現為真，也還沒有任何發現。

## Required repairs

| Priority | Finding | Evidence | Required repair | Stop condition | Recheck |
|---|---|---|---|---|---|
| P1 | F1 公司行動未知；註記欄空白≠無除息 | C-002 notes、C-003 unverified | 查官方除息與公司行動公告（ET-1），標出受影響日期 | 查不到可信的官方來源：維持 blocked，不得執行 | C-003 改為 verified 或 contested |
| P1 | F2 OHLC 與合併量的口徑可能錯配 | C-002（只說明量的口徑） | 查 TWSE 對 STOCK_DAY 價格欄的定義；若無法確認，在 Brief 寫成明示的限制 | 確認口徑不同而且無法說明：回 research-2-brief 修改構念 | 新增 claim 並驗證 |
| P1 | F5 沒有資料快照與雜湊 | C-001 只記錄端點與日期 | 保存三份原始 JSON 與 sha256、擷取時間 | 快照與日後重抓不一致：停止並記錄差異 | 雜湊回讀 |
| P2 | F3 特殊交易日未核對 | 2 月 13 日（C-001） | 核對 ET-3；事前決定這些日子保留或標記（建議全部保留並標記，不刪除） | 規則在看到數據之後才定：視為事後探索 | Brief 的規則段落 |
| P2 | F6 N=56、自我相關、顯著性的處理沒有事前決定 | RDR-0001 | 事前決定只報告 ρ 的描述，或附上考慮相依性的不確定性 | 看完結果才選呈現方式：標為 exploratory | DECISIONS 新增紀錄 |
| P3 | F4 單位與字串轉換規則沒有明訂 | C-001 欄位名 | 在方法中寫明：去掉逗號後轉成整數股；價格保留原始值 | 解析失敗率超過 5%：觸發既有門檻 | 腳本回讀 |

## Unresolved decisions

- **OD-3（F6）**：是否報告 p 值或信賴區間。建議只報告 ρ 和散佈圖作為樣本描述，不做顯著性主張。代價是學生看不到推論練習。
- **OD-4（F3）**：特殊日的處理規則。

## Next step

- 先由模型可調用的證據 primitive（evidence-research 或 data-feasibility）完成 P1 的 F1、F2、F5。
- 之後的核心入口建議是 **research-3-falsify**，用來定義描述性結論的失敗條件，並一起處理 OD-3、OD-4。
- 本審查不自動呼叫任何 skill。

## Readback

- Reviewed version unchanged: yes（審查前後 sha256 前 16 碼均為 ceead8c84bd9fc49）
- Report references resolve: RDR-0001, C-001, C-002, C-003, BRIEF-0001
- Final status: complete（domain verdict: repair）
