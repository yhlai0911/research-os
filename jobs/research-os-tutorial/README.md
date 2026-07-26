# Research OS HyperFrames 教學影片

這個資料夾是一個可重製的 HyperFrames 專案，成品為：

- [`output/research-os-tutorial-zh-TW.mp4`](output/research-os-tutorial-zh-TW.mp4)
- 1920×1080、30 fps、H.264 + AAC
- 170.166667 秒
- ElevenLabs voice ID：`kZ9lus3MKUfpqRaOvpJH`

影片採用參考影片的教學結構：強問題開場、工作流拆解、實際使用方法、案例與底層原則；不重用參考影片的畫面、逐字稿、人物、縮圖、品牌或音樂。

## 專案內容

| 檔案 | 用途 |
|---|---|
| `frame.md` | 視覺系統與禁止事項 |
| `.hyperframes/expanded-prompt.md` | 多場景 production brief |
| `STORYBOARD.md` | 八段分鏡 |
| `SCRIPT.md` | 鎖定旁白與 delivery |
| `audio_request.json` | HyperFrames 共用音訊引擎輸入 |
| `audio_meta.json` | 實際語音檔與長度 |
| `index.html` | HyperFrames composition |
| `snapshots/contact-sheet.jpg` | 八個場景與結尾 smoke test |
| `cost_ledger.json` | 付費嘗試與本機零成本步驟 |
| `render-receipt.json` | QA、輸出與 hash 證據 |

## 本機檢查

```bash
npx hyperframes check --json
npx hyperframes snapshot --at 8,26,46,65,88,110,133,158
```

正式重製：

```bash
npx hyperframes render \
  --quality high \
  --output output/research-os-tutorial-zh-TW.mp4
```

重製語音會再次使用 ElevenLabs 額度。不要因為音訊檔已存在就自動重送；先確認 `assets/voice/` 與 `audio_meta.json`。
