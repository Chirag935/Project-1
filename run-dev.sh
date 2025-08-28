#!/bin/bash

echo "🔧 Starting Urban Micro-Climate Map System in Development Mode..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Redis is available
if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis CLI not found. Starting Redis with Docker..."
    docker run -d -p 6379:6379 --name dev-redis redis:alpine
    sleep 3
fi

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "⚠️  Redis is not running. Starting Redis..."
    if docker ps -q -f name=dev-redis > /dev/null 2>&1; then
        docker start dev-redis
    else
        docker run -d -p 6379:6379 --name dev-redis redis:alpine
    fi
    sleep 3
fi

echo "✅ Redis is running"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Start backend in background
echo "🚀 Starting backend service..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend in background
echo "🚀 Starting frontend service..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 Development system started!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 Redis: localhost:6379"
echo ""
echo "💡 Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping development services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait