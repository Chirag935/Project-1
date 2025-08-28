import React from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

const MapView = ({ webcamData, selectedWebcam, onWebcamSelect }) => {
  const createCustomIcon = (climateScore) => {
    let color = '#6B7280' // Default gray
    
    if (climateScore >= 80) color = '#10B981' // Excellent - Green
    else if (climateScore >= 65) color = '#34D399' // Good - Light Green
    else if (climateScore >= 45) color = '#FBBF24' // Moderate - Yellow
    else if (climateScore >= 25) color = '#F87171' // Poor - Orange
    else color = '#EF4444' // Very Poor - Red

    return L.divIcon({
      className: 'custom-marker',
      html: `
        <div style="
          width: 20px;
          height: 20px;
          border-radius: 50%;
          background-color: ${color};
          border: 3px solid white;
          box-shadow: 0 2px 4px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: bold;
          color: white;
        ">
          🌡️
        </div>
      `,
      iconSize: [26, 26],
      iconAnchor: [13, 13],
      popupAnchor: [0, -13]
    })
  }

  const getComfortLabel = (score) => {
    if (score >= 80) return 'Excellent'
    if (score >= 65) return 'Good'
    if (score >= 45) return 'Moderate'
    if (score >= 25) return 'Poor'
    return 'Very Poor'
  }

  const formatSunShadowInfo = (analysis) => {
    if (!analysis || !analysis.sun_shadow) return 'No data'
    
    const { sun_exposure_percent, shadow_coverage_percent } = analysis.sun_shadow
    return `☀️ ${sun_exposure_percent}% sun, 🌑 ${shadow_coverage_percent}% shadow`
  }

  const formatWeatherInfo = (analysis) => {
    if (!analysis || !analysis.weather) return 'No data'
    
    const { weather_condition, cloud_coverage } = analysis.weather
    const weatherEmoji = {
      clear: '☀️',
      partly_cloudy: '⛅',
      overcast: '☁️',
      variable: '🌤️'
    }
    
    return `${weatherEmoji[weather_condition] || '🌤️'} ${weather_condition.replace('_', ' ')}`
  }

  return (
    <MapContainer
      center={[40.7128, -74.0060]} // New York as default center
      zoom={2}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {webcamData.map((webcam) => {
        const { location, analysis } = webcam
        const climateScore = analysis?.micro_climate_score?.score || 50
        
        return (
          <Marker
            key={webcam.webcam_id}
            position={[location.lat, location.lng]}
            icon={createCustomIcon(climateScore)}
            eventHandlers={{
              click: () => onWebcamSelect(webcam)
            }}
          >
            <Popup>
              <div className="p-2 min-w-[250px]">
                <h3 className="font-bold text-lg mb-2">{webcam.name}</h3>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Comfort Level:</span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      climateScore >= 80 ? 'bg-green-100 text-green-800' :
                      climateScore >= 65 ? 'bg-green-100 text-green-700' :
                      climateScore >= 45 ? 'bg-yellow-100 text-yellow-800' :
                      climateScore >= 25 ? 'bg-orange-100 text-orange-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {getComfortLabel(climateScore)} ({climateScore}/100)
                    </span>
                  </div>

                  <div className="text-sm">
                    <div className="mb-1">
                      <strong>☀️ Sun/Shadow:</strong><br />
                      {formatSunShadowInfo(analysis)}
                    </div>
                    
                    <div className="mb-1">
                      <strong>🌤️ Weather:</strong><br />
                      {formatWeatherInfo(analysis)}
                    </div>

                    {analysis?.brightness && (
                      <div className="mb-1">
                        <strong>💡 Brightness:</strong><br />
                        {analysis.brightness.brightness_level} ({Math.round(analysis.brightness.mean_brightness)}/255)
                      </div>
                    )}
                  </div>

                  <div className="pt-2 border-t">
                    <button
                      onClick={() => onWebcamSelect(webcam)}
                      className="w-full bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700"
                    >
                      View Details
                    </button>
                  </div>

                  {webcam.timestamp && (
                    <div className="text-xs text-gray-500 pt-1">
                      Last updated: {new Date(webcam.timestamp).toLocaleTimeString()}
                    </div>
                  )}
                </div>
              </div>
            </Popup>
          </Marker>
        )
      })}
    </MapContainer>
  )
}

export default MapView