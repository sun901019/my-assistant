# Windows 從零設定

本文件教你在 Windows 上把 LINE 每日推播系統跑起來。

## 需要準備

- Windows 10 或 Windows 11。
- PowerShell。
- Python 3.11 以上。
- 一個 LINE 帳號。
- 一個 LINE Developers Provider 與 Messaging API channel。
- 專案資料夾，例如：

```text
C:\Users\你的名字\projects\my-assistant
```

以下指令請把路徑改成你自己的專案位置。

## 1. 確認 Python

在 PowerShell 執行：

```powershell
python --version
```

成功時會看到類似：

```text
Python 3.11.8
```

如果找不到 Python，請安裝 Python，並勾選「Add python.exe to PATH」。

## 2. 建立虛擬環境

```powershell
cd C:\path\to\my-assistant
python -m venv .venv
```

安裝需要的套件：

```powershell
.\.venv\Scripts\python.exe -m pip install httpx
```

目前程式不依賴 `python-dotenv`，因為 `line_push.py` 會直接讀 `line-notify\.env`。

## 3. 建立 LINE Messaging API channel

1. 開啟 LINE Developers Console。
2. 建立或選擇一個 Provider。
3. 建立 Messaging API channel。
4. 進入 channel 的 Messaging API 設定頁。
5. 建立或複製 Channel access token。
6. 把 LINE 官方帳號加為好友，後續才能收到 push message。

你需要兩個值：

- `LINE_ACCESS_TOKEN`：Messaging API channel access token。
- `LINE_USER_ID`：接收推播的使用者 ID。

## 4. 取得 LINE_USER_ID

常見做法有兩種：

### 方法 A：從 webhook 事件取得

1. 在 LINE Developers 啟用 Webhook。
2. 用一個可接收 webhook 的服務，例如 ngrok + 本機小伺服器、或暫時使用 webhook 測試工具。
3. 用自己的 LINE 傳訊息給官方帳號。
4. 在 webhook event 內找到 `source.userId`。
5. 把該值填入 `.env` 的 `LINE_USER_ID`。

### 方法 B：請 AI 或工程師幫你做一次 webhook 擷取

如果你不熟 webhook，直接把 `docs/ai-handoff.md` 貼給 AI，請它協助你取得 `LINE_USER_ID`。這一步需要你能登入 LINE Developers，並能提供測試訊息。

## 5. 建立 .env

複製範本：

```powershell
cd C:\path\to\my-assistant\line-notify
Copy-Item .env.example .env
```

用文字編輯器打開 `.env`，填入：

```env
LINE_USER_ID=Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LINE_ACCESS_TOKEN=你的_channel_access_token
```

注意：變數名稱必須是 `LINE_ACCESS_TOKEN`，不是 `LINE_CHANNEL_ACCESS_TOKEN`。

## 6. 第一次測試

執行早報：

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe .\digest.py --mode morning
```

執行晚報：

```powershell
..\.venv\Scripts\python.exe .\digest.py --mode evening
```

成功時 PowerShell 會看到：

```text
--- 推播中 ---
[OK] 推播成功
```

你的 LINE 也會收到訊息。

## 7. 驗收清單

- [ ] `python --version` 可正常顯示版本。
- [ ] `.venv` 已建立。
- [ ] `httpx` 已安裝。
- [ ] `line-notify\.env` 已填入 `LINE_USER_ID`。
- [ ] `line-notify\.env` 已填入 `LINE_ACCESS_TOKEN`。
- [ ] `digest.py --mode morning` 可推播成功。
- [ ] `digest.py --mode evening` 可推播成功。
