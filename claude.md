# my-assistant 專案規則

## 專案簡介

胖陽的個人助理系統，包含：
- `slide-presenter/` — Vue 3 互動簡報播放器（GitHub Pages 部署）
- `line-notify/` — LINE 每日早晚報推播系統

---

## LINE 通知工作流

### 指令對照

| 使用者說 | Claude 動作 |
|---------|------------|
| 發早報、發一條早報、現在發早報 | `Bash: ~/projects/my-assistant/.venv/bin/python3 ~/projects/my-assistant/line-notify/digest.py --mode morning` |
| 發晚報、發一條晚報、現在發晚報 | `Bash: ~/projects/my-assistant/.venv/bin/python3 ~/projects/my-assistant/line-notify/digest.py --mode evening` |
| 更新行程、加行程、加一個行程 | 讀 `line-notify/schedule.json` → 編輯對應欄位 → 存檔 |
| 更新待辦、加待辦、完成某件事 | 讀 `line-notify/schedule.json` → 更新 tasks 欄位 → 存檔 |
| 看早報內容、預覽早報 | 執行 morning 腳本但只 print，不推播（用 `--dry-run` 若有，否則看 stdout） |

### schedule.json 結構

```json
{
  "events": [
    {
      "date": "YYYY-MM-DD",
      "time": "HH:MM",
      "title": "標題",
      "priority": "high | normal",
      "note": "備註（選填）",
      "done": false
    }
  ],
  "tasks": [
    {
      "title": "任務標題",
      "status": "todo | in_progress | done",
      "note": "備註（選填）",
      "done_at": "YYYY-MM-DD（完成時填）"
    }
  ]
}
```

### Python 環境

- venv 路徑：`~/projects/my-assistant/.venv/`
- 執行 Python：`~/projects/my-assistant/.venv/bin/python3`
- 已安裝套件：`python-dotenv`, `requests`, `httpx`
- `.env` 位置：`line-notify/.env`（含 LINE_ACCESS_TOKEN、LINE_USER_ID）

### 自動排程（LaunchAgent）

| 時間 | Label |
|------|-------|
| 08:00 每天 | `com.sunlee.line-morning` |
| 20:00 每天 | `com.sunlee.line-evening` |

plist 位置：`~/Library/LaunchAgents/`

---

## 簡報工作流

### 三種簡報類型

| 類型 | 觸發詞 | 格式 | 位置 | 設計系統 |
|------|--------|------|------|---------|
| **A. JSON 簡報**（Vue 渲染） | 「做成簡報」「概念教學」「快速做一個」 | JSON | `src/data/slides/{slug}.json` | Vue 元件 |
| **B. 互動式簡報** | **明確說「互動式簡報」**、「有程式碼步驟」「設定教學」「有 quiz」「有表單」 | 靜態 HTML | `public/slides/{slug}.html` | 深色 GitHub 風（git-github.html） |
| **C. 一般簡報** | **明確說「一般簡報」**、「簡報」、「slide」、演講/分享用途 | 靜態 HTML | `public/slides/{slug}.html` | html-ppt skill（暖色 Instrument Serif/Geist） |

**不確定時**：問使用者「互動式還是一般簡報？」，只問這一個問題。

---

### Type A：JSON 簡報流程

1. 讀取使用者提供的 .md 或文字
2. 依 `slide-presenter/src/data/slides/api-basics-json.json` 格式產出 JSON
3. 存到 `slide-presenter/src/data/slides/{slug}.json`
4. 在 `slide-presenter/src/data/courses.ts` 新增 entry（type: 不填或 `'vue'`）
5. git add → commit → push

Step types：`welcome` / `cards` / `analogy` / `calculator` / `selector` / `quiz` / `summary`

---

### Type B：互動 HTML 簡報流程

Design system 一律參照 `slide-presenter/public/slides/git-github.html`：
- 字型：`Noto Sans TC` + `JetBrains Mono`
- 色系：深色 `#0d1117`（GitHub 風格，使用 CSS 變數 `--bg/--bg2...`）
- Layout：`header`（badge + dots + 進度條）+ `.main`（`.slide` 絕對定位）+ `footer`（prev/next）
- 動畫：`translateX(40px)` slide-in transition

步驟：
1. 複製 git-github.html 的 CSS 框架，只改內容
2. 存到 `public/slides/{slug}.html`
3. 在 `slide-presenter/src/data/courses.ts` 新增 entry（`type: 'html'`, `htmlPath: '/my-assistant/slides/{slug}.html'`）
4. git add → commit → push

> 超過 50 行的 HTML 內容撰寫 → delegate 給 Codex，附上 git-github.html 路徑作為 design reference

---

### Type C：一般簡報流程（html-ppt skill）

啟動 `Skill("html-ppt")`，依 skill 規範製作：
- 字型：Instrument Serif + Geist + Geist Mono
- 色系：暖色 paper 風格，使用 skill 的 CSS token 系統
- 支援 S 鍵 presenter mode、逐字稿、T 鍵切換主題

步驟：
1. 呼叫 `Skill("html-ppt")` 並確認主題、頁數、受眾
2. 產出自帶 runtime.js 的獨立 HTML 檔
3. 存到 `public/slides/{slug}.html`
4. 在 `courses.ts` 新增 entry（`type: 'html'`）
5. git add → commit → push

---

### 部署驗證

GitHub Pages URL：`https://sun901019.github.io/my-assistant/`
- 首頁課程列表：`/#/`
- 靜態 HTML 簡報：`/slides/{slug}.html`

---

## 常用指令

```bash
# 本地開發
cd ~/projects/my-assistant/slide-presenter && npm run dev

# 型別檢查
npx vue-tsc --noEmit

# 手動發早報
~/projects/my-assistant/.venv/bin/python3 ~/projects/my-assistant/line-notify/digest.py --mode morning

# 手動發晚報
~/projects/my-assistant/.venv/bin/python3 ~/projects/my-assistant/line-notify/digest.py --mode evening

# 部署（push 即自動觸發 GitHub Actions）
git push origin main
```
