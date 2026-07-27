# Research OS HyperFrames 教學影片

這個資料夾是一個可重製的 HyperFrames 專案，成品為：

- [`output/research-os-tutorial-zh-TW.mp4`](output/research-os-tutorial-zh-TW.mp4)
- 1920×1080、30 fps、H.264 + AAC
- 241.048 秒（4 分 01 秒）
- ElevenLabs voice ID：`kZ9lus3MKUfpqRaOvpJH`

影片採用參考影片的教學結構：強問題開場、工作流拆解、實際使用方法、案例與底層原則；不重用參考影片的畫面、逐字稿、人物、縮圖、品牌或音樂。

v2 改以六步主線敘事。旁白刻意不唸出任何 skill 名稱——v1 第三段唸了「develop research」，skill 一改名影片就錯了。

## 專案內容

| 檔案 | 用途 |
|---|---|
| `frame.md` | 視覺系統與禁止事項 |
| `.hyperframes/expanded-prompt.md` | 多場景 production brief |
| `STORYBOARD.md` | 八段分鏡 |
| `SCRIPT.md` | 旁白與 delivery（鏡像 `scripts/regen_voice.py` 的 `NARRATION`） |
| `scripts/regen_voice.py` | 重錄旁白並更新 `audio_meta.json` |
| `scripts/retime.py` | 由 `audio_meta.json` 重算 `index.html` 全部時間軸 |
| `audio_request.json` | HyperFrames 共用音訊引擎輸入 |
| `audio_meta.json` | 實際語音檔與長度 |
| `index.html` | HyperFrames composition |
| `snapshots/contact-sheet.jpg` | 八個場景與結尾 smoke test |
| `cost_ledger.json` | 付費嘗試與本機零成本步驟 |
| `render-receipt.json` | QA、輸出與 hash 證據 |

## 本機檢查

```bash
npm run check
npx hyperframes snapshot --at 9,34,63,90,121,158,192,225
```

## 重製流程

```bash
# 1. 旁白（會消耗 ElevenLabs 額度）
uv run python scripts/regen_voice.py --all

# 2. 時間軸（由 audio_meta.json 推算，不要手改 index.html）
uv run python scripts/retime.py

# 3. 檢查與輸出
npm run check
npm run render
```

`npm run render` 已固定帶 `--quality high`。**不要用裸的 `hyperframes render`**：預設是 `standard`，會把 video bitrate 從約 1050 kbps 壓到約 660 kbps。

重錄語音會再次使用 ElevenLabs 額度。不要因為音訊檔已存在就自動重送；先確認 `assets/voice/` 與 `audio_meta.json`。換 voice ID 時必須用 `--all` 重錄全部八段，否則會有一段是不同音色——`regen_voice.py` 會直接拒絕單段重錄。

需要 `.env`（在 repository 根目錄）提供 `ELEVENLABS_API_KEY` 與 `ELEVENLABS_VOICE_ID`。API key 必須具備 `text_to_speech` 權限。輸出格式固定 `mp3_44100_128` 再本地解碼為 pcm_s16le / 44100 Hz / mono：`pcm_44100` 需要 Pro 方案，而可用的 22 kHz／24 kHz 格式會被迫上採樣。
