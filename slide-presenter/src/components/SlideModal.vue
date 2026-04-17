<script setup lang="ts">
import { computed, defineAsyncComponent, ref } from 'vue'

interface Props {
  slideId: string
  title: string
}

const props = defineProps<Props>()
const emit = defineEmits<{ close: [] }>()

const isMobile = ref(window.innerWidth < 768)

// Dynamic slide component registry
// Each new slide gets registered here
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

const slideComponent = computed(() => slideComponents[props.slideId] ?? null)

function handleClose() {
  emit('close')
}

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
        <!-- Close button -->
        <button
          class="absolute top-3 right-3 md:top-4 md:right-4 z-50 w-8 h-8 flex items-center justify-center rounded-full bg-white/10 hover:bg-white/20 text-white/70 hover:text-white transition-all"
          @click="handleClose"
        >
          ✕
        </button>

        <!-- Dynamic slide content -->
        <component
          v-if="slideComponent"
          :is="slideComponent"
          :is-mobile="isMobile"
          @complete="handleClose"
        />
        <div v-else class="flex items-center justify-center h-full text-white/50">
          找不到簡報：{{ slideId }}
        </div>
      </div>
    </div>
  </Teleport>
</template>
