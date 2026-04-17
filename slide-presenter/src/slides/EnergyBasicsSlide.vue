<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import InteractiveSlideTemplate from '../components/InteractiveSlideTemplate.vue'
import type { Step, FeedbackType } from '../types/slide'

defineProps<{ isMobile?: boolean }>()
const emit = defineEmits<{ complete: [] }>()

const steps: readonly Step[] = [
  { id: 0, view: 'welcome',       title: '歡迎',         desc: '搞懂電的基本概念' },
  { id: 1, view: 'power-basics',  title: '電壓、電流、功率', desc: '用水管來理解' },
  { id: 2, view: 'energy-kwh',    title: '電能是什麼',    desc: '你家電費帳單上的那個數字' },
  { id: 3, view: 'battery',       title: '電池怎麼運作',  desc: 'SOC、DoD、C-rate 一次搞清楚' },
  { id: 4, view: 'solar',         title: '太陽能發電',    desc: '陽光進來，電就出去' },
  { id: 5, view: 'charger',       title: '充電樁有幾種',  desc: '7kW、22kW、快充有什麼差' },
  { id: 6, view: 'quiz',          title: '小測驗',        desc: '確認你真的懂了' },
  { id: 7, view: 'summary',       title: '總結',          desc: '把今天學到的收起來' },
]

const currentStep = ref(0)
const currentSlide = computed(() => steps[currentStep.value])

// kWh 互動計算
const applianceHours = ref(8)
const appliancePower = ref(1.2) // kW，冷氣預設值
const calculatedKwh = computed(() => (appliancePower.value * applianceHours.value).toFixed(1))
const calculatedCost = computed(() => (Number(calculatedKwh.value) * 3.5).toFixed(0))

// 電池互動
const batterySOC = ref(80)
const batteryCapacity = 100 // kWh (Neta N7)
const remainingKwh = computed(() => Math.round(batteryCapacity * batterySOC.value / 100))
const dod = computed(() => 100 - batterySOC.value)

// 充電樁互動
const selectedCharger = ref<'slow' | 'medium' | 'fast'>('slow')
const chargerInfo = {
  slow:   { label: '慢充 AC 7kW',   power: 7,   hours: (100/7).toFixed(1),  icon: '🐢', color: 'sky',     use: '家用、一般停車場' },
  medium: { label: '中速 AC 22kW',  power: 22,  hours: (100/22).toFixed(1), icon: '🚗', color: 'emerald', use: '辦公室、校園' },
  fast:   { label: '快充 DC 150kW', power: 150, hours: (100/150).toFixed(1), icon: '⚡', color: 'amber',  use: '高速公路、商場' },
}
const selected = computed(() => chargerInfo[selectedCharger.value])

// 測驗
const quizAnswer = ref('')
const feedback = ref('')
const feedbackType = ref<FeedbackType>('neutral')

const canGoNext = computed(() => {
  if (currentSlide.value.view === 'quiz') return feedbackType.value === 'success'
  return true
})

function checkAnswer(answer: string) {
  quizAnswer.value = answer
  if (answer === 'kwh') {
    feedback.value = '✅ 答對了！kWh（千瓦時）就是電能的單位，你家電費帳單上計費的就是這個。'
    feedbackType.value = 'success'
  } else {
    feedback.value = '❌ 再想想看，電費帳單上說你「用了幾度電」，那個「度」是什麼單位？'
    feedbackType.value = 'error'
  }
}

watch(() => currentSlide.value.view, () => {
  feedback.value = ''
  feedbackType.value = 'neutral'
  quizAnswer.value = ''
})

function next() { if (currentStep.value < steps.length - 1) currentStep.value++ }
function prev() { if (currentStep.value > 0) currentStep.value-- }
function goto(i: number) { currentStep.value = i }
</script>

