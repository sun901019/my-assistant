<script setup lang="ts">
import { ref, computed } from 'vue'
import type { SelectorStep } from '../../types/slide-json'

const props = defineProps<{ step: SelectorStep }>()
const selectedKey = ref(props.step.options[0]?.key ?? '')
const selected = computed(() => props.step.options.find(o => o.key === selectedKey.value))

const detailColorMap: Record<string, string> = {
  sky:     'text-sky-300',
  amber:   'text-amber-300',
  emerald: 'text-emerald-300',
  purple:  'text-purple-300',
}
</script>

<template>
  <div class="animate-fade-in max-w-3xl mx-auto space-y-5">
    <p v-if="step.prompt" class="text-center text-white/60 text-sm">{{ step.prompt }}</p>
    <div :class="`grid grid-cols-${step.options.length} gap-3`">
      <button
        v-for="opt in step.options"
        :key="opt.key"
        class="p-4 rounded-xl border text-center transition-all"
        :class="selectedKey === opt.key
          ? 'border-sky-400 bg-sky-500/20'
          : 'border-white/10 bg-white/5 hover:bg-white/10'"
        @click="selectedKey = opt.key"
      >
        <div class="text-3xl mb-1">{{ opt.icon }}</div>
        <div class="text-xs font-medium text-white/80">{{ opt.label }}</div>
      </button>
    </div>
    <div v-if="selected" class="p-6 rounded-xl bg-white/5 border border-white/10 space-y-4">
      <div class="flex items-center gap-3">
        <span class="text-4xl">{{ selected.icon }}</span>
        <div class="font-bold text-lg text-white">{{ selected.label }}</div>
      </div>
      <div :class="`grid grid-cols-${Math.min(selected.details.length, 3)} gap-4`">
        <div
          v-for="detail in selected.details"
          :key="detail.label"
          class="p-3 rounded-lg bg-white/5 text-center"
        >
          <div
            class="text-2xl font-bold"
            :class="detailColorMap[detail.color ?? ''] ?? 'text-white/80'"
          >{{ detail.value }}</div>
          <div class="text-white/40 text-xs mt-1">{{ detail.label }}</div>
        </div>
      </div>
      <div v-if="selected.note" class="text-center text-xs text-white/40">{{ selected.note }}</div>
    </div>
  </div>
</template>
