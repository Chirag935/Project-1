import React from 'react'
import { format } from 'date-fns'

const WebcamCard = ({ webcam, onClick }) => {
  const { name, location, analysis, timestamp, status } = webcam
  
  const getComfortScore = () => {
    return analysis?.micro_climate_score?.score || 0
  }

  const getComfortLevel = () => {
    const score = getComfortScore()
    if (score >= 80) return { label: 'Excellent', color: 'text-green-600', bg: 'bg-green-50' }
    if (score >= 65) return { label: 'Good', color: 'text-green-600', bg: 'bg-green-50' }
    if (score >= 45) return { label: 'Moderate', color: 'text-yellow-600', bg: 'bg-yellow-50' }
    if (score >= 25) return { label: 'Poor', color: 'text-orange-600', bg: 'bg-orange-50' }
    return { label: 'Very Poor', color: 'text-red-600', bg: 'bg-red-50' }
  }

  const getWeatherEmoji = () => {
    const condition = analysis?.weather?.weather_condition
    const weatherEmojis = {
      clear: '☀️',
      partly_cloudy: '⛅',
      overcast: '☁️',
      variable: '🌤️'
    }
    return weatherEmojis[condition] || '🌤️'
  }

  const formatTime = (timestamp) => {
    if (!timestamp) return 'No data'
    try {
      return format(new Date(timestamp), 'HH:mm')
    } catch {
      return 'Invalid time'
    }
  }

  const comfort = getComfortLevel()

  return (
    <div
      className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 cursor-pointer hover:shadow-md transition-shadow"
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="font-semibold text-gray-800 text-sm leading-tight">
            {name}
          </h3>
          <p className="text-xs text-gray-500 mt-1">
            {location.city}, {location.country}
          </p>
        </div>
        
        <div className="flex items-center space-x-1">
          <div className={`w-2 h-2 rounded-full ${
            status === 'success' ? 'bg-green-500' : 'bg-red-500'
          }`} />
          <span className="text-xs text-gray-500">
            {formatTime(timestamp)}
          </span>
        </div>
      </div>

      {/* Status Check */}
      {status !== 'success' ? (
        <div className="text-center py-4">
          <div className="text-red-500 text-sm">❌ Data unavailable</div>
          <div className="text-xs text-gray-400 mt-1">
            {webcam.error || 'Connection error'}
          </div>
        </div>
      ) : (
        <>
          {/* Comfort Score */}
          <div className={`rounded-lg p-3 mb-3 ${comfort.bg}`}>
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">
                Comfort Level
              </span>
              <span className={`text-sm font-semibold ${comfort.color}`}>
                {comfort.label}
              </span>
            </div>
            <div className="mt-2">
              <div className="flex items-center justify-between text-xs text-gray-600">
                <span>Score</span>
                <span className="font-medium">{getComfortScore()}/100</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5 mt-1">
                <div
                  className={`h-1.5 rounded-full ${
                    getComfortScore() >= 80 ? 'bg-green-500' :
                    getComfortScore() >= 65 ? 'bg-green-400' :
                    getComfortScore() >= 45 ? 'bg-yellow-500' :
                    getComfortScore() >= 25 ? 'bg-orange-500' :
                    'bg-red-500'
                  }`}
                  style={{ width: `${getComfortScore()}%` }}
                />
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 gap-2 text-xs">
            {analysis?.sun_shadow && (
              <div className="bg-gray-50 rounded p-2">
                <div className="text-gray-600 mb-1">☀️ Sun Exposure</div>
                <div className="font-medium">
                  {Math.round(analysis.sun_shadow.sun_exposure_percent)}%
                </div>
              </div>
            )}

            {analysis?.weather && (
              <div className="bg-gray-50 rounded p-2">
                <div className="text-gray-600 mb-1">🌤️ Weather</div>
                <div className="font-medium">
                  {getWeatherEmoji()} {analysis.weather.weather_condition?.replace('_', ' ')}
                </div>
              </div>
            )}

            {analysis?.sun_shadow && (
              <div className="bg-gray-50 rounded p-2">
                <div className="text-gray-600 mb-1">🌑 Shadow</div>
                <div className="font-medium">
                  {Math.round(analysis.sun_shadow.shadow_coverage_percent)}%
                </div>
              </div>
            )}

            {analysis?.brightness && (
              <div className="bg-gray-50 rounded p-2">
                <div className="text-gray-600 mb-1">💡 Brightness</div>
                <div className="font-medium capitalize">
                  {analysis.brightness.brightness_level?.replace('_', ' ')}
                </div>
              </div>
            )}
          </div>

          {/* View Details Button */}
          <div className="mt-3 pt-3 border-t border-gray-100">
            <div className="text-center">
              <span className="text-xs text-blue-600 font-medium">
                Click for detailed analysis →
              </span>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default WebcamCard