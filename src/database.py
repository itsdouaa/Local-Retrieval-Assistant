import sqlite3
from sqlite_vss import loadable_extension
import os
from tkinter import Tk, filedialog

def init_db(db_path):
    sqlite3.enable_load_extension(True)
    with sqlite3.connect(db_path) as connect:
        connect.execute("PRAGMA foreign_keys = ON;")
        connect.enable_load_extension(True)
        try:
            connect.load_extension(loadable_extension.load())
        except sqlite3.OperationalError as e:
            print("Extension already loaded or unavailable:", e)
        cursor = connect.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historique(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS embeddings
            USING vss0(
                embedding(384)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embedding_links(
                embedding_rowid INTEGER,
                message_id INTEGER,
                FOREIGN KEY(message_id) REFERENCES historique(id)
            )
        """)
        connect.commit()

def create():
    root = Tk()
    root.withdraw()
    db_path = filedialog.asksaveasfilename(
        title="Create database",
        defaultextension=".db",
        filetypes=[("SQLite Database", "*.db")]
    )
    if not db_path:
        print("Database not created!")
        return None
    
    init_db(db_path)
    print(f"Database successfully created at: {db_path}")
    return db_path

def link_message_embeddings(db_path, message_id, embeddings):
    with sqlite3.connect(db_path) as connect:
        connect.execute("PRAGMA foreign_keys = ON;")
        connect.enable_load_extension(True)
        try:
            connect.load_extension(loadable_extension.load())
        except sqlite3.OperationalError as e:
            print("Extension already loaded or unavailable:", e)
        cursor = connect.cursor()
        cursor.execute("SELECT id FROM embeddings")
        for embedding in embeddings:
            cursor.fetchone()
        

def insert_record(db_path, message, embeddings):
    with sqlite3.connect(db_path) as connect:
        connect.execute("PRAGMA foreign_keys = ON;")
        connect.enable_load_extension(True)
        try:
            connect.load_extension(loadable_extension.load())
        except sqlite3.OperationalError as e:
            print("Extension already loaded or unavailable:", e)
        
        cursor = connect.cursor()
        cursor.execute("""
            INSERT INTO historique (role, content) VALUES (?, ?)
        """, (message["role"], message["content"]))
        
        message_id = cursor.lastrowid
        for embedding in embeddings:
            cursor.execute("""
                INSERT INTO embeddings (embedding, message_id) VALUES (?, ?)
            """, (embedding, message_id))
        connect.commit()
        
        
    return message_id

def open_existing():
    root = Tk()
    root.withdraw()
    db_path = filedialog.askopenfilename(
        title = "choose your database",
        filetypes=[("SQLite Database", "*.db")]
    )
    return db_path

def request():
    
