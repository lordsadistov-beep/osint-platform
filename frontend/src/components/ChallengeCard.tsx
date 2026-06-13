import { Link } from 'react-router-dom'
import { Card } from './common/Card'
import { Badge } from './common/Badge'

interface Challenge {
  id: string
  title: string
  slug: string
  difficulty: string
  points: number
  category: string
}

export function ChallengeCard({ challenge }: { challenge: Challenge }) {
  return (
    <Link to={`/challenges/${challenge.id}`}>
      <Card className="transition-colors hover:border-primary-700">
        <div className="flex items-start justify-between">
          <Badge variant={challenge.difficulty === 'easy' ? 'success' : challenge.difficulty === 'hard' ? 'danger' : 'warning'}>
            {challenge.difficulty}
          </Badge>
          <span className="text-sm font-bold text-yellow-400">{challenge.points} pts</span>
        </div>
        <h3 className="mt-2 font-semibold text-gray-100">{challenge.title}</h3>
        <p className="mt-1 text-xs text-gray-500">{challenge.category}</p>
      </Card>
    </Link>
  )
}
