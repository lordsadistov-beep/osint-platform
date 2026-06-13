import { useEffect, useState } from 'react'
import { dashboardApi } from '../api/dashboard'
import { toolsApi } from '../api/tools'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { Input } from '../components/common/Input'

export function GraphView() {
  const [graph, setGraph] = useState<any>(null)
  const [entityType, setEntityType] = useState('username')
  const [entityValue, setEntityValue] = useState('')

  useEffect(() => {
    dashboardApi.graph().then(({ data }) => setGraph(data))
  }, [])

  const handleSearch = async () => {
    if (!entityValue.trim()) return
    const { data } = await toolsApi.graph(entityType, entityValue)
    dashboardApi.graph().then(({ data: full }) => setGraph(full))
  }

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Граф связей</h1>
      <div className="mb-6 flex gap-3">
        <select
          className="rounded-lg border border-gray-700 bg-gray-900 px-3 py-2 text-sm text-gray-100"
          value={entityType}
          onChange={(e) => setEntityType(e.target.value)}
        >
          <option value="username">Username</option>
          <option value="email">Email</option>
          <option value="phone">Phone</option>
          <option value="domain">Domain</option>
        </select>
        <Input placeholder="Значение..." value={entityValue} onChange={(e) => setEntityValue(e.target.value)} />
        <Button onClick={handleSearch}>Построить граф</Button>
      </div>
      {graph && graph.nodes.length > 0 ? (
        <Card>
          <div className="mb-4 text-sm text-gray-500">
            Узлов: {graph.nodes.length} | Связей: {graph.edges.length}
          </div>
          <div className="grid gap-2">
            {graph.nodes.map((node: any) => (
              <div key={node.id} className="flex items-center gap-2 rounded-lg border border-gray-800 bg-gray-900/50 p-2 text-sm">
                <span className="h-2 w-2 rounded-full bg-primary-500" />
                <span className="text-gray-300">{node.label}</span>
                <span className="text-xs text-gray-600">({node.type})</span>
              </div>
            ))}
          </div>
          {graph.edges.length > 0 && (
            <div className="mt-4">
              <p className="mb-2 text-sm text-gray-500">Связи:</p>
              <div className="space-y-1">
                {graph.edges.map((edge: any, i: number) => (
                  <p key={i} className="text-xs text-gray-500">
                    {edge.source} → {edge.target} {edge.relationship ? `(${edge.relationship})` : ''}
                  </p>
                ))}
              </div>
            </div>
          )}
        </Card>
      ) : (
        <p className="text-sm text-gray-500">
          Введите сущность и нажмите "Построить граф". Сохраняйте связи из результатов поиска инструментов на Dashboard.
        </p>
      )}
    </div>
  )
}
