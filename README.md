# Real-time Urban Micro-Climate Map using Public Webcams

This project creates a hyper-local "comfort map" of a city by analyzing public webcam feeds in real-time. It infers environmental conditions like sun exposure and wetness that are not captured by official weather data.

## Project Overview

The system continuously ingests images from public webcams, analyzes them using computer vision to detect micro-climate conditions, and visualizes the data on a live map dashboard.

## Technology Stack

- **Backend & CV:** Python, FastAPI, WebSockets, asyncio, OpenCV
- **Database:** Redis (for caching current conditions)
- **Frontend:** React.js, Leaflet
- **DevOps:** Docker, Git

## Architecture

A Python service continuously fetches images from webcams. A CV pipeline processes each image, and the resulting data is sent via WebSockets to a frontend map dashboard for live visualization.

## Implementation Phases

1. **Phase 1:** Data Ingestion - Backend service for fetching webcam images
2. **Phase 2:** Computer Vision Analysis - OpenCV-based image analysis
3. **Phase 3:** Real-time Connection - WebSocket integration for live updates
4. **Phase 4:** Enhancements and Deployment - Advanced CV models and polished UI

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Start Redis: `docker run -d -p 6379:6379 redis:alpine`
3. Run backend: `python backend/main.py`
4. Run frontend: `cd frontend && npm install && npm start`

## Features

- Real-time webcam image ingestion
- Computer vision analysis for sun/shadow detection
- Live map visualization with WebSocket updates
- Responsive React frontend with Leaflet maps
