export const SITE_CATEGORIES = [
  'Social', 'Coding', 'Gaming', 'Forums', 'Dating', 'Other',
] as const

export const DIFFICULTIES = [
  { value: 'beginner', label: 'Начинающий' },
  { value: 'intermediate', label: 'Средний' },
  { value: 'advanced', label: 'Продвинутый' },
] as const

export const LESSON_CATEGORIES = [
  { value: 'username', label: 'Username', icon: 'User' },
  { value: 'email', label: 'Email', icon: 'Mail' },
  { value: 'domain', label: 'Domain/Network', icon: 'Globe' },
  { value: 'phone', label: 'Phone', icon: 'Phone' },
  { value: 'metadata', label: 'Metadata', icon: 'FileImage' },
  { value: 'social', label: 'Social Engineering', icon: 'Users' },
  { value: 'general', label: 'Advanced', icon: 'Sparkles' },
] as const
