import { ToolWidget } from '../components/ToolWidget'

export function ToolLeaks() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Leak Search</h1>
      <p className="mb-4 text-sm text-gray-500">Поиск по базам утечек (email/username/phone)</p>
      <ToolWidget toolSlug="leaks" />
    </div>
  )
}
