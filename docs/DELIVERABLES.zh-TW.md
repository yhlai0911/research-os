# 閱讀頁、學術稿與工具需求

[English](DELIVERABLES.en.md) · [研究助理入門](RESEARCH_ASSISTANT.zh-TW.md) · [使用教學](USAGE_GUIDE.zh-TW.md)

## 研究與呈現各有負責的 skill

`research-assistant` 選擇與交接適用 skill，再讀回產物和證據。資料、方法、執行、寫作與審閱由各自 skill 實施。`render-research-deliverable` 呈現已有的研究產物；`to-paper` 依論文目的協調寫作、引用、審閱與製作要求。兩者都不能替未執行研究補造結果。

## HTML 閱讀頁與真實回覆

當實際表格、圖表、段落或修訂較適合在瀏覽器檢視時，依當版來源建立閱讀頁。保留原始值、顯示精度、單位、來源與缺漏；沒有資料的視圖就不出現，沒有兩個真實版本就不造前後對照，空表不補成觀察結果。

回覆有三部分：簡短說明產物／重要結果、真實標題與可開啟連結、下一個研究動作。先生成、再驗證目標，最後才給連結。缺檔、生成失敗或沒有可用交付介面時直接說明，不給 placeholder。摘要仍須對照來源；連結 helper 的身分檢查不等於科學內容驗證。

頁面按內容提供排序、篩選、同步圖表、高亮、修訂對照與返回。每個控件須有真正目標或 handler；驗收要真的點回覆連結、操作控件、檢查空結果／缺值與桌面／窄視窗可讀性。截圖或定時游標動畫不能證明點擊；回覆 HTML 副本也不是原生聊天介面。

Renderer 僅用 Python 標準函式庫與隨包 HTML/CSS/JavaScript，不依賴外部資源。資料經安全編碼，會拒絕不安全來源、非有限數值與覆寫既有輸出；不要為展示而關掉檢查。

### 可重跑的合成資料範例

在 repository 根目錄執行，輸出檔名須尚未存在：

```bash
uv run python skills/primitives/render-research-deliverable/scripts/render_reading_view.py --input examples/interactive-reading/synthetic-comparison.json --output reading-demo.html
uv run python skills/primitives/render-research-deliverable/scripts/build_reading_reply.py --artifact reading-demo.html --next-step "檢視合成比較，再回到真正研究問題。" --output reading-demo-reply.md --response-html reading-demo-reply.html
```

[輸入資料](../examples/interactive-reading/synthetic-comparison.json)明確標為介面測試用合成值，不是實證研究。用正式支援的本機瀏覽器開啟產物。Reply helper 也可核對已授權 loopback 預覽的實際位元組；它不啟動伺服器或發布網站。詳見[renderer 契約](../skills/primitives/render-research-deliverable/references/html-reading-views.md)。

本機檔案與 `127.0.0.1` 不供另一台裝置直接讀取。依宿主使用真正的本機連結格式，跨裝置則用已授權的正式附件介面；不要把 Windows 路徑改寫成公開網址或猜下載連結。

## 學術正文

用專業學術散文連起問題、最接近的核實文獻、未解問題、機制／理由、研究問題、設計、含不確定性的結果、替代解釋與結論。論證鏈須完整；條列、漂亮句子、固定字數或引用篇數都不能代替學術完整度。

正文不混入 skill 名稱、程式變數／函式、路徑或操作日誌。必要的資料處理與統計細節用學科語言準確交代；程式重現資訊另放技術附錄，AI 協助依適用規範揭露。若有校級／期刊格式，先核實並使用；未指定學校時不宣稱通用格式等於學位核准。

中文可採指涉清楚、精確與術語一致等原則。ASD-STE100 是受控英文技術文件規範，不能據此宣稱中文學術寫作正式符合該標準；必要細節、論證與不確定性仍須保留。

重要方程式須編號、標籤及正文引用，近處定義符號、索引、單位與假設，交代推導／核實來源及方法選擇理由。保留反證條件、無效果／不利結果、失敗診斷與推論界線。

以 `.bib` 管理參考文獻，預設採 APA 7 的 BibLaTeX/Biber 與 `biblatex-apa`。分別核實作者順序、年份、題名、期刊與 DOI 身分，以及來源是否支持該句；DOI 可解析不等於主張成立，只讀摘要也不算精讀全文。正文鍵、Bib 與生成書目須雙向對上。詳見[學術交付契約](../skills/primitives/research-writing/references/scholarly-delivery.md)。

## 真正 LaTeX 交付

交付可編輯 `.tex`、`.bib`、合法圖表／樣式與由同一來源實際編譯的 PDF。保存引擎／書目後端版本、真實命令、exit、來源與 PDF 雜湊、最後記錄；完成引用與交叉參照重跑，解決未定義引用／參照、缺字、重複標籤及待重跑問題。首次交付逐頁檢查，修訂後再查變動與分頁影響。來源包須有當版輸入、建置方法、套件／字型版本及學術、引用、視覺審閱記錄。

HTML 是輔助，Word 轉 PDF 或直接繪製 PDF 都不能代替這項要求。缺少已授權可用的引擎、後端或字型時，保留來源並說明 partial／blocked；不能把嘗試編譯說成完成。內容審閱、引用審查、機械驗證和編譯各回答不同問題，不能互相代替，也不保證學位合格。

## 工具與跨平台範圍

| 工作 | 需要的能力 | Research OS 提供什麼 |
|---|---|---|
| 安裝與驗證 | Git、uv、Python 3.11+、支援的宿主 | catalog、installer、adapter、衝突檢查與 receipt |
| 文獻與資料取得 | 已授權瀏覽器、搜尋、連接器或本地來源 | 查核規範，不含付費存取或憑證 |
| 資料分析 | 適合設計的數值／統計工具 | 方法與執行契約，不假設通用分析工具都已安裝 |
| HTML 閱讀頁 | Python 標準函式庫，互動 QA 另需瀏覽器 | 自包含 renderer、assets 與真實回覆 helper |
| 中文 LaTeX | 如 XeLaTeX／LuaLaTeX、套件、合法 CJK 字型、APA 書目後端 | 交付規格，不含 TeX／字型安裝 |
| 教學截圖 | 正式支援的畫面擷取工具 | 留證規範；瀏覽器可用不等於整桌面可截圖 |
| Release ZIP | packager 所需 POSIX 安全原語 | fail-closed 打包；Windows copy 安裝是另一種能力 |

skill 需要某工具，不等於已獲准安裝、登入、付費、發布或更改安全設定。說清楚缺項，依實際授權處理。一般使用選預設 copy 安裝；Windows symlink 權限與 POSIX release 測試另有條件。見[品質關卡](QUALITY_GATES.md)與[疑難排解](TROUBLESHOOTING.zh-TW.md)。
