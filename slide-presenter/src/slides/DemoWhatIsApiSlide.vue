<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import InteractiveSlideTemplate from '../components/InteractiveSlideTemplate.vue'
import type { Step, FeedbackType } from '../types/slide'

defineProps<{ isMobile?: boolean }>()
const emit = defineEmits<{ complete: [] }>()

const steps: readonly Step[] = [
  { id: 0, view: 'welcome', title: '歡迎', desc: '今天來搞懂 API 是什麼' },
  { id: 1, view: 'restaurant', title: '餐廳比喻', desc: '用點餐來理解 API' },
  { id: 2, view: 'real-api', title: '真正的 API', desc: '從比喻回到程式世界' },
  { id: 3, view: 'quiz', title: '小測驗', desc: '確認你真的懂了' },
  { id: 4, view: 'summary', title: '總結', desc: '把概念收起來' },
]

const currentStep = ref(0)
const currentSlide = computed(() => steps[currentStep.value])

// Quiz state
const quizAnswer = ref('')
const feedback = ref('')
const feedbackType = ref<FeedbackType>('neutral')

const canGoNext = computed(() => {
  if (currentSlide.value.view === 'quiz') {
    return feedbackType.value === 'success'
  }
  return true
})

function checkAnswer(answer: string) {
  quizAnswer.value = answer
  if (answer === 'waiter') {
    feedback.value = '答對了！API 就像服務生，負責在你（前端）和廚房（後端）之間傳遞訊息。'
    feedbackType.value = 'success'
  } else {
    feedback.value = '再想想看，誰是負責「傳遞」你的需求給廚房的人？'
    feedbackType.value = 'error'
  }
}

watch(() => currentSlide.value.view, () => {
  feedback.value = ''
  feedbackType.value = 'neutral'
  quizAnswer.value = ''
})

function next() {
  if (currentStep.value < steps.length - 1) currentStep.value++
}
function prev() {
  if (currentStep.value > 0) currentStep.value--
}
function goto(index: number) {
  currentStep.value = index
}
</script>

