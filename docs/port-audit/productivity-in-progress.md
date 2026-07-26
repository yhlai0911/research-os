# Matt productivity 與 in-progress skills 的 prompt-level port audit

> 本文件保留稽核當下的逐項證據與缺口判讀；後續已完成的修補及 v1.0 最終狀態，以 [`../PORT_REMEDIATION.md`](../PORT_REMEDIATION.md) 的機械驗證紀錄為準。

## 範圍與判準

本稽核以 2026-07-26 的本機 source of truth 為準，逐字讀完 Matt 上游下列 14 個 `SKILL.md`：

- `skills/productivity/`：`grill-me`、`grilling`、`handoff`、`teach`、`writing-great-skills`
- `skills/in-progress/`：`batch-grill-me`、`claude-handoff`、`loop-me`、`setup-ts-deep-modules`、`to-questionnaire`、`wizard`、`writing-beats`、`writing-fragments`、`writing-shape`

上游來源根目錄是 `/tmp/matt-skills-analysis.qMpo5S/repo/skills`。除了 14 個主 prompt，也完整讀過：

- 兩個 bucket 的 `README.md` 與各 skill 的 `agents/openai.yaml`，用來核對 human/model invocation；
- `teach/{MISSION,LEARNING-RECORD,GLOSSARY,RESOURCES}-FORMAT.md`；
- `writing-great-skills/GLOSSARY.md`；
- `setup-ts-deep-modules/dependency-cruiser.config.cjs`；
- `wizard/template.sh`。

Research OS 端則核對 `skills/catalog.yaml`、架構與品質文件、所有現行 orchestrator、meta skill、primitive，以及 workspace contract、renderer、templates、scripts 與測試。以下的「已覆蓋」只表示 prompt 中有可執行的同等行為；只在設計文件提過、只有 catalog entry、只有空模板，均不算已覆蓋。

分類定義：

- **direct-port**：核心 prompt contract 可直接沿用；可以換研究領域名詞，但不改變控制流程與權責。
- **adapt**：保留 leading mechanism，但必須接上 Research OS 的 config-first 路徑解析、證據狀態、決策權、canonical writeback、readback 與 side-effect gate。
- **exclude**：不應成為 Research OS 核心 skill；若有可用機制，只抽出該機制放入既有 skill。

## 結論摘要

| 上游 skill | Invocation | Leading concept | 分類 | Research OS 落點 |
|---|---|---|---|---|
| `grill-me` | user-only | thin wrapper | direct-port | `grill-research-idea` → `research-grilling` |
| `grilling` | model-invoked | relentless decision tree | direct-port | `research-grilling` |
| `handoff` | user-only | compression by reference | adapt | `research-handoff` |
| `teach` | user-only | mission / zone of proximal development | exclude | 只借用 durable learning-state 原則 |
| `writing-great-skills` | user-only | predictability | adapt | `writing-research-skills` + catalog validator |
| `batch-grill-me` | user-only | frontier rounds | adapt | `research-wayfinder` 的 opt-in branch，不另立核心 skill |
| `claude-handoff` | user-only | launch a fresh background context | exclude | portable `research-handoff`；dispatch 另設明確授權與 ack |
| `loop-me` | user-only | loop / workflow | adapt | workpackage 與 research-operations contract |
| `setup-ts-deep-modules` | user-only | deep module / pass-fail-pass | exclude | 只移植 negative proof pattern |
| `to-questionnaire` | user-only | grill the send, target the gap | adapt | future recipient-aware deliverable branch |
| `wizard` | user-only | stable runtime + variable stages | adapt | declarative contract + receipted runner |
| `writing-beats` | user-only | exploit / grounded beats | adapt | `research-writing` 的 optional narrative mode |
| `writing-fragments` | user-only | explore / fragments | adapt | pre-brief intake quarry |
| `writing-shape` | user-only | exploit / grounded blocks | adapt | interactive block mode for `research-writing` |

整體判定是 2 個 direct-port、9 個 adapt、3 個 exclude。Research OS 已明顯強於上游的部分是：canonical artifact routing、claim/decision 分權、`complete|partial|blocked`、readback、外部寫入邊界與 catalog 單一真相。最大的缺口不在研究方法，而在「怎麼和人逐步談清楚、怎麼選輸出、怎麼真正切 context、怎麼共同寫作」。

### Port implementation matrix

