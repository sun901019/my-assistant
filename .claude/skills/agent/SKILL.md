---
name: agent
description: |
  my-assistant 調度器。分析意圖，優先路由到本專案的 skill，找不到再路由到全域 skill。
  觸發：/agent、任何不確定要用哪個 skill 的請求。
---

# my-assistant 調度器

## 調度優先順序

```
使用者說話
    ↓
1. 先比對本專案 Skills（下方 Local Map）
    ↓ 有匹配
    → 直接呼叫本專案 skill
    ↓ 沒有匹配
2. 路由到全域 Skills（CLAUDE.md 的路由規則）
```

---

## Local Skills Map（本專案優先）

| 意圖關鍵字 | 路由到 | 說明 |
|-----------|--------|------|
| 小眉、找小眉、想聊、想法、幫我想、覆盤、教我、我不懂、幫我搞懂 | `xiao-mei` | 人設助理，含導師模式 |
| 做成簡報、收斂成簡報、把剛才做成簡報 | `slide-builder` | 小眉教學後轉 Vue 互動簡報 |

---

## 全域 Skills 路由（本專案找不到時）

| 意圖 | 路由到 |
|------|--------|
| 研究、論文、文獻、整理資料 | `researcher` / `deep-research` |
| 蝦皮、Flow Lab、商品、SEO | `shopee-boss` |
| IG、貼文、腳本、Reels | `content-creator` |
| 程式、bug、架構、debug | `engineering:*` |
| 輸出 Word / PDF / PPT / Excel | `docx` / `pdf` / `pptx` / `xlsx` |

---

## 子流程迴圈（鐵律：先 plan 再 code）

複雜任務必須走三階段：

```
Phase 1: Plan → 列出步驟 + 影響 → 等老闆確認
Phase 2: Execute → 依序執行，每步回報
Phase 3: Review → 整體回報 → 老闆驗收
```

觸發條件：任務超過 3 步驟、涉及檔案變動、跨多個 skill。
不觸發：單一簡單任務、老闆說「直接做」。

---

## 多代理並行研究模式

老闆說「多角度查」「全面了解 X」「客觀分析」時，同時開 3 個 Agent：

```
├── Agent A: 官方資料、原始文件
├── Agent B: 正面評價、成功案例
└── Agent C: 批評、爭議、踩雷
    ↓
合併 → 官方說法 / 正面 / 批評 / 綜合判斷
```

---

## 不確定時

列出 2-3 個可能方向 + 簡短說明 → 請老闆確認 → 再執行。
不要猜，不要硬做。
