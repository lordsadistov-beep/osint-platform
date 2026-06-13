import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { challengesApi } from '../api/challenges'
import { Button } from '../components/common/Button'
import { Input } from '../components/common/Input'
import { Card } from '../components/common/Card'
import { Badge } from '../components/common/Badge'

export function ChallengeDetail() {
  const { id } = useParams<{ id: string }>()
  const [challenge, setChallenge] = useState<any>(null)
  const [flag, setFlag] = useState('')
  const [result, setResult] = useState<{ is_correct: boolean; points_awarded: number } | null>(null)
  const [hint, setHint] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!id) return
    challengesApi.get(id).then(({ data }) => {
      setChallenge(data)
      setLoading(false)
    })
  }, [id])

  const handleSubmit = async () => {
    if (!id || !flag.trim()) return
    const { data } = await challengesApi.submit(id, flag.trim())
    setResult(data)
  }

  const handleHint = async () => {
    if (!id) return
    const { data } = await challengesApi.hint(id)
    setHint(data.hint)
  }

  if (loading) return <p className="text-gray-500">Загрузка...</p>
  if (!challenge) return <p className="text-red-400">Челлендж не найден</p>

  return (
    <div className="max-w-2xl">
      <div className="mb-4 flex items-center gap-3">
        <Badge variant={challenge.difficulty === 'easy' ? 'success' : challenge.difficulty === 'hard' ? 'danger' : 'warning'}>
          {challenge.difficulty}
        </Badge>
        <span className="text-sm font-bold text-yellow-400">{challenge.points} pts</span>
      </div>
      <h1 className="text-2xl font-bold text-gray-100">{challenge.title}</h1>
      <p className="mt-4 text-gray-300">{challenge.description}</p>
      {challenge.hint && !hint && (
        <Button variant="ghost" size="sm" className="mt-4" onClick={handleHint}>
          Получить подсказку (-50% очков)
        </Button>
      )}
      {hint && <Card className="mt-4 border-yellow-700"><p className="text-sm text-yellow-400">{hint}</p></Card>}
      <div className="mt-6 flex gap-3">
        <Input placeholder="Введите flag..." value={flag} onChange={(e) => setFlag(e.target.value)} className="max-w-sm" />
        <Button onClick={handleSubmit} disabled={!flag.trim()}>Отправить</Button>
      </div>
      {result && (
        <Card className={`mt-4 ${result.is_correct ? 'border-green-700' : 'border-red-700'}`}>
          <p className={`text-sm ${result.is_correct ? 'text-green-400' : 'text-red-400'}`}>
            {result.is_correct ? `Верно! +${result.points_awarded} XP` : 'Неверно'}
          </p>
        </Card>
      )}
    </div>
  )
}
