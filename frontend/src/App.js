import React, { useState, useEffect, useCallback } from 'react';
import MicroClimateMap from './components/MicroClimateMap';
import WebSocketManager from './services/WebSocketManager';
import { fetchWebcams, triggerAnalysis } from './services/api';
import './App.css';

function App() {
  const [webcams, setWebcams] = useState([]);
  const [analysisData, setAnalysisData] = useState({});
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const wsManager = new WebSocketManager();
    
    wsManager.onConnect(() => {
      setIsConnected(true);
      console.log('WebSocket connected');
    });

    wsManager.onDisconnect(() => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    });

    wsManager.onMessage((data) => {
      try {
        const message = JSON.parse(data);
        if (message.type === 'analysis_update') {
          setAnalysisData(prev => ({
            ...prev,
            [message.webcam_id]: message.data
          }));
        }
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    });

    // Cleanup on unmount
    return () => {
      wsManager.disconnect();
    };
  }, []);

  // Fetch initial webcam data
  useEffect(() => {
    const loadWebcams = async () => {
      try {
        setIsLoading(true);
        const response = await fetchWebcams();
        setWebcams(response.webcams || []);
        setError(null);
      } catch (err) {
        setError('Failed to load webcam data');
        console.error('Error loading webcams:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadWebcams();
  }, []);

  const handleTriggerAnalysis = useCallback(async () => {
    try {
      setIsLoading(true);
      await triggerAnalysis();
      console.log('Analysis triggered successfully');
    } catch (err) {
      setError('Failed to trigger analysis');
      console.error('Error triggering analysis:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  if (isLoading && webcams.length === 0) {
    return (
      <div className="app">
        <div className="header">
          <h1>Urban Micro-Climate Map</h1>
          <p>Loading webcam data...</p>
        </div>
        <div className="main-content">
          <div style={{ padding: '2rem', textAlign: 'center' }}>
            <div>Loading...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="header">
        <h1>Urban Micro-Climate Map</h1>
        <p>Real-time micro-climate conditions from public webcams</p>
      </div>
      
      <div className="main-content">
        <div className="controls">
          <button 
            className="btn" 
            onClick={handleTriggerAnalysis}
            disabled={isLoading}
          >
            {isLoading ? 'Analyzing...' : 'Trigger Analysis'}
          </button>
          
          <div className="status-indicator">
            <div className={`status-dot ${isConnected ? '' : 'offline'}`}></div>
            <span>
              {isConnected ? 'WebSocket Connected' : 'WebSocket Disconnected'}
            </span>
          </div>
          
          {error && (
            <div style={{ color: '#dc3545', fontSize: '0.9rem' }}>
              {error}
            </div>
          )}
        </div>
        
        <div className="map-container">
          <MicroClimateMap 
            webcams={webcams}
            analysisData={analysisData}
            isConnected={isConnected}
          />
        </div>
      </div>
    </div>
  );
}

export default App;