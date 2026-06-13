import { useState } from 'react'
import { Button } from './common/Button'
import { Input } from './common/Input'
import { Card } from './common/Card'
import { useToolSearch } from '../hooks/useToolSearch'
import { SearchResult } from './SearchResult'

interface ToolWidgetProps {
  toolSlug: string
  compact?: boolean
  onResult?: (result: any) => void
  initialQuery?: string
}

const toolNames: Record<string, string> = {
  username: 'Username',
  email: 'Email',
  phone: 'Phone',
  domain: 'Domain',
  leaks: 'Leaks',
  metadata: 'Metadata',
}

export function ToolWidget({ toolSlug, compact = false, onResult, initialQuery }: ToolWidgetProps) {
  const [query, setQuery] = useState(initialQuery || '')
  const { data, loading, error, search } = useToolSearch(toolSlug)

  const handleSearch = () => {
    if (!query.trim()) return
    search(query.trim())
    if (onResult) onResult({ tool: toolSlug, query })
  }

  const handleFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    const { toolsApi } = await import('../api/tools')
    const res = await toolsApi.metadata(file)
    if (onResult) onResult(res.data)
  }

  return (
    <Card className={compact ? 'p-3' : 'p-4'}>
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <Input
            placeholder={toolSlug === 'metadata' ? 'Загрузите файл...' : `Введите ${toolNames[toolSlug] || toolSlug}...`}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          />
          {toolSlug === 'metadata' ? (
            <input type="file" onChange={handleFile} className="text-sm text-gray-400" />
          ) : (
            <Button size="sm" onClick={handleSearch} disabled={loading || !query.trim()}>
              {loading ? 'Поиск...' : 'Найти'}
            </Button>
          )}
        </div>
        {error && <p className="text-sm text-red-400">{error}</p>}
        {data && <SearchResult data={data} tool={toolSlug} />}
      </div>
    </Card>
  )
}
