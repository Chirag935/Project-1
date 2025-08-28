#!/bin/bash

echo "🐳 Starting Urban Micro-Climate Map with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "🏗️  Building and starting services..."
echo ""

# Build and start all services
docker-compose up --build -d

# Wait a moment for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose ps

# Check health
echo ""
echo "🏥 Health Checks:"

# Check Redis
if docker-compose exec redis redis-cli ping >/dev/null 2>&1; then
    echo "✅ Redis: Healthy"
else
    echo "❌ Redis: Unhealthy"
fi

# Check Backend
if curl -s http://localhost:8000/ >/dev/null 2>&1; then
    echo "✅ Backend API: Healthy (http://localhost:8000)"
else
    echo "❌ Backend API: Unhealthy"
fi

# Check Frontend
if curl -s http://localhost/ >/dev/null 2>&1; then
    echo "✅ Frontend: Healthy (http://localhost)"
else
    echo "❌ Frontend: Unhealthy"
fi

echo ""
echo "🌟 Urban Micro-Climate Map is now running!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo "   WebSocket: ws://localhost:8000/ws"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   View status: docker-compose ps"
echo ""
echo "Press Ctrl+C to view logs, or run 'docker-compose down' to stop all services"
echo ""

# Follow logs
docker-compose logs -f