<script setup lang="ts">
import type { CardsStep } from '../../types/slide-json'
defineProps<{ step: CardsStep }>()

const colorMap: Record<string, string> = {
  blue:    'bg-blue-500/10 border-blue-500/20 text-blue-300',
  cyan:    'bg-cyan-500/10 border-cyan-500/20 text-cyan-300',
  sky:     'bg-sky-500/10 border-sky-500/20 text-sky-300',
  green:   'bg-emerald-500/10 border-emerald-500/20 text-emerald-300',
  emerald: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-300',
  amber:   'bg-amber-500/10 border-amber-500/20 text-amber-300',
  orange:  'bg-orange-500/10 border-orange-500/20 text-orange-300',
  purple:  'bg-purple-500/10 border-purple-500/20 text-purple-300',
  red:     'bg-red-500/10 border-red-500/20 text-red-300',
}

function cardClass(color?: string): string {
  return colorMap[color ?? ''] ?? 'bg-white/5 border-white/10 text-white/80'
}
</script>

<template>
  <div class="animate-fade-in max-w-3xl mx-auto space-y-6">
    <div
      :class="step.cards.length === 2 ? 'grid grid-cols-1 md:grid-cols-2 gap-4' : 'grid grid-cols-1 md:grid-cols-3 gap-4'"
    >
      <div
        v-for="card in step.cards"
        :key="card.title"
        class="p-5 rounded-xl border text-center space-y-2"
        :class="cardClass(card.color)"
      >
        <div class="text-4xl">{{ card.icon }}</div>
        <div class="font-bold text-lg">{{ card.title }}</div>
        <div v-if="card.subtitle" class="text-white/50 text-xs">{{ card.subtitle }}</div>
        <div class="text-white/80 text-sm">{{ card.body }}</div>
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
