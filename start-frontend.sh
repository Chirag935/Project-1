#!/bin/bash

echo "🚀 Starting Urban Micro-Climate Map Frontend..."

# Check if we're in the correct directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    echo "Please install Node.js 16 or higher from https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "⚠️  Backend is not running. Please start the backend first:"
    echo "   ./start-backend.sh"
    echo ""
    echo "The frontend will still start, but you may see connection errors."
    echo ""
fi

echo "🌟 Starting React development server..."
echo "🌐 Frontend will be available at: http://localhost:3000"
echo "🔄 Hot reload is enabled for development"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm run dev