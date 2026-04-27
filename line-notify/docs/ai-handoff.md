# AI 交接模板

這份文件可以直接貼給 AI，請它照文件完成 LINE 每日推播系統。

## 任務模板：從零設定

```text
你現在要幫我在 Windows 設定一套 LINE 每日早晚報推播系統。

請先閱讀以下文件：
- line-notify/docs/README.md
- line-notify/docs/setup.md
- line-notify/docs/usage.md
- line-notify/docs/automation.md
- line-notify/docs/troubleshooting.md

目標：
1. 確認 Python 與虛擬環境可用。
2. 安裝必要套件。
3. 協助我建立 line-notify\.env。
4. 確認 .env 使用 LINE_USER_ID 與 LINE_ACCESS_TOKEN。
5. 執行 digest.py --mode morning。
6. 執行 digest.py --mode evening。
7. 兩者都成功後，再協助設定 Windows 工作排程器。

限制：
- 不要把 .env 內容印出來。
- 不要把 token 貼到任何回覆。
- 如果需要我登入 LINE Developers 或提供 user id，請明確告訴我要去哪裡找。
- 如果測試失敗，請先根據 troubleshooting.md 排錯，不要猜。

成功標準：
- PowerShell 手動執行早報，LINE 收到訊息。
- PowerShell 手動執行晚報，LINE 收到訊息。
- Windows 工作排程器有 line-notify-morning 與 line-notify-evening 兩個任務。
- 回報你修改過哪些檔案、跑過哪些指令、最後狀態是成功或卡在哪裡。
```

## 任務模板：只更新行程與待辦

```text
你現在要幫我更新 line-notify\schedule.json。

請先讀：
- line-notify/docs/usage.md
- line-notify/schedule.json

我要新增或修改的內容如下：
[在這裡貼行程或待辦]

規則：
- events 的日期使用 YYYY-MM-DD。
- tasks 的 status 只能用 todo、in_progress、done。
- 完成的 task 要填 done_at。
- 不要破壞 JSON 格式。
- 修改後請用 python -m json.tool 檢查 schedule.json。

成功標準：
- schedule.json 格式正確。
- 新資料會出現在早報或晚報的正確區塊。
- 回報修改摘要。
```

## 任務模板：排錯

```text
我的 LINE 每日推播失敗。請你照 line-notify/docs/troubleshooting.md 排錯。

請先問我或檢查以下資訊：
1. 我是在手動執行失敗，還是工作排程器失敗？
2. PowerShell 完整錯誤訊息是什麼？
3. .env 是否在 line-notify\.env？
4. 變數名稱是否為 LINE_USER_ID 與 LINE_ACCESS_TOKEN？
5. schedule.json 是否能通過 python -m json.tool？

限制：
- 不要要求我公開 token。
- 不要把 .env 內容貼出來。
- 先確認手動指令成功，再處理工作排程器。

成功標準：
- 找到失敗原因。
- 提供可執行修正步驟。
- 修正後手動推播成功。
```

## AI 執行時的固定檢查指令

檢查 Python：

```powershell
python --version
```

檢查套件：

```powershell
.\.venv\Scripts\python.exe -m pip show httpx
```

檢查 JSON：

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe -m json.tool .\schedule.json
```

手動早報：

```powershell
..\.venv\Scripts\python.exe .\digest.py --mode morning
```

手動晚報：

```powershell
..\.venv\Scripts\python.exe .\digest.py --mode evening
```
