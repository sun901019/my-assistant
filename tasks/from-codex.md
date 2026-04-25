# from-codex — my-assistant Codex 完成回報

> Codex 完成任務後寫這裡，Claude 下次 session 讀取。

---

## 待處理（Claude 需接手）

（目前無）

---

## 已完成

### ✅ [2026-04-25] JSON 引擎 courses.ts 接線

- **做了什麼**：在 `slide-presenter/src/data/courses.ts` 新增 `api-basics-json` 課程 entry（排在清單最前面）
- **觸發機制**：`SlideModal.vue` 已自動偵測 slideId 不在 Vue registry → 載入 `src/data/slides/api-basics-json.json`，不需額外設定
- **型別驗證**：`npx vue-tsc --noEmit` 通過，無錯誤
- **下一步**：可直接 `npm run dev` 在首頁看到新 JSON 卡片，點入即可測試 7 個 step
