import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response.data;
  },
  (error) => {
    console.error('API Response Error:', error);
    
    if (error.response) {
      // Server responded with error status
      console.error('Error data:', error.response.data);
      console.error('Error status:', error.response.status);
    } else if (error.request) {
      // Request was made but no response received
      console.error('No response received:', error.request);
    } else {
      // Something else happened
      console.error('Error setting up request:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// API endpoints
export const fetchWebcams = async () => {
  try {
    const response = await api.get('/webcams');
    return response;
  } catch (error) {
    console.error('Error fetching webcams:', error);
    throw error;
  }
};

export const getAnalysis = async (webcamId) => {
  try {
    const response = await api.get(`/analysis/${webcamId}`);
    return response;
  } catch (error) {
    console.error(`Error fetching analysis for ${webcamId}:`, error);
    throw error;
  }
};

export const triggerAnalysis = async () => {
  try {
    const response = await api.post('/trigger-analysis');
    return response;
  } catch (error) {
    console.error('Error triggering analysis:', error);
    throw error;
  }
};

export const getSystemStatus = async () => {
  try {
    const response = await api.get('/');
    return response;
  } catch (error) {
    console.error('Error fetching system status:', error);
    throw error;
  }
};

// Utility function to check if backend is available
export const checkBackendHealth = async () => {
  try {
    await api.get('/');
    return true;
  } catch (error) {
    return false;
  }
};

// Export the api instance for custom requests
export default api;