| Upstream | 建議 target skill | Retain mechanics | Reject mechanics |
|---|---|---|---|
| `grill-me` | `grill-research-idea` → `research-grilling` | user-only thin entry、規則只由共用 primitive 擁有 | 在 wrapper 複製 interviewing rules；未確認就執行 |
| `grilling` | `research-grilling` | dependency-first、一題一決策、每題附 recommendation、agent 查 facts、人做 decisions、確認後才結束 | 把可查 facts 問使用者；一次塞入相依問題；以 model prior 代替決策 |
| `handoff` | `research-handoff` | reference-first compression、focus tailoring、suggested skills、redaction | 無 readback 的 temp summary；handoff 檔本身冒充 upstream completion |
| `teach` | 無新增 target；狀態原則落在 `research-workspace-contract` / `research-domain-modeling` | mission、observable success、只有有證據的狀態才升級、supersession、高信任 resources | HTML lesson platform、ZPD/community subsystem、coverage 等同 learning |
| `writing-great-skills` | `writing-research-skills` | predictability、invocation boundary、leading concept、information hierarchy、completion criterion、pruning、real context boundary | 上游 harness-specific frontmatter 語意；手工 mirror inventories；只靠 prose 宣稱 forward-tested |
| `batch-grill-me` | `develop-research` + `research-wayfinder` 的 opt-in branch | dependency-proven frontier rounds、partial frontier progress、parallel fact lookup | 預設批次所有問題；把相依問題放同輪；不落地 in-flight prerequisite |
| `claude-handoff` | `research-handoff` + future portable dispatch adapter | fresh context、descriptive task name、minimal reference-first envelope | `claude --bg` 綁定、fire-and-forget、無 task ID/ack/result receipt |
| `loop-me` | `to-workpackages` 的 recurring-operations branch；規模成長後再考慮 `research-operations` | loop discovery、event-first trigger、conditional checkpoint、push right、decision brief、implementer-ready spec | 對所有研究強加 schedule/AI/checkpoint；把 spec 當 execution receipt |
| `setup-ts-deep-modules` | `research-workspace-contract` scripts/tests + repository validator | environment detection、preserve/merge、pass-fail-pass negative proof、agent context pointer | TypeScript/dependency-cruiser domain、package install、prompt/config rule count 漂移 |
| `to-questionnaire` | `render-research-deliverable` 的 recipient-aware profile | grill the send、recipient/need-back gap、priority order、single-idea questions、coverage gate | 自動寄送；把回答直接標 verified；current-directory 任意 source of truth |
| `wizard` | `research-workspace-contract` 的 contract/runner pattern；future authorized human-step runner | stable runtime / variable stages、source-to-destination trace、hidden secret input、static verification | 直接 port Bash/GitHub helpers；無逐項授權的 remote write；exit code 當 remote readback |
| `writing-beats` | `research-writing` 的 optional narrative mode | grounded concepts、2–3 reachable choices、一次一 beat、write 前重讀、natural ending | 用 beat 取代 academic argument/evidence spine；pile 清空才結束 |
| `writing-fragments` | `develop-research` intake + `research-writing` explore mode | explore/exploit boundary、從首則 prompt capture、append-only quarry、保留 user edits、leading-word mining | raw fragment 直接變 claim/decision；強迫 outline；靜默覆寫 |
| `writing-shape` | `research-writing` 的 interactive block mode | immutable input pile、candidate openings、逐 block acceptance、grounding、format argument、write 前重讀 | 缺料時憑空補；未同意就 batch drafting；以流暢 prose 修補 research validity |

---

## Productivity skills

### 1. `grill-me`

- **Invocation**：`disable-model-invocation: true`，OpenAI metadata 也設 `allow_implicit_invocation: false`；只能由使用者明確叫用。
- **Leading concept**：沒有自己的領域概念；它本身就是 **thin wrapper**。
- **Ordered mechanics**：唯一指令是「Run a `/grilling` session」。所有問答節奏、fact/decision 分工、停止條件都由 `grilling` 擁有。
- **Completion gate**：完全繼承 `grilling`；本檔沒有第二套 gate。
- **Failure / stop**：完全繼承；wrapper 不加入例外。
- **State / writeback**：無。
- **Composition**：user-only entry point 單向呼叫 model-reachable primitive。這是「人選長流程、模型執行共用 discipline」的最小範例。
- **Research OS mapping**：`grill-research-idea` 是 user-only 入口，`research-grilling` 是 model primitive，方向正確；`ask-research` 則負責建議入口而不暗中啟動。
- **目前缺少的行為**：現行 `grill-research-idea` 同時承擔 workspace resolution、九類研究分支、stress test、RDR 與 Artifact index，已不是 thin wrapper。這有合理的研究 writeback 需求，但也讓「先談一個尚未初始化、尚不值得建 workspace 的模糊想法」沒有低摩擦入口。若 `develop-research` 要承擔此入口，必須明確允許先 conversational intake、再於第一次 durable write 前建立 contract。
- **Port verdict**：**direct-port** 其 composition pattern，不新增通用 `grill-me`。保留一個短 user entry point，研究規則留在 `research-grilling`；durable orchestration 另由上層 workflow 負責。

### 2. `grilling`

- **Invocation**：唯一 model-invoked productivity skill；description 以「grill / stress-test」觸發。
- **Leading concept**：**relentless decision tree**。
- **Ordered mechanics**：
  1. 展開整棵 decision tree；
  2. 依 dependency 一次處理一個 branch；
  3. 每次只問一題，並附推薦答案；
  4. 可由環境查到的 facts 自己查；
  5. 真正 decisions 交給使用者；
  6. 每題等待回答後才繼續。
- **Completion gate**：雙方確認 shared understanding，且每個 in-scope branch 均已處理。
- **Failure / stop**：facts 不應轉嫁給使用者；多題同問被明確視為 bewildering；在使用者確認 shared understanding 前不得執行方案。
- **State / writeback**：只有 conversation state，沒有 durable artifact。
- **Composition**：作為其他 user workflow 的共用 interviewing discipline。
- **Research OS mapping**：`research-grilling` 幾乎完整直 port，並加上 prerequisite branch、RDR、fact-to-evidence、`partial|blocked`、re-read 與不執行研究的 stop boundary。
- **目前缺少的行為**：
  - `research-grilling` 強制先有 `.research/config.yaml`，因此沒有 pre-workspace 的低成本對話模式；
  - 尚未明訂「使用者在一段回答中順手回答多個後續問題」時，應先吸收全部已給答案、再只問下一個未決問題，容易機械式重問；
  - 沒有 question budget 或「資訊增益已足夠就縮短」的 adaptive depth 規則。
- **Port verdict**：**direct-port，且大致已完成**。後續修的是 adaptive runtime，不是 decision-authority 核心。

### 3. `handoff`

- **Invocation**：user-only，argument hint 是「下一個 session 要做什麼」。
- **Leading concept**：**compact by reference**。
- **Ordered mechanics**：
  1. 依目前對話與 optional argument 鎖定下一個 session；
  2. 摘要 live context；
  3. 已存在於 spec、plan、ADR、issue、commit、diff 的內容只放 path/URL，不重抄；
  4. 加入 `suggested skills`；
  5. redact credentials、password、PII；
  6. 寫到 OS temporary directory，而不是目前 workspace。
