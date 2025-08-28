"""
WebSocket Connection Manager
Handles real-time communication with frontend clients
"""

from fastapi import WebSocket
import json
import logging
from typing import List, Dict, Any
import asyncio

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total connections: {len(self.active_connections)}")
        
        # Send welcome message with current status
        await self.send_personal_message({
            'type': 'connection_established',
            'message': 'Connected to Urban Micro-Climate Map',
            'timestamp': str(asyncio.get_event_loop().time())
        }, websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected WebSocket clients"""
        if not self.active_connections:
            return
        
        message_json = json.dumps(message)
        disconnected_clients = []
        
        # Send to all connections
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected_clients.append(connection)
        
        # Clean up disconnected clients
        for client in disconnected_clients:
            self.disconnect(client)
        
        if disconnected_clients:
            logger.info(f"Cleaned up {len(disconnected_clients)} disconnected clients")
    
    async def broadcast_webcam_update(self, webcam_data: List[Dict[str, Any]]):
        """Broadcast webcam analysis updates"""
        message = {
            'type': 'webcam_analysis_update',
            'data': webcam_data,
            'timestamp': str(asyncio.get_event_loop().time())
        }
        await self.broadcast(message)
    
    async def broadcast_system_status(self, status: Dict[str, Any]):
        """Broadcast system status updates"""
        message = {
            'type': 'system_status',
            'data': status,
            'timestamp': str(asyncio.get_event_loop().time())
        }
        await self.broadcast(message)
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)