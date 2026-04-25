<script setup lang="ts">
import { ref, watch } from 'vue'
import type { QuizStep } from '../../types/slide-json'
import type { FeedbackType } from '../../types/slide'

const props = defineProps<{ step: QuizStep }>()
const emit = defineEmits<{ correct: [] }>()

const answer = ref('')
const feedback = ref('')
const feedbackType = ref<FeedbackType>('neutral')

watch(() => props.step, () => {
  answer.value = ''
  feedback.value = ''
  feedbackType.value = 'neutral'
})

function check(value: string) {
  answer.value = value
  if (value === props.step.correctAnswer) {
    feedback.value = props.step.successMsg
    feedbackType.value = 'success'
    emit('correct')
  } else {
    feedback.value = props.step.errorMsg
    feedbackType.value = 'error'
  }
}
</script>

<template>
  <div class="animate-fade-in max-w-2xl mx-auto space-y-6">
    <h3 class="text-xl font-bold text-center">{{ step.question }}</h3>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
      <button
        v-for="opt in step.options"
        :key="opt.value"
        class="p-4 rounded-xl border text-left transition-all"
        :class="answer === opt.value && feedbackType === 'success'
          ? 'border-emerald-400 bg-emerald-500/20 text-emerald-300'
          : answer === opt.value && feedbackType === 'error'
            ? 'border-red-400 bg-red-500/20 text-red-300'
            : 'border-white/10 bg-white/5 hover:bg-white/10 text-white/80'"
        @click="check(opt.value)"
      >
        {{ opt.label }}
      </button>
    </div>
    <div
      v-if="feedback"
      class="p-4 rounded-xl text-center text-sm"
      :class="feedbackType === 'success'
        ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-300'
        : 'bg-red-500/10 border border-red-500/20 text-red-300'"
    >
      {{ feedback }}
    </div>
  </div>
</template>
