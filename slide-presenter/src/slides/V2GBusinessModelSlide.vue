<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import InteractiveSlideTemplate from '../components/InteractiveSlideTemplate.vue'
import type { Step, FeedbackType } from '../types/slide'

defineProps<{ isMobile?: boolean }>()
const emit = defineEmits<{ complete: [] }>()

const steps: readonly Step[] = [
  { id: 0, view: 'welcome',      title: '收益潛力',   desc: '電動車停著也能賺錢' },
  { id: 1, view: 'stakeholders', title: '三角關係',   desc: '車主、MCUT、台電的分潤機制' },
  { id: 2, view: 'price-flow',   title: '電價流動',   desc: '套利空間是怎麼產生的' },
  { id: 3, view: 'calculation',  title: '互動計算器', desc: '拖拉 kWh，即時看收益' },
  { id: 4, view: 'battery-cost', title: '電池損耗',   desc: 'LFP vs NMC，功率如何影響壽命' },
  { id: 5, view: 'quiz',         title: '小測驗',     desc: '確認核心數字' },
  { id: 6, view: 'summary',      title: '總結',       desc: '誰能參與、怎麼參與、有什麼限制' },
]

const currentStep = ref(0)
const currentSlide = computed(() => steps[currentStep.value])

// 互動計算器 — Step 4
const adjustableKwh = ref(80)
const dailyProfit = computed(() => adjustableKwh.value * 10)
const monthlyProfit = computed(() => dailyProfit.value * 20)

// 小測驗 — Step 6
const quizAnswer = ref('')
const feedback = ref('')
const feedbackType = ref<FeedbackType>('neutral')

const canGoNext = computed(() => {
  if (currentSlide.value.view === 'quiz') return feedbackType.value === 'success'
  return true
})

