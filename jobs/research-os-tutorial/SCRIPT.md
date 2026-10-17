# SCRIPT — research-os-tutorial (v2)

**Voice:** ElevenLabs `kZ9lus3MKUfpqRaOvpJH`
**Voice settings:** multilingual v2 · `mp3_44100_128` then decoded to pcm_s16le / 44100 Hz / mono
**Voice direction:** 台灣繁體中文，清楚、沉著、有教學感；不使用廣告腔。重點句稍停頓。

**Source of truth:** the narration text lives in `scripts/regen_voice.py` → `NARRATION`.
That is what actually gets synthesized; this file mirrors it for review. Edit both together.

**Deliberate constraint:** no line speaks a skill name aloud. The v1 script said
"develop research" in line 3, which made the video wrong the moment the skill was
renamed. Naming only the *step* keeps the narration stable across renames.

**Retiming:** every take's length feeds `audio_meta.json`, and `scripts/retime.py`
recomputes `index.html` from it (scene = take + 2.0s tail, caption/audio = scene + 0.8s lead).
Never hand-edit the timings.

---

## Line 1 — Hook (Frame 1) · 16.440s

**Delivery:** 先指出常見錯誤，再收斂到 Research OS 的目的。

    只有一句模糊題目，AI 當然可以立刻寫出三十頁。但那通常只是把還不知道的地方，用流暢的文字蓋住。Research OS 的目的正好相反：先讓研究站得住，再開始寫。

## Line 2 — The six steps (Frame 2 · COMPOSABLE SKILLS) · 29.582s

**Delivery:** 六個步驟逐一唸清楚，不要趕。「過不了就停在那一步」放慢。

    它不是論文代寫器，也不是一條你只能一路走到底的大流程。固定流程最大的問題，是早期的錯誤會被一路傳到最後。這裡的六個步驟各自有明確的過關條件：逼問想法、鎖定設計、預先找碴、拆成任務、逐一執行、最後審查。過不了就停在那一步，並且告訴你卡在哪裡，不會把問題帶下去。

## Line 3 — Start (Frame 3) · 23.963s

**Delivery:** 像帶使用者操作，不要催促。

    使用時，不要只丟一個名詞。告訴它主題、最後要變成什麼、受眾是誰、目前手上有什麼，以及不能碰的限制。然後從主線第一步開始。它會先把這些變成一份可以回讀的任務紀錄，而不是假裝答案已經存在。你也可以交給自動模式，讓它自己判斷該走哪一步。

## Line 4 — One decision at a time (Frame 4) · 25.496s

**Delivery:** 「一個問題」與「代價」加重。

    第一步只做一件事：一次問一個真正需要你決定的問題。能查證的事實由 Agent 自己去查；只有目的、範圍、取捨與承諾，才交還給研究者。每個問題都會附上建議，也會說清楚採用這個建議要付出什麼代價。所有分支都收斂之後，它才會讓你進到下一步。

## Line 5 — Evidence and falsification (Frame 5) · 34.226s

**Delivery:** 節奏逐步加快，在「不算數」前停一下。

    設計鎖定之後，先不要急著拆任務。系統會查最接近的文獻，區分真正的貢獻和只是換個名字；檢查資料是不是真的拿得到；再逼你講清楚，什麼樣的結果會推翻自己的設計。這一步就像先寫一個一定會失敗的測試：標準必須事先講定，看到結果才回頭調整，不算數。必要時先做一個小型 pilot，用最低的成本確認可行性。

## Line 6 — Outputs (Frame 6 · ONE BRIEF · MANY OUTPUTS) · 34.737s

**Delivery:** 清楚列舉，不要變成廣告口播。

    所有通過驗證的狀態，最後會收斂成一份 Research Brief。它是單一的研究契約，不綁定特定受眾，也不會把還沒做的事寫成已經完成。之後才依照你的目的，轉成學術研究計畫、補助或專案企劃案、論文藍圖，或者在真的有實證結果的時候，形成論文草稿。任何時候都可以查看自己走到第幾步、手上有什麼、還缺什麼。

## Line 7 — Worked example (Frame 7 · WORKED EXAMPLE) · 30.186s

**Delivery:** 先鋪陳複雜，再在核心問題處放慢。

    舉一個實際的例子。原始構想想把波方程、熱方程、拉普拉斯，甚至 Maxwell–Boltzmann 全都放進金融預測。經過限制與審查之後，不能區分的分支被逐一刪掉，問題收斂成一句話：有限速度的阻尼傳播，能不能和普通的擴散，由資料真正區分開來。留下的不是最多的想法，而是唯一那個可以被拒絕的問題。

## Line 8 — Honest close (Frame 8) · 30.418s

**Delivery:** 沉著，不把 blocked 說成失敗。

    如果文獻邊界還沒掃完、資料還沒確認、實證還沒執行，系統就不應該捏造結果。conditional、blocked，甚至直接 kill 掉一個題目，都是有效的答案，而且比一份看起來完整、卻根本無法執行的計畫更有價值。現在，輸入你的主題，說明目的與限制，讓 Research OS 從第一個真正重要的問題開始。

---

## Write narration against the frame, not the other way round

Each line above names the frame it plays over, because the frames are fixed and
the narration has to serve them. An earlier v2 pass rewrote the script from the
skill list alone and produced three mismatches: line 2 announced "六個步驟" over a
frame arguing that rigid pipelines propagate early mistakes; line 6 described
execution over the ONE BRIEF · MANY OUTPUTS frame; line 7 described the brief
over the WORKED EXAMPLE frame. Read the frame first.

The Wave–Diffusion example stays in line 7 for that reason — frame 7 is built
around it. The full case lives in
`examples/financial-wave-diffusion/WALKTHROUGH.zh-TW.md`.

Running time grew from 2m50s to 4m01s: the v2 script keeps every evidence gate
the v1 script had and adds the step structure on top.
