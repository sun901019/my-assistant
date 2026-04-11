import type { CourseInfo } from '../types/slide'

export const courses: readonly CourseInfo[] = [
  {
    id: 'demo-what-is-api',
    title: 'API 是什麼？',
    subtitle: '用餐廳點餐來理解 API 的概念',
    icon: '🍽️',
    slideId: 'demo-what-is-api',
    themeColor: 'sky',
    tags: ['程式基礎', '後端'],
    createdAt: '2026-04-11',
    type: 'vue',
  },
  {
    id: 'git-github',
    title: 'Git & GitHub 完整入門',
    subtitle: '從小明的論文災難到版控完整流程',
    icon: '🌿',
    slideId: 'git-github',
    themeColor: 'emerald',
    tags: ['Git', 'GitHub', '版本控制'],
    createdAt: '2026-04-03',
    type: 'html',
    htmlPath: '/my-assistant/slides/git-github.html',
  },
]
