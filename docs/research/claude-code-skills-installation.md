# Claude Code Agent Skills 安裝規格查核

查核日期：2026-07-27（Asia/Taipei）

範圍：只採用 Anthropic／Claude Code 官方文件，確認一組 Agent Skills 在 Claude Code 的安裝位置、Plugin Marketplace 支援、`SKILL.md` frontmatter、呼叫方式與載入時機。

## 結論

Claude Code 原生支援兩種合理的散布方式，但它們是不同契約：

1. **純 skills 安裝**：把每個 `<skill-name>/` 目錄放進個人或專案的 skills 目錄。這種方式不需要 `.claude-plugin/plugin.json`。
2. **Plugin Marketplace 安裝**：repository 提供 `.claude-plugin/marketplace.json`，使用者先加入 marketplace，再安裝其中的 plugin。Plugin 可在根目錄的 `skills/` 放多個 skills；`.claude-plugin/plugin.json` 對預設目錄布局不是必填，但若需要明確 metadata、穩定 plugin 名稱或自訂元件路徑，應提供它。

因此，若 `research-os` 要讓 Claude Code 使用者「從 GitHub repository 直接安裝整套 skills」，官方、低歧義的使用者體驗是 **把整套 39 skills 包成一個 marketplace plugin**。若不新增 marketplace contract，README 必須明說這是「複製 39 個 skill 目錄」的純 skills 安裝，不能叫使用者對 repository 根網址直接執行 plugin install。

## 1. 純 skills 的安裝 scope 與路徑

Claude Code 官方定義：

| Scope | 路徑 | 適用範圍 |
| --- | --- | --- |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | 使用者的所有專案 |
| Project | `.claude/skills/<skill-name>/SKILL.md` | 目前 repository |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | 啟用該 plugin 的範圍 |

同名優先順序為 enterprise > personal > project；plugin skill 則有獨立的 `plugin-name:skill-name` namespace，不與前三者直接衝突。

