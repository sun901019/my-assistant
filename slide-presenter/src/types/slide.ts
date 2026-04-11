export interface Step {
  readonly id: number
  readonly view: string
  readonly title: string
  readonly desc: string
}

export interface QuizOption {
  readonly label: string
  readonly value: string
}

export interface QuizQuestion {
  readonly id: string
  readonly question: string
  readonly options: readonly QuizOption[]
  readonly correctAnswer: string
  readonly successMsg: string
  readonly errorMsg: string
}

export interface CourseInfo {
  readonly id: string
  readonly title: string
  readonly subtitle: string
  readonly icon: string
  readonly slideId: string
  readonly themeColor: ThemeColor
  readonly tags: readonly string[]
  readonly createdAt: string
  readonly type?: 'vue' | 'html'
  readonly htmlPath?: string
}

export type ThemeColor = 'amber' | 'sky' | 'emerald' | 'purple'

export type FeedbackType = 'neutral' | 'success' | 'error'
