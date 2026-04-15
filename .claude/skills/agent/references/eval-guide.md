# Eval 評估指南 — Skill 品質測試

用系統化方式測試 skill 效果，不靠感覺靠數據。

---

## 什麼時候跑 Eval

- 新 skill 上線前
- 修改 skill 的觸發條件或核心邏輯後
- 覺得某個 skill「怪怪的」但說不出哪裡怪

---

## 三步流程

### Step 1: 設計測試案例

每個 skill 準備 2-3 個測試提示詞，覆蓋：
- **簡單情境**：最典型的使用場景
- **複雜情境**：多步驟或跨 skill
- **邊界情境**：容易觸發錯 skill 的模糊請求

格式：
```
測試案例 1:
  提示詞：「幫我寫一篇 Flow Lab 的 IG 貼文」
  預期 skill：content-creator
  預期輸出包含：Hook 開頭、CTA、hashtag

測試案例 2:
  提示詞：「幫我寫蝦皮商品文案」
  預期 skill：content-creator（不是 shopee-boss）
  預期輸出包含：痛點開場、商品特色、購買理由
```

### Step 2: 執行 + 評分

跑兩個版本：
- **with_skill**：正常使用 skill
- **baseline**：不用 skill，直接問 AI

每個測試案例評分：
```
- 觸發正確性：是否呼叫了對的 skill？ PASS / FAIL
- 輸出品質：是否符合預期格式和內容？ PASS / PARTIAL / FAIL
- 執行效率：花了幾步完成？有沒有多餘動作？
```

### Step 3: 分析 + 改進

比較 with_skill vs baseline：
- skill 版明顯更好 → ✅ skill 有效
- 差不多 → ⚠️ skill 沒帶來價值，考慮簡化
- skill 版更差 → ❌ skill 有問題，需要修

改進原則：
- 改通用規則，不針對單一測試案例修補
- 每次只改一個地方，重跑確認效果
- 最多迭代 5 輪，超過就停下來重新思考

---

## 觸發準確度測試

專門測 description 的觸發精準度：

```
應觸發的提示詞（至少 5 個）：
1.「幫我寫 IG 貼文」→ 應觸發 content-creator
2.「這週發什麼好」→ 應觸發 content-creator
...

不應觸發的提示詞（至少 3 個，選容易混淆的）：
1.「幫我做 Logo」→ 不應觸發 content-creator（應是 brand-design）
2.「幫我寫蝦皮 SEO」→ 不應觸發 content-creator（應是 shopee-boss）
...
```

準確率目標：應觸發 ≥ 80%，不應觸發誤觸 ≤ 10%。
