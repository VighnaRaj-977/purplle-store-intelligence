from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI(
    title="Store Intelligence API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Store Intelligence System Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/events")
def get_events():

    conn = sqlite3.connect("database/store.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id,
               event_type,
               timestamp
        FROM events
    """)

    rows = cursor.fetchall()

    conn.close()

    events = []

    for row in rows:
        events.append(
            {
                "customer_id": row[0],
                "event_type": row[1],
                "timestamp": row[2]
            }
        )

    return events


@app.get("/metrics")
def metrics():

    conn = sqlite3.connect("database/store.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(DISTINCT customer_id) FROM events"
    )

    total_customers = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM events"
    )

    total_events = cursor.fetchone()[0]

    conn.close()

    return {
        "total_customers": total_customers,
        "total_events": total_events,
        "occupancy": total_customers
    }