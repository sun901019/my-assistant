<script setup lang="ts">
import type { ThemeColor } from '../types/slide'
import { computed } from 'vue'

interface Props {
  title: string
  subtitle?: string
  icon?: string
  totalSteps: number
  currentStep: number
  stepTitle?: string
  stepDesc?: string
  themeColor?: ThemeColor
  canGoNext?: boolean
  nextStepHint?: string
}

const props = withDefaults(defineProps<Props>(), {
  subtitle: '',
  icon: '📘',
  themeColor: 'sky',
  canGoNext: true,
  nextStepHint: '',
  stepTitle: '',
  stepDesc: '',
})

const emit = defineEmits<{
  prev: []
  next: []
  goto: [index: number]
  complete: []
}>()

const isLastStep = computed(() => props.currentStep >= props.totalSteps - 1)
const isFirstStep = computed(() => props.currentStep <= 0)
const progressPercent = computed(() =>
  Math.round(((props.currentStep + 1) / props.totalSteps) * 100)
)

const theme = computed(() => {
  const themes: Record<ThemeColor, {
    progressBg: string
    progressActive: string
    nextBtn: string
    dotActive: string
    headerBg: string
    accent: string
  }> = {
    sky: {
      progressBg: 'bg-sky-900/30',
      progressActive: 'bg-sky-400',
      nextBtn: 'bg-gradient-to-r from-sky-500 to-blue-500 hover:from-sky-400 hover:to-blue-400',
      dotActive: 'bg-sky-400',
      headerBg: 'from-sky-950 to-slate-900',
      accent: 'text-sky-400',
    },
    amber: {
      progressBg: 'bg-amber-900/30',
      progressActive: 'bg-amber-400',
      nextBtn: 'bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400',
      dotActive: 'bg-amber-400',
      headerBg: 'from-amber-950 to-slate-900',
      accent: 'text-amber-400',
    },
    emerald: {
      progressBg: 'bg-emerald-900/30',
      progressActive: 'bg-emerald-400',
      nextBtn: 'bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400',
      dotActive: 'bg-emerald-400',
      headerBg: 'from-emerald-950 to-slate-900',
      accent: 'text-emerald-400',
    },
    purple: {
      progressBg: 'bg-purple-900/30',
      progressActive: 'bg-purple-400',
      nextBtn: 'bg-gradient-to-r from-purple-500 to-violet-500 hover:from-purple-400 hover:to-violet-400',
      dotActive: 'bg-purple-400',
      headerBg: 'from-purple-950 to-slate-900',
      accent: 'text-purple-400',
    },
  }
  return themes[props.themeColor]
})

function handleNext() {
  if (isLastStep.value) {
    emit('complete')
  } else {
    emit('next')
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-white flex flex-col">
    <!-- Header -->
    <header
      class="bg-gradient-to-r px-4 py-3 md:px-6 md:py-4 flex items-center justify-between"
      :class="theme.headerBg"
    >
      <div class="flex items-center gap-2 md:gap-3">
        <span class="text-xl md:text-2xl">{{ icon }}</span>
        <div>
          <h1 class="text-sm md:text-lg font-bold leading-tight">{{ title }}</h1>
          <p v-if="subtitle" class="text-xs md:text-sm text-white/60">{{ subtitle }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2 text-xs md:text-sm text-white/50">
        <span>{{ currentStep + 1 }} / {{ totalSteps }}</span>
      </div>
    </header>

    <!-- Progress bar -->
    <div class="h-1" :class="theme.progressBg">
      <div
        class="h-full transition-all duration-500 ease-out rounded-r"
        :class="theme.progressActive"
        :style="{ width: `${progressPercent}%` }"
      />
    </div>

    <!-- Step info -->
    <div v-if="stepTitle" class="px-4 py-3 md:px-6 md:py-4 bg-slate-800/50 border-b border-white/5">
      <h2 class="text-base md:text-xl font-semibold" :class="theme.accent">{{ stepTitle }}</h2>
      <p v-if="stepDesc" class="text-xs md:text-sm text-white/50 mt-1">{{ stepDesc }}</p>
    </div>

    <!-- Content area (slot) -->
    <main class="flex-1 px-4 py-6 md:px-8 md:py-10 overflow-y-auto">
      <slot />
    </main>

    <!-- Navigation -->
    <nav class="px-4 py-3 md:px-6 md:py-4 bg-slate-800/80 border-t border-white/10 flex items-center justify-between">
      <!-- Prev button -->
      <button
        class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
        :class="isFirstStep
          ? 'text-white/20 cursor-not-allowed'
          : 'text-white/70 hover:text-white hover:bg-white/10'"
        :disabled="isFirstStep"
        @click="emit('prev')"
      >
        ← 上一步
      </button>

      <!-- Dot navigator -->
      <div class="hidden md:flex items-center gap-1.5">
        <button
          v-for="i in totalSteps"
          :key="i"
          class="w-2 h-2 rounded-full transition-all duration-300"
          :class="i - 1 === currentStep
            ? `${theme.dotActive} scale-125`
            : i - 1 < currentStep
              ? `${theme.dotActive} opacity-40`
              : 'bg-white/20'"
          @click="emit('goto', i - 1)"
        />
      </div>

      <!-- Next button -->
      <div class="flex flex-col items-end">
        <button
          class="px-5 py-2 rounded-lg text-sm font-bold text-white transition-all shadow-lg"
          :class="canGoNext
            ? theme.nextBtn
            : 'bg-white/10 text-white/30 cursor-not-allowed'"
          :disabled="!canGoNext"
          @click="handleNext"
        >
          {{ isLastStep ? '✅ 完成學習' : '下一步 →' }}
        </button>
        <span
          v-if="!canGoNext && nextStepHint"
          class="text-xs mt-1 text-amber-400/70"
        >
          {{ nextStepHint }}
        </span>
      </div>
    </nav>
  </div>
</template>
