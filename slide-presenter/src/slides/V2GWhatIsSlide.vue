<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import InteractiveSlideTemplate from '../components/InteractiveSlideTemplate.vue'
import type { Step, FeedbackType } from '../types/slide'

defineProps<{ isMobile?: boolean }>()
const emit = defineEmits<{ complete: [] }>()

const steps: readonly Step[] = [
  { id: 0, view: 'welcome', title: '車子賺錢？', desc: '你的電動車可以幫你賺錢' },
  { id: 1, view: 'ev-as-battery', title: '車即電池', desc: '電動車 = 移動式儲能裝置' },
  { id: 2, view: 'v2g-concept', title: 'V2G 概念', desc: '雙向充放電的核心邏輯' },
  { id: 3, view: 'money-flow', title: '錢怎麼流', desc: '套利空間約 10 元/度' },
  { id: 4, view: 'real-example', title: '實際試算', desc: 'Neta N7，每月 16,000 元' },
  { id: 5, view: 'quiz', title: '小測驗', desc: 'V2G 最主要的功能是什麼？' },
  { id: 6, view: 'summary', title: '總結', desc: '三個重點帶走' },
]

const currentStep = ref(0)
const currentSlide = computed(() => steps[currentStep.value])

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
  if (answer === 'discharge') {
    feedback.value = '答對了！V2G 最核心的功能就是讓車子放電回電網，並從電價差中獲利。'
    feedbackType.value = 'success'
  } else {
    feedback.value = '再想想看，V2G 的「G」是 Grid（電網），車子能對電網做什麼？'
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
    title="V2G 是什麼？"
    subtitle="你的電動車可以幫你賺錢"
    icon="⚡"
    :total-steps="steps.length"
    :current-step="currentStep"
    :step-title="currentSlide.title"
    :step-desc="currentSlide.desc"
    theme-color="emerald"
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
        <div class="text-6xl md:text-8xl">⚡</div>
        <h2 class="text-2xl md:text-4xl font-bold">你的車子可以幫你賺錢？</h2>
        <p class="text-lg md:text-xl text-white/70">
          不是賣車，也不是跑 Uber——<br>
          而是讓車子停著的時候，默默幫你產生收益。
        </p>
        <div class="mt-8 p-6 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
          <p class="text-emerald-300 text-lg font-medium">
            這個技術叫做 V2G（Vehicle-to-Grid）🚗⚡🏭
          </p>
          <p class="text-white/50 text-sm mt-2">五分鐘搞懂，從此看新聞不會再霧煞煞</p>
        </div>
      </div>
    </div>

    <!-- Step 2: EV as Battery -->
    <div v-if="currentSlide.view === 'ev-as-battery'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <h2 class="text-xl md:text-2xl font-bold text-center">電動車，其實是一顆會跑的大電池</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-6 rounded-xl bg-white/5 border border-white/10 text-center">
            <div class="text-5xl mb-3">🚗</div>
            <h3 class="font-bold text-white">一般人的認知</h3>
            <p class="text-white/60 mt-2 text-sm">電動車 = 交通工具<br>充電進來、消耗掉</p>
            <div class="mt-3 px-3 py-1 rounded-full bg-white/5 text-white/40 text-xs inline-block">單向消費</div>
          </div>
          <div class="p-6 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-center">
            <div class="text-5xl mb-3">🔋</div>
            <h3 class="font-bold text-emerald-300">V2G 的認知</h3>
            <p class="text-white/60 mt-2 text-sm">電動車 = 移動式儲能裝置<br>充電進來、也能放電出去</p>
            <div class="mt-3 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs inline-block">雙向儲能</div>
          </div>
        </div>

        <div class="p-5 rounded-xl bg-white/5 border border-white/10">
          <h3 class="font-bold mb-3">🏠 生活中的類比</h3>
          <div class="space-y-3">
            <div class="flex items-center gap-3">
              <span class="text-2xl">📱</span>
              <div>
                <span class="text-white/80">手機充電寶</span>
                <span class="text-white/40 text-sm ml-2">— 小容量、幫手機充電</span>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-2xl">🏠</span>
              <div>
                <span class="text-white/80">家用儲能牆（Tesla Powerwall）</span>
                <span class="text-white/40 text-sm ml-2">— 中容量、幫家庭供電</span>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-2xl">🚗</span>
              <div>
                <span class="text-emerald-300 font-medium">電動車電池（如 Neta N7）</span>
                <span class="text-white/40 text-sm ml-2">— 超大容量 100 kWh，可供整棟建物</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 3: V2G Concept -->
    <div v-if="currentSlide.view === 'v2g-concept'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <h2 class="text-xl md:text-2xl font-bold text-center">V2G = Vehicle-to-Grid，雙向充放電</h2>

        <!-- Flow diagram -->
        <div class="p-6 rounded-xl bg-white/5 border border-white/10">
          <div class="flex flex-col md:flex-row items-center justify-center gap-3 md:gap-4">
            <div class="text-center p-4 rounded-xl bg-blue-500/10 border border-blue-500/20 min-w-[100px]">
              <div class="text-3xl mb-1">🏭</div>
              <div class="text-blue-300 font-medium text-sm">台電電網</div>
            </div>

            <div class="flex flex-col items-center gap-2 text-center">
              <div class="flex items-center gap-2 text-emerald-300 text-sm">
                <span>夜間充電</span>
                <span class="text-lg">→</span>
              </div>
              <div class="flex items-center gap-2 text-yellow-300 text-sm">
                <span class="text-lg">←</span>
                <span>白天放電</span>
              </div>
            </div>

            <div class="text-center p-4 rounded-xl bg-slate-700/50 border border-white/10 min-w-[100px]">
              <div class="text-3xl mb-1">🔌</div>
              <div class="text-white/70 font-medium text-sm">雙向充電樁</div>
            </div>

            <div class="flex flex-col items-center gap-2 text-center">
              <div class="flex items-center gap-2 text-emerald-300 text-sm">
                <span>充電</span>
                <span class="text-lg">→</span>
              </div>
              <div class="flex items-center gap-2 text-yellow-300 text-sm">
                <span class="text-lg">←</span>
                <span>放電</span>
              </div>
            </div>

            <div class="text-center p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 min-w-[100px]">
              <div class="text-3xl mb-1">🚗</div>
              <div class="text-emerald-300 font-medium text-sm">你的電動車</div>
            </div>
          </div>
        </div>

        <!-- Key difference -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-5 rounded-xl bg-white/5 border border-white/10">
            <h3 class="font-bold text-white/60 mb-3">傳統充電（單向）</h3>
            <div class="flex items-center gap-3">
              <span class="text-2xl">🏭</span>
              <span class="text-white/40">→→→</span>
              <span class="text-2xl">🚗</span>
            </div>
            <p class="text-white/50 text-sm mt-2">電網 → 車，只能充進來</p>
          </div>
          <div class="p-5 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
            <h3 class="font-bold text-emerald-300 mb-3">V2G 充放電（雙向）</h3>
            <div class="flex items-center gap-3">
              <span class="text-2xl">🏭</span>
              <span class="text-emerald-400">⇄</span>
              <span class="text-2xl">🚗</span>
            </div>
            <p class="text-white/70 text-sm mt-2">電網 ⇄ 車，可充入也可賣出</p>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
          <p class="text-emerald-300 font-medium text-sm">
            💡 關鍵字拆解：<span class="text-white/80">Vehicle（車）to Grid（電網）= 車子把電賣回給電網</span>
          </p>
        </div>
      </div>
    </div>

    <!-- Step 4: Money Flow -->
    <div v-if="currentSlide.view === 'money-flow'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <h2 class="text-xl md:text-2xl font-bold text-center">錢怎麼流？電價差套利</h2>

        <!-- Price comparison -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-5 rounded-xl bg-blue-500/10 border border-blue-500/20 text-center">
            <div class="text-3xl mb-2">🌙</div>
            <div class="text-blue-300 font-bold text-lg">夜間買電</div>
            <div class="text-3xl font-bold text-white mt-2">2.08<span class="text-sm text-white/50">元/度</span></div>
            <p class="text-white/50 text-xs mt-2">台電離峰電價<br>深夜 23:00–07:00</p>
          </div>

          <div class="flex items-center justify-center">
            <div class="text-center">
              <div class="text-3xl text-emerald-400">→</div>
              <div class="text-emerald-300 font-bold text-lg mt-1">套利</div>
              <div class="text-2xl font-bold text-emerald-400">≈ 10 元/度</div>
              <p class="text-white/40 text-xs mt-1">12.5 − 2.08</p>
            </div>
          </div>

          <div class="p-5 rounded-xl bg-yellow-500/10 border border-yellow-500/20 text-center">
            <div class="text-3xl mb-2">☀️</div>
            <div class="text-yellow-300 font-bold text-lg">白天賣電</div>
            <div class="text-3xl font-bold text-white mt-2">12.5<span class="text-sm text-white/50">元/度</span></div>
            <p class="text-white/50 text-xs mt-2">場域收購車主電<br>MCUT 場域設計</p>
          </div>
        </div>

        <!-- Flow explanation -->
        <div class="p-6 rounded-xl bg-white/5 border border-white/10">
          <h3 class="font-bold mb-4">💸 每一度電的旅程</h3>
          <div class="space-y-3">
            <div class="flex items-start gap-3">
              <span class="text-blue-400 font-mono text-sm shrink-0 w-16">凌晨</span>
              <span class="text-white/80">用 <span class="text-blue-300 font-bold">2.08 元</span> 從台電買電，存進車子電池</span>
            </div>
            <div class="w-px h-4 bg-white/10 ml-7"></div>
            <div class="flex items-start gap-3">
              <span class="text-yellow-400 font-mono text-sm shrink-0 w-16">白天</span>
              <span class="text-white/80">電力需求高峰，場域以 <span class="text-yellow-300 font-bold">12.5 元</span> 向你收購</span>
            </div>
            <div class="w-px h-4 bg-white/10 ml-7"></div>
            <div class="flex items-start gap-3">
              <span class="text-emerald-400 font-mono text-sm shrink-0 w-16">獲利</span>
              <span class="text-white/80">每一度電賺 <span class="text-emerald-300 font-bold">約 10 元</span>，車子越大顆，賺越多</span>
            </div>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
          <p class="text-emerald-300 font-medium text-sm">
            🏪 本質就像「買低賣高」的電力批發，只是用你的車當倉庫
          </p>
        </div>
      </div>
    </div>

    <!-- Step 5: Real Example -->
    <div v-if="currentSlide.view === 'real-example'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <h2 class="text-xl md:text-2xl font-bold text-center">實際試算：Neta N7</h2>

        <!-- Car info -->
        <div class="p-5 rounded-xl bg-white/5 border border-white/10 flex flex-col md:flex-row items-center gap-4">
          <div class="text-5xl">🚗</div>
          <div>
            <h3 class="font-bold text-white text-lg">Neta N7</h3>
            <p class="text-white/50 text-sm">電池容量：100 kWh ｜ 操作區間：10%→90%</p>
            <p class="text-white/50 text-sm">每日可調度：<span class="text-emerald-300 font-bold">80 kWh</span></p>
          </div>
        </div>

        <!-- Calculation table -->
        <div class="p-6 rounded-xl bg-white/5 border border-white/10">
          <h3 class="font-bold mb-4">📊 收益試算</h3>
          <table class="w-full text-left">
            <thead>
              <tr class="text-white/40 text-sm border-b border-white/10">
                <th class="pb-2">項目</th>
                <th class="pb-2 text-right">數值</th>
                <th class="pb-2 text-right">說明</th>
              </tr>
            </thead>
            <tbody class="text-white/80">
              <tr class="border-b border-white/5">
                <td class="py-3">每日可調度電量</td>
                <td class="py-3 text-right font-mono">80 kWh</td>
                <td class="py-3 text-right text-xs text-white/40">100 × 80%</td>
              </tr>
              <tr class="border-b border-white/5">
                <td class="py-3">每度套利空間</td>
                <td class="py-3 text-right font-mono">10 元/度</td>
                <td class="py-3 text-right text-xs text-white/40">12.5 − 2.08</td>
              </tr>
              <tr class="border-b border-white/5">
                <td class="py-3 font-bold">每日收益</td>
                <td class="py-3 text-right font-mono font-bold text-emerald-300">800 元</td>
                <td class="py-3 text-right text-xs text-white/40">80 × 10</td>
              </tr>
              <tr>
                <td class="py-3 font-bold text-lg">每月收益（20工作天）</td>
                <td class="py-3 text-right font-mono font-bold text-emerald-400 text-xl">16,000 元</td>
                <td class="py-3 text-right text-xs text-white/40">800 × 20</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Context -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
            <p class="text-emerald-300 font-medium text-sm">🎉 相當於...</p>
            <p class="text-white/70 text-sm mt-1">一個月多出一筆兼職薪水，車子停著就幫你賺</p>
          </div>
          <div class="p-4 rounded-xl bg-white/5 border border-white/10">
            <p class="text-white/60 font-medium text-sm">⚠️ 前提條件</p>
            <p class="text-white/50 text-sm mt-1">需有雙向充電樁 + 參與 V2G 場域計畫</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Step 6: Quiz -->
    <div v-if="currentSlide.view === 'quiz'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto space-y-6">
        <h3 class="text-xl font-bold text-center">🧪 小測驗：V2G 最主要的功能是什麼？</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <button
            v-for="option in [
              { value: 'charge-faster', label: '⚡ 讓車子充電更快' },
              { value: 'discharge', label: '🔋 車子放電回電網獲利' },
              { value: 'save-energy', label: '💡 減少行駛時的耗電' },
              { value: 'auto-drive', label: '🤖 讓車子自動駕駛' },
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

    <!-- Step 7: Summary -->
    <div v-if="currentSlide.view === 'summary'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto text-center space-y-6">
        <div class="text-5xl">🎉</div>
        <h2 class="text-2xl md:text-3xl font-bold">你現在懂 V2G 了！</h2>

        <div class="text-left space-y-4 p-6 rounded-xl bg-white/5 border border-white/10">
          <div class="flex gap-3 items-start">
            <span class="text-emerald-400 text-lg shrink-0">①</span>
            <div>
              <p class="text-white/90 font-medium">電動車 = 移動式儲能裝置</p>
              <p class="text-white/50 text-sm">不只是交通工具，更是一顆可調度的大電池</p>
            </div>
          </div>
          <div class="flex gap-3 items-start">
            <span class="text-emerald-400 text-lg shrink-0">②</span>
            <div>
              <p class="text-white/90 font-medium">V2G = 雙向充放電 + 電價差套利</p>
              <p class="text-white/50 text-sm">夜間 2.08 元買電，白天 12.5 元賣電，每度賺 ~10 元</p>
            </div>
          </div>
          <div class="flex gap-3 items-start">
            <span class="text-emerald-400 text-lg shrink-0">③</span>
            <div>
              <p class="text-white/90 font-medium">Neta N7 可月賺 16,000 元</p>
              <p class="text-white/50 text-sm">80 kWh/天 × 10 元/度 × 20 工作天，車停著就在賺</p>
            </div>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
          <p class="text-emerald-300 text-sm">
            🔮 下一步：了解 V2G 技術架構、電池老化影響、以及台電輔助服務如何讓收益更高！
          </p>
        </div>

        <p class="text-white/50 text-sm">點擊「完成學習」回到首頁</p>
      </div>
    </div>
  </InteractiveSlideTemplate>
</template>
