"""
每日早晚報推播
用法：
    python3 digest.py --mode morning
    python3 digest.py --mode evening
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# 載入同目錄的 line_push
sys.path.insert(0, str(Path(__file__).parent))
from line_push import push

SCHEDULE_FILE = Path(__file__).parent / "schedule.json"

WEEKDAY_ZH = ["一", "二", "三", "四", "五", "六", "日"]


def load_schedule() -> dict:
    if not SCHEDULE_FILE.exists():
        return {"events": [], "tasks": []}
    with open(SCHEDULE_FILE, encoding="utf-8") as f:
        return json.load(f)


def priority_icon(priority: str) -> str:
    return "🔴" if priority == "high" else "🟡"


def status_icon(status: str) -> str:
    return {"done": "✅", "in_progress": "🔨", "todo": "[ ]"}.get(status, "[ ]")


def format_date_header(d: date) -> str:
    weekday = WEEKDAY_ZH[d.weekday()]
    return f"{d.month}/{d.day}（{weekday}）"


def build_morning(schedule: dict) -> str:
    today = date.today()
    yesterday = today - timedelta(days=1)
    lines: list[str] = []

    lines.append(f"📅 李老闆早報 — {format_date_header(today)}")
    lines.append("")

    # 今日行程
    today_events = [
        e for e in schedule.get("events", [])
        if e.get("date") == today.isoformat() and not e.get("done")
    ]
    if today_events:
        lines.append("🗓 今日行程")
        lines.append("━━━━━━━━━━━━━━━━━━")
        for e in sorted(today_events, key=lambda x: x.get("time", "")):
            icon = priority_icon(e.get("priority", "normal"))
            time_str = e.get("time", "")
            title = e["title"]
            note = e.get("note", "")
            lines.append(f"{icon} {time_str + ' ' if time_str else ''}{title}")
            if note:
                lines.append(f"   → {note}")
        lines.append("")

    # 近期高優先行程（非今日）
    upcoming = [
        e for e in schedule.get("events", [])
        if e.get("date", "") > today.isoformat()
        and e.get("priority") == "high"
        and not e.get("done")
    ]
    if upcoming:
        lines.append("📌 近期重要行程")
        lines.append("━━━━━━━━━━━━━━━━━━")
        for e in sorted(upcoming, key=lambda x: x.get("date", ""))[:3]:
            d = date.fromisoformat(e["date"])
            lines.append(f"🔴 {format_date_header(d)} {e.get('time', '')} {e['title']}")
            if e.get("note"):
                lines.append(f"   → {e['note']}")
        lines.append("")

    # 今日待辦（未完成）
    pending_tasks = [t for t in schedule.get("tasks", []) if t.get("status") != "done"]
    if pending_tasks:
        lines.append(f"📌 待辦（{len(pending_tasks)} 件）")
        lines.append("━━━━━━━━━━━━━━━━━━")
        for t in pending_tasks:
            icon = status_icon(t.get("status", "todo"))
            note = f"（{t['note']}）" if t.get("note") else ""
            lines.append(f"{icon} {t['title']}{note}")
        lines.append("")

    # 昨日完成
    done_yesterday = [
        t for t in schedule.get("tasks", [])
        if t.get("status") == "done" and t.get("done_at") == yesterday.isoformat()
    ]
    if done_yesterday:
        lines.append("✅ 昨日完成")
        lines.append("━━━━━━━━━━━━━━━━━━")
        for t in done_yesterday:
            lines.append(f"✅ {t['title']}")

    return "\n".join(lines).strip()


def build_evening(schedule: dict) -> str:
    today = date.today()
    tomorrow = today + timedelta(days=1)
    lines: list[str] = []

    lines.append(f"🌙 胖陽晚報 — {format_date_header(today)}")
    lines.append("")

    # 今日完成
    done_today = [
        t for t in schedule.get("tasks", [])
        if t.get("status") == "done" and t.get("done_at") == today.isoformat()
    ]
    if done_today:
        lines.append(f"✅ 今日完成（{len(done_today)} 件）")
        lines.append("━━━━━━━━━━━━━━━━━━")
        for t in done_today:
            lines.append(f"✅ {t['title']}")
        lines.append("")

    # 進行中
    in_progress = [t for t in schedule.get("tasks", []) if t.get("status") == "in_progress"]
    if in_progress:
        lines.append("🔨 進行中")
        lines.append("━━━━━━━━━━━━━━━━━━")
        for t in in_progress:
            note = f"（{t['note']}）" if t.get("note") else ""
            lines.append(f"🔨 {t['title']}{note}")
        lines.append("")

    # 未開始（最多顯示3件）
    todo = [t for t in schedule.get("tasks", []) if t.get("status") == "todo"]
    if todo:
        lines.append(f"[ ] 待開始（{len(todo)} 件）")
        lines.append("━━━━━━━━━━━━━━━━━━")
        for t in todo[:3]:
            lines.append(f"[ ] {t['title']}")
        if len(todo) > 3:
            lines.append(f"    …還有 {len(todo) - 3} 件")
        lines.append("")

    # 明日行程
    tomorrow_events = [
        e for e in schedule.get("events", [])
        if e.get("date") == tomorrow.isoformat() and not e.get("done")
    ]
    if tomorrow_events:
        lines.append(f"📅 明日行程（{format_date_header(tomorrow)}）")
        lines.append("━━━━━━━━━━━━━━━━━━")
        for e in sorted(tomorrow_events, key=lambda x: x.get("time", "")):
            icon = priority_icon(e.get("priority", "normal"))
            time_str = e.get("time", "")
            lines.append(f"{icon} {time_str + ' ' if time_str else ''}{e['title']}")
            if e.get("note"):
                lines.append(f"   → {e['note']}")
    else:
        lines.append(f"📅 明日行程（{format_date_header(tomorrow)}）")
        lines.append("━━━━━━━━━━━━━━━━━━")
        lines.append("目前無排程行程")

    return "\n".join(lines).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="每日 LINE 推播")
    parser.add_argument("--mode", choices=["morning", "evening"], required=True)
    args = parser.parse_args()

    schedule = load_schedule()

    if args.mode == "morning":
        message = build_morning(schedule)
    else:
        message = build_evening(schedule)

    print(message)
    print("\n--- 推播中 ---")

    ok = push(message)
    if ok:
        print("[OK] 推播成功")
    else:
        print("[FAIL] 推播失敗，請確認 .env 設定")
        sys.exit(1)


if __name__ == "__main__":
    main()