- **Completion gate**：fresh agent 能靠該文件繼續；上游沒有強制 readback、hash 或 recipient ack。
- **Failure / stop**：敏感資訊必須移除；既有 artifact 不可重複。未定義寫檔失敗、link 失效或 handoff 未被接收的狀態。
- **State / writeback**：一份 workspace 外的暫存 handoff 文件。
- **Composition**：只推薦 skills，不代替接手者啟動。
- **Research OS mapping**：`research-handoff` 已大幅強化為 canonical `HANDOFFS` artifact，包含 recipient context、next objective、verified state、artifact/version/hash、blockers、next authorized action、readback、Artifact index 與 `complete|partial|blocked`。handoff template 也有 `Received by` 與 receipt 欄位。
- **目前缺少的行為**：
  - workspace contract 壞掉或尚未建立時，現行 skill 只能 blocked，沒有安全的 emergency handoff fallback；
  - skill 要求先定義「何時 consumed」，但沒有把 consumed/accepted/expired 狀態、recipient ack 與 active pointer 納入必過 gate；
  - argument tailoring 沒有像上游一樣明說「使用者已傳入 focus 時不要再問」；
  - canonical handoff 只產檔，不形成真的 context boundary 或 dispatch receipt。
- **Port verdict**：**adapt，核心已落地**。保留 canonical manifest；另補 consumption/ack，而不是退回無 readback 的 temp summary。

### 4. `teach`

- **Invocation**：user-only，多 session、以目前目錄當 teaching workspace。
- **Leading concepts**：**mission**、**zone of proximal development**、knowledge / skills / wisdom，以及 fluency strength / storage strength。
- **Ordered mechanics**：
  1. 先以 `MISSION.md` 鎖定真實目的；模糊就先訪談；
  2. `RESOURCES.md` 蒐集高信任知識來源與 communities；
  3. 依 learning records 推估 proximal zone；
  4. 每次製作一個短、小、可很快完成的 HTML lesson；
  5. 先教足以練 skill 的 knowledge，再用 retrieval、spacing、interleaving 與 tight feedback loop 建 durability；
  6. 只有在使用者展現理解後，才更新 learning record / glossary；
  7. 需要實務 wisdom 時，導向真實 community；
  8. assets 預設重用，lesson 與 reference 互相連結。
- **Completion gates**：
  - `MISSION-FORMAT.md` 要求一個 workspace 一個 mission、具體 observable success、constraints 與 out-of-scope；
  - `LEARNING-RECORD-FORMAT.md` 只記「已證明理解、已知先備、已修正 misconception、mission shift」，不能把上過課當學會；
  - `GLOSSARY-FORMAT.md` 只收已理解術語，定義要短、canonical、可 supersede；
  - `RESOURCES-FORMAT.md` 要 primary/high-trust、逐筆註明用途、顯示 gaps 並移除低品質來源；
  - lesson 必須單一 tightly scoped win、可快速完成、連結 primary source 與 feedback。
- **Failure / stop**：mission 空白先問目的；resource 不足先查；mission 改變要先確認並留 learning record；user 不願加入 community 時必須尊重；不能以 coverage 冒充 learning。
- **State / writeback**：`MISSION.md`、`RESOURCES.md`、`NOTES.md`、`reference/*.html`、`lessons/*.html`、`assets/*`、`learning-records/NNNN-*.md`。
- **Composition**：沒有明示 skill call；依賴 primary-source research、HTML authoring、可能的 browser open。
- **Research OS mapping**：`CONTEXT` 的 mission/glossary/open decisions、`CLAIMS`、RDR supersession、templates 與 canonical paths 借用了 durable state discipline。
- **目前缺少的行為**：Research OS 沒有 lesson、ZPD、retrieval practice、learning evidence、community wisdom 或 teaching renderer。這是刻意的產品邊界，不是研究 pipeline 的 correctness bug。
- **Port verdict**：**exclude** 核心 skill。可保留「只有證明理解才升級狀態」「mission shift 要 supersede」「來源與 gaps 有紀錄」三個狀態原則，但不要把 Research OS 變成課程平台。

### 5. `writing-great-skills`

- **Invocation**：user-only；主檔是 reference，不是 ordered workflow。完整定義 progressive disclosure 到 `GLOSSARY.md`。
- **Leading concept**：**predictability**，指同一 process，不是同一 output。
- **Mechanics / reference rules**：
  - invocation 以 model context load 與 human cognitive load 取捨；user-only skills 多時用 router；
  - description 要 front-load leading word，一個真正 branch 一個 trigger；
  - information hierarchy 是 in-skill steps → in-skill reference → disclosed/external reference；
  - 每個 step 要有清楚且 demanding 的 completion criterion；
  - split 只為獨立 invocation，或用真的 context boundary 隱藏 post-completion steps；
  - co-locate 同一概念，維持 single source of truth；
  - 用 relevance 與 sentence-level no-op test 持續 pruning；
  - 以 pretrained leading word 壓縮並穩定行為；
  - failure vocabulary 包含 premature completion、duplication、sediment、sprawl、no-op、negation。
- **Completion gate**：此 skill 自身沒有 ordered finish；其 demand 是設計/審查時所有相關規則均應被套用。Glossary 特別指出，真正 context boundary 必須是 user handoff 或 subagent dispatch；inline skill call 不會清掉後續步驟。
- **Failure / stop**：以 failure-mode diagnosis 決定先 sharpen criterion、再考慮 split；不是遇到長 prompt 就拆。
- **State / writeback**：無；它是 meta reference。
- **Composition**：`SKILL.md` 的 context pointer 只在需要完整詞義時載入 `GLOSSARY.md`。
- **Research OS mapping**：`writing-research-skills` 已加入 trigger/near-miss prompts、invocation boundary、artifact/status contract、一層 disclosure、official initializer、catalog sync、validator、pytest 與 fresh-agent forward test 要求；`design-vocabulary.md` 保留核心詞彙。catalog 生成 metadata 也解掉上游 README/plugin 手工 mirror drift。
- **目前缺少的行為**：
  - 現行 reference 壓縮掉 `legwork`、`post-completion steps`、granularity 的兩種成本、context pointer wording 與 co-location 的完整診斷力；
  - meta skill 要求 fresh-agent success / near-miss / blocked forward test，但 repository tests 目前只自動驗結構、initializer 與 installer，沒有保存 prompt-level forward-test cases/receipts；
  - 多數 Research OS skills 重複相同 config resolution 與 Register-and-verify prose，形成 glossary 所稱 duplication/sprawl；應由 `research-workspace-contract` 成為唯一 runtime authority，再把各 domain skill 留下差異化 inputs/gates。
