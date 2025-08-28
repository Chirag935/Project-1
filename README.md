# 🌍 Real-time Urban Micro-Climate Map

A comprehensive web application that analyzes public webcam feeds to provide real-time micro-climate monitoring across urban locations worldwide. Using computer vision and machine learning, the system provides insights into local weather conditions, sun/shadow patterns, and environmental comfort levels.

## 🎯 Project Overview

This project creates a hyper-local "comfort map" of cities by analyzing public webcam feeds in real-time. It infers environmental conditions like sun exposure and wetness that are not captured by official weather data.

### Key Features

- **Real-time Data Pipeline**: Continuously ingests images from public webcams
- **Computer Vision Analysis**: Uses OpenCV for sun/shadow detection and weather analysis
- **Live Dashboard**: Interactive map with real-time updates via WebSockets
- **Micro-Climate Scoring**: Calculates comfort levels based on multiple environmental factors
- **Modern Web Interface**: Beautiful React frontend with Leaflet maps

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Public        │    │    Backend       │    │    Frontend     │
│   Webcams       │───▶│   (FastAPI)      │───▶│    (React)      │
│                 │    │                  │    │                 │
│ • NYC Times Sq  │    │ • Data Ingestion │    │ • Interactive   │
│ • London Bridge │    │ • CV Analysis    │    │   Map View      │
│ • Tokyo Shibuya │    │ • WebSocket API  │    │ • Real-time     │
│ • Paris Eiffel  │    │ • Redis Cache    │    │   Dashboard     │
│ • Sydney Harbor │    │                  │    │ • Detail Views  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Technology Stack

### Backend & CV
- **Python 3.8+**: Core backend language
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **WebSockets**: Real-time communication
- **asyncio**: Asynchronous data fetching
- **OpenCV**: Computer vision analysis
- **Redis**: Caching current conditions

### Frontend
- **React.js**: Modern UI framework
- **Leaflet/Mapbox**: Interactive map visualization
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Data visualization components
- **Vite**: Fast build tool and dev server

### DevOps
- **Docker**: Containerization
- **Git**: Version control

## 🏃‍♂️ Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Redis server (optional, for caching)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Start Redis (optional)**:
   ```bash
   redis-server
   ```

4. **Run the backend**:
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`
   Interactive API docs at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:3000`

## 📋 Phase-by-Phase Implementation

### ✅ Phase 1: Data Ingestion
- [x] Python script using asyncio and aiohttp for efficient image fetching
- [x] React application with Leaflet map displaying webcam locations
- [x] Backend service that reliably downloads images
- [x] Frontend showing data sources on map

### ✅ Phase 2: Computer Vision Analysis
- [x] OpenCV functions for sun/shadow detection
- [x] Grayscale conversion and binary thresholding
- [x] Percentage calculation of black vs. white pixels
- [x] Structured data output (e.g., {"sun_exposure": 0.75})

### ✅ Phase 3: Real-time Connection
- [x] WebSocket endpoint in FastAPI
- [x] Real-time data push after image analysis
- [x] React WebSocket connection
- [x] Live map marker updates based on analysis

### 🔄 Phase 4: Enhancements and Deployment
- [ ] Advanced CV models (reflection detection for wet streets)
- [ ] Enhanced UI (legend, tooltips, heatmap visualization)
- [ ] Docker deployment setup
- [ ] Production-ready configuration

## 🌡️ Micro-Climate Analysis

The system analyzes several environmental factors:

### Sun/Shadow Detection
- Converts images to grayscale and applies thresholding
- Calculates percentage of sun-exposed vs. shadowed areas
- Identifies discrete sun and shadow regions
- Provides sun/shadow ratio for comfort assessment

### Weather Indicators
- Detects cloud coverage using texture analysis
- Analyzes color dominance for sky conditions
- Identifies weather patterns (clear, cloudy, overcast)

### Brightness Analysis
- Measures overall image brightness and contrast
- Classifies lighting conditions (bright, moderate, dim, dark)
- Calculates dynamic range for visual comfort

### Comfort Score Calculation
Combines all factors into a 0-100 comfort score:
- **80-100**: Excellent conditions
- **65-79**: Good conditions  
- **45-64**: Moderate conditions
- **25-44**: Poor conditions
- **0-24**: Very poor conditions

## 🔌 API Endpoints

### REST API
- `GET /` - Health check
- `GET /api/webcams` - List all configured webcams
- `GET /api/webcams/{id}/latest` - Latest analysis for specific webcam
- `GET /api/all-latest` - Latest analysis for all webcams

### WebSocket
- `WS /ws` - Real-time updates stream

## 🗺️ Current Webcam Locations

- **New York**: Times Square
- **London**: Tower Bridge  
- **Tokyo**: Shibuya Crossing
- **Paris**: Eiffel Tower
- **Sydney**: Harbor Bridge

## 🔧 Configuration

### Environment Variables

Backend configuration in `backend/.env`:

```env
FETCH_INTERVAL=60          # Seconds between webcam fetches
REDIS_HOST=localhost       # Redis server host
REDIS_PORT=6379           # Redis server port
API_HOST=0.0.0.0          # API server host
API_PORT=8000             # API server port
LOG_LEVEL=INFO            # Logging level
```

### Adding New Webcams

Edit `backend/webcam_ingestion.py` to add new webcam sources:

```python
{
    'webcam_id': 'unique_id',
    'name': 'Display Name',
    'url': 'https://webcam-image-url.jpg',
    'location': {
        'lat': latitude,
        'lng': longitude,
        'city': 'City Name',
        'country': 'Country'
    },
    'update_interval': 60
}
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS errors**: Ensure backend CORS settings include frontend URL
2. **WebSocket connection fails**: Check that backend is running on port 8000
3. **No webcam data**: Verify internet connection and webcam URLs are accessible
4. **Redis connection errors**: Install and start Redis server, or disable caching

### Development Tips

- Use browser DevTools Network tab to debug API calls
- Check backend logs for detailed error information
- Use `npm run build` to create production build
- Monitor WebSocket messages in DevTools console

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Public webcam providers for data sources
- OpenCV community for computer vision tools
- FastAPI and React communities for excellent frameworks
- Leaflet for open-source mapping capabilities

---

**Built with ❤️ for urban environmental monitoring and smart city initiatives.**