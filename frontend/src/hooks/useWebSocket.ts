import { useEffect, useRef, useState } from 'react'

type WsMessage = {
  type: 'progress' | 'result'
  [key: string]: any
}

export function useWebSocket(url: string | null) {
  const [messages, setMessages] = useState<WsMessage[]>([])
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!url) return
    const ws = new WebSocket(url)
    wsRef.current = ws
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data)
      setMessages((prev) => [...prev, msg])
    }
    return () => {
      ws.close()
    }
  }, [url])

  const reset = () => setMessages([])

  return { messages, reset }
}
