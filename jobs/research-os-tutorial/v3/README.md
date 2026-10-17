# Research OS v3 原理介紹與安裝導覽

[播放／下載 MP4](paced/output/research-os-tutorial-v3-paced-zh-TW.mp4) · [繁中字幕](paced/captions.srt) · [完整旁白](SCRIPT.md) · [分鏡](paced/STORYBOARD.md) · [畫面總覽](paced/evidence/delivery-scenes-contact.jpg)

3 分 47 秒，1920×1080、30 fps、H.264／AAC。對應來源版本 `56159bb46194f513d4e4499f228abf3ad6455cb1`：通用核心 42 skills、同 repo 選配 finance-social-science 1 skill，涵蓋 Codex／Claude 安裝與呼叫、中英文輸出及六步研究流程。

本片屬原理介紹與安裝導覽。安裝指令與結果來自隔離目錄的真實驗證回放；研究對話、流程與模型圖為明示的教學示意。完整研究實操另見 [錄製計畫](../PRACTICAL_PLAN.md)，目前尚無可播放的實操片。

## 章節

| 時間 | 內容 |
|---|---|
| 00:00 | 先讓研究站得住 |
| 00:16 | 六步與過關條件 |
| 00:35 | 預檢、安裝、驗證 |
| 00:55 | Codex／Claude 呼叫差異 |
| 01:16 | 交代主題、成果與限制 |
| 01:37 | 一次決定一個分支 |
| 01:53 | 文獻、資料、反證與小型測試 |
| 02:13 | Brief 與不同成果 |
| 02:32 | 選配財金社科包 |
| 02:53 | 領域案例的問題縮小 |
| 03:13 | 繁中與英文 |
| 03:30 | status 與停止條件 |

## 聲音與同步

完整十二段新旁白使用 Eleven v4（`eleven_v4`、非 Turbo），原始 Stability 0.5、Similarity 0.75，MP3 44.1 kHz／128 kbps。原始錄音 266.684 秒；節奏版使用保留音高的 `atempo=1.18`，安裝三場採 `1.15` 並保留停頓，其餘場景只移除嚴格安靜區間中央共 2.8695 秒。字幕與場景同時重新計時。個人原始聲音檔僅由製作者在本機保留，不公開上傳。

`scenes.json` 保存順序與分鏡，引用 `narration-v3.json`。`alignment.json` 記錄原始 PCM sample 切點與經核對的字幕時間；`paced/alignment.json` 記錄節奏調整後的映射。建置器測量實際 WAV，以整數影格生成 HTML、時間軸、SCRIPT、STORYBOARD 及字幕，不手動維護多份時間軸。

## 重製

需要 Node ≥22.12（建議 24）、uv、ffmpeg／ffprobe。HyperFrames 鎖定 0.8.167，GSAP 3.14.2。製作者須先在本機提供已核對的原始 MP3 至 `assets/voice/full-narration-original.mp3`，其 hash 見 `voice-source.json`；該私有音檔不隨 repository 發布。使用既有原音重製不需 TTS、認證或新增額度。

```bash
cd jobs/research-os-tutorial/v3
npm ci
uv run python scripts/prepare_audio.py
uv run python scripts/build.py
npm run build:paced
uv run --with fonttools python scripts/verify_assets.py paced
npm run check -- paced --samples 24 --snapshots
npm run render:paced -- --workers 4
uv run --with numpy --with pillow python scripts/verify_delivery.py --paced
```

repository 只公開正式節奏版 MP4；原始 MP3、逐場 WAV、原速輸出及試錄留在製作端。逐場 WAV、渲染暫存與衍生字型可在具備原音的本機重建，不納入提交。沒有原始錄音仍可觀看正式影片、字幕、分鏡與程式來源。舊八段成片仍在 [上層目錄](../README.md)。

## 驗收與範例

- [安裝實測](evidence/install-transcript.json)：核心 42、選配 1，Codex／Claude 都通過；衝突拒絕覆寫。僅將本機絕對路徑替換為佔位符，其餘結果保留。
- [場景來源與文字](scenes.json)、[提示詞與案例](SCRIPT.md)：教學範例，不是已完成實證的研究成果。
- [畫面檢查](paced/evidence/production-check.json)：24 個版面與 300 個動作取樣，執行、版面、動作及對比檢查通過。
- [成品驗收](paced/render-receipt.json)：6,810 格、完整解碼無錯誤，12 場音軌與有聲短窗比對通過，最大偏移約 0.34 毫秒；147 條字幕無重疊。
- [節奏處理](paced/evidence/tempo-receipt.json)、[repository 測試](evidence/repository-final-checks.json)：保留可追查的 hash 與檢查結果，公開版移除本機絕對路徑。

QuickTime 已從頭連續播至 03:47 並正常結束。工具不能直接聽取音訊，未宣稱逐字人耳審聽；字幕時間仍為 ASR 估計。
