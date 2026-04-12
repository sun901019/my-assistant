---
name: slide-builder
description: |
  簡報生成器。自動判斷輸出格式：
  - 有小眉導師模式的教學 context → Vue 互動簡報（存入 slide-presenter，有測驗/動畫）
  - 獨立請求「我想學 X」「X 做成簡報」「圖解 X」→ HTML 靜態簡報（快速輸出）
  觸發：「做成簡報」「收斂成簡報」「產出簡報」「我想學 X」「X 做成簡報」「圖解 X」「幫我了解 X」
argument-hint: [主題名稱]
---

# slide-builder — 簡報生成器

## 自動判斷模式

```
本次對話有小眉導師教學討論？
    ↓ 是 → Vue 模式（精裝版）
    ↓ 否 → HTML 模式（快速版）
```

---

## Vue 模式（精裝版）

觸發情境：小眉導師模式教學完成後，說「做成簡報」「收斂成簡報」。
輸出：Vue 組件 → 存入 slide-presenter，有測驗互動、動畫、答對才能下一頁。

### 專案路徑

```
slide-presenter：C:\Users\sun90\OneDrive\桌面\my-assistant\slide-presenter\
組件目錄：src/slides/
課程資料：src/data/courses.ts
```

### 執行流程

```
Step 1: 從教學對話萃取核心概念（1-3 個）、比喻、步驟、測驗題
Step 2: 規劃頁面（標準 5-7 頁）：
        歡迎頁 → 核心概念頁 → 拆解頁 → 對照表頁 → 測驗頁 → 總結頁
Step 3: 產出 src/slides/{SlideId}Slide.vue
Step 4: 更新 src/data/courses.ts
Step 5: 更新 SlideModal.vue（新增 lazy import）
Step 6: 告知老闆：「請打開 http://localhost:5173/my-assistant/ 確認」
```

### Slide ID 命名

格式：`{主題}-{關鍵字}`（全小寫，空格用 `-`）
範例：`what-is-api`、`git-basics`、`vue-reactivity`

### Vue 組件模板

```vue
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import InteractiveSlideTemplate from '../components/InteractiveSlideTemplate.vue'
import type { Step, FeedbackType } from '../types/slide'

defineProps<{ isMobile?: boolean }>()
const emit = defineEmits<{ complete: [] }>()

const steps: readonly Step[] = [
  { id: 0, view: 'welcome', title: '歡迎', desc: '...' },
  { id: 1, view: 'concept', title: '核心概念', desc: '...' },
  { id: 2, view: 'quiz', title: '測驗', desc: '...' },
  { id: 3, view: 'summary', title: '總結', desc: '...' },
]

const currentStep = ref(0)
const currentSlide = computed(() => steps[currentStep.value])
const quizAnswer = ref('')
const feedback = ref('')
const feedbackType = ref<FeedbackType>('neutral')

const canGoNext = computed(() => {
  if (currentSlide.value.view === 'quiz') return feedbackType.value === 'success'
  return true
})

watch(() => currentSlide.value.view, () => {
  feedback.value = ''
  feedbackType.value = 'neutral'
  quizAnswer.value = ''
})

function next() { if (currentStep.value < steps.length - 1) currentStep.value++ }
function prev() { if (currentStep.value > 0) currentStep.value-- }
function goto(index: number) { currentStep.value = index }
function checkAnswer(answer: string, correct: string, successMsg: string, errorMsg: string) {
  quizAnswer.value = answer
  feedbackType.value = answer === correct ? 'success' : 'error'
  feedback.value = answer === correct ? successMsg : errorMsg
}
</script>

<template>
  <InteractiveSlideTemplate
    title="[主題]" subtitle="[副標]" icon="[Emoji]"
    :total-steps="steps.length" :current-step="currentStep"
    :step-title="currentSlide.title" :step-desc="currentSlide.desc"
    theme-color="[sky|amber|emerald|purple]"
    :can-go-next="canGoNext" :next-step-hint="!canGoNext ? '請先回答題目' : ''"
    @prev="prev" @next="next" @goto="goto" @complete="emit('complete')"
  >
    <div v-if="currentSlide.view === 'welcome'" class="animate-fade-in">
      <!-- 歡迎頁 -->
    </div>
    <div v-if="currentSlide.view === 'quiz'" class="animate-fade-in">
      <!-- 測驗頁 -->
    </div>
  </InteractiveSlideTemplate>
</template>
```

### 主題色

| 主題類型 | 顏色 |
|---------|------|
| 程式、後端 | `sky` |
| 工具、流程 | `amber` |
| 成功、完成 | `emerald` |
| 抽象、架構 | `purple` |

### courses.ts 格式

```typescript
{
  id: '{slideId}',
  title: '{主題標題}',
  subtitle: '{一句話說明}',
  icon: '{Emoji}',
  slideId: '{slideId}',
  themeColor: '{color}',
  tags: ['{標籤}'],
  createdAt: '{YYYY-MM-DD}',
}
```

---

## HTML 模式（快速版）

觸發情境：「我想學 X」「X 做成簡報」「圖解 X」，沒有前置教學討論。
輸出：獨立 `.html`，直接雙擊開瀏覽器，不需 server。

### 設計原則：生活故事設計法

- 不說定義，說故事（角色要有名字：小明、小美、阿強）
- 場景要具體（飲料店、買房、辦公室）
- 數字說人話（「每投入 100 元賺 10 元」比「10% 報酬率」好記）

### 執行流程

```
Step 1: 分析主題（核心概念、分類、生活比喻）
Step 2: 設計頁面（封面 → 故事引入 → 核心概念 → 比較 → 應用 → 總結）
Step 3: 產出 HTML 檔
        命名：全小寫空格用 -（roa-roi.html、js-basics.html）
        存檔：C:\Users\sun90\.claude\skills\slide-generator\slides\{slug}.html
Step 4: 更新 slides/index.json（append，不覆蓋既有資料）
Step 5: 回報：檔案路徑 + 摘要
```

### 品質標準

- [ ] 每個概念有對應的生活故事
- [ ] 角色有名字、場景有細節
- [ ] 每頁只有一個核心重點
- [ ] 最後一頁有一句話記憶點

---

## 完成後固定輸出

**Vue 模式**：
```
簡報建好了！
- 檔案：src/slides/{SlideId}Slide.vue
- 請打開 http://localhost:5173/my-assistant/ 點課程卡片確認
- 哪頁有問題直接跟我說
```

**HTML 模式**：
```
✅ 簡報已生成：{路徑}
直接雙擊檔案用瀏覽器開啟
```
