# Urban Micro-Climate Map - Project Overview

## 🎯 Project Description

This project implements a **Real-time Urban Micro-Climate Map using Public Webcams** as outlined in the implementation plan. The system creates a hyper-local "comfort map" of cities by analyzing public webcam feeds in real-time to infer environmental conditions like sun exposure and wetness.

## 🏗️ System Architecture

The system follows a modern microservices architecture with the following components:

```
┌─────────────────┐    WebSocket    ┌─────────────────┐
│   React.js      │◄──────────────►│   FastAPI       │
│   Frontend      │                 │   Backend       │
│   (Leaflet)     │                 │   (OpenCV)      │
└─────────────────┘                 └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │     Redis       │
                                    │   (Cache)       │
                                    └─────────────────┘
```

## 🚀 Implementation Phases

### Phase 1: Data Ingestion ✅
- **Backend**: Python service using `asyncio` and `aiohttp` for efficient webcam image fetching
- **Frontend**: React application with Leaflet maps showing webcam locations
- **Deliverable**: Backend service that downloads images + frontend showing data sources

### Phase 2: Computer Vision Analysis ✅
- **Backend**: OpenCV-based image analysis for sun/shadow detection
- **Algorithm**: Converts images to grayscale, applies thresholds, calculates pixel ratios
- **Deliverable**: Function returning structured data like `{"sun_exposure": 0.75}`

### Phase 3: Real-time Connection ✅
- **Backend**: WebSocket endpoint in FastAPI for live data streaming
- **Frontend**: React WebSocket integration for real-time map updates
- **Deliverable**: Map markers change appearance in real-time based on analysis

### Phase 4: Enhancements and Deployment ✅
- **Backend**: Advanced CV models for wetness detection
- **Frontend**: Polished UI with legend, tooltips, and responsive design
- **DevOps**: Docker containerization and deployment scripts

## 🛠️ Technology Stack

### Backend & Computer Vision
- **Python 3.11**: Core backend language
- **FastAPI**: Modern, fast web framework with WebSocket support
- **OpenCV**: Computer vision library for image analysis
- **asyncio**: Asynchronous programming for concurrent operations
- **aiohttp**: Async HTTP client for webcam image fetching
- **Redis**: In-memory data store for caching analysis results

### Frontend
- **React 18**: Modern UI framework
- **Leaflet**: Open-source mapping library
- **WebSockets**: Real-time bidirectional communication
- **Axios**: HTTP client for API communication

### DevOps
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Multi-service orchestration
- **Git**: Version control

## 📁 Project Structure

```
urban-micro-climate-map/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Main application entry point
│   ├── models.py            # Pydantic data models
│   ├── webcam_ingestion.py # Webcam image ingestion service
│   ├── cv_analysis.py      # Computer vision analysis
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   └── MicroClimateMap.js
│   │   ├── services/       # API and WebSocket services
│   │   │   ├── api.js
│   │   │   └── WebSocketManager.js
│   │   ├── App.js          # Main React component
│   │   └── index.js        # React entry point
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile          # Frontend container
├── docker-compose.yml       # Multi-service orchestration
├── start.sh                 # Production startup script
├── stop.sh                  # Production stop script
├── run-dev.sh               # Development startup script
└── README.md                # Project documentation
```

## 🔧 Key Features

### Computer Vision Analysis
- **Sun/Shadow Detection**: Analyzes image brightness to determine sun exposure
- **Wetness Detection**: Uses Laplacian variance to detect smooth/wet surfaces
- **Confidence Scoring**: Calculates analysis reliability based on image quality
- **Weather Classification**: Categorizes conditions (sunny, shady, wet, dry)

### Real-time Updates
- **WebSocket Integration**: Live data streaming from backend to frontend
- **Auto-reconnection**: Robust WebSocket handling with exponential backoff
- **Live Map Updates**: Map markers change color and data in real-time

### Interactive Map
- **Leaflet Integration**: Professional mapping with OpenStreetMap tiles
- **Custom Markers**: Color-coded markers based on weather conditions
- **Rich Popups**: Detailed information display for each webcam
- **Responsive Design**: Mobile-friendly interface

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for development)
- Node.js 18+ (for development)

### Quick Start (Production)
```bash
# Start all services
./start.sh

# Stop all services
./stop.sh
```

