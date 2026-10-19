# 從安裝到研究初稿：公債資料實作教學

[觀看／下載完整有聲 v4](https://github.com/yhlai0911/research-os/releases/download/granger-tutorial-voiced-v4/research-os-granger-follow-along-voiced-v4.mp4) · [Release 與校驗碼](https://github.com/yhlai0911/research-os/releases/tag/granger-tutorial-voiced-v4) · [English](TUTORIAL_GRANGER.en.md)

影片共 40 場景、7 分 57.93 秒，以 2015–2024 年美國兩年期與十年期公債殖利率，示範安裝、六步研究、診斷修訂及初稿交付。研究者用短句說明目的和取捨，助手處理資料與程式。

畫面是教學用文字重現與操作示意，包含選資料夾、輸入、等待、打開檔案與換對話恢復工作。畫面中的按鈕與動作不是 Codex 或 Claude 原生介面的即時錄影。片中保留中斷、模型未通過及修訂前後的差異，沒有把流程剪成一次就成功。

## 開始自己的研究

先安裝並登入 Codex 或 Claude Code，確認能聊天，再建立新的研究資料夾。依 [README](../README.md) 的對應工具安裝指令，請助手安裝並驗證 42 個通用核心。財金社科 profile 是另外選用的擴充，本例沒有安裝。不要直接覆蓋同名衝突檔案。

驗證應回報 `INSTALL OK: 42 skills`。保存安裝 receipt 中的來源 commit；本例先用 `4f7c162`，中途換入公開 `a9174de` 的寫作規範並重新驗證，這些是案例版本，不代表目前 `main` 永遠不變。

下一輪在同一研究資料夾輸入：

```text
$research-setup 請幫我準備研究資料夾，討論和草稿都用繁體中文。
```

上面是 Codex 的 `$skill-name` 形式；Claude Code 使用 `/skill-name`，安裝與驗證時指定 `--harness claude-code`。可自行指定討論與草稿語言，技能名稱和路徑維持原樣。

## 跟著六步讀交付檔案

| 步驟 | 研究者要確認的事 | 打開的產物 |
|---|---|---|
| `research-1-grill` | 研究目的、資料期間、兩個方向與預測目標 | 研究決定 |
| `research-2-brief` | 問題、範圍與方法是否保存，哪些規則仍待固定 | Research Brief |
| `research-3-falsify` | 資料、實作或模型不合格時如何停止 | 反證計畫 |
| `research-4-tasks` | 每項工作交什麼，如何驗收 | 工作清單與規格 |
| `research-5-run` | 實際完成什麼，資料與模型是否通過檢查 | 分析報告與結果 |
| `research-6-review` | 失敗原因、最小修訂與保留的限制 | 獨立審查報告 |

每一步都打開助手給的檔案連結。不了解時可以直接請助手解釋；文件已產生、工作已跑完與模型可供推論，需要分開判斷。換對話時留在同一研究資料夾，先讀目前研究紀錄再繼續。

本例在模型診斷停止後接受一項修訂，再由 `research-auto` 接續分析、初稿與比較審查。一次 `research-5-run` 只執行一項合格工作，不代表自動完成整個研究。

## 如何理解片中的結果

Granger 檢查的是指定模型中的額外預測資訊，不能直接當成經濟因果。兩方向主檢定與預先固定的敏感度分析均未達指定門檻；可說本例證據不足，不能推論不存在預測關係，也不能延伸成投資收益。

原模型的停止結果保留。修訂只針對診斷對異質變異的處理，保留同一資料、選模與主方程；新診斷未拒絕也不能證明模型正確。最後交付的是附有限制的基礎初稿，包含高槓桿、有限樣本近似、前置選模及事後診斷修訂等限制，不代表投稿認證。

## 來源與舊版

[v4 來源說明](../jobs/research-os-granger-tutorial/v4/README.md)包含旁白、40 場景時間軸、HyperFrames 畫面、已錄好的音訊、離線重建程式與檔案雜湊。重建不需要語音服務登入或付費呼叫。公開套件只含成片使用的教學節錄，不附完整原始私人對話、安裝 receipt、私人研究工作區或私人 skills。

[舊版 4:01 概要影片](../jobs/research-os-tutorial/README.md)及其來源保留。v4 沿用已完成的 MP4；本次發布未重製影片或重新配音。