- **Port verdict**：**adapt，已完成大部分**。下一步是用自己的 pruning 原則清掉 contract boilerplate，並把 forward tests 變成可追溯 gate。

---

## In-progress skills

### 6. `batch-grill-me`

- **Invocation**：user-only。
- **Leading concept**：**frontier**；不是一次問所有問題，而是一次問所有 prerequisites 已 settled 的獨立問題。
- **Ordered mechanics**：
  1. 建 design tree；
  2. 計算目前 frontier；
  3. 每題編號並附推薦答案；
  4. 一輪問完整 frontier；
  5. 等使用者整輪回答；
  6. 依答案重算 tree/frontier；
  7. downstream 依賴尚未回答的同輪問題時，延到下一輪。
- **Completion gate**：frontier 為空、每個 branch 都走過、沒有 silent assumption，且使用者確認 shared understanding。
- **Failure / stop**：discoverable fact 必須 dispatch subagent；正在查的 fact 是 unsettled prerequisite，只擋 downstream 問題，不擋其他獨立 frontier；確認前不得執行方案。
- **State / writeback**：只有 conversation tree；無 durable map。
- **Composition**：與 subagents 平行找 facts，但人類 decisions 保留在主對話。
- **Research OS mapping**：`research-wayfinder` 有 durable fog/frontier/blocking edges、允許平行 factual investigations；`to-workpackages` 也會算 unblocked frontier；預設 `research-grilling` 仍是一題一題。
- **目前缺少的行為**：
  - 沒有 opt-in「獨立問題可同輪批次」模式，對大量互不依賴的 audience/format/resource decisions 會過慢；
  - 沒有把 in-flight evidence task 當成有 ID、有依賴邊、有狀態的 frontier node；
  - 沒有 round response 的 partial-answer 處理規則：應只重問未答或被答案改寫的節點。
- **Port verdict**：**adapt** 成 `research-grilling` / `develop-research` 的明確 branch。預設仍一題；只有 dependency graph 證明獨立且使用者接受批次時才啟用，不另建 core skill。

### 7. `claude-handoff`

- **Invocation**：user-only，接受 next-session focus argument。
- **Leading concept**：**launch a fresh background context**。
- **Ordered mechanics**：
  1. 產生和 `handoff` 同型的 redacted、reference-first summary；
  2. 一定產生 descriptive job name；
  3. 直接執行 `claude --bg --name "<name>" "<summary>"`；
  4. 立即返回，使用者透過 `claude agents` 管理。
- **Completion gate**：command 已啟動；沒有要求 child acknowledgement、summary readback、job health 或成果 receipt。
- **Failure / stop**：只規定 redaction 與不重抄 artifacts；未處理 CLI 不存在、launch 失敗、cwd 錯誤、prompt 截斷或 child 未消費 handoff。
- **State / writeback**：沒有 handoff file；summary 只成為新 agent prompt，外部 job list 是唯一狀態。
- **Composition**：把 context compression 與 vendor-specific process launch 綁成一步。
- **Research OS mapping**：`research-handoff` 刻意分離 manifest 與 dispatch，保存 canonical artifact、version/hash、next authorized action 與 readback。架構也要求 workpackage/review axis 在獨立 context 中工作。
- **目前缺少的行為**：Research OS 仍沒有一個 portable、明確授權、會回報 task/thread ID、acknowledged manifest version、完成狀態與結果 artifact 的 dispatch protocol。單純「產生 handoff」不會真的清 context。
- **Port verdict**：**exclude** 此 Claude-specific skill。若未來補 dispatch，應是 `prepare → explicit dispatch authority → child ack → bounded wait → result receipt`，支援 Codex task/subagent，而不是 port `claude --bg`。

### 8. `loop-me`

- **Invocation**：user-only，argument 可是一個 workflow，也可空白讓 agent 找 loop。
- **Leading concepts**：**loop**（生活中重複發生的 pattern）與 **workflow**（loop 的可實作 spec）。
- **Ordered mechanics**：
  1. 讀 `NOTES.md` 與既有 `workflows/*.md`；
  2. NOTES 太薄就先訪談使用者的工具、channels、術語與生活；
  3. 用 loop lens 找出值得 delegation 的重複行為，也主動提出使用者沒看見的 loop；
  4. 透過 stateful grilling 建立、修改或刪除 workflow spec；
  5. 只在實際需要時採用 trigger、checkpoint、push right、brief，不把 vocabulary 當 checklist；
  6. 直到 implementer 不必再問問題。
- **Completion gate**：workflow spec 對 implementer 完整到零追問。
- **Failure / stop**：NOTES 薄先補世界模型；任何未決問題都不能稱 done；無 evidence 要求、retry/idempotency、side-effect authorization 或 execution receipt。
- **State / writeback**：`workflows/*.md` 是 source of truth；`NOTES.md` 保存 raw world model 與 canonical terminology。只寫 spec，不實作。
- **Composition**：明確重用 `/grilling` discipline。
- **Research OS mapping**：`research-wayfinder` 管 multi-session dependencies；`to-workpackages` 產生可驗證 tracer；workpackage template 有 inputs、procedure、acceptance、falsifier、receipt；handoff 有 brief-like next action。
- **目前缺少的行為**：
  - Research OS 的 workpackage 是一次性 uncertainty-reduction slice，不是 recurring workflow；沒有 first-class trigger、schedule/event preference、idempotency key、retry、dedupe、checkpoint、push-right 或 operator brief；
  - 沒有「先發現研究團隊反覆 loops，再決定哪些值得自動化」的 discovery mode；
  - 沒有把 recurring run receipt 與一次性 artifact completion 分開。
