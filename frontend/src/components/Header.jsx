import React from 'react'
import { format } from 'date-fns'

const Header = ({ connectionStatus, webcamCount, lastUpdate }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'connected':
        return 'bg-green-500'
      case 'connecting':
        return 'bg-yellow-500 animate-pulse'
      case 'disconnected':
        return 'bg-red-500'
      default:
        return 'bg-gray-500'
    }
  }

  const formatLastUpdate = (timestamp) => {
    if (!timestamp) return 'No updates yet'
    try {
      return format(new Date(timestamp), 'HH:mm:ss')
    } catch {
      return 'Invalid timestamp'
    }
  }

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold text-gray-900">
            🌍 Urban Micro-Climate Map
          </h1>
          <div className="flex items-center space-x-2">
            <div
              className={`w-3 h-3 rounded-full ${getStatusColor(connectionStatus)}`}
              title={`Connection status: ${connectionStatus}`}
            />
            <span className="text-sm text-gray-600 capitalize">
              {connectionStatus}
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-6 text-sm text-gray-600">
          <div className="flex items-center space-x-2">
            <span className="font-medium">📹 Webcams:</span>
            <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">
              {webcamCount}
            </span>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className="font-medium">🕒 Last Update:</span>
            <span className="bg-gray-100 px-2 py-1 rounded">
              {formatLastUpdate(lastUpdate)}
            </span>
          </div>

          <div className="flex items-center space-x-2">
            <span className="font-medium">⚡ Real-time:</span>
            <span className={`px-2 py-1 rounded text-xs font-medium ${
              connectionStatus === 'connected' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {connectionStatus === 'connected' ? 'LIVE' : 'OFFLINE'}
            </span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header