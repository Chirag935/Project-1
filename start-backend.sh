#!/bin/bash

echo "🚀 Starting Urban Micro-Climate Map Backend..."

# Check if we're in the correct directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ Error: pip is not installed"
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Redis is running (optional)
if command -v redis-cli &> /dev/null; then
    if redis-cli ping >/dev/null 2>&1; then
        echo "✅ Redis is running and accessible"
    else
        echo "⚠️  Redis is not running. The app will work without caching."
    fi
else
    echo "⚠️  Redis is not installed. The app will work without caching."
fi

# Navigate to backend directory
cd backend

# Set environment variables if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating default .env file..."
    cat > .env << EOL
FETCH_INTERVAL=60
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
EOL
fi

echo "🌟 Starting FastAPI server..."
echo "📡 API will be available at: http://localhost:8000"
echo "📚 API docs will be available at: http://localhost:8000/docs"
echo "🔌 WebSocket endpoint: ws://localhost:8000/ws"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py