來源：[Extend Claude with skills — Where skills live](https://code.claude.com/docs/en/skills#where-skills-live)

對「一組 skills」而言，純 skills 安裝的檔案形狀應是：

```text
~/.claude/skills/
├── skill-a/
│   └── SKILL.md
├── skill-b/
│   └── SKILL.md
└── ...
```

專案 scope 則將相同的子目錄集合放在 `<project>/.claude/skills/`。不能再多包一層 `research-os/skills/`，否則 Claude Code 不會把其中每個直接子目錄視為上述標準位置的 skill。

## 2. Plugin Marketplace 與 manifest

Claude Code 官方支援 plugin marketplace。GitHub repository 若要被 `/plugin marketplace add owner/repo` 加入，repository 根目錄需有：

```text
.claude-plugin/
└── marketplace.json
```

`marketplace.json` 至少列出 marketplace 名稱、owner，以及 plugin 的 `name` 與 `source`。加入 marketplace 只會註冊 catalog，**不會安裝 plugin**；使用者還要另外執行：

```text
/plugin marketplace add owner/repo
/plugin install plugin-name@marketplace-name
/reload-plugins
```

來源：

- [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Discover and install prebuilt plugins](https://code.claude.com/docs/en/discover-plugins)

一個包含多個 skills 的 plugin，可使用以下預設布局：

```text
plugin-root/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── skill-a/
    │   └── SKILL.md
    └── skill-b/
        └── SKILL.md
```

官方 reference 明確指出：

- plugin 會自動發現根目錄 `skills/` 下的 skills。
- `.claude-plugin/plugin.json` **是 optional**；省略時，Claude Code 會掃描預設元件目錄，並用目錄名稱推導 plugin 名稱。
- 需要 metadata 或自訂 component paths 時才必須依賴 manifest。
- 已安裝的 marketplace plugin 會被複製到 `~/.claude/plugins/cache`，不能依賴 plugin 根目錄以外的相對路徑。

來源：[Plugins reference — Plugin manifest schema and default locations](https://code.claude.com/docs/en/plugins-reference#plugin-manifest-schema)

雖然 `plugin.json` 不是預設布局的技術必填，但公開散布套件仍適合提供它，避免 plugin 名稱靠安裝目錄推導，也可提供 description、repository 等 metadata。若在 `plugin.json` 設定固定 `version`，每次發布更新都必須 bump；否則 Claude Code 會認為版本未變。省略 manifest 與 marketplace entry 的 `version` 時，Git source 會以 commit SHA 作版本。

來源：[Plugins reference — Version management](https://code.claude.com/docs/en/plugins-reference#version-management)

### Plugin installation scope

| Scope | 寫入設定 | 說明 |
| --- | --- | --- |
| `user` | `~/.claude/settings.json` | 個人所有專案，CLI 預設 |
| `project` | `.claude/settings.json` | 可提交到版本控制，供協作者共享 |
| `local` | `.claude/settings.local.json` | 僅本人、僅此專案 |

非互動 CLI 可使用 `claude plugin install plugin-name@marketplace-name --scope project` 等形式。

來源：

- [Plugins reference — Plugin installation scopes](https://code.claude.com/docs/en/plugins-reference#plugin-installation-scopes)
- [Discover plugins — Install plugins](https://code.claude.com/docs/en/discover-plugins#install-plugins)

## 3. `SKILL.md` frontmatter 與 invocation

Claude Code 的 `SKILL.md` 由 YAML frontmatter 與 Markdown 指令本體組成。官方目前將所有 frontmatter 欄位都列為 optional，僅建議提供 `description`，讓 Claude 判斷何時自動使用 skill。`name` 也受支援。

最小、清楚且與本 repository 規範相容的形式為：

```yaml
---
name: skill-name
description: What the skill does and when to use it.
---
```

重要行為：

- `description` 供 Claude 判斷何時自動載入；未提供時會取 Markdown 第一段。
- 初始 discovery 只把 skill 名稱與 `description` 等輕量 metadata 放進 context；完整 `SKILL.md` 本體要等 skill 被呼叫時才載入，載入後會留在該對話的 context。
- `disable-model-invocation: true` 可禁止 Claude 自動呼叫，保留手動 `/name`。
- `user-invocable: false` 可從 `/` 選單隱藏。
- 純 personal/project skill 的實際 slash command 來自**目錄名稱**；frontmatter `name` 只影響顯示名稱。
- Plugin skill 的 slash command 會被 namespace，例如 `/research-os:skill-name`；其最後一段可由 frontmatter `name` 決定。
- 沒有停用 model invocation 時，Claude 可依 `description` 自動選用；使用者也能直接輸入 slash command。

來源：

- [Extend Claude with skills — Frontmatter reference](https://code.claude.com/docs/en/skills#frontmatter-reference)
- [Extend Claude with skills — How a skill gets its command name](https://code.claude.com/docs/en/skills#how-a-skill-gets-its-command-name)
- [Extend Claude with skills — Skill content lifecycle](https://code.claude.com/docs/en/skills#skill-content-lifecycle)

## 4. 安裝或修改後何時載入

### 純 skills

Claude Code 會監看已存在的 `~/.claude/skills/`、專案 `.claude/skills/` 與 `--add-dir` 中的 `.claude/skills/`。在這些已存在目錄裡新增、編輯或移除 skill，可在目前 session 生效，不必重啟。

但若 Claude Code 啟動時，該頂層 skills 目錄尚不存在，之後才建立，必須重啟 Claude Code，讓它開始監看該目錄。

來源：[Extend Claude with skills — Live change detection](https://code.claude.com/docs/en/skills#live-change-detection)

### Marketplace plugins

在 session 中安裝、啟用或停用 plugin 後，執行 `/reload-plugins` 可立即載入變更，不必重啟。只修改 plugin skill 的 `SKILL.md` 可即時生效；hooks、agents、MCP 等其他 plugin components 的變更則需要 `/reload-plugins`，部分 component 可能需要重啟。

來源：

- [Discover plugins — Apply plugin changes without restarting](https://code.claude.com/docs/en/discover-plugins#apply-plugin-changes-without-restarting)
- [Plugins reference — Skills-directory plugins](https://code.claude.com/docs/en/plugins-reference#skills-directory-plugins)

## 5. 對 `research-os` README／發行契約的建議

README 應把 Codex 與 Claude Code 分開寫，因為兩者的 personal skills 路徑不同：

- Codex：`~/.codex/skills/`
- Claude Code：`~/.claude/skills/`

Claude Code 至少應提供一條完整、可驗證的路徑：

### 路徑 A：純 skills 批次安裝

1. clone repository。
2. 將 `skills/` 下的每個 skill 子目錄複製到 `~/.claude/skills/`，或指定專案的 `.claude/skills/`。
3. 確認每個目標子目錄都有 `SKILL.md`，並核對預期 skill 數量。
4. 若目標頂層目錄是在 session 啟動後才建立，重啟 Claude Code；否則既有目錄內的變更可即時偵測。
5. 用 `/skill-name` 或符合 description 的自然語言請求驗證一個 skill。

### 路徑 B：Marketplace plugin（建議作為 GitHub 安裝入口）

1. repository 提供合法的 `.claude-plugin/marketplace.json`。
2. 將整個 `skills/` 宣告為一個 plugin 的預設 skill 集合。
3. 使用者執行 `/plugin marketplace add owner/repo`。
4. 使用者執行 `/plugin install research-os@marketplace-name`，並選擇 user/project/local scope。
5. 使用者執行 `/reload-plugins`。
6. 以 `/research-os:<skill-name>` 驗證安裝。
7. 發布前執行 `claude plugin validate .`，並以乾淨環境做 add → install → reload → invocation 回歸測試。

這兩條都合法；關鍵是 README 不能混寫。純 skills 安裝不應要求 plugin manifest，marketplace 安裝則必須有 marketplace catalog，且「加入 marketplace」不能被描述成已完成安裝。