<template>
  <InteractiveSlideTemplate
    title="能源基礎入門"
    subtitle="從電壓、電池到充電樁，一次搞清楚"
    icon="🔋"
    :total-steps="steps.length"
    :current-step="currentStep"
    :step-title="currentSlide.title"
    :step-desc="currentSlide.desc"
    theme-color="sky"
    :can-go-next="canGoNext"
    :next-step-hint="!canGoNext ? '請先完成測驗' : ''"
    @prev="prev"
    @next="next"
    @goto="goto"
    @complete="emit('complete')"
  >

    <!-- ── Step 0: Welcome ─────────────────────────────── -->
    <div v-if="currentSlide.view === 'welcome'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto text-center space-y-6">
        <div class="text-7xl">⚡</div>
        <h2 class="text-2xl md:text-4xl font-bold">電，你真的懂嗎？</h2>
        <p class="text-lg text-white/70">每天都在用電、充電，但你知道「電壓」「電流」「kWh」是什麼意思嗎？</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-6">
          <div v-for="item in [
            { icon: '💧', text: '電壓、電流、功率' },
            { icon: '🔋', text: '電池 SOC / DoD' },
            { icon: '🔌', text: '充電樁 7kW vs 快充' },
          ]" :key="item.text"
            class="p-4 rounded-xl bg-sky-500/10 border border-sky-500/20 text-sky-300 text-sm font-medium">
            <div class="text-2xl mb-2">{{ item.icon }}</div>
            {{ item.text }}
          </div>
        </div>
        <p class="text-white/40 text-sm mt-4">5 分鐘，全部搞定 👇</p>
      </div>
    </div>

    <!-- ── Step 1: Power Basics ────────────────────────── -->
    <div v-if="currentSlide.view === 'power-basics'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <p class="text-center text-white/70">想像一條水管 🚿</p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-5 rounded-xl bg-blue-500/10 border border-blue-500/20 text-center space-y-2">
            <div class="text-4xl">💧</div>
            <div class="text-blue-300 font-bold text-lg">電壓（V）</div>
            <div class="text-white/60 text-sm">= 水壓</div>
            <div class="text-white/80 text-sm">推動電子流動的「壓力」<br/>家用插座約 110V</div>
          </div>
          <div class="p-5 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-center space-y-2">
            <div class="text-4xl">🌊</div>
            <div class="text-cyan-300 font-bold text-lg">電流（A）</div>
            <div class="text-white/60 text-sm">= 水流量</div>
            <div class="text-white/80 text-sm">每秒流過的電子數量<br/>越大，能驅動越大的設備</div>
          </div>
          <div class="p-5 rounded-xl bg-sky-500/10 border border-sky-500/20 text-center space-y-2">
            <div class="text-4xl">⚡</div>
            <div class="text-sky-300 font-bold text-lg">功率（W）</div>
            <div class="text-white/60 text-sm">= 水管出力</div>
            <div class="text-white/80 text-sm">W = V × A<br/>燈泡 60W、冷氣 1200W</div>
          </div>
        </div>
        <div class="p-5 rounded-xl bg-white/5 border border-white/10 text-center">
          <p class="text-white/80">💡 <strong class="text-sky-300">功率越大</strong>，代表設備「工作能力」越強——但也吃更多電！</p>
          <div class="mt-3 flex justify-center gap-6 text-sm text-white/50">
            <span>💡 LED燈 = 10W</span>
            <span>❄️ 冷氣 = 1,200W = 1.2kW</span>
            <span>🔌 電動車充電 = 7,000–22,000W</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Step 2: Energy kWh ──────────────────────────── -->
    <div v-if="currentSlide.view === 'energy-kwh'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <div class="text-center space-y-2">
          <p class="text-white/70">功率（kW）× 時間（小時）= <strong class="text-sky-300 text-xl">電能（kWh）</strong></p>
          <p class="text-white/40 text-sm">就是你家電費帳單上的「度數」</p>
        </div>

        <!-- 互動計算器 -->
        <div class="p-6 rounded-xl bg-white/5 border border-white/10 space-y-5">
          <h3 class="font-bold text-center">🧮 算算看：冷氣開一晚用多少電？</h3>
          <div class="space-y-4">
            <div>
              <label class="text-white/60 text-sm">冷氣功率</label>
              <div class="flex items-center gap-3 mt-1">
                <input type="range" v-model.number="appliancePower" min="0.5" max="3" step="0.1"
                  class="flex-1 accent-sky-400" />
                <span class="text-sky-300 font-mono w-16 text-right">{{ appliancePower }} kW</span>
              </div>
            </div>
            <div>
              <label class="text-white/60 text-sm">使用時數</label>
              <div class="flex items-center gap-3 mt-1">
                <input type="range" v-model.number="applianceHours" min="1" max="24" step="1"
                  class="flex-1 accent-sky-400" />
                <span class="text-sky-300 font-mono w-16 text-right">{{ applianceHours }} 小時</span>
              </div>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4 pt-2">
            <div class="p-4 rounded-xl bg-sky-500/10 border border-sky-500/20 text-center">
              <div class="text-3xl font-bold text-sky-300">{{ calculatedKwh }}</div>
              <div class="text-white/50 text-sm mt-1">度電（kWh）</div>
            </div>
            <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
              <div class="text-3xl font-bold text-amber-300">約 {{ calculatedCost }} 元</div>
              <div class="text-white/50 text-sm mt-1">電費（約 3.5元/度）</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Step 3: Battery ─────────────────────────────── -->
    <div v-if="currentSlide.view === 'battery'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 space-y-2">
            <div class="text-2xl">🔋</div>
            <div class="text-emerald-300 font-bold">SOC</div>
            <div class="text-white/50 text-xs">State of Charge</div>
            <div class="text-white/80 text-sm">剩餘電量百分比，就像手機電池格數，0% = 沒電，100% = 充滿</div>
          </div>
          <div class="p-5 rounded-xl bg-orange-500/10 border border-orange-500/20 space-y-2">
            <div class="text-2xl">📉</div>
            <div class="text-orange-300 font-bold">DoD</div>
            <div class="text-white/50 text-xs">Depth of Discharge</div>
            <div class="text-white/80 text-sm">放電深度。從 100% 放到 20%，DoD = 80%。DoD 越大，電池老化越快</div>
          </div>
          <div class="p-5 rounded-xl bg-purple-500/10 border border-purple-500/20 space-y-2">
            <div class="text-2xl">⏱️</div>
            <div class="text-purple-300 font-bold">C-rate</div>
            <div class="text-white/50 text-xs">充放電倍率</div>
            <div class="text-white/80 text-sm">1C = 1小時充滿。0.5C = 2小時，2C = 30分鐘。倍率越高，老化越快</div>
          </div>
        </div>

        <!-- 互動電池 -->
        <div class="p-5 rounded-xl bg-white/5 border border-white/10 space-y-3">
          <h3 class="font-bold text-center text-sm text-white/70">🎮 拖拉看看：調整電動車的 SOC</h3>
          <div class="flex items-center gap-3">
            <input type="range" v-model.number="batterySOC" min="0" max="100" step="5"
              class="flex-1 accent-emerald-400" />
            <span class="text-emerald-300 font-mono w-16 text-right">{{ batterySOC }}%</span>
          </div>
          <div class="grid grid-cols-3 gap-3 text-center text-sm">
            <div class="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
              <div class="text-emerald-300 font-bold text-lg">{{ batterySOC }}%</div>
              <div class="text-white/40 text-xs">SOC</div>
            </div>
            <div class="p-3 rounded-lg bg-sky-500/10 border border-sky-500/20">
              <div class="text-sky-300 font-bold text-lg">{{ remainingKwh }} kWh</div>
              <div class="text-white/40 text-xs">剩餘電量</div>
            </div>
            <div class="p-3 rounded-lg bg-orange-500/10 border border-orange-500/20">
              <div class="text-orange-300 font-bold text-lg">{{ dod }}%</div>
              <div class="text-white/40 text-xs">DoD（已放電）</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Step 4: Solar ───────────────────────────────── -->
    <div v-if="currentSlide.view === 'solar'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-6">
        <div class="text-center">
          <div class="text-5xl">☀️</div>
          <p class="text-white/70 mt-2">太陽能板把陽光直接轉成電，不需要燃料</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-5 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-3">
            <h3 class="font-bold text-amber-300">⚡ 影響發電量的因素</h3>
            <div class="space-y-2 text-sm text-white/80">
              <div class="flex gap-2"><span class="text-amber-400">☀️</span><span><strong>日照強度</strong>（W/m²）— 雲越多越少電</span></div>
              <div class="flex gap-2"><span class="text-red-400">🌡️</span><span><strong>模組溫度</strong>— 越熱效率越低（反直覺！）</span></div>
              <div class="flex gap-2"><span class="text-blue-400">🌧️</span><span><strong>雨水清洗</strong>— 灰塵遮蔽會減少發電</span></div>
            </div>
          </div>
          <div class="p-5 rounded-xl bg-white/5 border border-white/10 space-y-3">
            <h3 class="font-bold text-white/80">🔍 異常偵測邏輯</h3>
            <div class="space-y-2 text-sm text-white/70">
              <div class="p-2 rounded bg-white/5">1. 用日照 + 溫度預測「應該發多少電」</div>
              <div class="p-2 rounded bg-white/5">2. 對照「實際發了多少電」</div>
              <div class="p-2 rounded bg-amber-500/10 border border-amber-500/20 text-amber-200">3. 誤差太大 → 可能是板子髒了、設備故障</div>
            </div>
          </div>
        </div>
        <div class="p-4 rounded-xl bg-sky-500/10 border border-sky-500/20 text-center text-sm text-sky-300">
          💡 明志科大已裝設太陽能板 + 日照計 + 溫度感測器，正在研究如何預測發電與偵測異常
        </div>
      </div>
    </div>

    <!-- ── Step 5: Charger ─────────────────────────────── -->
    <div v-if="currentSlide.view === 'charger'" class="animate-fade-in">
      <div class="max-w-3xl mx-auto space-y-5">
        <p class="text-center text-white/60 text-sm">點選充電樁，看看差在哪</p>
        <div class="grid grid-cols-3 gap-3">
          <button v-for="(info, key) in chargerInfo" :key="key"
            class="p-4 rounded-xl border text-center transition-all"
            :class="selectedCharger === key
              ? `border-${info.color}-400 bg-${info.color}-500/20`
              : 'border-white/10 bg-white/5 hover:bg-white/10'"
            @click="selectedCharger = key as 'slow' | 'medium' | 'fast'">
            <div class="text-3xl mb-1">{{ info.icon }}</div>
            <div class="text-xs font-medium text-white/80">{{ info.label }}</div>
          </button>
        </div>

        <div class="p-6 rounded-xl bg-white/5 border border-white/10 space-y-4">
          <div class="flex items-center gap-3">
            <span class="text-4xl">{{ selected.icon }}</span>
            <div>
              <div class="font-bold text-lg text-white">{{ selected.label }}</div>
              <div class="text-white/50 text-sm">適用：{{ selected.use }}</div>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div class="p-3 rounded-lg bg-white/5 text-center">
              <div class="text-2xl font-bold text-sky-300">{{ selected.power }} kW</div>
              <div class="text-white/40 text-xs mt-1">充電功率</div>
            </div>
            <div class="p-3 rounded-lg bg-white/5 text-center">
              <div class="text-2xl font-bold text-emerald-300">~{{ selected.hours }} 小時</div>
              <div class="text-white/40 text-xs mt-1">充滿 100kWh 電動車</div>
            </div>
          </div>
          <div class="text-center text-xs text-white/40">
            V2G 雙向充放電樁 = 7–22kW，可以充電也可以把電賣回電網
          </div>
        </div>
      </div>
    </div>

    <!-- ── Step 6: Quiz ────────────────────────────────── -->
    <div v-if="currentSlide.view === 'quiz'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto space-y-6">
        <h3 class="text-xl font-bold text-center">🧪 你家電費帳單上計費的單位是什麼？</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <button v-for="opt in [
            { value: 'watt',  label: '⚡ 瓦特（W）' },
            { value: 'kwh',   label: '🔋 千瓦時（kWh）' },
            { value: 'volt',  label: '💧 伏特（V）' },
            { value: 'amp',   label: '🌊 安培（A）' },
          ]" :key="opt.value"
            class="p-4 rounded-xl border text-left transition-all"
            :class="quizAnswer === opt.value && feedbackType === 'success'
              ? 'border-emerald-400 bg-emerald-500/20 text-emerald-300'
              : quizAnswer === opt.value && feedbackType === 'error'
                ? 'border-red-400 bg-red-500/20 text-red-300'
                : 'border-white/10 bg-white/5 hover:bg-white/10 text-white/80'"
            @click="checkAnswer(opt.value)">
            {{ opt.label }}
          </button>
        </div>
        <div v-if="feedback"
          class="p-4 rounded-xl text-center text-sm"
          :class="feedbackType === 'success'
            ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-300'
            : 'bg-red-500/10 border border-red-500/20 text-red-300'">
          {{ feedback }}
        </div>
      </div>
    </div>

    <!-- ── Step 7: Summary ─────────────────────────────── -->
    <div v-if="currentSlide.view === 'summary'" class="animate-fade-in">
      <div class="max-w-2xl mx-auto text-center space-y-6">
        <div class="text-5xl">🎉</div>
        <h2 class="text-2xl font-bold">能源基礎，搞定！</h2>
        <div class="text-left space-y-3 p-6 rounded-xl bg-white/5 border border-white/10">
          <div class="flex gap-3 items-start">
            <span class="text-sky-400 font-bold">1</span>
            <span class="text-white/80"><strong class="text-sky-300">W = V × A</strong>，功率是電壓乘以電流；kWh = kW × 小時，是電費帳單的計算單位</span>
          </div>
          <div class="flex gap-3 items-start">
            <span class="text-emerald-400 font-bold">2</span>
            <span class="text-white/80">電池用 <strong class="text-emerald-300">SOC</strong>（剩餘電量）、<strong class="text-emerald-300">DoD</strong>（放電深度）、<strong class="text-emerald-300">C-rate</strong>（充放速率）來描述狀態與老化</span>
          </div>
          <div class="flex gap-3 items-start">
            <span class="text-amber-400 font-bold">3</span>
            <span class="text-white/80">充電樁有 <strong class="text-amber-300">7kW 慢充</strong>、<strong class="text-amber-300">22kW 中速</strong>、<strong class="text-amber-300">150kW 快充</strong>；V2G 雙向樁讓電動車可以充電也可以放電賺錢</span>
          </div>
        </div>
        <p class="text-white/40 text-sm">下一步：V2G 是什麼？→ 你的電動車如何幫你賺錢 ⚡</p>
      </div>
    </div>

  </InteractiveSlideTemplate>
</template>
