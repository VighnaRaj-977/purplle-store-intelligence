import sqlite3

conn = sqlite3.connect("database/store.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM events"
)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()