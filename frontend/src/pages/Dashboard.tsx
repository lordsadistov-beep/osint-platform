import { useEffect, useState } from 'react'
import { dashboardApi } from '../api/dashboard'
import { Card } from '../components/common/Card'
import { ProgressBar } from '../components/ProgressBar'
import { useAuthStore } from '../stores/authStore'

export function Dashboard() {
  const [stats, setStats] = useState<any>(null)
  const [history, setHistory] = useState<any[]>([])
  const user = useAuthStore((s) => s.user)

  useEffect(() => {
    dashboardApi.stats().then(({ data }) => setStats(data))
    dashboardApi.history({ limit: 10 }).then(({ data }) => setHistory(data.items))
  }, [])

  const xpForNext = 150 * (user?.level || 1)

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Dashboard</h1>
      {stats && user && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Card>
            <p className="text-sm text-gray-500">Уровень</p>
            <p className="text-2xl font-bold text-primary-400">{stats.level}</p>
            <ProgressBar value={user.experience} max={xpForNext} className="mt-2" />
            <p className="mt-1 text-xs text-gray-500">{user.experience} / {xpForNext} XP</p>
          </Card>
          <Card>
            <p className="text-sm text-gray-500">Уроков пройдено</p>
            <p className="text-2xl font-bold text-green-400">{stats.lessons_completed}</p>
          </Card>
          <Card>
            <p className="text-sm text-gray-500">Челленджей решено</p>
            <p className="text-2xl font-bold text-yellow-400">{stats.challenges_solved}</p>
          </Card>
          <Card>
            <p className="text-sm text-gray-500">Поисков</p>
            <p className="text-2xl font-bold text-blue-400">{stats.total_searches}</p>
          </Card>
        </div>
      )}
      <h2 className="mb-4 mt-8 text-lg font-semibold text-gray-200">Последние поиски</h2>
      {history.length === 0 ? (
        <p className="text-sm text-gray-500">Нет истории</p>
      ) : (
        <div className="space-y-2">
          {history.map((h: any) => (
            <Card key={h.id} className="flex items-center justify-between p-3">
              <div>
                <span className="text-sm font-medium text-gray-300">{h.tool_slug}</span>
                <span className="ml-2 text-sm text-gray-500">{h.query}</span>
              </div>
              <span className="text-xs text-gray-600">{new Date(h.created_at).toLocaleString()}</span>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
