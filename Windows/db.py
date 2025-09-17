import sqlite3
import json
import os

def save(data):
    """
    Save data to SQLite database in the project directory.
    """
    # Create database in the same directory as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "test.db")
    
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dict (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            tags TEXT
        )
    """)
    
    # Check for duplicates
    cursor.execute(
        "SELECT * FROM dict WHERE (title, content, tags) = (?, ?, ?)", 
        (data["title"], data["content"], json.dumps(data["tags"]))
    )
    result = cursor.fetchone()
    
    # Insert if not duplicate
    if result is None:
        cursor.execute(
            "INSERT INTO dict (title, content, tags) VALUES (?, ?, ?)",
            (data["title"], data["content"], json.dumps(data["tags"]))
        )

    connect.commit()
    connect.close()