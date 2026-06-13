import { useEffect, useState } from 'react'
import { lessonsApi } from '../api/lessons'
import { LessonCard } from '../components/LessonCard'
import { Button } from '../components/common/Button'
import { LESSON_CATEGORIES } from '../lib/constants'

export function Learn() {
  const [lessons, setLessons] = useState<any[]>([])
  const [category, setCategory] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    lessonsApi.list({ category: category || undefined }).then(({ data }) => {
      setLessons(data.items)
      setLoading(false)
    })
  }, [category])

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Уроки</h1>
      <div className="mb-6 flex flex-wrap gap-2">
        <Button variant={!category ? 'primary' : 'secondary'} size="sm" onClick={() => setCategory('')}>
          Все
        </Button>
        {LESSON_CATEGORIES.map((c) => (
          <Button
            key={c.value}
            variant={category === c.value ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => setCategory(c.value)}
          >
            {c.label}
          </Button>
        ))}
      </div>
      {loading ? (
        <p className="text-gray-500">Загрузка...</p>
      ) : lessons.length === 0 ? (
        <p className="text-gray-500">Нет уроков в этой категории</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {lessons.map((lesson) => (
            <LessonCard key={lesson.id} lesson={lesson} />
          ))}
        </div>
      )}
    </div>
  )
}
