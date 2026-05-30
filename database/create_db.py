import sqlite3

conn = sqlite3.connect("database/store.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    event_type TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")