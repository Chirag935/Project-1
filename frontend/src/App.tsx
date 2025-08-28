import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet'
import { useEffect, useMemo, useRef, useState } from 'react'
import L from 'leaflet'

interface Webcam {
  id: string
  name: string
  latitude: number
  longitude: number
  image_url: string
}

interface AnalysisPayload {
  webcam_id: string
  sun_exposure: number
  timestamp: number
  image_url?: string
}

const backendBase = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

const defaultIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
})

export default function App() {
  const [cams, setCams] = useState<Webcam[]>([])
  const [analysis, setAnalysis] = useState<Record<string, AnalysisPayload>>({})

  useEffect(() => {
    fetch(`${backendBase}/api/webcams`)
      .then(r => r.json())
      .then(setCams)
      .catch(() => {})
  }, [])

  useEffect(() => {
    const wsUrl = backendBase.replace('http', 'ws') + '/ws'
    const ws = new WebSocket(wsUrl)
    ws.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data)
        if (msg?.type === 'analysis' && msg?.payload?.webcam_id) {
          setAnalysis(prev => ({ ...prev, [msg.payload.webcam_id]: msg.payload as AnalysisPayload }))
        }
      } catch {}
    }
    return () => ws.close()
  }, [])

  const center = useMemo(() => {
    if (cams.length > 0) {
      return [cams[0].latitude, cams[0].longitude] as [number, number]
    }
    return [20, 0] as [number, number]
  }, [cams])

  return (
    <>
      <div className="panel">
        <div><strong>Urban Micro-Climate Map</strong></div>
        <div>Sun exposure: green=low, red=high</div>
      </div>
      <MapContainer id="map" center={center} zoom={3} scrollWheelZoom>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {cams.map(cam => {
          const a = analysis[cam.id]
          const color = a ? exposureToColor(a.sun_exposure) : '#8888ff'
          return (
            <>
              <Marker key={cam.id} position={[cam.latitude, cam.longitude]} icon={defaultIcon}>
                <Popup>
                  <div style={{minWidth: 220}}>
                    <div><strong>{cam.name}</strong></div>
                    <div>{cam.latitude.toFixed(4)}, {cam.longitude.toFixed(4)}</div>
                    {a && (
                      <div>Sun exposure: {(a.sun_exposure*100).toFixed(0)}%</div>
                    )}
                    <div style={{marginTop: 8}}>
                      <img src={cam.image_url} style={{width: '100%'}}/>
                    </div>
                  </div>
                </Popup>
              </Marker>
              <CircleMarker key={cam.id+"-circle"} center={[cam.latitude, cam.longitude]} radius={12} pathOptions={{color, fillColor: color, fillOpacity: 0.6}}/>
            </>
          )
        })}
      </MapContainer>
    </>
  )
}

function exposureToColor(value: number): string {
  // 0 -> green, 1 -> red
  const r = Math.round(value * 255)
  const g = Math.round((1 - value) * 200 + 30)
  return `rgb(${r}, ${g}, 60)`
}