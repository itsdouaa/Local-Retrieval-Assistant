import sqlite3
import json

def update(data):
    connect = sqlite3.connect("/home/douaa/assistant/test.db")
    cursor = connect.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dict (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            tags TEXT
        )
    """)
    
    cursor.execute("SELECT * FROM dict WHERE (title, content, tags) = (?, ?, ?)", (data["title"], data["content"], json.dumps(data["tags"]))) 
    result = cursor.fetchone()
    if result is None:
        cursor.execute("""
            INSERT INTO dict (title, content, tags) VALUES (?, ?, ?)
        """, (data["title"], data["content"], json.dumps(data["tags"])))

    connect.commit()
    connect.close()
