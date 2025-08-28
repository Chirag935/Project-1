import { useState, useEffect, useRef } from 'react'

export function useWebSocket(url) {
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState(null)
  const [error, setError] = useState(null)
  const ws = useRef(null)
  const reconnectTimeoutRef = useRef(null)
  const reconnectAttempts = useRef(0)
  const maxReconnectAttempts = 10

  const connect = () => {
    try {
      ws.current = new WebSocket(url)
      
      ws.current.onopen = () => {
        console.log('WebSocket connected')
        setIsConnected(true)
        setError(null)
        reconnectAttempts.current = 0
      }
      
      ws.current.onmessage = (event) => {
        setLastMessage(event)
      }
      
      ws.current.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason)
        setIsConnected(false)
        
        // Attempt to reconnect if it wasn't a manual close
        if (event.code !== 1000 && reconnectAttempts.current < maxReconnectAttempts) {
          const timeout = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 30000)
          console.log(`Reconnecting in ${timeout}ms... (attempt ${reconnectAttempts.current + 1})`)
          
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttempts.current++
            connect()
          }, timeout)
        }
      }
      
      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error)
        setError('WebSocket connection error')
      }
    } catch (err) {
      console.error('Failed to create WebSocket connection:', err)
      setError('Failed to create WebSocket connection')
    }
  }

  useEffect(() => {
    connect()
    
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (ws.current) {
        ws.current.close(1000, 'Component unmounting')
      }
    }
  }, [url])

  const sendMessage = (message) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(typeof message === 'string' ? message : JSON.stringify(message))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  return {
    isConnected,
    lastMessage,
    error,
    sendMessage
  }
}