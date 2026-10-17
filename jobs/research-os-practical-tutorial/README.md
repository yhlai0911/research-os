# 真實實操：0050 研究設計 / Hands-on research design

[播放 4:44 MP4](output/research-os-practical-0050-captioned-zh-en.mp4) · [中英字幕](captions.bilingual.srt) · [實際範例](example/) · [執行摘要](evidence/run-summary.json)

對應 research-os `56159bb46194f513d4e4499f228abf3ad6455cb1`（2026-10-17）。1920×1080、30 fps、284 秒。這一版是**無音軌的中英字幕版**；沒有新增 TTS。概念介紹與安裝另見 [3:47 原理片](../research-os-tutorial/v3/README.md)。

This captioned edition contains no audio track. It demonstrates a real isolated Claude Code session: setup, clarification, researcher choices, conditional Brief, optional domain audit, revision, and read-only status. All seven calls returned `claude-opus-5-5` (Opus 5.5), effort low, standard speed.

## 紀錄方式與界限 / Recording and scope

影片重播真實 PTY 執行紀錄與實際檔案快照，**不是原生桌面螢幕錄影**。等待有剪輯、部分段落停格供閱讀；來源時間、檔案行號與雜湊顯示於畫面。公開的 `.cast` 節錄移除本機路徑、用量資訊與無關的完成提示，調整換行；模型輸出未改寫。模型建議是待檢查的產物：例如初始追問對跳空的表述，在 Brief v0.2 已明確收緊為日內幅度不涵蓋隔夜跳空。示範中的研究者答覆是為課堂選定的案例決策。

This is a replay of real CLI captures and file snapshots, with waits cut and reading holds marked. Public excerpts redact local paths and omit usage counters and irrelevant completion speech. They do not fabricate terminal output. Model suggestions require verification; the final Brief corrects the initial proxy boundary. Learner answers are scripted teaching choices.

安裝驗證為核心 42 skills，加同 repo 的 finance-social-science 選配 1 skill；Claude 啟動訊息中的 `skills=36` 是 CLI 當次列出的可呼叫清單數，不能當成安裝清冊。領域審查是選配 skill，不等於主線第六步完成。

TWSE 0050 的 2024Q1 三個官方月份回傳共 56 列，實際保存並核對格式。**未計算相關係數、未做統計估計**，沒有因果、預測或投資結論。Brief v0.2 仍 conditional；審查只指向 v0.1，尚未重審。公司行動、特殊交易日、價量口徑可比性及資料再發布授權仍 unverified。原始市場 JSON 未公開；MANIFEST 只保留官方網址、擷取時間、列數及雜湊。

No statistical estimation or correlation was run. Brief v0.2 remains conditional, and the audit targets v0.1. Data retrieval is not research completion. The raw market JSON is withheld because redistribution rights remain unverified; its provenance metadata is retained.

## 章節 / Chapters

| 時間 / Time | 操作 / Action |
|---|---|
| 00:00 | 01  空白研究專案：明確呼叫 setup |
| 00:12 | 02  真正預檢、建立、check |
| 00:25 | 03  實際新增的 config.yaml |
| 00:37 | 04  把題目、受眾與限制交給第一步 |
| 00:50 | 05  真正核對官方資料 |
| 01:01 | 06  真實追問：你說的波動是什麼？ |
| 01:20 | 07  示範研究者給出真正答覆 |
| 01:34 | 08  選擇真正寫入 RDR-0001 |
| 01:47 | 09  由研究者明確啟動第二步 |
| 01:58 | 10  打開真正產生的 Brief v0.1 |
| 02:13 | 11  把識別與資料限制寫清楚 |
| 02:27 | 12  在同一 target 真正預檢選配包 |
| 02:37 | 13  選配安裝與驗證確實成功 |
| 02:47 | 14  真正呼叫領域檢查 skill |
| 02:58 | 15  審查原文：三個優先修復項目 |
| 03:20 | 16  研究者明確決定修正方向 |
| 03:33 | 17  真正檔案差異：Brief v0.1 → v0.2 |
| 03:54 | 18  原始資料已實際保存與核對雜湊 |
| 04:08 | 19  真正呼叫唯讀 status |
| 04:17 | 20  實際狀態：目前仍有關卡 |
| 04:34 | 21  回讀完成：零檔案變動 |

## 範例與重製 / Examples and reproduction

`example/.research/` 是本次執行後的教學快照，含 config、CONTEXT、claims、RDR、Brief v0.2、領域審查與 MANIFEST。`example/history/` 保留 v0.1；[真實 diff](evidence/brief-v01-to-v02.diff) 可對照修訂。raw JSON 被刻意省略，因此此副本不能宣稱具備完整資料重現條件。新專案應自行 setup，避免把教學快照覆蓋到已有研究。

Frozen HyperFrames HTML, local assets, and public recording excerpts are included. Node >=22.12, HyperFrames 0.8.167. Render does not require Claude, private original logs, or new TTS:

```sh
npm ci
npm run check
npm run render
```

`timeline.json` 是此片唯一時間軸，21 段共 8520 frames；中英字幕已燒入畫面，SRT 另存。原始未裁剪私人紀錄保留在作者本機，不屬於公開重製的必要輸入。
