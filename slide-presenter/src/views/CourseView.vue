<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { courses } from '../data/courses'
import SlideModal from '../components/SlideModal.vue'

const props = defineProps<{ courseId: string }>()
const router = useRouter()

const course = computed(() => courses.find(c => c.id === props.courseId))

function handleClose() {
  router.push('/')
}
</script>

<template>
  <div v-if="course" class="min-h-screen">
    <SlideModal
      :slide-id="course.slideId"
      :title="course.title"
      @close="handleClose"
    />
  </div>
  <div v-else class="min-h-screen bg-slate-950 flex items-center justify-center text-white/50">
    找不到課程：{{ courseId }}
  </div>
</template>
