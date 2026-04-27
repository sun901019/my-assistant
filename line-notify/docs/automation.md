# Windows 自動排程

本文件教你用 Windows 工作排程器每天自動發早報與晚報。

## 排程目標

- 每天 08:00 發早報。
- 每天 20:00 發晚報。

以下假設專案位置是：

```text
C:\path\to\my-assistant
```

請改成你的實際路徑。

## 先確認手動推播成功

設定自動排程前，先手動跑一次：

```powershell
cd C:\path\to\my-assistant\line-notify
..\.venv\Scripts\python.exe .\digest.py --mode morning
```

如果手動推播失敗，不要先設定排程，請先看 `troubleshooting.md`。

## 方法 A：用工作排程器介面

1. 開啟「工作排程器」。
2. 點「建立基本工作」。
3. 名稱填入 `line-notify-morning`。
4. 觸發程序選「每天」。
5. 時間設定 `08:00`。
6. 動作選「啟動程式」。
7. 程式或指令碼填入：

```text
C:\path\to\my-assistant\.venv\Scripts\python.exe
```

8. 新增引數填入：

```text
C:\path\to\my-assistant\line-notify\digest.py --mode morning
```

9. 開始位置填入：

```text
C:\path\to\my-assistant\line-notify
```

10. 完成後，對 `line-notify-evening` 重複一次，時間改 `20:00`，引數改：

```text
C:\path\to\my-assistant\line-notify\digest.py --mode evening
```

## 方法 B：用 PowerShell 建立排程

以一般使用者 PowerShell 執行：

```powershell
$Project = "C:\path\to\my-assistant"
$Python = "$Project\.venv\Scripts\python.exe"
$Script = "$Project\line-notify\digest.py"
$WorkDir = "$Project\line-notify"

$MorningAction = New-ScheduledTaskAction -Execute $Python -Argument "`"$Script`" --mode morning" -WorkingDirectory $WorkDir
$MorningTrigger = New-ScheduledTaskTrigger -Daily -At 8:00AM
Register-ScheduledTask -TaskName "line-notify-morning" -Action $MorningAction -Trigger $MorningTrigger -Description "Send LINE morning digest"

$EveningAction = New-ScheduledTaskAction -Execute $Python -Argument "`"$Script`" --mode evening" -WorkingDirectory $WorkDir
$EveningTrigger = New-ScheduledTaskTrigger -Daily -At 8:00PM
Register-ScheduledTask -TaskName "line-notify-evening" -Action $EveningAction -Trigger $EveningTrigger -Description "Send LINE evening digest"
```

如果系統要求管理員權限，請用「以系統管理員身分執行」開啟 PowerShell。

## 手動測試排程

```powershell
Start-ScheduledTask -TaskName "line-notify-morning"
Start-ScheduledTask -TaskName "line-notify-evening"
```

查詢排程狀態：

```powershell
Get-ScheduledTask -TaskName "line-notify-morning"
Get-ScheduledTask -TaskName "line-notify-evening"
```

查看最近一次結果：

```powershell
Get-ScheduledTaskInfo -TaskName "line-notify-morning"
Get-ScheduledTaskInfo -TaskName "line-notify-evening"
```

## 刪除排程

```powershell
Unregister-ScheduledTask -TaskName "line-notify-morning" -Confirm:$false
Unregister-ScheduledTask -TaskName "line-notify-evening" -Confirm:$false
```

## macOS 附註

Sun 的本機版本使用 macOS LaunchAgent：

- `com.sunlee.line-morning`
- `com.sunlee.line-evening`

Windows 使用者不要照 macOS LaunchAgent 設定，請使用本文件的工作排程器。
