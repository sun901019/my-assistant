<script setup lang="ts">
import { courses } from '../data/courses'
import { ref } from 'vue'
import SlideModal from '../components/SlideModal.vue'

const activeSlideId = ref<string | null>(null)
const activeSlideTitle = ref('')

function openSlide(courseId: string, title: string) {
  activeSlideId.value = courseId
  activeSlideTitle.value = title
}

function closeSlide() {
  activeSlideId.value = null
}
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-white">
    <!-- Header -->
    <header class="border-b border-white/10 px-6 py-8 text-center">
      <h1 class="text-3xl md:text-4xl font-bold">📘 Sun 的學習簡報</h1>
      <p class="text-white/50 mt-2">用互動式簡報把知識視覺化，學一次就記住</p>
    </header>

    <!-- Course list -->
    <main class="max-w-4xl mx-auto px-4 py-8">
      <div v-if="courses.length === 0" class="text-center text-white/30 py-20">
        還沒有簡報，請小眉教你一個新觀念吧！
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button
          v-for="course in courses"
          :key="course.id"
          class="text-left p-6 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all group"
          @click="openSlide(course.slideId, course.title)"
        >
          <div class="flex items-start gap-4">
            <span class="text-3xl">{{ course.icon }}</span>
            <div class="flex-1">
              <h3 class="font-bold text-lg group-hover:text-sky-300 transition-colors">
                {{ course.title }}
              </h3>
              <p class="text-sm text-white/50 mt-1">{{ course.subtitle }}</p>
              <div class="flex gap-2 mt-3">
                <span
                  v-for="tag in course.tags"
                  :key="tag"
                  class="text-xs px-2 py-0.5 rounded-full bg-white/10 text-white/40"
                >
                  {{ tag }}
                </span>
              </div>
              <p class="text-xs text-white/30 mt-2">{{ course.createdAt }}</p>
            </div>
          </div>
        </button>
      </div>
    </main>

    <!-- Slide modal -->
    <SlideModal
      v-if="activeSlideId"
      :slide-id="activeSlideId"
      :title="activeSlideTitle"
      @close="closeSlide"
    />
  </div>
</template>
