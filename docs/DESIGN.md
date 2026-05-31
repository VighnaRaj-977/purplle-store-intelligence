# Store Intelligence System Design

## Overview

The Store Intelligence System processes CCTV footage to generate real-time store analytics and operational insights.

The pipeline consists of:

1. Video Ingestion
2. Person Detection
3. Multi-Object Tracking
4. Event Generation
5. Metrics Aggregation
6. Database Storage
7. API Layer
8. Dashboard Visualization

---

## Architecture

CCTV Cameras
      |
      v
YOLOv8 Person Detection
      |
      v
DeepSORT Tracking
      |
      v
Event Engine
      |
      v
SQLite Database
      |
      v
FastAPI Backend
      |
      +----> REST APIs
      |
      +----> Dashboard

---

## Components

### Detection Layer

YOLOv8 is used for person detection in CCTV frames.

### Tracking Layer

DeepSORT assigns a unique ID to each detected customer and maintains identity across frames.

### Event Engine

Generates events such as:

- Customer Entered
- Customer Exited
- Occupancy Updated
- Anomaly Detected

### Database

SQLite stores:

- Events
- Metrics
- Timestamps

### API Layer

FastAPI exposes:

- /health
- /events
- /metrics

### Dashboard

Displays:

- Customer Count
- Occupancy
- Total Events
- System Health

---

## Scalability

Future improvements:

- Kafka Event Streaming
- PostgreSQL
- Redis Caching
- Multi-Camera Correlation
- Cloud Deployment