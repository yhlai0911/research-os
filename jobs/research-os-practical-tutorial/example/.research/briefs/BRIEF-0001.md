# Research Brief: 0050 日內幅度代理與同日成交股數的描述性單調關聯

- ID: BRIEF-0001
- Status: conditional（研究設計草稿；尚未執行任何統計分析）
- Version: 0.2
- Updated: 2026-10-17
- Decision records: RDR-0001（proposed；grill 為 partial，尚未達 researchable）
- Claim IDs: C-001 (verified), C-002 (verified), C-003 (unverified), C-004 (verified), C-005 (unverified), C-006 (unverified), C-007 (unverified)
- Change log: v0.2 依 REVIEW-0001（審查對象是 v0.1）修改，處理 F2、F4、F5、F6、F3 規則；v0.2 尚未重審。
- Inputs: .research/CONTEXT.md, RDR-0001, .research/evidence/claims.yaml, REVIEW-0001, .research/evidence/raw/MANIFEST.md。

## Research question

描述 0050 在 2024 年第一季，日內幅度與同日成交股數的單調關聯。〔accepted decision: RDR-0001〕

## Why the answer matters

這是課堂研究設計示範，用來說明如何把「波動與量」從口語概念轉成可重現、範圍有限的描述性設計。範例本身不支援任何決策或投資推論。〔accepted decision〕

## Closest literature and contribution delta

- 近似文獻：**blocker**，屬證據任務 ET-2，尚未查證，本 Brief 不引用任何文獻。
- 貢獻：不宣稱新穎性。只做教學性的描述性重現，不主張學術貢獻增量。〔accepted decision: RDR-0001 非目標〕

## Mechanism and rival explanations

- 本研究不檢定機制。〔accepted decision〕
- 解讀時須記錄的混淆來源〔explicit assumption，未驗證〕：
  - 機械共變：成交越多，價格區間可能越大。
  - 鉅額交易可能讓單日量暴增，但價格區間未必跟著變（C-002 口徑）。
  - 公司行動或特殊交易日可能扭曲單日價格區間（ET-1、ET-3）。

## Constructs, estimand, and hypotheses

- **日內幅度代理** =（最高價−最低價）/收盤價。不是完整波動率，也不涵蓋隔夜跳空（前收到今開）；不估 GARCH，也不加日報酬對照。〔RDR-0001〕
- **成交股數**：TWSE 合併口徑，包含一般、零股、盤後定價、鉅額交易，不得稱為「僅一般盤量」。單位：去掉逗號後轉成整數「股」（不是張）；價格維持原始欄位。〔RDR-0001, OD-2; C-002; C-004〕
- **明示限制（F2）**：開高低收是否與合併量口徑相同，**未查證**（C-005）。價量口徑可能不一致，在查清前，任何解讀都必須附上這項限制。
- 單位與樣本：交易日；0050；2024Q1，候選 N=56。〔C-001〕
- 估計目標：同日單調關聯的描述（Spearman 等級相關），不設方向性假說。〔RDR-0001〕

## Data and identification

- **來源**：TWSE STOCK_DAY JSON，`stockNo=0050`，`date=20240101/20240201/20240301`。三個月都回傳 stat=OK，價格為未調整原始值。〔C-001〕
- **資料品質**：56 列的註記欄全空，必要欄位無缺值。〔C-002〕
- **快照**：三份原始 JSON 已存於 `.research/evidence/raw/`，sha256、UTC 擷取時間與列數見 MANIFEST（C-004）。
- **授權**：重現與再發布授權**未核對**（C-006），快照不得發布。
- **公司行動與特殊交易日**：**未核對**（C-003、C-007）。註記欄全空不代表沒有除息。
- **識別**：沒有識別策略，所以不能做因果解讀。只能描述同日共同變動，不能說明方向、時序或因果。〔RDR-0001〕

## Methods and baselines

- 候選方法：散佈圖（成交股數可取 log，只用於視覺化）與 Spearman 等級相關。
- 只報 Spearman ρ 與散佈圖，作為這 56 日樣本的描述；不報 p 值或信賴區間，不做顯著性或母體推論（OD-3）。
- 特殊日全部保留並在核對後標記，不得看完結果再刪除；敏感性分析只能事前規劃，並標明未執行（OD-4）。
- 不設基準模型。
- **以上全部尚未執行**，也沒有任何數值結果。〔accepted decision〕

## Falsifiers and kill criteria

事前停止門檻（教學用的事前選擇，不是經驗證的統計標準）〔RDR-0001〕：

- 有效交易日 < 40，或任一必要欄位缺失 > 5%：停止並說明。
- ET-1 或 ET-3 若發現會扭曲價格區間的日子，須在執行前另外決定處理規則；在此之前不得執行。
- 描述性結論本身的失敗條件尚未定義，交給 research-3-falsify 處理。〔blocker〕

## Ethics and reproducibility

- 只用免費公開的市場彙總資料，不涉及個人資料。
- 重現所需資訊：三個 GET 端點與擷取日期 2026-10-17（C-001）。
- 原始回應已保存成快照並附雜湊（C-004）；尚未寫成可執行的處理腳本。

## Scope and exclusions

不能主張的事情：
- 因果關係；
- 領先或預測；
- 投資建議；
- 新穎貢獻；
- 外推到其他 ETF 或期間；
- 「完整波動率」；
- 「僅一般盤量」；
- 顯著性或母體推論；
- 任何實證結果（本 Brief 沒有任何實證結果）。

## Open decisions

證據任務：
- ET-1：2024Q1 的除息或其他公司行動日（C-003, unverified）
- ET-2：近似文獻（未查證）
- ET-3：特殊交易日（未核對）

- C-005：價量口徑（F2）
- C-006：再發布授權

已決：OD-3、OD-4（RDR-0001）。另有一項待定：描述性結論的失敗條件。

## Acceptance

- Owner: 示範研究者（教學角色，不代表使用者本人的研究承諾）
- Accepted at: 未接受（conditional 草稿）
- Readback: 2026-10-17（v0.2）
- Readiness rationale: 研究句、構念、口徑、方法與停止門檻都已有決策或查證來源。v0.2 修復了 F4、F5、F6 和 F3 的規則，但 ET-1、ET-3 在執行前必須完成，F2 只是改寫成限制，v0.2 也尚未重審，ET-2 未完成前不得引用文獻，失敗條件也還沒定義，因此是 conditional，不是 ready。
