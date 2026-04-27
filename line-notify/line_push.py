"""
Line Notify 推播工具 — 小眉用來傳訊息給老闆
使用方式：
    from line_notify.line_push import push
    push("✅ 任務已建立：V2G 月報")

需要環境變數（在專案根目錄建 .env 檔）：
    LINE_USER_ID=<老闆的 Line User ID>
    LINE_ACCESS_TOKEN=<Line Channel Access Token>
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import httpx

# 從腳本自己的目錄載入 .env（不依賴 python-dotenv）
_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

# 從環境變數讀取
LINE_USER_ID = os.getenv("LINE_USER_ID", "")
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN", "")

LINE_API_URL = "https://api.line.me/v2/bot/message/push"


def _validate_config() -> bool:
    """檢查必要環境變數是否存在。"""
    missing = []
    if not LINE_USER_ID:
        missing.append("LINE_USER_ID")
    if not LINE_ACCESS_TOKEN:
        missing.append("LINE_ACCESS_TOKEN")
    if missing:
        print(
            f"[Line Push] 缺少環境變數：{', '.join(missing)}\n"
            f"→ 請在專案根目錄建立 .env 檔，或在 shell export LINE_USER_ID=... "
            f"/ export LINE_ACCESS_TOKEN=...",
            file=sys.stderr,
        )
        return False
    return True


def push(message: str) -> bool:
    """推播文字訊息給老闆的 Line。

    Args:
        message: 要傳送的訊息內容

    Returns:
        True 表示成功，False 表示失敗
    """
    if not _validate_config():
        return False

    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message,
            }
        ],
    }

    try:
        response = httpx.post(LINE_API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            print(f"[Line Push] 失敗：{response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[Line Push] 錯誤：{e}")
        return False


def push_task_created(task_name: str, due_date: str = "", priority: str = "") -> bool:
    """任務建立後的推播通知。"""
    lines = [f"✅ 新任務已建立"]
    lines.append(f"📌 {task_name}")
    if priority:
        lines.append(f"優先級：{priority}")
    if due_date:
        lines.append(f"截止日：{due_date}")
    lines.append("→ Notion Tasks 已記錄")
    return push("\n".join(lines))


def push_reminder(task_name: str, due_date: str, message: str = "") -> bool:
    """任務提醒推播。"""
    lines = [f"⏰ 任務提醒"]
    lines.append(f"📌 {task_name}")
    lines.append(f"截止：{due_date}")
    if message:
        lines.append(message)
    return push("\n".join(lines))


if __name__ == "__main__":
    # 測試推播
    result = push("👋 小眉連線成功！Line 推播正常運作。")
    print("推播成功！" if result else "推播失敗，請檢查 token 與 user ID。")
