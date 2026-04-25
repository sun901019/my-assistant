import type { ThemeColor } from './slide'

export interface WelcomeStep {
  type: 'welcome'
  title: string
  desc?: string
  icon: string
  headline: string
  subheadline?: string
  features: Array<{ icon: string; text: string }>
  footer?: string
}

export interface CardItem {
  icon: string
  title: string
  subtitle?: string
  body: string
  color?: string
}

export interface CardsStep {
  type: 'cards'
  title: string
  desc?: string
  cards: CardItem[]
  note?: string
}

export interface AnalogyPair {
  concept: string
  real: string
  icon?: string
}

export interface AnalogyStep {
  type: 'analogy'
  title: string
  desc?: string
  conceptLabel?: string
  realLabel?: string
  pairs: AnalogyPair[]
  note?: string
}

export interface SliderConfig {
  key: string
  label: string
  min: number
  max: number
  step: number
  default: number
  unit: string
  color?: string
}

export interface OutputConfig {
  label: string
  formula: string
  unit: string
  color?: string
  decimals?: number
}

export interface CalculatorStep {
  type: 'calculator'
  title: string
  desc?: string
  prompt?: string
  sliders: SliderConfig[]
  outputs: OutputConfig[]
  note?: string
}

export interface SelectorOption {
  key: string
  icon: string
  label: string
  details: Array<{ label: string; value: string; color?: string }>
  note?: string
}

export interface SelectorStep {
  type: 'selector'
  title: string
  desc?: string
  prompt?: string
  options: SelectorOption[]
}

export interface QuizOptionItem {
  value: string
  label: string
}

export interface QuizStep {
  type: 'quiz'
  title: string
  desc?: string
  question: string
  options: QuizOptionItem[]
  correctAnswer: string
  successMsg: string
  errorMsg: string
}

export interface SummaryPoint {
  color?: string
  text: string
}

export interface SummaryStep {
  type: 'summary'
  title: string
  desc?: string
  icon?: string
  headline: string
  points: SummaryPoint[]
  nextHint?: string
}

export type AnyJsonStep =
  | WelcomeStep
  | CardsStep
  | AnalogyStep
  | CalculatorStep
  | SelectorStep
  | QuizStep
  | SummaryStep

export interface SlideJSON {
  id: string
  title: string
  subtitle: string
  icon: string
  theme: ThemeColor
  steps: AnyJsonStep[]
}
