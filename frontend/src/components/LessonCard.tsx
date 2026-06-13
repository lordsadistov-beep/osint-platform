import { Link } from 'react-router-dom'
import { Card } from './common/Card'
import { Badge } from './common/Badge'
import { ProgressBar } from './ProgressBar'
import { LESSON_CATEGORIES } from '../lib/constants'

interface Lesson {
  id: string
  title: string
  slug: string
  description?: string
  category: string
  difficulty: string
  xp_reward: number
  estimated_minutes?: number
}

export function LessonCard({ lesson, progress }: { lesson: Lesson; progress?: { completed: boolean } }) {
  const cat = LESSON_CATEGORIES.find((c) => c.value === lesson.category)

  return (
    <Link to={`/learn/${lesson.slug}`}>
      <Card className="h-full transition-colors hover:border-primary-700">
        <div className="flex items-start justify-between">
          <Badge variant={lesson.difficulty === 'beginner' ? 'success' : lesson.difficulty === 'advanced' ? 'danger' : 'warning'}>
            {lesson.difficulty}
          </Badge>
          {progress?.completed && <Badge variant="success">✓</Badge>}
        </div>
        <h3 className="mt-2 font-semibold text-gray-100">{lesson.title}</h3>
        {lesson.description && (
          <p className="mt-1 text-xs text-gray-500 line-clamp-2">{lesson.description}</p>
        )}
        <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
          <span>{cat?.label || lesson.category}</span>
          <span>{lesson.xp_reward} XP</span>
          {lesson.estimated_minutes && <span>{lesson.estimated_minutes} мин</span>}
        </div>
        {progress && <ProgressBar value={progress.completed ? 100 : 0} className="mt-2" />}
      </Card>
    </Link>
  )
}
