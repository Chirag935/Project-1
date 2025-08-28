from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI(title="Urban Micro-Climate Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connected_clients.add(ws)
    try:
        while True:
            # keep connection open, backend pushes messages externally
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        connected_clients.remove(ws)

async def broadcast(message: dict):
    for client in list(connected_clients):
        try:
            await client.send_json(message)
        except Exception:
            connected_clients.remove(client)