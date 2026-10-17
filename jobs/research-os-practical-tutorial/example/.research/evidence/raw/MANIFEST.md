# Raw snapshot manifest（TWSE STOCK_DAY, 0050, 2024Q1）

| File | Source URL | Retrieved (UTC) | sha256 | Rows | stat | fields match | shares parse to int | OHLC parse |
|---|---|---|---|---|---|---|---|---|
| twse_stock_day_0050_202401.json | https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20240101&stockNo=0050 | 2026-10-17T08:26:21Z | 81b3c4b88bba504ad47c61d269002ef34057e7e87c07819bc817d9c66851338e | 22 | OK | True | True | True |
| twse_stock_day_0050_202402.json | https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20240201&stockNo=0050 | 2026-10-17T08:26:21Z | 34b02e64c7be981289cb6b1cf2093efddd8cc86b936095204e6d92671669faa0 | 13 | OK | True | True | True |
| twse_stock_day_0050_202403.json | https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20240301&stockNo=0050 | 2026-10-17T08:26:21Z | 9b2cc370942bbea5ee14789e73a341901d5b06753522b55b85ea977de4ac7626 | 21 | OK | True | True | True |

Total rows: 56

- 驗證範圍：只做格式驗證（stat、欄位、列數、字串能否轉成數字），沒有計算任何統計量，也沒有畫圖。
- 重現與再發布授權：**未核對**（TWSE 使用條款沒有查證）。本快照只供本專案內部重現，不得發布或再散布。
- 擷取方式：curl GET，沒有帶任何認證。
