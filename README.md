# Real-time Urban Micro-Climate Map

End-to-end example from the reference images: FastAPI + OpenCV backend, Redis cache, WebSocket updates, and a React + Leaflet frontend.

## Quick start (Docker)

Requirements: Docker + Docker Compose

```bash
# From repo root
docker compose up --build
```

- Backend: http://localhost:8000 (docs at /docs)
- Frontend: http://localhost:5173

The backend ingests demo images every 60s and broadcasts sun exposure per webcam. The frontend map colors each marker by sun exposure (green=low, red=high).

## Run locally without Docker

Backend requires Python 3.11+

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Frontend requires Node 18+

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173

## Configuration

- `backend/.env.example` documents `REDIS_URL`, `FETCH_INTERVAL_SEC`, and `WEBCAMS_CONFIG_PATH`.
- `backend/webcams.json` contains sample webcams with coordinates and image URLs.

## Notes

- Redis is optional; backend falls back to in-memory cache if Redis is unavailable.
- OpenCV is used for a simple grayscale + Otsu threshold to estimate sun exposure.
