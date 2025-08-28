import React, { useState, useEffect } from 'react'
import MapView from './components/MapView'
import Dashboard from './components/Dashboard'
import Header from './components/Header'
import { useWebSocket } from './hooks/useWebSocket'
import { webcamService } from './services/webcamService'
import './App.css'

function App() {
  const [webcamData, setWebcamData] = useState([])
  const [selectedWebcam, setSelectedWebcam] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [connectionStatus, setConnectionStatus] = useState('connecting')

  // WebSocket connection for real-time updates
  const { isConnected, lastMessage } = useWebSocket('ws://localhost:8000/ws')

  // Load initial webcam data
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setLoading(true)
        const data = await webcamService.getAllLatest()
        setWebcamData(data)
        setError(null)
      } catch (err) {
        console.error('Failed to load webcam data:', err)
        setError('Failed to load webcam data')
      } finally {
        setLoading(false)
      }
    }

    loadInitialData()
  }, [])

  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      try {
        const message = JSON.parse(lastMessage.data)
        
        if (message.type === 'webcam_update' || message.type === 'webcam_analysis_update') {
          setWebcamData(message.data)
          console.log('Received webcam update:', message.data.length, 'webcams')
        } else if (message.type === 'connection_established') {
          console.log('WebSocket connected:', message.message)
        }
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err)
      }
    }
  }, [lastMessage])

  // Update connection status
  useEffect(() => {
    setConnectionStatus(isConnected ? 'connected' : 'disconnected')
  }, [isConnected])

  const handleWebcamSelect = (webcam) => {
    setSelectedWebcam(webcam)
  }

  const handleCloseDetails = () => {
    setSelectedWebcam(null)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading urban micro-climate data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️ Error</div>
          <p className="text-gray-600">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Header 
        connectionStatus={connectionStatus}
        webcamCount={webcamData.length}
        lastUpdate={webcamData.length > 0 ? webcamData[0].timestamp : null}
      />
      
      <div className="flex h-screen">
        {/* Main Map View */}
        <div className="flex-1 relative">
          <MapView
            webcamData={webcamData}
            selectedWebcam={selectedWebcam}
            onWebcamSelect={handleWebcamSelect}
          />
        </div>

        {/* Dashboard Sidebar */}
        <div className="w-96 bg-white shadow-lg overflow-y-auto">
          <Dashboard
            webcamData={webcamData}
            selectedWebcam={selectedWebcam}
            onWebcamSelect={handleWebcamSelect}
            onCloseDetails={handleCloseDetails}
          />
        </div>
      </div>
    </div>
  )
}

export default App