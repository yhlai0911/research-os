# 銀行定期存款行銷與聯繫優先序

[English](README.md) · [跟做教學](../../docs/TUTORIAL_BANK.zh-TW.md) · [公開素材 Release](https://github.com/yhlai0911/research-os/releases/tag/bank-term-deposit-tutorial-v1)

正式研究題名：**銀行定期存款行銷模型選擇與聯繫優先序的穩健性：資訊可用性假設與驗證方式之比較**。這是有界限的商管財金碩士教學範例，研究公開歷史紀錄中，資訊假設與驗證程序如何影響模型與聯繫名單；不主張新演算法、因果行銷效果或學位核准。

Release 提供本人 **ivan-advanced／Eleven v4 standard** 配音影片、真正 XeLaTeX／Biber 編譯的 30 頁 PDF，以及乾淨的 LaTeX／Bib／資料／分析來源包。本目錄只放[研究設計](STUDY_DESIGN.md)、[六個主要情境](focal-policy.csv)與[資產身分及下載連結](assets.json)，大型檔案不放 Git 歷史。

影片 13 章串接從沒有題目、否決候選與轉向，到設計、事前反證、任務、實證、審閱、學術寫作和可見修訂。研究助理選路並交接，接收 skill 實施研究；畫面來自教學角色問答與真實瀏覽器產物。這不代表原生 Codex 自動啟動已驗證，也沒有宣稱真人學生學習成效或人工聽驗通過。

## 核對與重現

下載並解壓 [assets.json](assets.json) 所列來源 ZIP。包內含未改動的 UCI **41,188 筆新版資料**、DOI 與 CC BY 4.0 歸屬；不是 45,211 筆舊版。在已有相容 Python 環境下：

```bash
python analysis/reproduce.py verify
python analysis/reproduce.py refit-primary --output fresh-primary-output
```

第一行重算保存分數的指標、比較、重抽樣分位數及數值 fixture，不重新訓練；第二行明確要求主要模型重擬合，只寫全新目錄。公開準備時，兩組重擬合預測與原結果完全相同；沒有宣稱全敏感性網格重新訓練過。套件版本列在包內，不會自動安裝。

論文編譯依 `manuscript/BUILD.md` 使用 XeLaTeX→Biber→XeLaTeX→XeLaTeX。需自行提供合法中文字型與 TeX 工具；原 PDF 用 Windows Microsoft JhengHei，不分發字型或安裝工具。換字型可能改變分頁與 PDF 位元組。影片中的待編譯狀態屬當時畫面；本次 PDF 是後續完成的排版成果。

下載檔使用 **PUBLIC_ASSETS_SHA256SUMS.txt** 核對。GitHub 會移除中文附件檔名字元，因此公開附件用完整英文主題名稱，中文題名仍保留。原 SHA256SUMS.txt 對應本機原始中文檔名，Release 已分別說明。

來源包不含私人對話、憑證、帳號額度、聲音模型、安裝工具或期刊全文；資料、程式與媒體範圍見包內 RIGHTS.md。較早的[公債／Granger 範例](../../docs/TUTORIAL_GRANGER.zh-TW.md)另行保留。
