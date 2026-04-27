# 日常使用

日常主要改 `schedule.json`，再執行 `digest.py` 發送早報或晚報。

## 手動發早報

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe .\digest.py --mode morning
```

## 手動發晚報

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe .\digest.py --mode evening
```

## schedule.json 結構

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
    }
  ]
}
```

## 新增行程

在 `events` 陣列加入一筆：

```json
{
  "id": "evt-004",
  "date": "2026-05-30",
  "time": "10:00",
  "title": "專案進度會議",
  "priority": "high",
  "note": "準備 5 分鐘口頭更新",
  "done": false
}
```

欄位規則：

- `id`：不要跟其他 event 重複。
- `date`：使用 `YYYY-MM-DD`。
- `time`：使用 `HH:MM`，可以留空字串。
- `priority`：`high` 會顯示紅色重要，`normal` 會顯示一般提醒。
- `done`：行程完成後改成 `true`，未完成保持 `false`。

## 新增待辦

在 `tasks` 陣列加入一筆：

```json
{
  "id": "task-006",
  "title": "整理 LINE 推播文件",
  "status": "todo",
  "note": "先完成 Windows 版",
  "done_at": null
}
```

欄位規則：

- `status`: 可用 `todo`、`in_progress`、`done`。
- `done_at`: 完成日期，格式 `YYYY-MM-DD`；未完成請用 `null`。

## 標記待辦完成

把：

```json
{
  "id": "task-006",
  "title": "整理 LINE 推播文件",
  "status": "todo",
  "note": "先完成 Windows 版",
  "done_at": null
}
```

改成：

```json
{
  "id": "task-006",
  "title": "整理 LINE 推播文件",
  "status": "done",
  "note": "先完成 Windows 版",
  "done_at": "2026-04-27"
}
```

## 修改早晚報文字

推播內容由 `digest.py` 產生：

- `build_morning(schedule)`：早報。
- `build_evening(schedule)`：晚報。
- `priority_icon(priority)`：行程重要度圖示。
- `status_icon(status)`：待辦狀態圖示。

如果只要改資料，改 `schedule.json`。
如果要改訊息排版或顯示邏輯，改 `digest.py`。

## 檢查 JSON 格式

如果修改 `schedule.json` 後程式報錯，先檢查 JSON 是否有效：

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe -m json.tool .\schedule.json
```

如果 JSON 正確，PowerShell 會輸出格式化後的內容。
