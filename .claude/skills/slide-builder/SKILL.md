---
name: slide-builder
description: |
  互動式簡報生成器。當小眉導師模式教學完成後，把教學內容轉成 Vue 互動簡報。
  觸發：「幫我做成簡報」「收斂成簡報」「產出簡報」「把剛才的內容做成簡報」。
  需要有教學討論內容才能執行。
argument-hint: [主題名稱]
---

# slide-builder — 互動式簡報生成器

## 定位

把小眉導師模式的教學討論，**自動轉成可播放的 Vue 互動簡報**，存入 slide-presenter 專案。

---

## 專案路徑

```
slide-presenter 路徑：C:\Users\sun90\OneDrive\桌面\my-assistant\slide-presenter\
簡報組件目錄：src/slides/
課程資料：src/data/courses.ts
```

---

## 執行流程

```
Step 1: 接收教學內容
    從本次對話中的導師模式教學，萃取：
    - 核心概念（1-3 個）
    - 關鍵比喻或視覺化邏輯
    - 步驟拆解
    - 測驗題目
    ↓
Step 2: 設計簡報結構
    規劃頁面順序（標準 5-7 頁）：
    1. 歡迎頁 — 提問切入，引發好奇
    2. 核心概念頁 — 一句話白話解釋 + 比喻
    3. 拆解頁 — 步驟對照、視覺化
    4. 對照表頁 — 比喻 vs 真實世界對照
    5. 測驗頁 — 互動選擇題（答對才能前進）
    6. 總結頁 — 重點收斂 + 完成
    ↓
Step 3: 產出 Vue 組件
    建立 src/slides/{SlideId}Slide.vue
    套用 InteractiveSlideTemplate
    ↓
Step 4: 更新 courses.ts
    在 courses 陣列新增這份簡報的資訊
    ↓
Step 5: 更新 SlideModal.vue
    在 slideComponents 中新增對應的 lazy import
    ↓
Step 6: 確認老闆審查
    告訴老闆：「簡報建好了，請打開 http://localhost:5173/my-assistant/ 看看，哪頁有問題跟我說」
```

---

## 簡報 ID 命名規則

```
格式：{主題}-{關鍵字}
範例：
- what-is-api
- http-methods
- git-basics
- vue-reactivity
- async-await
```

---

## Vue 組件結構模板

```vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import InteractiveSlideTemplate from '../components/InteractiveSlideTemplate.vue'
import type { Step, FeedbackType } from '../types/slide'

defineProps<{ isMobile?: boolean }>()
const emit = defineEmits<{ complete: [] }>()

// 1. 定義步驟
const steps: readonly Step[] = [
  { id: 0, view: 'welcome', title: '歡迎', desc: '...' },
  { id: 1, view: 'concept', title: '核心概念', desc: '...' },
  // ...更多步驟
]

// 2. 步驟狀態
const currentStep = ref(0)
const currentSlide = computed(() => steps[currentStep.value])

// 3. 測驗狀態（如有）
const quizAnswer = ref('')
const feedback = ref('')
const feedbackType = ref<FeedbackType>('neutral')

const canGoNext = computed(() => {
  if (currentSlide.value.view === 'quiz') return feedbackType.value === 'success'
  return true
})

// 4. 換頁時重置測驗
watch(() => currentSlide.value.view, () => {
  feedback.value = ''
  feedbackType.value = 'neutral'
  quizAnswer.value = ''
})

// 5. 導覽函式
function next() { if (currentStep.value < steps.length - 1) currentStep.value++ }
function prev() { if (currentStep.value > 0) currentStep.value-- }
function goto(index: number) { currentStep.value = index }

// 6. 測驗邏輯
function checkAnswer(answer: string, correct: string, successMsg: string, errorMsg: string) {
  quizAnswer.value = answer
  if (answer === correct) {
    feedback.value = successMsg
    feedbackType.value = 'success'
  } else {
    feedback.value = errorMsg
    feedbackType.value = 'error'
  }
}
</script>

<template>
  <InteractiveSlideTemplate
    title="[主題標題]"
    subtitle="[副標題]"
    icon="[Emoji]"
    :total-steps="steps.length"
    :current-step="currentStep"
    :step-title="currentSlide.title"
    :step-desc="currentSlide.desc"
    theme-color="[sky|amber|emerald|purple]"
    :can-go-next="canGoNext"
    :next-step-hint="!canGoNext ? '請先回答題目' : ''"
    @prev="prev"
    @next="next"
    @goto="goto"
    @complete="emit('complete')"
  >
    <!-- 每頁用 v-if 切換 -->
    <div v-if="currentSlide.view === 'welcome'" class="animate-fade-in">
      <!-- 歡迎頁內容 -->
    </div>

    <div v-if="currentSlide.view === 'quiz'" class="animate-fade-in">
      <!-- 測驗頁：選項按鈕 + 回饋文字 -->
    </div>
  </InteractiveSlideTemplate>
</template>
```

---

## 主題色選擇建議

| 主題類型 | 顏色 |
|---------|------|
| 程式概念、後端 | `sky`（藍） |
| 工具、流程 | `amber`（橘） |
| 成功、完成類 | `emerald`（綠） |
| 抽象概念、架構 | `purple`（紫） |

---

## 更新 courses.ts 格式

```typescript
{
  id: '{slideId}',
  title: '{主題標題}',
  subtitle: '{一句話說明}',
  icon: '{Emoji}',
  slideId: '{slideId}',
  themeColor: '{color}',
  tags: ['{標籤1}', '{標籤2}'],
  createdAt: '{YYYY-MM-DD}',
}
```

---

## 更新 SlideModal.vue 格式

在 `slideComponents` 物件中新增：
```typescript
'{slideId}': defineAsyncComponent(
  () => import('../slides/{SlideId}Slide.vue')
),
```

---

## 完成後告訴老闆

```
簡報建好了！

- 檔案位置：src/slides/{SlideId}Slide.vue
- 主題：{主題}
- 共 X 頁

請打開 http://localhost:5173/my-assistant/ 點擊課程卡片看看效果。
哪一頁有問題或想加強的，直接跟我說。
```