- **Port verdict**：**adapt**。不把所有 research workpackage 變成 loop；只為真正 recurring research operations 增加一個 workflow contract 或 conditional schema，至少含 `trigger → inputs → state → action → checkpoint → retry/dedupe → receipt`。

### 9. `setup-ts-deep-modules`

- **Invocation**：user-only。
- **Leading concepts**：**deep module**，以及最重要的 runtime proof：**pass → fail → pass**。
- **Ordered mechanics**：
  1. 偵測 package manager、packages root、既有 dependency-cruiser config；
  2. 安裝 `dependency-cruiser`；
  3. 複製 config 並只改 `PACKAGES_ROOT`；
  4. 接入 `lint:boundaries` 與 umbrella check；
  5. 建可刪除的 example package；
  6. clean pass；
  7. 暫時加入 deep import，必須因 `tests-through-entrypoints` fail；
  8. 還原，再次 pass；
  9. 在 packages README 寫 convention，並從 `CLAUDE.md` / `AGENTS.md` 放 context pointer。
- **Completion gates**：每階段都有 observable done；全 skill 只有在真實觀察 pass-fail-pass 才完成。
- **Failure / stop**：既有 config 必須 merge 不覆寫；非標準 root 要確認；沒有 umbrella script 就回報 CI 待接；negative test 沒 fail 必須修，不得結案。
- **State / writeback**：package dependency、`.dependency-cruiser.cjs`、package scripts、example package、README、agent pointer。
- **Composition**：要求先用 `/codebase-design` 的 deep-module vocabulary。
- **Direct asset finding**：`dependency-cruiser.config.cjs` 實際有五個 `forbidden` entries（app boundary、cross-package boundary、tests-through-entrypoints、tests-folder-private、no-circular），而 SKILL 文字多次稱「four rules / four forbidden rules」。`intra-package freedom` 是 cross-package rule 的 exception，不是獨立 forbidden entry。這是 prompt 與 copyable config 的真實 drift。
- **Research OS mapping**：workspace initializer 已有 dry-run → apply → check；installer tests 有 conflict preflight 與 no-overwrite；validator會抓 catalog、placeholder、links、canonical keys。
- **目前缺少的行為**：
  - initializer happy-path test 沒有故意破壞 contract 再觀察 `--check` fail、修復後 pass 的 semantic negative proof；
  - prompt-level forward tests 尚未形成 pass-fail-pass receipts；
  - copyable asset 與 prompt 宣稱的 invariant 沒有機械比對，正是上游「四 vs 五」漂移的來源。
- **Port verdict**：**exclude** TypeScript skill；**directly adopt** 其 negative proof pattern 到 initializer、validator、renderer truth gate 與 skill forward tests。

### 10. `to-questionnaire`

- **Invocation**：user-only。
- **Leading concept**：**grill the send, not the subject**；問題瞄準 recipient knowledge 與 user need 之間的 **gap**。
- **Ordered mechanics**：
  1. 一次問清 recipient role、expertise、與使用者關係；
  2. 一次問清使用者需要帶回的 facts / decisions；
  3. 依 gap 寫 discovery questionnaire；
  4. 重要問題優先，問題多時依 theme 分組；
  5. 每題只問一件事、直接附 answer stub；只有容易被誤讀時才加 why-it-matters；
  6. 寫到 current directory 的 `to-questionnaire-<slug>.md` 並回報 path。
- **Completion gate**：recipient 與其獨有 knowledge 已知；need-back 是具體可行動清單；該清單每一項都有對應問題；檔案存在。
- **Failure / stop**：不逼使用者回答本來就不知道的 subject；缺 send context 就先不寫。文件鼓勵 partial answers 與 `I don't know`，避免空白被誤認為無問題。
- **State / writeback**：單一 Markdown questionnaire；上游不寄送、不追蹤回覆、不 ingest 答案。
- **Composition**：無。
- **Research OS mapping**：`evidence-research` 處理可查的 external facts；`research-handoff` 的 recipient 是接手 agent；proposal/workpackage 會列 external dependencies。但沒有針對 collaborator、domain expert、data owner 或 IRB contact 的 async knowledge-acquisition artifact。
- **目前缺少的行為**：
  - unresolved fact 若只能由特定人回答，目前常停在 `blocked`，沒有 recipient-aware output route；
  - 沒有 questionnaire ID、來源 claim/decision、requested-by、deadline/effort、敏感資訊最小化、response provenance、ingest 與 supersession gate；
  - `render-research-deliverable` 的 output profiles 尚不含 questionnaire。
- **Port verdict**：**adapt**，列為後續 output branch，不列 v1 核心入口。答案回來後必須經 evidence/decision 分流，不能直接把 recipient prose 升級為 verified claim。

### 11. `wizard`

- **Invocation**：user-only。
- **Leading concept**：**wizard**；固定且可重用的 runtime library，搭配每次不同的 procedure stages。
- **Ordered mechanics**：
  1. 先讀 repo 的 env、README、compose、framework config 與 GitHub workflow secret/var references；
  2. 列出 stages、每個 captured value 的來源、寫入位置與 secret/public 屬性，先讓使用者確認；
  3. 對每個 stage 查清 URL、點擊路徑、copy location 與 variable mapping，不知道就查 docs 或問；
  4. 複製 `template.sh`，只改 `STAGES` 以下；
  5. 以 helpers 實作 open、ask、secret input、env upsert、GitHub secret/var、pause/confirm；
  6. 設 honest stage/time estimates；
  7. `bash -n`、可用時 shellcheck、`chmod +x`；
  8. static trace 每個 value 的 source-to-destination；
  9. 不代替人 end-to-end 執行。