### Development Mode
```bash
# Start development environment
./run-dev.sh
```

### Manual Setup
```bash
# 1. Start Redis
docker run -d -p 6379:6379 redis:alpine

# 2. Start Backend
cd backend
pip install -r requirements.txt
python main.py

# 3. Start Frontend
cd frontend
npm install
npm start
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Redis**: localhost:6379
- **API Documentation**: http://localhost:8000/docs

## 📊 Sample Webcam Locations

The system includes sample webcam locations for demonstration:
- **Times Square, NYC**: 40.7580°N, 73.9855°W
- **Trafalgar Square, London**: 51.5080°N, 0.1281°W
- **Eiffel Tower, Paris**: 48.8584°N, 2.2945°E
- **Shibuya Crossing, Tokyo**: 35.6595°N, 139.7004°E

## 🔍 API Endpoints

### REST API
- `GET /`: System status
- `GET /webcams`: List all webcams
- `GET /analysis/{webcam_id}`: Get analysis for specific webcam
- `POST /trigger-analysis`: Manually trigger analysis

### WebSocket
- `WS /ws`: Real-time analysis updates

## 🎨 UI Features

### Map Interface
- **Interactive Markers**: Click for detailed information
- **Color Coding**: 
  - 🟡 Yellow: Sunny conditions
  - 🔵 Blue: Shady conditions
  - 🟢 Green: Wet conditions
  - 🔴 Red: Dry conditions
  - ⚫ Gray: Unknown/No data

### Controls
- **Analysis Trigger**: Manual analysis button
- **Connection Status**: WebSocket connection indicator
- **Real-time Updates**: Live data streaming

## 🔬 Computer Vision Details

### Sun/Shadow Analysis
1. Convert image to grayscale
2. Apply Gaussian blur to reduce noise
3. Use thresholding to separate bright/dark areas
4. Calculate percentage of bright pixels (sun exposure)
5. Shadow percentage = 1 - sun exposure

### Wetness Detection
1. Convert to grayscale and apply blur
2. Calculate Laplacian variance (image sharpness)
3. Lower variance indicates smoother surfaces (likely wet)
4. Apply threshold for conservative detection

### Confidence Calculation
- **Contrast Score**: High contrast = high confidence
- **Brightness Score**: Optimal brightness = high confidence
- **Combined Score**: Average of contrast and brightness metrics

## 🚧 Future Enhancements

### Advanced CV Models
- **Machine Learning**: Train models on labeled weather data
- **Reflection Detection**: Better wetness detection algorithms
- **Cloud Cover Analysis**: Detect overcast conditions
- **Time-based Patterns**: Learn seasonal and daily patterns

### Additional Features
- **User Accounts**: Personalized dashboards
- **Historical Data**: Time series analysis and trends
- **Mobile App**: Native mobile applications
- **API Integration**: Weather service integrations
- **Alert System**: Notifications for extreme conditions

## 🐛 Troubleshooting

### Common Issues
1. **Redis Connection Failed**: Ensure Redis is running on port 6379
2. **WebSocket Disconnected**: Check backend service status
3. **Analysis Not Updating**: Verify computer vision dependencies
4. **Map Not Loading**: Check frontend build and dependencies

### Debug Commands
```bash
# View service logs
docker-compose logs -f

# Check service health
docker-compose ps

# Restart specific service
docker-compose restart backend

# Access Redis CLI
docker-compose exec redis redis-cli
```

## 📈 Performance Considerations

- **Image Processing**: Optimized OpenCV operations for real-time analysis
- **Caching**: Redis caching for analysis results (1-hour TTL)
- **Concurrent Processing**: Async webcam ingestion for parallel processing
- **Memory Management**: Efficient image handling and cleanup

## 🔒 Security Notes

- **CORS Configuration**: Configured for development (localhost:3000)
- **Input Validation**: Pydantic models for data validation
- **Error Handling**: Comprehensive error handling and logging
- **Rate Limiting**: Consider implementing for production use

## 📝 License

This project is implemented as a demonstration of the Urban Micro-Climate Map concept. Please refer to the original project documentation for licensing information.

---

**🎉 Congratulations!** You now have a fully functional Real-time Urban Micro-Climate Map system that demonstrates all four implementation phases with a modern, scalable architecture.