<template>
  <InteractiveSlideTemplate
    title="API 是什麼？"
    subtitle="用餐廳點餐來理解 API 的概念"
    icon="🍽️"
    :total-steps="steps.length"
    :current-step="currentStep"
    :step-title="currentSlide.title"
    :step-desc="currentSlide.desc"
    theme-color="sky"
    :can-go-next="canGoNext"
    :next-step-hint="!canGoNext ? '請先回答題目' : ''"
    @prev="prev"
    @next="next"
    @goto="goto"
    @complete="emit('complete')"
  >
    <!-- Step 1: Welcome -->
    <div v-if="currentSlide.view === 'welcome'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto text-center space-y-6">
        <div class="text-6xl md:text-8xl">🍽️</div>
        <h2 class="text-2xl md:text-4xl font-bold">你有沒有想過...</h2>
        <p class="text-lg md:text-xl text-white/70">
          當你打開一個 App，按下按鈕，資料是怎麼跑出來的？
        </p>
        <div class="mt-8 p-6 rounded-xl bg-sky-500/10 border border-sky-500/20">
          <p class="text-sky-300 text-lg">
            今天我們用「去餐廳吃飯」來搞懂這件事 🍜
          </p>
        </div>
      </div>
    </div>

    <!-- Step 2: Restaurant metaphor -->
    <div v-if="currentSlide.view === 'restaurant'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-6 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
            <div class="text-4xl mb-3">🧑</div>
            <h3 class="font-bold text-amber-300">你（客人）</h3>
            <p class="text-sm text-white/60 mt-2">= 前端 / 使用者</p>
            <p class="text-xs text-white/40 mt-1">只管點餐，不用進廚房</p>
          </div>
          <div class="p-6 rounded-xl bg-sky-500/10 border border-sky-500/20 text-center">
            <div class="text-4xl mb-3">🤵</div>
            <h3 class="font-bold text-sky-300">服務生</h3>
            <p class="text-sm text-white/60 mt-2">= API</p>
            <p class="text-xs text-white/40 mt-1">負責接收需求、傳遞給廚房、把結果端回來</p>
          </div>
          <div class="p-6 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-center">
            <div class="text-4xl mb-3">👨‍🍳</div>
            <h3 class="font-bold text-emerald-300">廚房</h3>
            <p class="text-sm text-white/60 mt-2">= 後端 / 伺服器</p>
            <p class="text-xs text-white/40 mt-1">處理你的需求，產出結果</p>
          </div>
        </div>

        <div class="p-6 rounded-xl bg-white/5 border border-white/10">
          <h3 class="font-bold text-lg mb-4">📋 點餐流程 = API 請求流程</h3>
          <div class="space-y-3 text-left">
            <div class="flex items-start gap-3">
              <span class="text-sky-400 font-mono text-sm shrink-0">Step 1</span>
              <span class="text-white/80">你跟服務生說：「我要一碗拉麵」<span class="text-white/40">（= 發送 Request）</span></span>
            </div>
            <div class="flex items-start gap-3">
              <span class="text-sky-400 font-mono text-sm shrink-0">Step 2</span>
              <span class="text-white/80">服務生把你的需求告訴廚房<span class="text-white/40">（= API 轉發請求到 Server）</span></span>
            </div>
            <div class="flex items-start gap-3">
              <span class="text-sky-400 font-mono text-sm shrink-0">Step 3</span>
              <span class="text-white/80">廚房做好菜<span class="text-white/40">（= Server 處理資料）</span></span>
            </div>
            <div class="flex items-start gap-3">
              <span class="text-sky-400 font-mono text-sm shrink-0">Step 4</span>
              <span class="text-white/80">服務生把拉麵端給你<span class="text-white/40">（= API 回傳 Response）</span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 3: Real API -->
    <div v-if="currentSlide.view === 'real-api'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <div class="p-6 rounded-xl bg-white/5 border border-white/10">
          <h3 class="font-bold text-lg mb-4">🔄 比喻 → 程式對照</h3>
          <table class="w-full text-left">
            <thead>
              <tr class="text-white/40 text-sm border-b border-white/10">
                <th class="pb-2">餐廳</th>
                <th class="pb-2">程式世界</th>
                <th class="pb-2">範例</th>
              </tr>
            </thead>
            <tbody class="text-white/80">
              <tr class="border-b border-white/5">
                <td class="py-3">菜單</td>
                <td>API 文件</td>
                <td class="text-xs text-white/50">告訴你有哪些功能可以用</td>
              </tr>
              <tr class="border-b border-white/5">
                <td class="py-3">點餐</td>
                <td>HTTP Request</td>
                <td class="text-xs text-white/50">GET /api/menu</td>
              </tr>
              <tr class="border-b border-white/5">
                <td class="py-3">餐點送到</td>
                <td>HTTP Response</td>
                <td class="text-xs text-white/50">{ "item": "拉麵", "price": 200 }</td>
              </tr>
              <tr>
                <td class="py-3">「沒有這道菜」</td>
                <td>404 Error</td>
                <td class="text-xs text-white/50">你點了菜單上沒有的東西</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="p-5 rounded-xl bg-sky-500/10 border border-sky-500/20">
          <p class="text-sky-300 font-medium">💡 一句話總結</p>
          <p class="text-white/80 mt-2">
            API 就是兩個系統之間的「溝通橋樑」。它定義了「你可以問什麼」和「你會得到什麼」。
          </p>
        </div>
      </div>
    </div>

    <!-- Step 4: Quiz -->
    <div v-if="currentSlide.view === 'quiz'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto space-y-6">
        <h3 class="text-xl font-bold text-center">🧪 小測驗：在餐廳比喻中，API 對應的是誰？</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <button
            v-for="option in [
              { value: 'customer', label: '🧑 客人（你）' },
              { value: 'waiter', label: '🤵 服務生' },
              { value: 'chef', label: '👨‍🍳 廚師' },
              { value: 'menu', label: '📋 菜單' },
            ]"
            :key="option.value"
            class="p-4 rounded-xl border text-left transition-all"
            :class="
              quizAnswer === option.value && feedbackType === 'success'
                ? 'border-emerald-400 bg-emerald-500/20 text-emerald-300'
                : quizAnswer === option.value && feedbackType === 'error'
                  ? 'border-red-400 bg-red-500/20 text-red-300'
                  : 'border-white/10 bg-white/5 hover:bg-white/10 text-white/80'
            "
            @click="checkAnswer(option.value)"
          >
            {{ option.label }}
          </button>
        </div>

        <div
          v-if="feedback"
          class="p-4 rounded-xl text-center"
          :class="feedbackType === 'success'
            ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-300'
            : 'bg-red-500/10 border border-red-500/20 text-red-300'"
        >
          {{ feedback }}
        </div>
      </div>
    </div>

    <!-- Step 5: Summary -->
    <div v-if="currentSlide.view === 'summary'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto text-center space-y-6">
        <div class="text-5xl">🎉</div>
        <h2 class="text-2xl md:text-3xl font-bold">恭喜你搞懂 API 了！</h2>
        <div class="text-left space-y-4 p-6 rounded-xl bg-white/5 border border-white/10">
          <div class="flex gap-3 items-start">
            <span class="text-emerald-400">✓</span>
            <span class="text-white/80">API = 兩個系統之間的溝通橋樑（服務生）</span>
          </div>
          <div class="flex gap-3 items-start">
            <span class="text-emerald-400">✓</span>
            <span class="text-white/80">你（前端）發送 Request → API 轉發 → 伺服器處理 → 回傳 Response</span>
          </div>
          <div class="flex gap-3 items-start">
            <span class="text-emerald-400">✓</span>
            <span class="text-white/80">API 文件 = 菜單，告訴你可以點什麼</span>
          </div>
        </div>
        <p class="text-white/50 text-sm">點擊「完成學習」回到首頁</p>
      </div>
    </div>
  </InteractiveSlideTemplate>
</template>
