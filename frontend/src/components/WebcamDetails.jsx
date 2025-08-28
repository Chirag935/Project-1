import React from 'react'
import { format } from 'date-fns'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const WebcamDetails = ({ webcam, onClose }) => {
  const { name, location, analysis, timestamp, status, image_url } = webcam

  if (status !== 'success' || !analysis) {
    return (
      <div className="h-full flex flex-col">
        <div className="p-4 border-b bg-red-50">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-red-800">Data Unavailable</h2>
            <button
              onClick={onClose}
              className="text-red-600 hover:text-red-800 text-xl"
            >
              ✕
            </button>
          </div>
        </div>
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="text-red-500 text-4xl mb-4">❌</div>
            <p className="text-gray-600">Unable to load analysis data</p>
            <p className="text-sm text-gray-400 mt-2">
              {webcam.error || 'Connection error'}
            </p>
          </div>
        </div>
      </div>
    )
  }

  const { sun_shadow, brightness, weather, micro_climate_score } = analysis

  // Prepare chart data
  const sunShadowData = [
    { name: 'Sun Exposure', value: sun_shadow?.sun_exposure_percent || 0, color: '#F59E0B' },
    { name: 'Shadow Coverage', value: sun_shadow?.shadow_coverage_percent || 0, color: '#6B7280' },
    { name: 'Neutral', value: 100 - (sun_shadow?.sun_exposure_percent || 0) - (sun_shadow?.shadow_coverage_percent || 0), color: '#E5E7EB' }
  ].filter(item => item.value > 0)

  const brightnessData = [
    { name: 'Mean Brightness', value: brightness?.mean_brightness || 0 },
    { name: 'Contrast', value: brightness?.brightness_std || 0 },
    { name: 'Dynamic Range', value: (brightness?.dynamic_range || 0) / 2.55 } // Normalize to 0-100
  ]

  const getComfortColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 65) return 'text-green-500'
    if (score >= 45) return 'text-yellow-600'
    if (score >= 25) return 'text-orange-600'
    return 'text-red-600'
  }

  const getComfortBg = (score) => {
    if (score >= 80) return 'bg-green-50 border-green-200'
    if (score >= 65) return 'bg-green-50 border-green-200'
    if (score >= 45) return 'bg-yellow-50 border-yellow-200'
    if (score >= 25) return 'bg-orange-50 border-orange-200'
    return 'bg-red-50 border-red-200'
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-gray-800">{name}</h2>
            <p className="text-sm text-gray-600">
              {location.city}, {location.country}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-xl"
          >
            ✕
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {/* Webcam Image */}
        {image_url && (
          <div className="bg-white rounded-lg border">
            <img
              src={image_url}
              alt={`Live view from ${name}`}
              className="w-full h-48 object-cover rounded-lg"
              onError={(e) => {
                e.target.style.display = 'none'
              }}
            />
          </div>
        )}

        {/* Comfort Score */}
        <div className={`rounded-lg border-2 p-4 ${getComfortBg(micro_climate_score?.score || 0)}`}>
          <h3 className="text-lg font-semibold mb-3">🌡️ Micro-Climate Comfort Score</h3>
          <div className="flex items-center justify-between">
            <div>
              <div className={`text-3xl font-bold ${getComfortColor(micro_climate_score?.score || 0)}`}>
                {micro_climate_score?.score || 0}/100
              </div>
              <div className={`text-sm font-medium ${getComfortColor(micro_climate_score?.score || 0)}`}>
                {micro_climate_score?.comfort_level || 'Unknown'}
              </div>
            </div>
            <div className="text-right text-sm text-gray-600">
              <div>Factors:</div>
              <div>☀️ Sun: {micro_climate_score?.factors?.sun_exposure || 0}%</div>
              <div>💡 Brightness: {micro_climate_score?.factors?.brightness || 'N/A'}</div>
              <div>🌤️ Weather: {micro_climate_score?.factors?.weather || 'N/A'}</div>
            </div>
          </div>
        </div>

        {/* Sun/Shadow Analysis */}
        {sun_shadow && (
          <div className="bg-white rounded-lg border p-4">
            <h3 className="text-lg font-semibold mb-3">☀️ Sun/Shadow Analysis</h3>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-600">
                  {Math.round(sun_shadow.sun_exposure_percent)}%
                </div>
                <div className="text-sm text-gray-600">Sun Exposure</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-600">
                  {Math.round(sun_shadow.shadow_coverage_percent)}%
                </div>
                <div className="text-sm text-gray-600">Shadow Coverage</div>
              </div>
            </div>

            <div className="h-40">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={sunShadowData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={70}
                    dataKey="value"
                  >
                    {sunShadowData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-4 text-sm">
              <div>
                <span className="text-gray-600">Sun Regions:</span>
                <span className="ml-2 font-medium">{sun_shadow.sun_regions_count || 0}</span>
              </div>
              <div>
                <span className="text-gray-600">Shadow Regions:</span>
                <span className="ml-2 font-medium">{sun_shadow.shadow_regions_count || 0}</span>
              </div>
              <div>
                <span className="text-gray-600">Sun/Shadow Ratio:</span>
                <span className="ml-2 font-medium">{sun_shadow.sun_shadow_ratio || 0}</span>
              </div>
              <div>
                <span className="text-gray-600">Largest Sun Area:</span>
                <span className="ml-2 font-medium">{sun_shadow.largest_sun_area || 0}</span>
              </div>
            </div>
          </div>
        )}

        {/* Brightness Analysis */}
        {brightness && (
          <div className="bg-white rounded-lg border p-4">
            <h3 className="text-lg font-semibold mb-3">💡 Brightness Analysis</h3>
            
            <div className="grid grid-cols-3 gap-4 mb-4 text-center">
              <div>
                <div className="text-xl font-bold text-blue-600">
                  {Math.round(brightness.mean_brightness)}
                </div>
                <div className="text-sm text-gray-600">Mean (0-255)</div>
              </div>
              <div>
                <div className="text-xl font-bold text-purple-600 capitalize">
                  {brightness.brightness_level?.replace('_', ' ')}
                </div>
                <div className="text-sm text-gray-600">Level</div>
              </div>
              <div>
                <div className="text-xl font-bold text-green-600 capitalize">
                  {brightness.contrast_level}
                </div>
                <div className="text-sm text-gray-600">Contrast</div>
              </div>
            </div>

            <div className="h-32">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={brightnessData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-4 text-sm">
              <div>
                <span className="text-gray-600">Standard Deviation:</span>
                <span className="ml-2 font-medium">{brightness.brightness_std?.toFixed(1) || 0}</span>
              </div>
              <div>
                <span className="text-gray-600">Dynamic Range:</span>
                <span className="ml-2 font-medium">{brightness.dynamic_range || 0}</span>
              </div>
            </div>
          </div>
        )}

        {/* Weather Analysis */}
        {weather && (
          <div className="bg-white rounded-lg border p-4">
            <h3 className="text-lg font-semibold mb-3">🌤️ Weather Indicators</h3>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="text-center">
                <div className="text-2xl mb-2">
                  {weather.weather_condition === 'clear' && '☀️'}
                  {weather.weather_condition === 'partly_cloudy' && '⛅'}
                  {weather.weather_condition === 'overcast' && '☁️'}
                  {weather.weather_condition === 'variable' && '🌤️'}
                </div>
                <div className="font-medium capitalize">
                  {weather.weather_condition?.replace('_', ' ') || 'Unknown'}
                </div>
                <div className="text-sm text-gray-600">Condition</div>
              </div>
              <div className="text-center">
                <div className="text-xl font-bold text-gray-600 capitalize">
                  {weather.cloud_coverage}
                </div>
                <div className="text-sm text-gray-600">Cloud Coverage</div>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Blue Dominance:</span>
                <span className="ml-2 font-medium">{weather.blue_dominance?.toFixed(2) || 0}</span>
              </div>
              <div>
                <span className="text-gray-600">Color Uniformity:</span>
                <span className="ml-2 font-medium">{weather.color_uniformity?.toFixed(2) || 0}</span>
              </div>
              <div>
                <span className="text-gray-600">Texture Variance:</span>
                <span className="ml-2 font-medium">{weather.texture_variance?.toFixed(0) || 0}</span>
              </div>
            </div>
          </div>
        )}

        {/* Metadata */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-3">📊 Analysis Metadata</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Location:</span>
              <span className="ml-2 font-medium">{location.lat.toFixed(4)}, {location.lng.toFixed(4)}</span>
            </div>
            <div>
              <span className="text-gray-600">Last Updated:</span>
              <span className="ml-2 font-medium">
                {timestamp ? format(new Date(timestamp), 'PPp') : 'Unknown'}
              </span>
            </div>
            <div>
              <span className="text-gray-600">Webcam ID:</span>
              <span className="ml-2 font-medium font-mono">{webcam.webcam_id}</span>
            </div>
            <div>
              <span className="text-gray-600">Status:</span>
              <span className="ml-2 font-medium text-green-600">✓ Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WebcamDetails