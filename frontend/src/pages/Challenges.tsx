import { useEffect, useState } from 'react'
import { challengesApi } from '../api/challenges'
import { ChallengeCard } from '../components/ChallengeCard'

export function Challenges() {
  const [challenges, setChallenges] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    challengesApi.list().then(({ data }) => {
      setChallenges(data.items)
      setLoading(false)
    })
  }, [])

  if (loading) return <p className="text-gray-500">Загрузка...</p>

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Челленджи</h1>
      {challenges.length === 0 ? (
        <p className="text-gray-500">Нет активных челленджей</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {challenges.map((c) => (
            <ChallengeCard key={c.id} challenge={c} />
          ))}
        </div>
      )}
    </div>
  )
}
