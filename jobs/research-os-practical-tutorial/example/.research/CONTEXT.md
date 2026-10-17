# Research Context

## Mission

為財金大學生做一份課堂研究設計 Research Brief：描述 0050 ETF 的「波動」與成交量之間的關聯（不涉因果，也不是投資建議）。

## Artifact index

This table is the single registry of current research artifacts and task outcomes. Use `complete`, `partial`, or `blocked` for current rows and `superseded` only when `Supersedes` or a replacement row preserves the chain. Claim-only tasks list their affected claim IDs in the artifact-ID column.

| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |
|---|---|---|---|---|---|
| review | 財金效度檢查 BRIEF-0001 | REVIEW-0001 | complete | 2026-10-17 | — |
| evidence | 2024Q1 原始快照 | C-004 | complete | 2026-10-17 | — |
| brief | 0050 日內幅度與成交股數 | BRIEF-0001 (v0.2) | partial | 2026-10-17 | BRIEF-0001 v0.1 |
| grill | 0050 波動與成交量 | RDR-0001; C-001, C-002, C-003 | partial | 2026-10-17 | — |
| setup | research-workspace-contract | .research/config.yaml | complete | 2026-10-17 | — |

## Research question

描述 0050 在 2024 年第一季，日內幅度與同日成交股數的單調關聯（RDR-0001）。

## Unit of analysis and scope

交易日；0050；2024Q1（候選 N=56，見 C-001、C-002）。不外推到其他 ETF 或期間。

## Constructs and measures

| Construct | Meaning | Proposed measure | Status |
|---|---|---|---|
| 日內幅度代理 | 單日價格區間相對收盤價 | (最高−最低)/收盤 | decided（RDR-0001） |
| 成交量 | 同日成交股數 | 成交股數（合併口徑：一般＋零股＋盤後定價＋鉅額；log 僅用於視覺化） | decided（RDR-0001, OD-2） |

## Mechanism and rival explanations

Unresolved.

## Estimand or prediction target

描述性：同日單調關聯（Spearman 等級相關，候選方法）。不做因果、不做預測。

## Data and timing

TWSE STOCK_DAY（免費、官方），見 C-001。原始快照存於 .research/evidence/raw/（C-004）；再發布授權未核對（C-006）。單位：股（不是張）。

## Identification

Unresolved.

## Contribution claim

Unresolved.

## Constraints and exclusions

- 已授權的教學實操案例；僅在本隔離專案內操作（2026-10-17 使用者指示）。
- 只能用免費公開資料；本階段不跑統計、不寫實證結果。
- 尚無研究資料、結果或文獻；不得虛構。
- 不讀金鑰／認證／私有檔案，不修改專案外檔案，不對外發送、上傳、發布、購買或推送。

## Glossary

| Canonical term | Definition | Avoid |
|---|---|---|

## Open decisions

- OD-1 已決（RDR-0001）。
- OD-2 已決：接受合併口徑（RDR-0001）。
- OD-3、OD-4 已決（RDR-0001）：只做描述，不報 p 值；特殊日全部保留並標記。
- 未決證據：C-003、C-005、C-006、C-007；描述性結論的失敗條件。
- 證據任務：ET-1 除息日（C-003）、ET-2 近似文獻、ET-3 特殊交易日，均未核對。

## Reviewer concerns

- REVIEW-0001（審查 v0.1，判定 repair）；v0.2 尚未重審。
