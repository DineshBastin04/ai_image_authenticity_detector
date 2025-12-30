import sqlite3

conn = sqlite3.connect("logs.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS detections(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    result TEXT,
    confidence REAL,
    created_at TEXT
)""")
conn.commit()
conn.close()
print("Database initialized!")
