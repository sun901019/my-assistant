<script setup lang="ts">
import { computed, defineAsyncComponent, ref, shallowRef, onMounted } from 'vue'
import type { SlideJSON } from '../types/slide-json'
import JsonSlideRenderer from './JsonSlideRenderer.vue'

interface Props {
  slideId: string
  title: string
}

const props = defineProps<Props>()
const emit = defineEmits<{ close: [] }>()

const isMobile = ref(window.innerWidth < 768)

// Vue component slides registry
const slideComponents: Record<string, ReturnType<typeof defineAsyncComponent>> = {
  'demo-what-is-api': defineAsyncComponent(
    () => import('../slides/DemoWhatIsApiSlide.vue')
  ),
  'energy-basics': defineAsyncComponent(
    () => import('../slides/EnergyBasicsSlide.vue')
  ),
  'v2g-what-is': defineAsyncComponent(
    () => import('../slides/V2GWhatIsSlide.vue')
  ),
  'v2g-business-model': defineAsyncComponent(
    () => import('../slides/V2GBusinessModelSlide.vue')
  ),
}

// JSON slide data
const jsonSlideData = shallowRef<SlideJSON | null>(null)
const isJson = computed(() => !(props.slideId in slideComponents))

onMounted(async () => {
  if (!isJson.value) return
  try {
    const mod = await import(`../data/slides/${props.slideId}.json`)
    jsonSlideData.value = mod.default as SlideJSON
  } catch {
    jsonSlideData.value = null
  }
})

const slideComponent = computed(() => slideComponents[props.slideId] ?? null)

function handleClose() { emit('close') }
function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') handleClose()
}
</script>

<template>
  <Teleport to="body">
    <div
      class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center"
      @click.self="handleClose"
      @keydown="handleKeydown"
    >
      <div class="w-full h-full md:w-[95%] md:h-[92%] md:rounded-2xl overflow-hidden shadow-2xl bg-slate-900">
        <button
          class="absolute top-3 right-3 md:top-4 md:right-4 z-50 w-8 h-8 flex items-center justify-center rounded-full bg-white/10 hover:bg-white/20 text-white/70 hover:text-white transition-all"
          @click="handleClose"
        >
          ✕
        </button>

        <!-- Vue component slides -->
        <component
          v-if="!isJson && slideComponent"
          :is="slideComponent"
          :is-mobile="isMobile"
          @complete="handleClose"
        />

        <!-- JSON-driven slides -->
        <JsonSlideRenderer
          v-else-if="isJson && jsonSlideData"
          :slide-data="jsonSlideData"
          :is-mobile="isMobile"
          @complete="handleClose"
        />

        <div v-else class="flex items-center justify-center h-full text-white/50">
          {{ isJson ? '載入中…' : `找不到簡報：${slideId}` }}
        </div>
      </div>
    </div>
  </Teleport>
</template>