- **Completion gates**：stage/value matrix 完整、每條人類 journey 可照做、script syntax/static trace 通過、handoff 告知執行方式。
- **Failure / stop**：未知 UI 不得編造；irreversible action 前要 confirm；`gh` 缺失或未登入時記入 `SKIPPED`；wizard 預設 ephemeral。
- **State / writeback**：生成的 Bash script；真正執行時可改 `.env`、GitHub secrets/variables。template 會記本輪寫入的 key/name 與 skipped summary。
- **Direct script finding**：
  - library 有跨平台 browser open、hidden input、idempotent env upsert、stage progress；
  - `set_secret` / `set_var` 只以 command exit code判斷，沒有 remote readback、值 hash 或 GitHub receipt；
  - rerun 的「remember」只對 `.env` 生效，GitHub state 沒有 readback；
  - helper 不驗證 required value 是否為空或格式正確；
  - `confirm` 只是可用 helper，template 無法機械保證每個 irreversible stage 實際用了它。
- **Composition**：不呼叫其他 skill；template 是 deterministic mechanics 的 single source。
- **Research OS mapping**：`research-workspace-contract` 已將穩定 initializer script、conditional guidance、assets 分開；`pilot-study` 與 ethics skill 有 explicit authorization/receipt；renderer 把 destination contract 與 profile 分開。
- **目前缺少的行為**：沒有一個受控的人機 runner，協助完成資料存取、license、IRB、institution portal 等人工 research setup，並逐步收集 receipt。現行 skills 只能把它們列為 blocker 或由 agent直接操作。
- **Port verdict**：**adapt pattern，不 port Bash template**。先產生 declarative stage/value/authority contract，再由平台適配 runner 執行；每個 external write 都要逐項授權、identity、readback、`complete|partial|blocked`，secret 不得進 prompt 或一般 artifact。

### 12. `writing-beats`

- **Invocation**：user-only。
- **Leading concepts**：**exploit**、**grounding**、**beat**。
- **Ordered mechanics**：
  1. raw pile 固定；未給 output path 時只問一次並記住；
  2. 先和使用者確認 audience prerequisites；
  3. 從 pile 提 2–3 個不同 starting beats，標出各自會 ground 的 concepts 與解鎖方向；
  4. 使用者選一個後，只寫該 beat；
  5. 從 disk 重讀 article；
  6. 提 2–3 個目前 grounded set 可到達的 next beats；
  7. 使用者選擇、一次只 append 一 beat；
  8. 直到 journey 自然完成，而不是 pile 用完。
- **Completion gate**：每個 beat 只做一個 move、依賴的 concepts 已 grounded、使用者選擇後才寫、文章 journey 有自然終點。過長且含多個 move 的 beat 必須 split。
- **Failure / stop**：想用 ungrounded concept 時，只能先加 grounding beat 或經使用者決定升為 prerequisite；使用者改舊 beat 時必須重算後續；可針對特定 beat rewrite，不動其他內容。
- **State / writeback**：article file 逐 beat append；grounded set 只在 conversation 中維持，沒有 durable ledger。
- **Composition**：無。
- **Research OS mapping**：`research-writing` 有 evidence-led cumulative argument、paragraph job、section function、claim mapping；`to-paper-draft` 有 argument spine、evidence gate、review/readback。
- **目前缺少的行為**：
  - 現行 writing flow 會在確認 argument spine 後直接「draft sections」，沒有候選 opening/next move、使用者選路、一次一 beat 的協作節奏；
  - 沒有 audience prerequisite / grounded-concept tracking；
  - 多數 writeback 只要求完成後 readback，沒有「每次寫前重讀 target，保留使用者中途修改」；
  - 沒有 natural-ending gate，較容易把所有可用 material 都塞進稿件。
- **Port verdict**：**adapt** 成 optional narrative mode。學術稿核心仍是 argument/evidence，不採 choose-your-own-adventure 作為唯一 contract；適合 introduction、discussion、public-facing research narrative。

### 13. `writing-fragments`

- **Invocation**：user-only。
- **Leading concepts**：**explore** 與 **fragment**；尤其鼓勵找能統攝整篇的 leading word。
- **Ordered mechanics**：
  1. 不做 phase、outline 或 article structure；
  2. 以 grilling 持續挖使用者與 agent 對話中的可用 fragments；
  3. 未給 path 時只問一次；
  4. 從第一則 prompt 就開始 capture；
  5. 首次寫入只有一個 working-title H1；
  6. fragments 以 horizontal rule 分隔，沒有 body headings、tags 或重排；
  7. 每次寫前從 disk 重讀；
  8. 預設安靜 append；使用者可 cut、rewrite、merge 指定 fragment。
- **Completion gate**：沒有有限終點，因為它是 ongoing quarry。單一 fragment 的門檻是「作者看得懂且可能留到成稿」，不是 cold reader 可獨立理解。
- **Failure / stop**：一旦開始強迫結構就是越界到 exploit；不可盲目 overwrite 或還原使用者刪除/重排；不要為每個 fragment 打斷對話要求 save confirmation。
- **State / writeback**：一份 append-oriented raw Markdown pile。
- **Composition**：概念上依賴 grilling，但不另呼叫 skill。
- **Research OS mapping**：`CONTEXT`、domain maps、claims 與 RDR 都是 canonical/structured state；它們適合已辨識的 construct、fact、decision，不適合未成熟的作者 noticing。
- **目前缺少的行為**：
  - Research OS 沒有「raw author material」層，早期想法容易被過早轉成 research claim、decision 或正式 brief；
  - 沒有 explore → exploit 的明確 promotion gate；
  - 沒有同時保存 `verbatim user fragment`、`agent paraphrase`、來源 turn/file 與 acceptance state；
  - 沒有 append-before-next-question 的對話寫回節奏。
