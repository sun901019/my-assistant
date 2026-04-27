# LINE Notify 文件入口

> 適用讀者：會基本 Windows 操作與 PowerShell 的人，以及可以照文件執行任務的 AI 助理。

這套工具會每天產生 LINE 早報與晚報，並透過 LINE Messaging API 推播到指定使用者。

## 它能做什麼

- 早報：今日行程、近期重要行程、未完成待辦、昨日完成事項。
- 晚報：今日完成、進行中、待開始、明日行程。
- 手動推播：用 PowerShell 立刻發一則早報或晚報。
- 自動推播：用 Windows 工作排程器每天固定時間執行。

## 檔案地圖

```text
line-notify/
  digest.py              # 產生早報 / 晚報，並呼叫 LINE 推播
  line_push.py           # LINE Messaging API 推播工具
  schedule.json          # 行程與待辦資料
  .env.example           # 環境變數範本
  .env                   # 真實 token 與 user id，不要公開
  docs/
    README.md            # 本入口
    setup.md             # Windows 從零設定
    usage.md             # 日常使用
    automation.md        # Windows 自動排程
    troubleshooting.md   # 排錯
    ai-handoff.md        # 丟給 AI 的任務模板
```

## 最短成功路徑

1. 讀 `docs/setup.md`，完成 LINE Developers 設定與 `.env`。
2. 執行一次測試推播：

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe .\digest.py --mode morning
```

3. 收到 LINE 訊息後，讀 `docs/usage.md` 學會修改 `schedule.json`。
4. 要每天自動發送，再讀 `docs/automation.md` 設定 Windows 工作排程器。

## 成功標準

- PowerShell 執行 `digest.py --mode morning` 時，LINE 收到早報。
- PowerShell 執行 `digest.py --mode evening` 時，LINE 收到晚報。
- `schedule.json` 可被修改，且下一次推播內容會反映新資料。
- Windows 工作排程器可在指定時間自動執行。

## 注意事項

- 本專案使用 LINE Messaging API，不是已停用的舊 LINE Notify 服務。
- 程式讀取的 token 名稱是 `LINE_ACCESS_TOKEN`。
- `.env` 內有私密金鑰，不要貼到聊天、GitHub、截圖或公開文件。
