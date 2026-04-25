# for-codex — my-assistant 任務佇列

> Claude 規劃，Codex 實作。完成後更新狀態並寫入 from-codex.md。

---

## 🔄 Codex — [LINE-01] 每日定時通知系統

### 目標

在 `/Users/sunlee/Desktop/my-assistant/line-notify/` 建立一套每日早晚推播系統：
- **08:00 早報**：今日行程 + 今日待辦
- **20:00 晚報**：今日完成 + 明日預告

### 參考格式（照這個排版）

```
📅 胖陽早報 — 2026-04-26（日）

🔴 今日行程
━━━━━━━━━━━━━━━━━━
🔴 10:00 博覽會 2 分鐘報告
   → 800萬核准關鍵場
🟡 15:00 V2G 月報 check
   → 小眉正在幫你起草中

📌 今日待辦（3 件）
━━━━━━━━━━━━━━━━━━
🔨 能源系列簡報製作中（7張）
🔨 slide-presenter JSON 引擎設計
[ ] Docker 環境建立

✅ 昨日完成
━━━━━━━━━━━━━━━━━━
✅ V2G 研究知識庫已建立
✅ _shared/ 跨專案知識庫完成
```

晚報格式：
```
🌙 胖陽晚報 — 2026-04-26（日）

✅ 今日完成（2 件）
━━━━━━━━━━━━━━━━━━
✅ 能源系列簡報 3 張完成
✅ LINE 通知系統完成

🔨 進行中
━━━━━━━━━━━━━━━━━━
🔨 slide-presenter JSON 引擎

📅 明日行程
━━━━━━━━━━━━━━━━━━
🔴 09:00 中山大學報告
   → 發電預測內容確認
```

---

### 需要建立的檔案

#### 1. `line-notify/schedule.json`（資料存放）

```json
{
  "events": [
    {
      "id": "evt-001",
      "date": "2026-05-07",
      "time": "09:00",
      "title": "博覽會 2 分鐘報告",
      "priority": "high",
      "note": "800萬核准關鍵場",
      "done": false
    }
  ],
  "tasks": [
    {
      "id": "task-001",
      "title": "能源系列簡報製作（7張）",
      "status": "in_progress",
      "note": "3/7 完成",
      "done_at": null
    },
    {
      "id": "task-002",
      "title": "V2G 研究知識庫",
      "status": "done",
      "note": "",
      "done_at": "2026-04-25"
    }
  ]
}
```

欄位規則：
- `priority`: `"high"` → 🔴，`"normal"` → 🟡
- `status`: `"todo"` → `[ ]`，`"in_progress"` → 🔨，`"done"` → ✅
- `done_at`: 完成日期字串（YYYY-MM-DD），未完成為 `null`

---

#### 2. `line-notify/digest.py`（主邏輯）

```
執行方式：
  python3 digest.py --mode morning
  python3 digest.py --mode evening

邏輯：
  - 讀取 schedule.json
  - 依 mode 決定內容
  - morning：今日行程（today events）+ 未完成 tasks + 昨日完成 tasks
  - evening：今日完成 tasks + 進行中 tasks + 明日行程（tomorrow events）
  - 呼叫 line_push.push() 送出
  - 成功印 [OK]，失敗印 [FAIL] + 原因

依賴：
  - line_push.py（已存在，用 from line_push import push）
  - .env（LINE_USER_ID + LINE_ACCESS_TOKEN）
  - schedule.json
```

---

#### 3. `line-notify/.env.example`

```
LINE_USER_ID=Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LINE_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

#### 4. LaunchAgent plist × 2

位置：`~/Library/LaunchAgents/`

> 注意：專案已從 `~/Desktop/my-assistant/` 移至 `~/projects/my-assistant/`，plist 路徑請用：
> `/Users/sunlee/projects/my-assistant/line-notify/digest.py`

**com.sunlee.line-morning.plist**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sunlee.line-morning</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/sunlee/Desktop/my-assistant/line-notify/digest.py</string>
        <string>--mode</string>
        <string>morning</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/sunlee/Desktop/my-assistant/line-notify/morning.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/sunlee/Desktop/my-assistant/line-notify/morning.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

**com.sunlee.line-evening.plist**（同上，Hour=20，Label/log 改 evening）

---

### 安裝指令（Codex 請附在 from-codex.md）

```bash
# 啟動兩個 LaunchAgent
launchctl load ~/Library/LaunchAgents/com.sunlee.line-morning.plist
launchctl load ~/Library/LaunchAgents/com.sunlee.line-evening.plist

# 測試（立刻跑一次）
python3 /Users/sunlee/Desktop/my-assistant/line-notify/digest.py --mode morning
```

---

### 驗收標準

- [ ] `digest.py --mode morning` 跑不報錯，LINE 收到訊息
- [ ] `digest.py --mode evening` 跑不報錯，LINE 收到訊息
- [ ] LaunchAgent 兩個 plist 已放在 `~/Library/LaunchAgents/`（未 load，等老闆確認 .env 後自行 load）
- [ ] `schedule.json` 有初始資料（含本週幾個真實行程）
- [ ] `.env.example` 存在

---

### 注意

- `.env` 不存在時 `digest.py` 要能給出友善提示（不 crash）
- LaunchAgent 建立但**不自動 load**，等老闆確認 .env 設定後手動 load
- `schedule.json` 日期用 ISO 格式 `YYYY-MM-DD`
