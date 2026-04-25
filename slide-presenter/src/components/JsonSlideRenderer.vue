<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { SlideJSON, AnyJsonStep } from '../types/slide-json'
import type { FeedbackType } from '../types/slide'
import InteractiveSlideTemplate from './InteractiveSlideTemplate.vue'
import WelcomeStep from './steps/WelcomeStep.vue'
import CardsStep from './steps/CardsStep.vue'
import AnalogyStep from './steps/AnalogyStep.vue'
import CalculatorStep from './steps/CalculatorStep.vue'
import SelectorStep from './steps/SelectorStep.vue'
import QuizStep from './steps/QuizStep.vue'
import SummaryStep from './steps/SummaryStep.vue'

const props = defineProps<{
  slideData: SlideJSON
  isMobile?: boolean
}>()

const emit = defineEmits<{ complete: [] }>()

const currentStep = ref(0)
const quizSolved = ref(false)

const step = computed<AnyJsonStep>(() => props.slideData.steps[currentStep.value])
const stepMeta = computed(() => ({
  title: step.value.title,
  desc:  step.value.desc ?? '',
}))

const canGoNext = computed(() => {
  if (step.value.type === 'quiz') return quizSolved.value
  return true
})

watch(() => currentStep.value, () => { quizSolved.value = false })

function next() { if (currentStep.value < props.slideData.steps.length - 1) currentStep.value++ }
function prev() { if (currentStep.value > 0) currentStep.value-- }
function goto(i: number) { currentStep.value = i }
function onQuizCorrect() { quizSolved.value = true }
</script>

<template>
  <InteractiveSlideTemplate
    :title="slideData.title"
    :subtitle="slideData.subtitle"
    :icon="slideData.icon"
    :total-steps="slideData.steps.length"
    :current-step="currentStep"
    :step-title="stepMeta.title"
    :step-desc="stepMeta.desc"
    :theme-color="slideData.theme"
    :can-go-next="canGoNext"
    :next-step-hint="!canGoNext ? '請先完成測驗' : ''"
    @prev="prev"
    @next="next"
    @goto="goto"
    @complete="emit('complete')"
  >
    <WelcomeStep    v-if="step.type === 'welcome'"    :step="step" />
    <CardsStep      v-else-if="step.type === 'cards'"      :step="step" />
    <AnalogyStep    v-else-if="step.type === 'analogy'"    :step="step" />
    <CalculatorStep v-else-if="step.type === 'calculator'" :step="step" />
    <SelectorStep   v-else-if="step.type === 'selector'"   :step="step" />
    <QuizStep
      v-else-if="step.type === 'quiz'"
      :step="step"
      @correct="onQuizCorrect"
    />
    <SummaryStep    v-else-if="step.type === 'summary'"    :step="step" />
  </InteractiveSlideTemplate>
</template>
