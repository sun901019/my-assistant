---
name: slide-generator
description: 個人知識簡報生成技能。當使用者說「我想學 X」、「幫我了解 X」、「X 做成簡報」、「圖解 X」時觸發。用生活故事設計互動式 HTML 簡報，存到 slides/ 並更新 index.json。
---

# 知識簡報生成器 (Slide Generator)

你的任務是把任何學習主題，用「生活故事設計法」轉成互動式 HTML 簡報，讓人一看就懂、一用就記得。

---

## 設計哲學：生活故事設計法

每一個抽象概念，都要找到對應的生活場景。

- **不要說定義，說故事**：「ROA 是資產報酬率」→「小美用 100 萬開飲料店，一年賺 10 萬，ROA = 10%」
- **角色要有名字**：小明、小美、阿強，不用「某人」或「一個人」
- **場景要具體**：飲料店、買房、炒菜，不用「某個情境」
- **數字要說人話**：「每投入 100 元賺 10 元」比「10% 報酬率」更容易記

---

## 觸發條件

| 使用者說的話 | 動作 |
|------------|------|
| 「我想學 X」「幫我了解 X」 | 生成 X 主題的互動 HTML 簡報 |
| 「X 做成簡報」「圖解 X」 | 生成 X 主題的互動 HTML 簡報 |
| 「幫我複習 X」「X 是什麼」 | 生成 X 主題的互動 HTML 簡報 |

---

## 執行流程

### Step 1：分析主題

確認以下資訊（不足則自行判斷，不要問使用者）：
- **主題名稱**：要學的是什麼
- **複雜度**：幾個核心概念需要解釋
- **分類**：財經投資 / 程式技術 / 行銷商業 / 通識生活 / 其他
- **生活比喻**：用什麼日常場景來類比

---

### Step 2：設計簡報內容

每份簡報包含：

1. **封面頁**：主題 + 副標 + 核心問題（讓人想繼續看）
2. **故事引入頁**：用生活場景拋出問題
3. **核心概念頁**（可多頁）：每頁一個概念，搭配故事
4. **比較 / 對比頁**（如有多個概念）：視覺化對比
5. **實際應用頁**：「學完這個，你可以做什麼」
6. **總結頁**：一句話記住核心 + 記憶點

---

### Step 3：生成 HTML 簡報

依照 `references/slide-template.md` 的模板生成 HTML 檔案。

**命名規則**（全小寫，空格用 `-`）：
- ROA & ROI → `roa-roi.html`
- JavaScript 基礎 → `js-basics.html`
- 複利效應 → `compound-interest.html`
- 幾何平均數 → `geometric-mean.html`

存檔路徑：`C:\Users\sun90\.claude\skills\slide-generator\slides\{slug}.html`

---

### Step 4：更新 slides/index.json

讀取現有的 `C:\Users\sun90\.claude\skills\slide-generator\slides\index.json`，在陣列末尾 append 一筆（**不要覆蓋已有資料**）：

```json
{
  "title": "主題名稱",
  "file": "slug.html",
  "category": "📈 財經投資",
  "tags": ["標籤1", "標籤2"],
  "date": "YYYY-MM-DD",
  "summary": "用一句話說明這份簡報在教什麼，帶入故事角色更好"
}
```

**分類對應**：
- `📈 財經投資`：股市、投資、財務、經濟
- `💻 程式技術`：程式語言、演算法、開發工具
- `📣 行銷商業`：行銷、品牌、創業、商業策略
- `🌱 通識生活`：心理學、科學、歷史、日常知識
- `📚 其他`：不屬於以上分類

---

### Step 5：更新 slides/index.html 的 slides 陣列

讀取 `C:\Users\sun90\.claude\skills\slide-generator\slides\index.html`，找到 `var slides = [` 這行，將新簡報的資料 append 進去。

**格式：**
```js
  {
    title: "主題名稱",
    file: "slug.html",
    category: "💻 程式技術",
    tags: ["標籤1", "標籤2"],
    date: "YYYY-MM-DD",
    summary: "一句話摘要"
  }
```

注意：
- 讀取現有 index.html，找到 `var slides = [` 區塊
- 在最後一筆資料後面加上逗號，再 append 新資料
- 用 Edit 工具修改，不要整個覆蓋檔案

---

### Step 6：回報完成

生成完後固定輸出：

```
✅ 簡報已生成：C:\Users\sun90\.claude\skills\slide-generator\slides\{slug}.html
📋 index.json 已更新
🏠 AI OS 簡報庫：http://localhost:3001/slides
```

---

## 品質標準

- [ ] 每個概念都有對應的生活故事
- [ ] 角色有名字、場景有具體細節
- [ ] 數字說人話，不用百分比就不用
- [ ] 每頁只有一個核心重點
- [ ] 視覺有足夠留白，不塞滿文字
- [ ] 最後一頁給使用者帶走「一句話記憶點」

---

## 參考資源

- `references/slide-template.md` — HTML 簡報模板與設計規範
