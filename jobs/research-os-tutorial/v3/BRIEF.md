---
workflow: general-video
flow: automation
storyboard: no
language: zh-TW
---

# Research OS v3 教學影片

以 56159bb46194f513d4e4499f228abf3ad6455cb1 為內容依據。保留 v2 所有檔案，新版全部放在 v3/。完整十二段新 ElevenLabs 旁白，未確認聲音與額度授權前不生成。不得用舊旁白或無聲卡充數。

概念：把模糊題目放上研究工作桌，逐步變成能回查證據的研究契約；安裝畫面展示實際驗證過的命令與回讀結果。

畫面：1920×1080、30 fps；沿用 ink #0B1020、paper #F2F4E9、amber #FFCE57，強調局部放大、真實 CLI 操作回放、分支收斂、證據流與結果對照。案例動畫標示示意，不捏造實證或假裝已執行 Agent 研究。核心 42 與選配 profile 1 分開；Codex 與 Claude 呼叫符號分開；中英文入口明確。

時長由每段實際新音訊決定。scenes.json 保存順序與分鏡並引用 narration-v3.json；alignment.json 記錄實際 PCM 切點與字幕對齊。build.py 測量每段 WAV，生成 HTML、SCRIPT、STORYBOARD、timeline.json 與字幕。音訊或內容核對紀錄缺漏時，拒絕生成正式影片。

公開來源只包含教學必要內容；帳號、認證與原始製作紀錄不納入版本控制。重製使用已保存音訊，不呼叫 TTS。
