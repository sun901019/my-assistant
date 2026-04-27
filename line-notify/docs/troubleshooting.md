# 排錯手冊

先用手動指令確認問題，再處理自動排程。

## 1. 沒收到 LINE 訊息

先執行：

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe .\digest.py --mode morning
```

如果 PowerShell 顯示 `[FAIL] 推播失敗`，常見原因如下。

## 2. 缺少 LINE_USER_ID 或 LINE_ACCESS_TOKEN

錯誤訊息可能包含：

```text
缺少環境變數：LINE_USER_ID, LINE_ACCESS_TOKEN
```

檢查：

- `.env` 是否放在 `line-notify\.env`。
- 變數名稱是否正確。
- 是否誤寫成 `LINE_CHANNEL_ACCESS_TOKEN`。
- `=` 前後不要多放奇怪符號。

正確格式：

```env
LINE_USER_ID=Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LINE_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 3. LINE 回傳 401

401 通常是 token 錯誤。

處理方式：

1. 回到 LINE Developers Console。
2. 確認使用的是 Messaging API channel 的 channel access token。
3. 重新發行 token。
4. 更新 `line-notify\.env` 的 `LINE_ACCESS_TOKEN`。
5. 重跑 `digest.py --mode morning`。

## 4. LINE 回傳 400

400 通常是 payload 或 user id 問題。

處理方式：

- 確認 `LINE_USER_ID` 是 `source.userId`，不是 channel id、basic id 或 bot id。
- 確認接收者已經把 LINE 官方帳號加為好友。
- 確認訊息文字沒有超過 LINE 限制。

## 5. 找不到 httpx

錯誤可能是：

```text
ModuleNotFoundError: No module named 'httpx'
```

安裝：

```powershell
cd C:\path\to\my-assistant
.\.venv\Scripts\python.exe -m pip install httpx
```

再測：

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe .\digest.py --mode morning
```

## 6. schedule.json 格式壞掉

錯誤可能是：

```text
json.decoder.JSONDecodeError
```

檢查 JSON：

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe -m json.tool .\schedule.json
```

常見錯誤：

- 陣列或物件最後一筆後面多逗號。
- 字串沒有用雙引號。
- `null` 寫成 `"null"`。
- `true` / `false` 寫成 `"true"` / `"false"`。

## 7. 手動成功，但工作排程器沒有發

檢查工作排程器設定：

- 「程式或指令碼」必須是 `.venv\Scripts\python.exe` 的完整路徑。
- 「新增引數」必須包含 `digest.py --mode morning` 或 `digest.py --mode evening`。
- 「開始位置」必須是 `line-notify` 資料夾。
- 電腦在排程時間必須開機。
- 使用者帳號需要有讀取專案資料夾的權限。

查詢：

```powershell
Get-ScheduledTaskInfo -TaskName "line-notify-morning"
```

如果 `LastTaskResult` 不是 `0`，代表最近一次執行失敗。

## 8. 路徑有空白

如果專案路徑包含空白，例如：

```text
C:\Users\Sun Lee\projects\my-assistant
```

工作排程器的引數請用引號包住 script：

```text
"C:\Users\Sun Lee\projects\my-assistant\line-notify\digest.py" --mode morning
```

PowerShell 指令也要用 `&`：

```powershell
& "C:\Users\Sun Lee\projects\my-assistant\.venv\Scripts\python.exe" "C:\Users\Sun Lee\projects\my-assistant\line-notify\digest.py" --mode morning
```
