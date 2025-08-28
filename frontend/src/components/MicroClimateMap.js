import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const MicroClimateMap = ({ webcams, analysisData, isConnected }) => {
  const mapRef = useRef(null);

  // Custom marker icons based on weather conditions
  const getMarkerIcon = (webcamId) => {
    const analysis = analysisData[webcamId];
    if (!analysis) {
      return L.divIcon({
        className: 'custom-marker',
        html: `<div style="
          width: 20px; 
          height: 20px; 
          background: #6c757d; 
          border: 2px solid white; 
          border-radius: 50%;
          box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        "></div>`,
        iconSize: [20, 20],
        iconAnchor: [10, 10]
      });
    }

    const { weather_condition, sun_exposure, wetness_score } = analysis;
    
    let color = '#6c757d'; // default gray
    
    switch (weather_condition) {
      case 'sunny':
        color = '#ffc107'; // yellow
        break;
      case 'shady':
        color = '#17a2b8'; // blue
        break;
      case 'wet':
        color = '#28a745'; // green
        break;
      case 'dry':
        color = '#dc3545'; // red
        break;
      default:
        color = '#6c757d'; // gray
    }

    return L.divIcon({
      className: 'custom-marker',
      html: `<div style="
        width: 20px; 
        height: 20px; 
        background: ${color}; 
        border: 2px solid white; 
        border-radius: 50%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
      ">
        <div style="
          position: absolute;
          top: -2px;
          right: -2px;
          width: 8px;
          height: 8px;
          background: ${isConnected ? '#28a745' : '#dc3545'};
          border: 1px solid white;
          border-radius: 50%;
        "></div>
      </div>`,
      iconSize: [20, 20],
      iconAnchor: [10, 10]
    });
  };

  // Create popup content for webcam markers
  const createPopupContent = (webcam, analysis) => {
    if (!analysis) {
      return (
        <div className="webcam-popup">
          <h3>{webcam.name}</h3>
          <div className="info-row">
            <span className="label">Location:</span>
            <span className="value">{webcam.city}, {webcam.country}</span>
          </div>
          <div className="info-row">
            <span className="label">Coordinates:</span>
            <span className="value">{webcam.latitude.toFixed(4)}, {webcam.longitude.toFixed(4)}</span>
          </div>
          <div className="info-row">
            <span className="label">Status:</span>
            <span className="value">No recent data</span>
          </div>
        </div>
      );
    }

    const { 
      sun_exposure, 
      shadow_percentage, 
      wetness_score, 
      weather_condition, 
      confidence,
      timestamp 
    } = analysis;

    return (
      <div className="webcam-popup">
        <h3>{webcam.name}</h3>
        
        <div className="info-row">
          <span className="label">Condition:</span>
          <span className={`weather-condition ${weather_condition}`}>
            {weather_condition}
          </span>
        </div>
        
        <div className="info-row">
          <span className="label">Sun Exposure:</span>
          <span className="value">{(sun_exposure * 100).toFixed(1)}%</span>
        </div>
        
        <div className="info-row">
          <span className="label">Shadow:</span>
          <span className="value">{(shadow_percentage * 100).toFixed(1)}%</span>
        </div>
        
        <div className="info-row">
          <span className="label">Wetness:</span>
          <span className="value">{(wetness_score * 100).toFixed(1)}%</span>
        </div>
        
        <div className="info-row">
          <span className="label">Confidence:</span>
          <span className="value">{(confidence * 100).toFixed(1)}%</span>
        </div>
        
        <div className="info-row">
          <span className="label">Last Updated:</span>
          <span className="value">
            {new Date(timestamp).toLocaleTimeString()}
          </span>
        </div>
        
        <div className="info-row">
          <span className="label">Location:</span>
          <span className="value">{webcam.city}, {webcam.country}</span>
        </div>
      </div>
    );
  };

  // Fit map bounds to show all webcams
  useEffect(() => {
    if (mapRef.current && webcams.length > 0) {
      const bounds = L.latLngBounds(
        webcams.map(webcam => [webcam.latitude, webcam.longitude])
      );
      mapRef.current.fitBounds(bounds, { padding: [20, 20] });
    }
  }, [webcams]);

  if (webcams.length === 0) {
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100%',
        color: '#666'
      }}>
        No webcam data available
      </div>
    );
  }

  return (
    <>
      <MapContainer
        ref={mapRef}
        center={[40.7580, -73.9855]} // Default to NYC
        zoom={10}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        
        {webcams.map((webcam) => (
          <Marker
            key={webcam.id}
            position={[webcam.latitude, webcam.longitude]}
            icon={getMarkerIcon(webcam.id)}
          >
            <Popup>
              {createPopupContent(webcam, analysisData[webcam.id])}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
      
      {/* Legend */}
      <div className="legend">
        <h3>Weather Conditions</h3>
        <div className="legend-item">
          <div className="legend-color" style={{ background: '#ffc107' }}></div>
          <span className="legend-text">Sunny</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ background: '#17a2b8' }}></div>
          <span className="legend-text">Shady</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ background: '#28a745' }}></div>
          <span className="legend-text">Wet</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ background: '#dc3545' }}></div>
          <span className="legend-text">Dry</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ background: '#6c757d' }}></div>
          <span className="legend-text">Unknown</span>
        </div>
        
        <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid #e0e0e0' }}>
          <div className="legend-item">
            <div className="legend-color" style={{ background: '#28a745' }}></div>
            <span className="legend-text">Live</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ background: '#dc3545' }}></div>
            <span className="legend-text">Offline</span>
          </div>
        </div>
      </div>
    </>
  );
};

export default MicroClimateMap;