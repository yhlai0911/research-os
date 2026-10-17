# Lifecycle、非 promoted skills 與 repository distribution 深度稽核

> 本文件保留稽核當下的逐項證據與缺口判讀；後續已完成的修補及 v1.0 最終狀態，以 [`../PORT_REMEDIATION.md`](../PORT_REMEDIATION.md) 的機械驗證紀錄為準。

## 稽核契約

本文件稽核 Matt upstream 位於 `deprecated/`、`misc/`、`personal/` 的 10 個 skills，並追查 repository 如何決定 skill 的可發現性、安裝集合、plugin 集合、版本與 release。

- Upstream repository：`/tmp/matt-skills-analysis.qMpo5S/repo`
- Upstream pinned commit：`ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- Upstream commit date：2026-07-21
- Research OS comparison root：`/Users/apple/Downloads/research-os`
- Audit date：2026-07-26，Asia/Taipei

為了判斷「為何存在、如何演變」，本輪已將 upstream shallow clone 補齊為完整歷史，再依 repository 自己的 commits 判讀；不是只看當輪 prompt。若 upstream 沒有正式宣告 `replaced_by`，本文會明標為「依 mechanics 與歷史推定」。

### 已完整閱讀的 skill

- `skills/deprecated/design-an-interface/SKILL.md`
- `skills/deprecated/qa/SKILL.md`
- `skills/deprecated/request-refactor-plan/SKILL.md`
- `skills/deprecated/ubiquitous-language/SKILL.md`
- `skills/misc/git-guardrails-claude-code/SKILL.md`
- `skills/misc/migrate-to-shoehorn/SKILL.md`
- `skills/misc/scaffold-exercises/SKILL.md`
- `skills/misc/setup-pre-commit/SKILL.md`
- `skills/personal/edit-article/SKILL.md`
- `skills/personal/obsidian-vault/SKILL.md`

### 已讀取的直接 metadata 與 resources

- 上述 10 個 skills 的全部 `agents/openai.yaml`；
- `skills/deprecated/README.md`、`skills/misc/README.md`、`skills/personal/README.md`；
- 這 10 個 skills 唯一 bundled script：`skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh`。

其餘 9 個 skills 都沒有 bundled `references/`、`scripts/` 或 `assets/`。像 `UBIQUITOUS_LANGUAGE.md`、`.claude/settings.json`、`/mnt/d/Obsidian Vault/AI Research/` 是目標 workspace 路徑，不是 skill resource。

### 已讀取的 repository architecture 檔案

- Root contract 與歷史：`README.md`、`CLAUDE.md`、`AGENTS.md -> CLAUDE.md` symlink、`CONTEXT.md`、`CHANGELOG.md`、`LICENSE`；
- Invocation 與 docs 規則：`.agents/invocation.md`、`.agents/writing-docs.md`、`.agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md`、`.agents/adr/0002-ship-as-a-claude-code-plugin.md`；
- Discovery/install：`scripts/link-skills.sh`、`scripts/list-skills.sh`；
- Plugin：`.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`；
- Release：`package.json`、`package-lock.json`、`.changeset/config.json`、`.changeset/README.md`、9 份 pending changesets、`.github/workflows/release.yml`、release tags 與相關 commits。

Research OS 端則讀取 `skills/catalog.yaml`、`docs/ARCHITECTURE.md`、`docs/QUALITY_GATES.md`、`docs/SKILL_CATALOG.md`、`scripts/{install_skills.py,package_release.py,scaffold_skills.py,sync_catalog.py,validate_repository.py}`、`tests/test_repository.py`、`pyproject.toml`、`.github/workflows/validate.yml`，以及下文列出的 exact target skills。

### 分類語意

- **Adapt**：保留 upstream 的行為核心，但更換研究 domain、authority、artifact 或 stop topology。
- **Replace**：Research OS 有對應的正當需求，但不應照搬 upstream workflow。
- **Exclude**：不應成為 Research OS core skill；最多只保留一小段 mechanics 到 repository tooling。

## 快照結論

Pinned upstream 共 41 個 skills：

| Bucket | 數量 | Public/plugin 狀態 |
|---|---:|---|
| `engineering` | 17 | promoted |
| `productivity` | 5 | promoted |
| `in-progress` | 9 | not promoted |
| `deprecated` | 4 | not promoted |
| `misc` | 4 | not promoted |
| `personal` | 2 | not promoted |

當輪 upstream Claude plugin 正好包含 22 個 promoted skills；top-level README、promoted bucket READMEs、docs pages 與 plugin paths 也一致。實際執行 `claude plugin validate . --strict` 通過。

但這個綠色快照不代表 lifecycle 已封閉：

- Lifecycle 只有目錄位置與 prose，沒有 machine-readable metadata；
- public plugin、maintainer linker、repository listing 與外部 `skills.sh` 看到的 skill 集合不同；
- deprecated skills 仍是完整可執行 prompt，也仍有 Codex UI metadata，卻沒有 replacement pointer；
- deprecated `qa` 仍殘留在 promoted setup/context；
- 版本分裂為 `package.json=1.1.0`、`plugin.json=1.2.0`、`package-lock.json=0.0.0`；
- release CI 不執行 repository mirror、skill、plugin 或 reference validation。

Research OS 已修好最大的 manual mirror 問題：`skills/catalog.yaml` 管理 inventory 與 UI metadata，`sync_catalog.py` 生成 Codex metadata 與人類 catalog。剩餘結構缺口是 lifecycle schema、cross-harness invocation、installer failure atomicity、managed update/uninstall，以及 release receipt 的完整性。

## Port disposition matrix

| Upstream skill | Invocation | Leading concept | 處置 | Exact Research OS target | Retain mechanics | Reject mechanics |
|---|---|---|---|---|---|---|
| `design-an-interface` | model | design it twice / contrast | Adapt | `design-research-three-ways` | 固定共同 constraints、隔離產生 alternatives、真差異、先比較再 hybrid | 把 module/interface 評分直接套到研究；沒有 status gate 的選單 |
| `qa` | model | durable behavioral issue / thin issue | Replace | `research-triage`、`research-diagnosis`、`research-4-tasks` | 輕量澄清、先驗證 claim、以行為描述、dependency-aware slices | 自動 `gh issue create`、GitHub-only、無授權與 readback |
| `request-refactor-plan` | model | tiny working steps | Adapt | `research-auto` 組合 `research-grilling`、`synthesize-research-brief`、`research-4-tasks`、`research-5-run` | 查明 facts、定 scope、保留 testing/falsification 決策、小而可獨立驗證的 slices | 一個 god skill 同時訪談、設計、規劃與發布 |
| `ubiquitous-language` | user | canonical language | Adapt | `research-domain-modeling` | canonical terms、aliases to avoid、typed relations、ambiguity、持續 refinement | 一次性 conversation export、root overwrite、無證據仍強迫定義 |
| `git-guardrails-claude-code` | model | pre-execution denylist | Exclude | none；authority 留在 `AGENTS.md` 與 operation-aware tooling | scope confirmation、可執行 negative test，只當 defense in depth | 把 regex hook 當 security/authority boundary；Claude-only global mutation |
| `migrate-to-shoehorn` | model | partial test fixture | Exclude | none | 狹窄 migration 應有明確 search、transform、verify | TypeScript/package 特化流程、文字盲改、隱含 dependency install |
| `scaffold-exercises` | model | lint-ready filesystem contract | Exclude | 不建 skill；mechanics 歸 `research-workspace-contract` 與 scripts | deterministic schema、dry-run、validator-backed completion | AI Hero course 規則、自動 commit、無保護 stub writes |
| `setup-pre-commit` | model | commit-time feedback loop | Exclude | none；repository target 是 `docs/QUALITY_GATES.md` 與 CI | environment detection、保留既有 config、observable verification | Node-only defaults、未釘版本假設、stage-all-and-commit |
| `edit-article` | user | information DAG | Replace | `research-writing` | dependency-aware section order、section purpose、使用者擁有 narrative 決策 | 全域 240-character paragraph 規則、無 evidence 的 rewrite |
| `obsidian-vault` | model | wikilink graph | Replace | storage authority 由 `research-workspace-contract` 負責；core 不做 Obsidian adapter | linked artifacts、index nodes、configurable canonical paths | hard-coded personal vault、WSL/GNU commands、隱含修改個人資料 |

## 逐 skill prompt-level 稽核

### 1. `design-an-interface`

**為何存在與演變。** Commit `74dbf0d` 在 2026-02-03 加入此 skill，把 Ousterhout 的「Design It Twice」變成 agent workflow：第一個 interface 通常不是最佳解。Commit `949472a` 於 2026-04-23 把同一套 multiple-interface mechanics 吸收到更大的 architecture flow。Commit `3e3ca9b` 於 2026-04-28 將 standalone skill 放進 `deprecated/`，同時建立最初 plugin manifest。現在 promoted owner 是 `skills/engineering/codebase-design/DESIGN-IT-TWICE.md`，由 `codebase-design/SKILL.md` conditional disclosure。Upstream 未正式寫 `replaced_by`，這是依 mechanics 與歷史推定。

**Invocation 與 leading concept。** Claude frontmatter 沒有 `disable-model-invocation`，Codex metadata 也沒有 `policy`，所以是 model-invoked。核心不是「列三個想法」，而是 **radical contrast**。

**Ordered mechanics。**

1. 查明 callers、operations、constraints、該藏在 module 內的 complexity。
2. 同時啟動至少三個 subagents，各自承受不同 design pressure。
3. 每案必須交 interface signature、usage example、hidden complexity、trade-offs。
4. 逐案呈現，避免一次塞滿。
5. 比較 simplicity、generality、implementation efficiency、depth、misuse risk。
6. 由使用者選擇，再考慮 hybrid。

**Completion / failure。** Prompt 沒有正式 status。隱含完成是「多個真正不同的 interfaces + 完整比較 + 使用者選擇」。Anti-patterns 要求相似設計重生、不可跳過比較、不可實作、不可按實作成本評分。缺少的 branches 包含：parallelism 不可用、requirements 不完整、使用者延後選擇、全部方案違反 hard constraint。

**Research OS target。** `skills/primitives/design-research-three-ways/SKILL.md` 是正確 adaptation。保留 shared brief、isolated generation、compare-before-hybrid，並把 lens 改成 theory-first、identification-first、data-first。它再補 stable candidate IDs、identification/evidence gate、`partial/blocked`、使用者 selection authority、durable decision 與 readback。

**Current gap。** Research OS 沒有明確保留兩個有用的 presentation mechanics：產生前先讓使用者看到共同 problem frame，以及 matrix 前逐案呈現。Exactly-three lenses 是合理 domain adaptation；若 selection 在 scope 內，可再明定 agent 是否應提供 opinionated recommendation。

### 2. `qa`

**為何存在與演變。** Commit `6a87ed0` 於 2026-03-25 加入 conversational QA，內建 issue breakdown 與 blocking relationships。目的是讓使用者用自然語言報錯，背景 explorer 只學 domain language 與 expected behavior，不先找 fix。Commit `62f43a1` 於 2026-04-28 將它移入 `deprecated/`。後來 promoted `triage` 有 claim verification、configured tracker adapter、maintainer confirmation，因此可推定是 engineering successor，但 upstream 沒有正式 replacement metadata。

**Invocation 與 leading concept。** 它仍是 model-invoked。最強概念是 **durable behavioral issue**：描述使用者可觀察的 boundary，不寫容易腐敗的 files/lines。第二概念是 **thin issue**：只有真的可獨立修復、驗證時才拆分。

**Ordered mechanics。**

1. 最多問 2–3 個短問題，集中 expected/actual、reproduction、intermittency。
2. 背景 agent 讀 codebase 與 `UBIQUITOUS_LANGUAGE.md`，只找 domain context。
3. 判斷單一 issue 或 dependency-ordered breakdown。
4. 不經 review gate，直接執行 `gh issue create`。
5. 回傳 URLs 與 blocking summary，一次處理一個 report，直到使用者結束。

**Completion / failure。** 完成證據是 GitHub issue URLs。Reproduction 必填；不清楚就回問。缺少 duplicate search、tracker config、`gh` auth/failure、partial receipt、current readback。更關鍵的是 prompt 明確要求 external write 前不要給使用者 review。

**Research OS target。** 不移植 issue-filing workflow，只分別保留：

- `research-triage`：驗證 load-bearing premises，提出一個 verdict，讓使用者決定；
- `research-diagnosis`：先重現、辨識真正 failure，再談 repair；
- `research-4-tasks`：把 approved work 切成可獨立驗證且有 blocking edges 的 slices。

Remote issue 仍必須由使用者明確要求並做 readback；本地 `.research/` 寫入則受已授權 workspace contract 限制。

**Current gaps 暴露。** Upstream `CONTEXT.md` 與 `skills/engineering/setup-matt-pocock-skills/SKILL.md` 仍出現 deprecated `qa`；不是 historical changelog，而是真 ghost references。Research OS 現在檢查 filesystem inventory 與 Markdown links，卻還沒驗證所有 `$skill` 或 router/dependency 的 plain names。正式引入 deprecation 前，需要 lifecycle-aware ghost-reference gate。

### 3. `request-refactor-plan`

**為何存在與演變。** 它來自 initial commit `985d8fc`（2026-02-03），`d1beb4f` 於 2026-03-13 改善 metadata，`62f43a1` 於 2026-04-28 移入 `deprecated/`。原 prompt 把後來拆開的 grilling、repo verification、spec、tiny-step tickets 與 publication 全綁在一起。

**Invocation 與 leading concept。** 仍是 model-invoked。Leading concept 是 **每一個 refactor step 都要小到讓程式保持可工作**。

**Ordered mechanics。**

1. 收集長篇 problem 與 candidate solution。
2. 回 repo 驗證使用者 assertions。
3. 提出 alternatives。
4. 詳細訪談 implementation。
5. 定清 in/out scope。
6. 檢查 tests；coverage 不足就問 testing plan。
7. 切成 tiny green commits。
8. 建 GitHub issue，內容含 problem、solution、commits、decisions、tests、scope、notes。

**Completion / failure。** 完成被等同為 external issue created。唯一明顯 branch 是可 skip steps、tests 不足時回問。缺少 accepted-plan gate、no-change、tracker adapter、external-write authority、publish failure 與 readback。Discovery、decision、planning、publishing 無法獨立 resume 或驗證。

**Research OS target。** `research-auto` 是 end-to-end orchestrator，但正確 mechanics 分層在：

- `research-grilling`：解 human decisions；
- `synthesize-research-brief`：把 verified state collapse 成唯一 research contract；
- `research-4-tasks`：建立 dependency-aware tracer studies；
- `research-5-run`：claim 並執行一個 bounded slice，留下 receipt。

Research analogue 不是 tiny commits，而是每個 workpackage 都產出 independently verifiable artifact 並降低 uncertainty。

**Current gap。** Research OS prompt graph 很完整，但 catalog 還沒宣告 `research-auto -> synthesize-research-brief -> research-4-tasks -> research-5-run` 等 dependencies；目前只存在 prose，repository validator 不會驗證。

### 4. `ubiquitous-language`

**為何存在與演變。** `d3850f1` 於 2026-03-16 新增。`eebfb3c` 於 2026-03-26 強化 table grouping、domain-only filtering 與 example dialogue。`949472a` 讓它 user-only，並把 DDD awareness 帶入 architecture。`62f43a1` 後進入 `deprecated/`。後來的 `domain-modeling` 把一次性 export 改成工作中即時維護 terms 與 decisions。

**Invocation 與 leading concept。** Claude/Codex 皆 user-only。Leading concept 是 **一個 meaning 對應一個 canonical term**，同時列 aliases to avoid 與 ambiguity。

**Ordered mechanics。**

1. 掃描 conversation 的 domain nouns、verbs、relations。
2. 找 overloaded words、synonyms、vague terms。
3. Opinionatedly 選 canonical terms。
4. 在 working root 寫 `UBIQUITOUS_LANGUAGE.md`。
5. 依 subdomain 分組，記 relationships/cardinality、domain-expert dialogue、ambiguities。
6. Rerun 時整份讀回、吸收新 terms、更新 definitions 與 dialogue。

**Completion / failure。** 完成是 rewritten glossary 與 inline summary。雖然會指出 ambiguity，prompt 仍傾向強行 canonicalize。沒有 `contested/blocked`、provenance、safe merge、configured path、或 semantic change 的 decision record。

**Research OS target。** `skills/primitives/research-domain-modeling/SKILL.md` 是 direct adaptation。保留 canonical definitions、aliases、typed relations、collision detection、iterative refinement；再分離 construct/measure/estimand，提供 stable IDs、provenance、`proposed/contested/superseded/blocked`，並從 `.research/config.yaml` resolve paths。

**Current gap。** Research OS target 已顯著更強。僅有一個可選機制值得補：用短 dialogue 或 edge-case scenario 測試兩個 table terms 在實際使用時是否真的不同；它適合 explanatory aid，不應成 completion gate。

### 5. `git-guardrails-claude-code`

**為何存在與演變。** `30e0fdc` 在 2026-02-10 新增 `setup-git-guardrails`；同日 `b81729c` 改名為 `git-guardrails-claude-code`，把 harness binding 說清楚。`62f43a1` 移入 `misc/`，`7efc3d2` 於 2026-07-01 正式把 `misc/` 降為 non-promoted。

**Invocation 與 leading concept。** 它是 model-invoked，即使會修改 project/global Claude settings。Leading concept 是 **pre-execution denylist**。

**Ordered mechanics。**

1. 問 project 或 global scope。
2. 複製 bundled shell script 到 `.claude/hooks/` 或 `~/.claude/hooks/`。
3. 設 executable。
4. 合併 `PreToolUse` Bash hook 到 settings JSON。
5. 可再客製 blocked patterns。
6. Pipe 一個 `git push` payload，要求 exit 2。

Script 以 `jq` 讀 `.tool_input.command`，對 raw command string 跑 regex；match 就 exit 2，否則 exit 0。

**實測。**

```text
git push origin main        -> exit 2
git -C . push origin main   -> exit 0
printf git push             -> exit 2
malformed JSON              -> jq error, then exit 0
```

因此同時存在 semantic bypass、false positive 與 malformed-input fail-open。Aliases、wrapper executable、flag reorder、shell expansion、未列入 denylist 的 destructive command 也都可繞過。

**Completion / failure。** 完成是 script placement、JSON merge、executable bit、一次 negative test。雖說既有 settings 要 merge，卻沒有 deterministic merger、backup、uninstall、update、malformed-input denial、或透過 Claude 的 readback。

**Research OS disposition。** Core exclude。只保留 scope choice 與 executable negative test，且明確定位為 defense in depth。Authority 應由 agent instructions 與 operation-specific tools 執行：resolve exact target、preflight conflict、receipt/readback。

**Current gap。** Research OS 沒有 technical enforcement layer；只要文件明說這是 agent policy 而非 security boundary，即可接受。若未來加 hook，必須 structured parsing、fail-closed、harness packaging、bypass/false-positive tests。

### 6. `migrate-to-shoehorn`

**為何存在與演變。** `64b2f99` 於 2026-02-03 加入此 TypeScript migration。`c90b246` 隔日補「test code only」與 requirements interview。`62f43a1` 移入 `misc/`，`7efc3d2` 正式 demote。

**Invocation 與 leading concept。** Model-invoked。Leading concept 是 **partial test fixture**，只提供 test 真正用到的 fields。

**Ordered mechanics。**

1. 問哪些 tests 有 assertions、invalid fixture 是否刻意。
2. 安裝 `@total-typescript/shoehorn`。
3. 用 `grep` 找 `as Type` 與 `as unknown as Type`。
4. 換成 `fromPartial()`、`fromAny()`。
5. 加 imports 並跑 typecheck。

**Completion / failure。** 完成只是不具體的 typecheck green。Prompt 一面說 test-only，一面用 `npm i` 而非 dev-dependency flag。搜尋只涵蓋部分 uppercase、single-line assertions；沒有 AST transform、package-manager detection、changed-file inventory、tests、rollback，或「這個 assertion 是正確 boundary」的保留 branch。

**Research OS disposition。** Exclude。它可當「窄 migration 應有 scope -> deterministic transform -> real verifier」的反例教材，但 package、grep pattern 與 fixture semantics 都不屬於研究核心。

**Current gap。** Research prompts 無缺口。Repository meta-skill 應繼續要求 bulk mechanics 寫成 scripts，不要用 prose 指示盲改。

### 7. `scaffold-exercises`

**為何存在與演變。** `8e51ff7` 於 2026-02-20 為 Matt 的 course repo 加入。`d1beb4f` 標準化 metadata，`62f43a1` 移入 `misc/`，`7efc3d2` demote。

**Invocation 與 leading concept。** Model-invoked。Leading concept 是 **lint-ready filesystem contract**。

**Ordered mechanics。**

1. 從 plan parse sections、exercises、variants。
2. 建 numbered dash-case directories。
3. 建非空 `readme.md` 與必要的 `main.ts`。
4. 跑 `pnpm ai-hero-cli internal lint`。
5. 修到 green。
6. 後續 renumber 用 `git mv`。
7. 開頭另要求 commit，但 workflow 沒定義 commit step 或 acceptance gate。

**Completion / failure。** 唯一 crisp signal 是 proprietary linter 通過。沒有既有非空檔案、mixed numbering、缺 `pnpm`/CLI、I/O partial scaffold、使用者不接受結構等 branches。Stub writes 沒有 no-overwrite contract，自動 commit 也超出純 scaffolding。

**Research OS disposition。** Course skill exclude；保留 deterministic schema 與 validator-backed completion 到 `research-workspace-contract` 與 scripts。Research OS 已有 preview、conflict refusal、idempotence tests。

**Current gap。** `scripts/scaffold_skills.py` 仍預設 machine-specific `/Users/apple/.codex/skills/.system/skill-creator/scripts/init_skill.py`，重複 personal skill 的 portability 問題。應由 explicit argument、environment capability 或 repository config resolve；不可用時回傳清楚 blocked。

### 8. `setup-pre-commit`

**為何存在與演變。** `4458b65` 於 2026-02-10 新增，`62f43a1` 移入 `misc/`，`7efc3d2` demote。

**Invocation 與 leading concept。** Model-invoked。Leading concept 是 **commit-time feedback loop**：先 format staged files，再 typecheck/test。

**Ordered mechanics。**

1. 從 lockfile 推斷 npm/pnpm/yarn/bun。
2. 安裝 Husky、lint-staged、Prettier。
3. 跑 `npx husky init`。
4. 用偵測到的 package manager 建 hook。
5. 建 `.lintstagedrc`；沒有 Prettier config 才建 `.prettierrc`。
6. 驗證 files 並跑 `npx lint-staged`。
7. Stage 所有 changed files 並 commit。

**Completion / failure。** Checklist 涵蓋 file presence、executable、scripts 與一次 tool run；缺少 multiple lockfiles、existing non-Husky hook、既有 lint-staged config、tool-version drift、slow/flaky suite、install failure、rollback。選完其他 package manager 後仍 hard-code `npx`。Automatic stage/commit 可能帶入 unrelated user work。

**Research OS disposition。** Node-specific skill exclude。保留 environment detection、conflict preservation、observable proof。Research OS 真正 authority 是 `uv`、`docs/QUALITY_GATES.md`、`.github/workflows/validate.yml`，setup 完成不代表可自動 commit。

**Current gap。** 沒有 local pre-commit integration 不是 correctness defect；CI 與三道 documented gate 才是 source of truth。若新增 hook，只能是 optional convenience。

### 9. `edit-article`

**為何存在與演變。** 來自 initial commit `985d8fc`。`d1beb4f` 改善 description，`62f43a1` 移入 `personal/`，`0a4b767` 在 2026-05-31 明確設為 user-only；`697d4ce` 再補 Codex explicit-only policy。

**Invocation 與 leading concept。** Claude/Codex 皆 user-only。Leading concept 是 **information dependency DAG**：段落或 section 不應依賴後面才介紹的資訊。

**Ordered mechanics。**

1. 依 headings 分 sections。
2. 理解每節 main point 與資訊 dependencies。
3. 調整順序以符合 DAG。
4. 先與使用者確認 sections。
5. 逐節重寫 clarity/coherence/flow；每 paragraph 最多 240 characters。

**Completion / failure。** Prompt 到 rewrite 就結束。沒有 target file、provenance/citation、voice、change summary、逐節 acceptance、final readback、partial、或 already-correct branch。240-character 是個人偏好，卻被當 universal invariant。

**Research OS target。** 由 `skills/primitives/research-writing/SKILL.md` replace。保留 argument dependency graph 與使用者對 material narrative/scope 的 authority；Research OS 再加 claim-linked argument map、section-function contracts、calibrated claim strength、evidence/citation gates、canonical paths、readback。

**Current gap。** 不需要移植 240-character 規則。非學術 article 應另走 general writing skill，不要削弱 academic primitive。

### 10. `obsidian-vault`

**為何存在與演變。** `8e51ff7` 於 2026-02-20 加入，`d1beb4f` 補標準 frontmatter，`62f43a1` 歸到 `personal/`。其路徑與 conventions 描述的是作者本人的 WSL-mounted vault，不是 portable Obsidian interface。

**Invocation 與 leading concept。** Model-invoked。Leading concept 是 **wikilink graph**：flat note store 上用 index notes 當 navigation nodes。

**Ordered mechanics。**

1. Vault hard-code 為 `/mnt/d/Obsidian Vault/AI Research/`。
2. 用 `find`/`grep` 搜 filenames 與 contents。
3. 在 flat root 建 Title Case notes。
4. 加 `[[wikilinks]]`。
5. 用 shell 找 backlinks 與 `*Index*`。

**Completion / failure。** 無正式 completion。建 note 隱含要有 file 與 links，卻不檢查 vault existence、name collision、concurrent edits、encoding、invalid filename、backlink readback、index update。Model-invoked prompt 可直接改個人 knowledge base。

**Research OS target。** 用 `research-workspace-contract` replace storage behavior，不建 Obsidian core skill。保留 linked artifacts、single current index、configurable paths。Research OS 已從 `.research/config.yaml` resolve canonical paths、分隔 authorities、保護既有檔案、要求 readback。

**Current gap。** Version 1.0 不需 storage adapter abstraction。未來若做 Obsidian adapter，必須有 explicit vault config、note identity/collision、no-overwrite、receipt，且 note 只能連回 canonical artifact，不能成為第二 source of truth。

## Repository program architecture

### 1. Lifecycle 是 directory convention，不是 data model

`CLAUDE.md` 定義六個 buckets，只有 `engineering/` 與 `productivity/` promoted；promoted skill 要同步 root README、bucket README、docs、plugin、必要時 router。

這套 convention 可讀，但沒有 machine-readable lifecycle：

- 無 `status`、`distribution`、`replaced_by`、`since`、`removal_after`；
- deprecated `SKILL.md` 被單獨 copy 後，看起來仍像 live skill；
- 10 個 audited skills 都還有 `agents/openai.yaml`，其中 8 個可 implicit invocation；
- deprecated prompt 本身沒有 warning/replacement；
- retirement 靠人工刪除全部 prose references。

歷史已證明會 drift。`62f43a1` 起初把 `misc/` 視為 promoted 並加入 plugin；`51384f4` 的標題是「Remove deprecated skills from plugin.json」，卻也刪掉四個 `misc/` entries，使 README 與 plugin policy 不一致；直到 `7efc3d2` 才正式把 misc 定義成 non-promoted。

**Research OS disposition。** `bucket` 應只表責任分層，不兼任 lifecycle。加入 experimental/deprecated 前，catalog 至少需要：

```yaml
lifecycle: stable | experimental | deprecated
distribution: core | optional | none
replaced_by: <skill-name-or-null>
depends_on: [<skill-name>]
```

Docs、installer、plugin、deprecation views 都由此生成。Deprecated entry 必須有 replacement 或明確 no-replacement rationale；stable skill/router 不得依賴 deprecated entry。

### 2. Invocation metadata 有雙份 authority

`.agents/invocation.md` 要求 user-only skill 同時維護：

- `SKILL.md` 的 `disable-model-invocation: true`；
- `agents/openai.yaml` 的 `policy.allow_implicit_invocation: false`。

10 個 audited skills 的 pairing 都一致，只有 `ubiquitous-language`、`edit-article` user-only。但兩者 description 仍保留 “Use when…” trigger list，違反同一文件對 user-only description 的規則；證明 policy pairing green 不代表相鄰 semantics 不 drift。

Research OS 由 catalog 生成 Codex policy，避免雙寫，這對 Codex 正確；但 user-only `SKILL.md` 沒有 Claude 的 `disable-model-invocation`。

**必須決策。** 要嘛清楚宣告目前 package 是 Codex-only；要嘛生成 harness-specific views/manifests，讓 Claude install 也維持同一 user/model boundary。Generic “Agent Skills” 不應暗示只有 OpenAI metadata 才真正 enforce 的 cross-harness 等價性。

### 3. Upstream 有四種不同 distribution sets

| Surface | Pinned commit 的 effective set | Source |
|---|---:|---|
| Claude plugin | 22 promoted | `.claude-plugin/plugin.json` explicit paths |
| top-level public docs | 22 promoted | 手動 `README.md` |
| maintainer symlink install | 37 | `link-skills.sh` 安裝所有非 `deprecated/` |
| repository listing | 41 | `list-skills.sh` 列全部 |
| `skills.sh` copy installer | user-selected；repo 內沒有 exact allowlist | README 呼叫外部 installer |

Maintainer 想要 drafts/personal 工具可以是合理需求，但現在沒有一個 policy model 說明 audience；`misc/`、`personal/`、`in-progress/` 在 linker 裡完全同待遇。

`skills.sh` 更把 selection semantics 外包。README 叫使用者自己選並記得裝 `setup-matt-pocock-skills`，卻沒有 local dependency graph 證明 partial selection 包含 `ask-matt`、`to-spec`、`to-tickets` 或 shared primitives 所需依賴。Breaking dependencies 只寫在 CHANGELOG。

**Research OS disposition。** 目前安裝整份 catalog，避免 partial dependency breakage。未來若有 optional bundles，必須由 catalog 算 dependency closure，不可回到人腦記憶。

### 4. Maintainer linker 具 destructive 與 incomplete lifecycle

`scripts/link-skills.sh` 明標 dev-only，但仍有：

- conflicting real directory 先 `rm -rf` 再 symlink；
- unrelated symlink 無 conflict receipt 直接替換；
- mutation 前沒有 whole-install transactional preflight；
- removed/renamed skill 的 stale links 不會清理；
- drafts、misc、personal 全裝；
- flat basenames 無 duplicate preflight；
- `find` 結果沒轉成 audited manifest；
- `readlink -f` 有 platform assumption；
- 無 version、tree hash、source commit、uninstall receipt。

它不是 supported installer，這個聲明是正確的；Research OS 不應複製其 mechanics。

### 5. Plugin curated 正確，但仍靠人工 mirrors

`.claude-plugin/marketplace.json` 把 repo 變成 single-plugin marketplace，`plugin.json` explicit 列 promoted paths。ADR 0002 記錄當時測試：Claude 可列 path array；Codex manifest 只能給 single recursive path，cache copy 又會丟 symlinks。

優點：

- non-promoted paths 明確排除；
- managed bundle 一次裝齊 promoted dependencies；
- strict validation 當輪通過；
- marketplace/plugin names 對齊。

缺點：

- 新增或搬動 promoted skill 要人工改多個 mirrors；
- plugin validation 只驗 manifest shape，不驗 README/router/docs equality；
- plugin version 手填；
- release workflow 不跑 strict plugin validation；
- ADR 記的是 historical Codex constraint，沒有 current capability probe。

**Research OS disposition。** 不新增手寫 plugin path list。若要 managed plugin，由 catalog 生成 stable-skill paths、version 與 promoted export tree，再把 exact tree 納入 release receipt。

### 6. Manual mirrors 當輪一致，但沒有 gate 保護

當輪 programmatic comparison 證實：

- 22 promoted directories 全在 plugin，無 extras；
- 每個 bucket README 與實際 directories 一致；
- top README 只列 promoted set；
- 22 promoted skills 都有 matching docs；
- 10 個 audited invocation pairs 一致。

但 repo 沒有 tests enforce。Ghosts 已存在：

- `CONTEXT.md` 還寫 deprecated `qa`；
- `skills/engineering/setup-matt-pocock-skills/SKILL.md` 還寫 deprecated `qa`；
- `.agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md` 還用舊名 `diagnose`，而現名是 `diagnosing-bugs`。

Research OS 已有 catalog sync/structural validation，下一步應驗：

- 每個 `$skill` token 都對應 catalog dependency；
- router 覆蓋全部 user-invoked skills；
- plain-text dependency/replacement 不指向 retired name；
- 未來 root/plugin generated surfaces 完全由 catalog 對照。

### 7. Research OS installer 較安全，但還不是真 transactional

`scripts/install_skills.py` 已顯著優於 upstream linker：

- catalog 定 complete set；
- copy 前先 preflight 全部 destinations；
- 不同內容 exit 2，且不先建其他 skill；
- identical tree idempotent；
- copy 預設，symlink explicit；
- receipt 含 per-skill tree hash；
- tests 覆蓋 idempotence 與 whole-target conflict。

剩餘 gaps：

1. **Marker 未 preflight。** 既有 user-owned `.research-os-install.json` 會在成功後被覆寫。
2. **Unexpected failure 非 atomic。** 直接 copy 到 final destinations；中途 I/O error 可留下前半批。
3. **Receipt provenance 不足。** 無 catalog version、source commit、timestamp、installer version、dirty state。
4. **沒有 managed update。** 舊版 copy 一有差異就成 conflict；雖安全，但無法區分 untouched old install 與 local customization，再做 atomic upgrade。
5. **沒有 uninstall。** Marker 尚不能只移除 hash 仍相同的 installed files。
6. **Symlink mode 未完整測試。** 無 symlink conflicts、source changed、broken link cases。

完整 lifecycle 應是 `plan -> stage -> verify -> atomic promote -> receipt`；`update/uninstall` 讀 prior receipt，遇 local changes fail closed。

### 8. Release：upstream 產 tags；Research OS 產可驗證 artifacts

Upstream 用 private npm package 驅動 Changesets：

- `package.json` 只有 `changeset`、`version`；
- `.changeset/config.json` 允許 private package version/tag；
- `.github/workflows/release.yml` 在 main push 後開 version PR，再 `changeset tag`；
- 有 tags/GitHub releases，但不建 install bundle、manifest、checksum、source receipt。

當輪版本分裂：

| Surface | Value |
|---|---|
| `package.json` | `1.1.0` |
| `CHANGELOG.md` latest | `1.1.0` |
| latest `v*` tag | `v1.1.0` |
| `.claude-plugin/plugin.json` | `1.2.0` |
| `package-lock.json` root | `0.0.0` |

9 份 pending changesets 說明有 unreleased work，卻沒解決架構問題：Changesets 只知道 `package.json`，不會同步 `plugin.json`。文件要求 keep in sync，但 invariant 在 main 上暫時為 false，CI 也不檢查。

Release workflow 亦不跑 skill validation、mirror comparison、broken-reference check、tests 或 `claude plugin validate . --strict`；只裝 dependencies，再把 version/tag 交給 Changesets。

Research OS 強項：

- catalog/`pyproject.toml` version 由 validator 對齊；
- `package_release.py` 預設拒絕 dirty tree；
- sorted files、normalized timestamps、file modes；
- ZIP 內 `MANIFEST.sha256`；
- sidecar hash archive；
- `release-receipt.json` 記 source commit、version、file count。

Research OS release gaps：

1. `package_release.py` 只跑 `validate_repository.py`，不跑 `sync_catalog.py --check` 與 `pytest`；stale generated docs 或 behavioral failure 可被打包。
2. `--allow-dirty` 仍只記 `source_commit`，沒有 dirty flag 或 working-tree digest；receipt 可能讓人誤以為 archive 等於該 commit。
3. 無 packaging tests：double-build determinism、internal manifest verification、dirty refusal、extract、receipt consistency。
4. 寫完 manifest 後沒有 reopen archive 並重算所有 entries。
5. SHA sidecar 提供 integrity，不提供 authenticity；無 signing 或 remote/tag verification。
6. Artifacts 只留 local。這符合 no-external-write；未來 GitHub release 必須拆成另一個明確授權、上傳後 readback 的步驟。

### 9. Source-of-truth 對照

| Concern | Matt upstream | Research OS 現況 | Required end state |
|---|---|---|---|
| inventory | directory buckets + prose | `skills/catalog.yaml` | 保留 catalog |
| invocation | frontmatter + 手寫 OpenAI YAML | catalog + generated OpenAI YAML | 宣告 Codex-only 或生成 per-harness views |
| lifecycle | directory only | 只有 future policy | 加 lifecycle/distribution/replacement |
| dependency graph | prose/CHANGELOG | prompt `$skill` references | catalog dependencies + validator |
| public plugin set | manual explicit list | 無 native plugin | 需要時才生成 |
| local install | destructive symlink/external selector | conflict-preflighted copy/symlink | stage/atomic promote + update/uninstall receipts |
| version authority | package/plugin/lock 分裂 | catalog/pyproject 對齊 | 所有 release surfaces 由 catalog 生成 |
| release proof | tags/GitHub release | deterministic ZIP/manifest/receipt | 跑全部 gates，打包後再驗 archive |
| deprecation proof | manual bucket move | architecture prose | machine ghost scan + replacement gate |

## Prioritized Research OS gaps

### P0 — Port safety gates

1. **不得移植自動 remote issue creation 或 automatic commits。** `qa`、`request-refactor-plan`、`setup-pre-commit` 的 side effects 超出 planning/setup request；Research OS 現況正確，必須維持。
2. **不得把 regex git hook 當 authorization。** 實測 bypass 與 fail-open 已證明它最多是 convenience control。

這些是 port blockers，不是當輪 Research OS test failures。

### P1 — 對外稱 installation/release lifecycle 完成前必修

1. 在第一個 experimental/deprecated skill 出現前，catalog 加 lifecycle、distribution、replacement、dependency。
2. Validator 拒絕 unknown skill references、stale router routes、ghost replacement names。
3. Installer 在 preflight 後仍要 atomic；marker 也先 preflight；receipt 加 version/commit/dirty provenance。
4. `package_release.py` 執行三道 required gates，移除或誠實 attestation `--allow-dirty`，並驗成品 archive。
5. 加 installer/release failure tests：symlink、marker conflict、mid-copy failure、double-build、manifest recomputation。
6. 移除 `scripts/scaffold_skills.py` 的 user-specific absolute initializer path。
7. 明定 harness boundary：Codex-only，或生成 Claude/Codex invocation views。

### P2 — Managed ecosystem 需要，但 local v1 可延後

1. Receipt-aware `update/uninstall`，保留 locally modified skills。
2. 未來 plugin manifest 與 promoted export tree 全由 catalog 生成。
3. 建 manually authorized release workflow：build/verify 與 publish authority 分開。
4. CI actions pin immutable commits；release receipt 記 build-tool versions。
5. 要重訪 Codex plugin constraint，必須重新做 capability test，不可只依舊 ADR 重構 source。

## Acceptance readback

本稽核已逐一交代 10 個 skills 的存在原因與演變、invocation、leading concept、ordered mechanics、completion/failure、exact Research OS target、retain/reject mechanics 與 current gaps；也涵蓋 10 個 Codex metadata、3 個 bucket READMEs、唯一 direct script、root lifecycle rules、兩個 plugin manifests、兩個 install/discovery scripts、Changesets、package manifests、release workflow、version history，以及 Research OS catalog/install/release implementation。

稽核當下的 Research OS readback 已納入新完成的 `research-5-run`：`SYNC OK: 38 skills`、`VALIDATION OK: 38 skills, 0 errors`、`8 passed`。這組數字只保存該稽核快照；後續修補與最終 release gates 以 [`../PORT_REMEDIATION.md`](../PORT_REMEDIATION.md) 及 release receipt 為準。

本輪沒有修改任何 upstream skill 或 Research OS source。唯一新增檔案就是本文件。