- **Port verdict**：**adapt** 成 pre-brief intake quarry。它必須與 `CLAIMS` 隔離，預設 `unstructured/unaccepted`；只有使用者確認或 evidence verification 後，才各自升級為 decision、construct 或 claim。

### 14. `writing-shape`

- **Invocation**：user-only。
- **Leading concepts**：**exploit**、**grounding**、逐 block shaping。
- **Ordered mechanics**：
  1. 先把 raw pile end-to-end 讀完，且保持 read-only；
  2. 未給 article path 時只問一次；
  3. 和使用者確認 audience prerequisites；
  4. 提 2–3 個暗示不同 thesis/angle 的 openings，迫使使用者 pick 或組 hybrid；
  5. 每次問「在這個 opening 與目前 grounded set 下，reader 下一步需要什麼？」；
  6. 從 quarry 挖 material，並和使用者公開辯論 prose/list/table/callout/quote/code 的格式；
  7. 每個 agreed block 立即 append，不 batch；
  8. 每次寫前重讀 article；
  9. pile 缺關鍵 material 時，明說要補例子或砍 section；
  10. 使用者決定文章何時完成。
- **Completion gate**：opening 承諾與後文一致；每個 block 只有一個可辯護功能；每個依賴 concept 已 grounded；格式選擇有理由；raw pile 未修改；使用者確認完成。
- **Failure / stop**：弱 transition 要 push back；不賺取位置的 paragraph 要 cut；pile 缺料不得憑空補；不得出版、加未要求 frontmatter 或修改 input。
- **State / writeback**：raw pile read-only，article file incremental；grounded set 是 runtime state。
- **Composition**：無。
- **Research OS mapping**：`research-writing` 已有 section conclusion、logical claim order、verified claim mapping、section functions、citation/causality gate與 canonical writeback；renderer 新增 destination profile 與 source matrix。
- **目前缺少的行為**：
  - 沒有 paragraph/block-level user acceptance；argument map 確認後仍可能一次產出大量 prose；
  - 沒有 immutable input-pile identity/hash 與「不得改 input」gate；
  - 沒有 grounded-concept set 或 prerequisite decision；
  - 沒有格式辯論與 repeat-shape-to-table 的明確規則；
  - 沒有每次 write 前 re-read，因此 user-in-the-loop 共編時仍有覆蓋風險；
  - renderer 解決「產物類型」，尚未解決「共同成形的節奏」。
- **Port verdict**：**adapt** 成 `research-writing` 的 interactive block mode。保留 Research OS 的 evidence gate、claim strength、citation 與 canonical output；只引入它的 co-authoring loop。

---

## 跨 skill 的優先缺口

### P0 — 建立真正 adaptive 的對話主流程

目前 `ask-research` 是 router，各 orchestrator 多半是固定 Stage 1 → Stage N；`research-grilling` 則固定一題一題。兩者都正確，但中間缺一個能依使用者當下成熟度調整深度的 control loop。

建議 `develop-research` 以 **adaptive loop** 明訂：

1. 接受 topic、方向、問題、來源、半成品或既有 artifact，不要求使用者先知道該叫哪個 skill；
2. 先吸收使用者已給的所有 facts、preferences 與 decisions，避免模板式重問；
3. 將可查 facts、需人決定、外部 access、raw author material 分流；
4. 每回合選資訊增益最高的下一個 decision；只有 frontier 經證明互相獨立時，才 opt-in 批次；
5. 能查的 facts 平行查，將 in-flight evidence task 寫成有 ID/依賴/status 的 node；
6. 每次回答後重新計算，不把原始 stage checklist 當必走流程；
7. 在第一次 durable write 前建立或解析 workspace contract；conversation intake 本身不應因 workspace 尚未初始化而無法開始；
8. 當 requested destination 的 readiness gate 已達成就停止，不為了跑完整個 Research OS 而繼續問；
9. 每回合回報目前已確定、尚缺什麼、下一題為何能解鎖產物。

驗收不能只是「prompt 看起來 adaptive」。至少要有 fresh-agent forward tests：

- 一句完整 brief 幾乎不追問；
- 一個模糊題目逐步收斂；
- 使用者一段話回答多個 branches 時不重問；
- 兩個獨立 decisions 可批次、相依 decisions 不可批次；
- 找不到 load-bearing evidence 時停在 `blocked`；
- 使用者中途改目標時 supersede，而不是把新舊方向混在同一 artifact。

### P0 — 完成 output routing，分開 source contract 與 rendered artifact

`render-research-deliverable` 已建立正確方向：Research Brief 是 audience-neutral source contract，plan/proposal/blueprint/manuscript 是 destination profile；真實狀態不能被漂亮 prose 升級。仍需收緊：

- 入口要先取得 `destination + audience + use/decision + required format/template + language + path/export preference`，但使用者已給的欄位不能重問；
- canonical source 與 export/rendered copy 必須分開。canonical ID/status 留在 `.research/`，使用者指定的 DOCX/PDF/Markdown 路徑是 derived output，兩者各有 hash/readback；
- `academic research plan`、`grant/institutional proposal`、`project proposal`、`paper blueprint`、`manuscript draft` 要各自有 completion gate，不能只靠共享 prose；
- 缺結果時只產 blueprint/outline；缺 authority 時 proposal 只能 partial；缺 source brief 時 blocked；
- 需要外部專家回答的 gap 應能 route 到 recipient-aware questionnaire，而不是硬塞進 proposal 或永遠停在聊天；
- 所有 wrapper 只能傳 destination contract 給 renderer，不能各自複製 truth/writeback rules；
- catalog、pointer 名稱與 skill composition 必須由 validator 做 ghost-reference check，避免 wrapper 指向不存在或已更名的 skill。

