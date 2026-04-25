<script setup lang="ts">
import type { SummaryStep } from '../../types/slide-json'
defineProps<{ step: SummaryStep }>()

const colorMap: Record<string, string> = {
  sky:     'text-sky-400',
  amber:   'text-amber-400',
  emerald: 'text-emerald-400',
  purple:  'text-purple-400',
  red:     'text-red-400',
}
function numColor(color?: string) {
  return colorMap[color ?? ''] ?? 'text-white/40'
}
</script>

<template>
  <div class="animate-fade-in max-w-2xl mx-auto text-center space-y-6">
    <div v-if="step.icon" class="text-5xl">{{ step.icon }}</div>
    <h2 class="text-2xl font-bold">{{ step.headline }}</h2>
    <div class="text-left space-y-3 p-6 rounded-xl bg-white/5 border border-white/10">
      <div
        v-for="(point, i) in step.points"
        :key="i"
        class="flex gap-3 items-start"
      >
        <span class="font-bold text-lg" :class="numColor(point.color)">{{ i + 1 }}</span>
        <span class="text-white/80" v-html="point.text" />
      </div>
    </div>
    <p v-if="step.nextHint" class="text-white/40 text-sm">{{ step.nextHint }}</p>
  </div>
</template>
