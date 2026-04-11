import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/course/:courseId',
      name: 'course',
      component: () => import('../views/CourseView.vue'),
      props: true,
    },
  ],
})

export default router
