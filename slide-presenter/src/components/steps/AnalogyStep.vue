<script setup lang="ts">
import type { AnalogyStep } from '../../types/slide-json'
defineProps<{ step: AnalogyStep }>()
</script>

<template>
  <div class="animate-fade-in max-w-3xl mx-auto space-y-4">
    <div class="grid grid-cols-2 gap-2 text-center text-xs font-bold uppercase tracking-widest text-white/40">
      <div>{{ step.conceptLabel ?? '概念' }}</div>
      <div>{{ step.realLabel ?? '生活比喻' }}</div>
    </div>
    <div class="space-y-3">
      <div
        v-for="pair in step.pairs"
        :key="pair.concept"
        class="grid grid-cols-2 gap-3"
      >
        <div class="p-4 rounded-xl bg-white/5 border border-white/10 text-center">
          <div v-if="pair.icon" class="text-2xl mb-1">{{ pair.icon }}</div>
          <div class="font-bold text-white/90">{{ pair.concept }}</div>
        </div>
        <div class="p-4 rounded-xl bg-sky-500/10 border border-sky-500/20 text-center">
          <div class="text-white/80 text-sm">{{ pair.real }}</div>
        </div>
      </div>
    </div>
    <div
      v-if="step.note"
      class="p-4 rounded-xl bg-white/5 border border-white/10 text-center text-sm text-white/70 mt-2"
    >
      💡 {{ step.note }}
    </div>
  </div>
</template>
