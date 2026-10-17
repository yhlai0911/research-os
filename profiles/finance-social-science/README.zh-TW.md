# 財金與社會科學 profile（選用擴充）

[English](README.md) · [通用核心](../../README.md)

此擴充獨立標示版本 **0.1.0**，需要此 checkout 的 Research OS core **2.0.0**。新增 `research-finance-social-science` 一個研究設計稽核入口。通用核心仍是 42 個 skills；預設安裝不含此擴充，也不以財金社科流程取代核心。

## 安裝及驗證

先在 repository 根目錄執行 `uv sync --locked` 並完成核心安裝，再執行：

```bash
uv run python scripts/install_skills.py --profile finance-social-science --dry-run
uv run python scripts/install_skills.py --profile finance-social-science
uv run python scripts/verify_install.py --profile finance-social-science
```

Claude Code 使用者在三個指令都加上 `--harness claude-code`。若核心安裝在自訂目錄，三個指令都加上相同的 `--target /absolute/path/to/skills`。安裝器會先驗證同目錄、同 harness 的核心，再寫入獨立的 `.research-os-finance-social-science-install.json`；核心的 `.research-os-install.json` 保持不變。有同名內容衝突時停止，不覆寫。

## 使用範例

先以 `research-setup` 建立專案工作區，再於 Codex 呼叫 `$research-finance-social-science`，或在 Claude Code 使用 `/research-finance-social-science`：

> 請用繁體中文檢視我的政策效果研究設計：以公司追蹤資料分析政策對投資的影響。區分識別假設與估計方法，列出還缺的證據；不要虛構結果。

它會依財金、量化社科、質性或混合方法選用必要檢查，包括時間點資料、資訊洩漏、存活者偏誤、識別、測量、同意與重現性。稽核寫入核心設定的正式 review 位置，並建議下一個核心步驟。不會自動執行整條研究流程、另建一份競爭的 brief，或提供投資建議。

## 同一個 repo，清楚區分用途

獨立的 [catalog](catalog.yaml)、[skill](skills/orchestrators/research-finance-social-science/SKILL.md) 與方法參考均放在此目錄。兩個版本維持在同一個 repository：通用核心可用於各研究領域，明確選用的擴充才加入財金社科檢查。擴充依賴相容核心，不複製核心。請使用 repository 根目錄的安裝工具；此目錄不是獨立發行套件，也沒有另外建立 repo。

這是研究設計輔助工具，尚未驗證其能提升實證研究品質。結構測試與安裝驗證不代表研究結論、法規符合性或投稿品質已驗證。適用本 repository 的 [MIT 授權](../../LICENSE)，不因此取得對通用核心的獨占權。
