import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { lessonsApi } from '../api/lessons'
import { ToolWidget } from '../components/ToolWidget'
import { Button } from '../components/common/Button'
import { Badge } from '../components/common/Badge'
import { Card } from '../components/common/Card'
import { useAuthStore } from '../stores/authStore'

export function LessonDetail() {
  const { slug } = useParams<{ slug: string }>()
  const [lesson, setLesson] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!slug) return
    lessonsApi.get(slug).then(({ data }) => {
      setLesson(data)
      setLoading(false)
    })
  }, [slug])

  const handleComplete = async () => {
    if (!slug) return
    await lessonsApi.complete(slug)
    useAuthStore.getState().fetchMe()
  }

  if (loading) return <p className="text-gray-500">Загрузка...</p>
  if (!lesson) return <p className="text-red-400">Урок не найден</p>

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div>
        <div className="mb-4 flex items-center gap-3">
          <Badge variant={lesson.difficulty === 'beginner' ? 'success' : lesson.difficulty === 'advanced' ? 'danger' : 'warning'}>
            {lesson.difficulty}
          </Badge>
          <span className="text-sm text-gray-500">{lesson.xp_reward} XP</span>
          {lesson.estimated_minutes && <span className="text-sm text-gray-500">{lesson.estimated_minutes} мин</span>}
        </div>
        <h1 className="text-2xl font-bold text-gray-100">{lesson.title}</h1>
        <div className="prose prose-invert mt-4 max-w-none text-gray-300">
          {lesson.content.split('\n').map((line: string, i: number) => (
            <p key={i}>{line}</p>
          ))}
        </div>
        <Button className="mt-6" onClick={handleComplete}>
          Отметить как пройденный
        </Button>
      </div>
      <div>
        <h2 className="mb-3 text-lg font-semibold text-gray-200">Практика</h2>
        {lesson.tool_slug ? (
          <ToolWidget toolSlug={lesson.tool_slug} compact />
        ) : (
          <Card>
            <p className="text-sm text-gray-500">К этому уроку нет привязанного инструмента</p>
          </Card>
        )}
      </div>
    </div>
  )
}
