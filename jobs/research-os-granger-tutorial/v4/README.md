# 完整有聲教學 v4 / Voiced tutorial v4

[觀看／下載 MP4](https://github.com/yhlai0911/research-os/releases/download/granger-tutorial-voiced-v4/research-os-granger-follow-along-voiced-v4.mp4) · [Release](https://github.com/yhlai0911/research-os/releases/tag/granger-tutorial-voiced-v4) · [旁白](SCRIPT.zh-TW.md) · [40 場景分鏡](STORYBOARD.zh-TW.md) · [繁中導覽](../../../docs/TUTORIAL_GRANGER.zh-TW.md) · [English walkthrough](../../../docs/TUTORIAL_GRANGER.en.md)

40 場景、477.933333 秒（7:57.93）、1920×1080、30fps、14,338 格、AAC 音軌。MP4 為 19,403,538 bytes，SHA256：

```text
765e97ed4f253107a215afdd476d9d8cd422b531cba5f82087988f295ceb115c
```

本次發布沿用已交付成品，未重新生成影片或付費配音。畫面是教學文字重現與操作示意；獨立研究審查只支持附有限制的基礎初稿，沒有投稿或人類耳聽認證。原有 [4:01 教學](../../research-os-tutorial/README.md)與來源保留。

## 離線音訊重建與完整影片重建

需要 Python 3.11+、uv、ffmpeg，以及完整影片重建使用的 Node/npm。先在本目錄驗證來源，再選擇需要的操作：

```bash
uv run --no-project python scripts/verify_package.py
# 只重建音軌，不連線語音服務：
uv run --no-project python scripts/rebuild.py --audio-only
# 檢查畫面與完整重建；首次執行 npx 需要下載套件及瀏覽器依賴：
npm run check
npm run render
```

`npm run render` 固定使用 HyperFrames `0.8.167`，從 `composition/index.html` 重建畫面。音訊程式依 `voice/selection.json` 的原始 sample 邊界，從兩份已錄好的 MP3 選出 40 段，按 `timeline.json` 對齊，經兩階段音量處理後封裝。輸出為 `output/rebuilt.mp4`；音訊模式為 `output/rebuilt-voice.wav`。程式遇到同名輸出會停止，保留既有檔案。

已選定的旁白 sample 與時間軸可檢查；不同 ffmpeg／編碼器版本的完整輸出不保證逐 byte 相同。正式成品以 Release MP4 的 SHA256 為準。首次 npx 安裝需要網路；已安裝的素材與重建音訊不需要 ElevenLabs 憑證或新付費呼叫。不要把 `render` 當成安裝 skills 或執行研究的指令。

## 公開來源範圍

- `composition/`：已編譯的 40 場景畫面、字型、GSAP、公開公債示意圖。重建不需要原製作機上的研究檔案。
- `timeline.json`、`voice/`：正式時間軸、兩份完整錄音、所選 sample 與旁白文字。未採用的首錄片段仍在原錄音中。
- `qa/`：先前製作驗收的媒體、40 場景畫面／音訊比對與播放摘要。`source_file`／`encoded_file` 是當時的證據路徑，對應原始畫面快取未包含在本精簡套件內。
- `PUBLICATION.json`、`PACKAGE_MANIFEST.json`：發布邊界與公開檔案 hash。原始完整對話、receipt、完整研究工作區、私人 skills、登入資料、瀏覽器狀態與快取均未納入。

影片中的教學節錄已內嵌於畫面；原始完整私人對話不隨套件發布。選資料夾場景出現的 `/Users/apple/Documents/Codex/2026-10-17/task` 是原教學畫面的示範路徑，不是重建依賴或讀者應使用的路徑。

保留字型的 [SIL OFL 授權](composition/assets/OFL-NotoSansCJK.txt)，GSAP 原檔保留其版權與授權網址；這些第三方素材依各自授權使用。

## Verification and reuse (English)

This package rebuilds all 40 scenes from the compiled visual composition and the retained recordings. It excludes full private conversations, receipts, private research workspaces, credentials, and private skills. The film's selected teaching excerpts remain embedded. The example's local folder path is illustrative and is not a build dependency.

Run `scripts/verify_package.py` before rebuilding. `--audio-only` uses only local audio and ffmpeg; full rendering also needs the pinned HyperFrames package. No speech-service account or paid generation call is required. Rebuilt media bytes can vary across encoder versions; use the Release asset's checksum to identify the delivered film.

Production QA records report full audio/video decoding, 40 scene comparisons, and full-duration unmuted 1× playback. These are retained evidence from the completed production, not a claim of human listening certification. A publication check repeats full decoding and verifies source hashes without rerendering the film.