### P0 — 把 workspace mechanics 收斂成真正 single source of truth

Research OS 多數 skills 重複約一整段 config-first resolution、Artifact index、`complete|partial|blocked` 與 readback prose。這些規則很重要，但重複本身會製造：

- token/context load；
- adapter key 或 status wording 漂移；
- domain prompt 被 boilerplate 淹沒；
- 修改 contract 時必須多檔同步。

`research-workspace-contract` 應成為唯一 authority：

- setup wrapper 只傳 explicit objective；
- model primitives 只宣告「需要哪些 canonical bindings、會改哪些 artifact、domain-specific gate」；
- deterministic resolution、schema validation、register/upsert、supersession、readback receipt 由共享 script 或共用 contract 執行；
- 每個 domain skill 仍保留自己的 stop branch，不能因抽象化而把「哪一項 research evidence 才算 pass」交給 generic helper。

完成標準是刪除重複後行為仍由 success、near-miss、blocked、adapter-path、conflict、readback-failure 測試證明，而不是只剩一個「請遵守 workspace contract」的弱 pointer。

### P1 — 讓 context boundary 成為可觀察事件

架構文件已說 workpackage、review axis、handoff 是 context boundaries，但 prompts 仍多為同一長 context 內 inline 組合。真正 boundary 應有：

```text
context envelope
  = objective
  + immutable/canonical input pointers
  + allowed reads/writes
  + completion criterion
  + stop branches
  + expected output/receipt
```

需要補：

- subagent/thread/task ID；
- child 對 envelope 與 handoff version 的 acknowledgement；
- 狀態 `queued|running|needs-input|complete|partial|blocked`；
- output artifact ID/hash/readback；
- aggregation 前的 target-version check；
- handoff consumed/expired/ superseded；
- parent 不把完整 conversation 塞給 child，也不把 inline skill call誤稱為 context break。

這會同時補上 `claude-handoff` 的速度優點與 Research OS 要求的 portability/receipt。

### P1 — 增加 evidence-safe 的共同寫作模式

Research OS 現有寫作的 truth gate 很強，但 interaction model 偏「先確認 argument map，再大量生成」。建議在同一 evidence authority 下增加三種明確模式：

1. **Explore / fragments**：保存 raw user material、來源與 acceptance；不升級成 verified claim，也不強迫 outline。
2. **Shape / blocks**：input pile read-only；先定 audience prerequisites，候選 openings，逐 block 選擇、格式辯論、寫前重讀、保存 user edits。
3. **Draft / audit**：依 Research Brief、claim chain 與 section function 完稿，再跑 citation/research review。

共同 invariant：

- 每個 material claim 都維持來源與 evidence strength；
- `grounded` 只代表讀者已被介紹，不代表 claim 已被驗證；
- 每次寫前 re-read target；每次寫後 readback；
- user edit 優先，agent 不以舊 in-context copy 覆蓋；
- raw pile、canonical research contract、rendered draft 是三個不同 authority；
- article 在 argument 完成時停，不在 pile 清空時停。

### P1 — 為 recurring research operations 補 workflow contract

只在確實重複的工作使用下列 schema，不強迫每個研究流程都排程化：

```text
trigger → inputs/provenance → durable state → idempotency/dedupe
→ action → checkpoint pushed right → decision brief
→ retry/stop → receipt/readback
```

這可涵蓋定期 data refresh、literature alert、replication monitor、submission checklist 等；與一次性 workpackage、pilot、handoff 的 status 必須分開。

### P1 — 用 negative proof 與 forward receipts 驗 prompt

結構 validator 已很好，但不足以證明 prompt 行為。優先新增：

- workspace initializer：clean pass → 故意破壞 required key/header/type → check fail → repair → pass；
- output renderer：完整 brief 成功；缺 results 只能 blueprint；缺 authority proposal partial；錯誤 adapter 不可 fallback；
- research grilling：fact 不問人、decision 不自作主張、一次一 dependent question；
- writing：使用者中途改檔後不覆蓋、ungrounded concept 不可直接使用、raw pile 不可被修改；
- handoff：broken pointer、hash mismatch、unacknowledged recipient 不得 complete。

每個 forward test 要保存 raw prompt、workspace fixture、預期 process events、實際 artifact/receipt 與 verdict。只測最後文字不像在測 skill。

### P2 — 明確維持排除邊界

- `teach`：除非產品要做 research-methods tutor，否則不加入 lessons/ZPD/community subsystem。
- `claude-handoff`：不綁 Claude CLI；只取 real-context-boundary 的需求。
- `setup-ts-deep-modules`：不進 Research OS；只取 pass-fail-pass 與「prompt/asset invariant 必須機械一致」。
- `wizard`：不直接複製會寫 `.env` / GitHub 的 Bash library；任何研究 portal、IRB、license runner 都必須另有逐項授權與 receipt。

## 最終 port 順序

1. 完成 `develop-research` adaptive loop，並用 forward tests 證明不重問、不過度訪談、會隨 evidence/decision 重算。
2. 以 `research-workspace-contract` 收斂 duplicated mechanics，同時保留 domain gates。
3. 封好 `render-research-deliverable` 的 destination/profile/readback contract，補 recipient-aware questionnaire branch。
4. 讓 handoff/subagent dispatch 具備真正 context boundary、ack 與 result receipt。
5. 在 `research-writing` 內加入 explore fragments、interactive block shaping、draft/audit 三種 evidence-safe 模式。
6. 為真正 recurring operations 增加 conditional loop schema。
7. 建立 prompt-level forward-test receipts 與 pass-fail-pass negative tests。

若只能先做一件事，應先做第 1 項。現在的研究 primitives 已夠深，但缺少 adaptive conversation 會讓使用者必須先理解系統架構、選對 skill、再配合固定 stages；這是目前最大的產品摩擦，也會放大後續 output routing、context 與 writing 的所有問題。
