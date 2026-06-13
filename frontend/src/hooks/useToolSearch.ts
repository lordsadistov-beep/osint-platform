import { useState } from 'react'
import { toolsApi } from '../api/tools'

export function useToolSearch(tool: string) {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const search = async (query: string) => {
    setLoading(true)
    setError(null)
    try {
      let res
      switch (tool) {
        case 'username':
          res = await toolsApi.username(query)
          break
        case 'email':
          res = await toolsApi.email(query)
          break
        case 'phone':
          res = await toolsApi.phone(query)
          break
        case 'domain':
          res = await toolsApi.domain(query)
          break
        case 'leaks':
          res = await toolsApi.leaks(query, 'email')
          break
        default:
          throw new Error('Unknown tool')
      }
      setData(res.data)
    } catch (e: any) {
      setError(e.response?.data?.detail || e.message)
    } finally {
      setLoading(false)
    }
  }

  return { data, loading, error, search }
}
