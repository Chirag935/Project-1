#!/bin/bash

echo "🛑 Stopping Urban Micro-Climate Map System..."

# Stop all services
docker-compose down

echo "✅ All services stopped"
echo ""
echo "💡 Use './start.sh' to start the system again"