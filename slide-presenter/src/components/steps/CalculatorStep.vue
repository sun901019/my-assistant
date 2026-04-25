<script setup lang="ts">
import { ref, computed } from 'vue'
import type { CalculatorStep } from '../../types/slide-json'

const props = defineProps<{ step: CalculatorStep }>()

const sliderValues = ref<Record<string, number>>(
  Object.fromEntries(props.step.sliders.map(s => [s.key, s.default]))
)

function evaluate(formula: string): number {
  try {
    const keys = Object.keys(sliderValues.value)
    const vals = Object.values(sliderValues.value)
    // eslint-disable-next-line no-new-func
    return new Function(...keys, `return ${formula}`)(...vals)
  } catch {
    return 0
  }
}

const outputValues = computed(() =>
  props.step.outputs.map(o => ({
    ...o,
    computed: evaluate(o.formula).toFixed(o.decimals ?? 1),
  }))
)

const colorMap: Record<string, string> = {
  sky:     'bg-sky-500/10 border-sky-500/20 text-sky-300',
  amber:   'bg-amber-500/10 border-amber-500/20 text-amber-300',
  emerald: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-300',
  purple:  'bg-purple-500/10 border-purple-500/20 text-purple-300',
}
function outputClass(color?: string) {
  return colorMap[color ?? ''] ?? 'bg-white/5 border-white/10 text-white/80'
}
</script>

<template>
  <div class="animate-fade-in max-w-3xl mx-auto space-y-6">
    <div class="p-6 rounded-xl bg-white/5 border border-white/10 space-y-5">
      <h3 v-if="step.prompt" class="font-bold text-center">{{ step.prompt }}</h3>
      <div class="space-y-4">
        <div v-for="slider in step.sliders" :key="slider.key">
          <label class="text-white/60 text-sm">{{ slider.label }}</label>
          <div class="flex items-center gap-3 mt-1">
            <input
              type="range"
              v-model.number="sliderValues[slider.key]"
              :min="slider.min"
              :max="slider.max"
              :step="slider.step"
              class="flex-1 accent-sky-400"
            />
            <span class="text-sky-300 font-mono w-20 text-right">
              {{ sliderValues[slider.key] }} {{ slider.unit }}
            </span>
          </div>
        </div>
      </div>
      <div :class="step.outputs.length === 1 ? 'flex justify-center' : `grid grid-cols-${step.outputs.length} gap-4`">
        <div
          v-for="out in outputValues"
          :key="out.label"
          class="p-4 rounded-xl border text-center"
          :class="outputClass(out.color)"
        >
          <div class="text-3xl font-bold">{{ out.computed }}</div>
          <div class="text-xs mt-1 opacity-60">{{ out.unit }}</div>
          <div class="text-xs mt-1 opacity-50">{{ out.label }}</div>
        </div>
      </div>
    </div>
    <div
      v-if="step.note"
      class="p-4 rounded-xl bg-white/5 border border-white/10 text-center text-sm text-white/70"
    >
      💡 {{ step.note }}
    </div>
  </div>
</template>