function checkAnswer(answer: string) {
  quizAnswer.value = answer
  if (answer === '10') {
    feedback.value = '答對了！車主每度電套利空間約 10 元（場域收購 12.5 元 − 離峰電費 2.08 元 ≈ 10 元）。'
    feedbackType.value = 'success'
  } else {
    feedback.value = '再想想：用場域收購價減去你實際購電的離峰電費，大約是多少？'
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
    title="V2G 商業模式"
    subtitle="套利機制、分潤設計與電池成本分析"
    icon="💰"
    :total-steps="steps.length"
    :current-step="currentStep"
    :step-title="currentSlide.title"
    :step-desc="currentSlide.desc"
    theme-color="amber"
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
        <div class="text-6xl md:text-8xl">🚗⚡</div>
        <h2 class="text-2xl md:text-4xl font-bold">一台電動車，每月多賺 16,000 元？</h2>
        <p class="text-lg md:text-xl text-white/70">
          車停在停車場的那段時間，電池其實可以幫你工作。
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
            <div class="text-3xl mb-2">🔋</div>
            <p class="text-amber-300 font-semibold">可調度容量</p>
            <p class="text-2xl font-bold mt-1">80 kWh</p>
            <p class="text-xs text-white/40 mt-1">100 kWh 電池，10%→90%</p>
          </div>
          <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
            <div class="text-3xl mb-2">💹</div>
            <p class="text-amber-300 font-semibold">每日收益</p>
            <p class="text-2xl font-bold mt-1">800 元</p>
            <p class="text-xs text-white/40 mt-1">套利空間 10 元/kWh</p>
          </div>
          <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
            <div class="text-3xl mb-2">📅</div>
            <p class="text-amber-300 font-semibold">每月收益</p>
            <p class="text-2xl font-bold mt-1">16,000 元</p>
            <p class="text-xs text-white/40 mt-1">20 個工作天試算</p>
          </div>
        </div>
        <div class="mt-4 p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
          <p class="text-amber-300 text-sm">
            這不是空談——這是 MCUT 場域以 Neta N7（LFP 電池）進行的實際試算。
          </p>
        </div>
      </div>
    </div>

    <!-- Step 2: Stakeholders -->
    <div v-if="currentSlide.view === 'stakeholders'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <h2 class="text-xl md:text-2xl font-bold text-center">三角分潤關係</h2>

        <!-- 三角圖 -->
        <div class="relative flex flex-col items-center gap-2">
          <!-- 台電（頂端） -->
          <div class="p-5 rounded-xl bg-blue-500/10 border border-blue-500/30 text-center w-52">
            <div class="text-3xl mb-1">🏭</div>
            <h3 class="font-bold text-blue-300">台電</h3>
            <p class="text-xs text-white/50 mt-1">購買輔助服務<br>15–16 元/kWh</p>
          </div>

          <!-- 箭頭行 -->
          <div class="flex items-center gap-6">
            <div class="flex flex-col items-center text-white/40 text-xs">
              <span>▲ 上售電力</span>
              <span class="text-amber-400">＋輔助服務費</span>
            </div>
          </div>

          <!-- MCUT 營運商（中間） -->
          <div class="p-5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-center w-64">
            <div class="text-3xl mb-1">🏢</div>
            <h3 class="font-bold text-amber-300">MCUT 營運商</h3>
            <p class="text-xs text-white/50 mt-1">聚合調度平台<br>收購車主電 12.5 元/kWh<br>差價利潤 ≈ 3–4 元/kWh</p>
          </div>

          <!-- 箭頭行 -->
          <div class="text-white/40 text-xs text-center">
            <span>▲ 提供電力 &nbsp;|&nbsp; ▼ 收取費用 12.5 元/kWh</span>
          </div>

          <!-- 車主（底部） -->
          <div class="p-5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-center w-52">
            <div class="text-3xl mb-1">🧑‍💼</div>
            <h3 class="font-bold text-emerald-300">EV 車主</h3>
            <p class="text-xs text-white/50 mt-1">離峰充電 2.08 元/kWh<br>套利空間 ≈ 10 元/kWh</p>
          </div>
        </div>

        <!-- 補充說明 -->
        <div class="p-4 rounded-xl bg-white/5 border border-white/10">
          <p class="text-white/60 text-sm text-center">
            台電出的是「需量反應」費用；MCUT 負責聚合、調度、投標；車主只需設定「最低保留電量」，其餘由系統自動處理。
          </p>
        </div>
      </div>
    </div>

    <!-- Step 3: Price Flow -->
    <div v-if="currentSlide.view === 'price-flow'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <h2 class="text-xl md:text-2xl font-bold text-center">電價流動與套利空間</h2>

        <!-- 電價流動圖 -->
        <div class="space-y-3">
          <div class="flex items-center gap-4">
            <div class="w-40 shrink-0 p-3 rounded-xl bg-slate-700/50 border border-white/10 text-center">
              <p class="text-xs text-white/50">離峰電費（夜間充）</p>
              <p class="text-xl font-bold text-white">2.08 <span class="text-sm font-normal text-white/60">元/kWh</span></p>
            </div>
            <div class="flex-1 text-center text-white/40 text-lg">→</div>
            <div class="flex-1 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-center">
              <p class="text-xs text-amber-300/70">MCUT 場域收購</p>
              <p class="text-xl font-bold text-amber-300">12.5 <span class="text-sm font-normal text-amber-300/60">元/kWh</span></p>
            </div>
            <div class="flex-1 text-center text-white/40 text-lg">→</div>
            <div class="flex-1 p-3 rounded-xl bg-blue-500/10 border border-blue-500/30 text-center">
              <p class="text-xs text-blue-300/70">台電收購（含輔助服務）</p>
              <p class="text-xl font-bold text-blue-300">15–16 <span class="text-sm font-normal text-blue-300/60">元/kWh</span></p>
            </div>
          </div>
        </div>

        <!-- 套利拆解 -->
        <div class="p-5 rounded-xl bg-white/5 border border-white/10">
          <h3 class="font-bold text-lg mb-4 text-amber-300">套利空間拆解</h3>
          <div class="space-y-3">
            <div class="flex justify-between items-center border-b border-white/10 pb-3">
              <span class="text-white/80">車主套利（收購 − 充電成本）</span>
              <span class="font-mono text-emerald-300 font-bold">12.5 − 2.08 ≈ <span class="text-white">10</span> 元/kWh</span>
            </div>
            <div class="flex justify-between items-center border-b border-white/10 pb-3">
              <span class="text-white/80">MCUT 差價（台電 − 收購車主）</span>
              <span class="font-mono text-amber-300 font-bold">15 − 12.5 ≈ <span class="text-white">2.5–3.5</span> 元/kWh</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-white/80">台電支付（輔助服務市場）</span>
              <span class="font-mono text-blue-300 font-bold"><span class="text-white">15–16</span> 元/kWh</span>
            </div>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
          <p class="text-amber-300 text-sm">
            <strong>關鍵前提：</strong>台電尖峰電價約 4.91 元/kWh，輔助服務（dReg/E-dReg）讓收購價可達 15–16 元，這才讓整個套利鏈成立。
          </p>
        </div>
      </div>
    </div>

    <!-- Step 4: Interactive Calculator -->
    <div v-if="currentSlide.view === 'calculation'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto space-y-6">
        <h2 class="text-xl md:text-2xl font-bold text-center">互動收益計算器</h2>
        <p class="text-center text-white/60 text-sm">拖拉下方滑桿，即時估算您的 V2G 收益</p>

        <!-- Slider -->
        <div class="p-6 rounded-xl bg-white/5 border border-white/10 space-y-4">
          <div class="flex justify-between items-center">
            <label class="text-white/70 text-sm font-medium">每日可調度電量</label>
            <span class="text-amber-300 font-bold text-xl">{{ adjustableKwh }} kWh</span>
          </div>
          <input
            v-model="adjustableKwh"
            type="range"
            min="20"
            max="100"
            step="5"
            class="w-full h-2 rounded-full appearance-none cursor-pointer"
            style="accent-color: #f59e0b;"
          />
          <div class="flex justify-between text-xs text-white/40">
            <span>20 kWh（小型 EV）</span>
            <span>100 kWh（Neta N7 滿充）</span>
          </div>
        </div>

        <!-- 即時結果 -->
        <div class="grid grid-cols-2 gap-4">
          <div class="p-5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-center">
            <p class="text-amber-300/80 text-sm mb-1">每日收益</p>
            <p class="text-3xl font-bold text-white">{{ dailyProfit.toLocaleString() }}</p>
            <p class="text-white/50 text-xs mt-1">元</p>
          </div>
          <div class="p-5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-center">
            <p class="text-emerald-300/80 text-sm mb-1">每月收益（×20天）</p>
            <p class="text-3xl font-bold text-white">{{ monthlyProfit.toLocaleString() }}</p>
            <p class="text-white/50 text-xs mt-1">元</p>
          </div>
        </div>

        <!-- 計算說明 -->
        <div class="p-4 rounded-xl bg-white/5 border border-white/10 text-sm text-white/60">
          <p class="font-mono">收益 = {{ adjustableKwh }} kWh × 10 元（套利空間）= {{ dailyProfit.toLocaleString() }} 元/日</p>
          <p class="mt-1 text-xs text-white/40">套利空間 = 場域收購價 12.5 − 離峰充電成本 2.08 ≈ 10 元/kWh（未扣除電池損耗成本）</p>
        </div>
      </div>
    </div>

    <!-- Step 5: Battery Cost -->
    <div v-if="currentSlide.view === 'battery-cost'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <h2 class="text-xl md:text-2xl font-bold text-center">電池損耗成本分析</h2>

        <!-- LFP vs NMC -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-5 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-2xl">✅</span>
              <h3 class="font-bold text-emerald-300 text-lg">LFP（磷酸鐵鋰）</h3>
            </div>
            <ul class="space-y-2 text-sm text-white/70">
              <li class="flex justify-between">
                <span>循環壽命</span>
                <span class="text-emerald-300 font-semibold">5,000–10,000 次</span>
              </li>
              <li class="flex justify-between">
                <span>V2G 適合度</span>
                <span class="text-emerald-300 font-semibold">首選</span>
              </li>
              <li class="flex justify-between">
                <span>代表車款</span>
                <span class="text-white/60">Neta N7、比亞迪</span>
              </li>
            </ul>
            <div class="mt-3 p-2 rounded-lg bg-emerald-500/10 text-xs text-emerald-300/80">
              每次循環損耗成本低，V2G 頻繁充放電仍划算
            </div>
          </div>

          <div class="p-5 rounded-xl bg-red-500/10 border border-red-500/30">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-2xl">⚠️</span>
              <h3 class="font-bold text-red-300 text-lg">NMC（三元鋰）</h3>
            </div>
            <ul class="space-y-2 text-sm text-white/70">
              <li class="flex justify-between">
                <span>循環壽命</span>
                <span class="text-red-300 font-semibold">500–1,500 次</span>
              </li>
              <li class="flex justify-between">
                <span>V2G 適合度</span>
                <span class="text-red-300 font-semibold">需補償才划算</span>
              </li>
              <li class="flex justify-between">
                <span>代表車款</span>
                <span class="text-white/60">特斯拉 Model 3 舊款</span>
              </li>
            </ul>
            <div class="mt-3 p-2 rounded-lg bg-red-500/10 text-xs text-red-300/80">
              每次循環損耗成本高，需要更高補償費率才有誘因
            </div>
          </div>
        </div>

        <!-- 充電功率影響 -->
        <div class="p-5 rounded-xl bg-white/5 border border-white/10">
          <h3 class="font-bold text-lg mb-3 text-amber-300">充電功率建議</h3>
          <div class="space-y-3">
            <div class="flex items-center gap-4">
              <div class="w-20 text-right shrink-0">
                <span class="font-mono text-emerald-300 font-bold">7 kW</span>
              </div>
              <div class="flex-1 h-2 rounded-full bg-emerald-500/30">
                <div class="h-2 rounded-full bg-emerald-500" style="width: 35%;"></div>
              </div>
              <div class="w-36 text-xs text-white/60">0.3C — 日常 V2G 建議</div>
            </div>
            <div class="flex items-center gap-4">
              <div class="w-20 text-right shrink-0">
                <span class="font-mono text-yellow-300 font-bold">11 kW</span>
              </div>
              <div class="flex-1 h-2 rounded-full bg-yellow-500/30">
                <div class="h-2 rounded-full bg-yellow-500" style="width: 55%;"></div>
              </div>
              <div class="w-36 text-xs text-white/60">0.4C — 可接受</div>
            </div>
            <div class="flex items-center gap-4">
              <div class="w-20 text-right shrink-0">
                <span class="font-mono text-red-300 font-bold">22 kW</span>
              </div>
              <div class="flex-1 h-2 rounded-full bg-red-500/30">
                <div class="h-2 rounded-full bg-red-500" style="width: 100%;"></div>
              </div>
              <div class="w-36 text-xs text-white/60">1.0C — 僅緊急調峰用</div>
            </div>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
          <p class="text-amber-300 text-sm">
            <strong>最佳操作區間：</strong>SOC 20%–90%，V2G 放電維持在 90%→65%（DoD 25%），研究顯示可有效延長電池壽命。
          </p>
        </div>
      </div>
    </div>

    <!-- Step 6: Quiz -->
    <div v-if="currentSlide.view === 'quiz'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto space-y-6">
        <h3 class="text-xl font-bold text-center">🧪 小測驗：車主每度電的套利空間約是多少？</h3>
        <p class="text-center text-white/50 text-sm">提示：場域收購 12.5 元/kWh，離峰充電 2.08 元/kWh</p>

        <div class="grid grid-cols-2 gap-3">
          <button
            v-for="option in [
              { value: '4', label: '約 4 元/kWh' },
              { value: '7', label: '約 7 元/kWh' },
              { value: '10', label: '約 10 元/kWh' },
              { value: '15', label: '約 15 元/kWh' },
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
      <div class="max-w-3xl mx-auto space-y-6">
        <div class="text-center space-y-2">
          <div class="text-5xl">💡</div>
          <h2 class="text-2xl md:text-3xl font-bold">總結：V2G 商業模式關鍵點</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- 誰能參與 -->
          <div class="p-5 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
            <h3 class="font-bold text-emerald-300 mb-3">誰能參與？</h3>
            <ul class="space-y-2 text-sm text-white/70">
              <li class="flex gap-2"><span class="text-emerald-400">✓</span>擁有 LFP 電池 EV</li>
              <li class="flex gap-2"><span class="text-emerald-400">✓</span>支援 ISO 15118-20 雙向充電</li>
              <li class="flex gap-2"><span class="text-emerald-400">✓</span>停車於 MCUT 場域</li>
              <li class="flex gap-2"><span class="text-emerald-400">✓</span>簽署調度授權協議</li>
            </ul>
          </div>

          <!-- 怎麼參與 -->
          <div class="p-5 rounded-xl bg-amber-500/10 border border-amber-500/20">
            <h3 class="font-bold text-amber-300 mb-3">怎麼參與？</h3>
            <ul class="space-y-2 text-sm text-white/70">
              <li class="flex gap-2"><span class="text-amber-400">1.</span>離峰時段充飽（2.08 元/kWh）</li>
              <li class="flex gap-2"><span class="text-amber-400">2.</span>在 App 設定最低保留電量</li>
              <li class="flex gap-2"><span class="text-amber-400">3.</span>系統自動調度放電</li>
              <li class="flex gap-2"><span class="text-amber-400">4.</span>每月結算收益入帳</li>
            </ul>
          </div>

          <!-- 限制與風險 -->
          <div class="p-5 rounded-xl bg-red-500/10 border border-red-500/20">
            <h3 class="font-bold text-red-300 mb-3">限制與風險</h3>
            <ul class="space-y-2 text-sm text-white/70">
              <li class="flex gap-2"><span class="text-red-400">⚠</span>NMC 電池損耗成本較高</li>
              <li class="flex gap-2"><span class="text-red-400">⚠</span>台電輔助服務規則可能調整</li>
              <li class="flex gap-2"><span class="text-red-400">⚠</span>22 kW 高功率加速老化</li>
              <li class="flex gap-2"><span class="text-red-400">⚠</span>聚合商信任與合約條款</li>
            </ul>
          </div>
        </div>

        <!-- 數字總結 -->
        <div class="p-5 rounded-xl bg-white/5 border border-white/10">
          <h3 class="font-bold text-lg mb-3 text-amber-300">核心數字回顧</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-center text-sm">
            <div>
              <p class="text-white/50">離峰電費</p>
              <p class="text-lg font-bold text-white">2.08 元</p>
            </div>
            <div>
              <p class="text-white/50">場域收購</p>
              <p class="text-lg font-bold text-amber-300">12.5 元</p>
            </div>
            <div>
              <p class="text-white/50">套利空間</p>
              <p class="text-lg font-bold text-emerald-300">≈ 10 元</p>
            </div>
            <div>
              <p class="text-white/50">月收益試算</p>
              <p class="text-lg font-bold text-emerald-300">16,000 元</p>
            </div>
          </div>
        </div>

        <p class="text-white/40 text-sm text-center">
          參考文獻：Kempton & Tomic (2005)、Sovacool et al. (2020)、MCUT 場域試算
        </p>
      </div>
    </div>

  </InteractiveSlideTemplate>
</template>
