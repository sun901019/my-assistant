<script setup lang="ts">
import type { WelcomeStep } from '../../types/slide-json'
defineProps<{ step: WelcomeStep }>()
</script>

<template>
  <div class="animate-fade-in max-w-2xl mx-auto text-center space-y-6">
    <div class="text-7xl">{{ step.icon }}</div>
    <h2 class="text-2xl md:text-4xl font-bold">{{ step.headline }}</h2>
    <p v-if="step.subheadline" class="text-lg text-white/70">{{ step.subheadline }}</p>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-6">
      <div
        v-for="f in step.features"
        :key="f.text"
        class="p-4 rounded-xl bg-white/5 border border-white/10 text-white/80 text-sm font-medium"
      >
        <div class="text-2xl mb-2">{{ f.icon }}</div>
        {{ f.text }}
      </div>
    </div>
    <p v-if="step.footer" class="text-white/40 text-sm mt-4">{{ step.footer }}</p>
  </div>
</template>
