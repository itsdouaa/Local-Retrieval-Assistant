from sentence_transformers import SentenceTransformer
import sqlite3
import subprocess
import faiss
import numpy as np
import file_loader

def manager(question):
    add_file = {"yes": file_loader.main}
    
    context = []
    context += embeddings(question)
    
    file = add_file.get(input("do you want to add some context/files ?\n").lower())
    while file:
        new_context = file()
        if not new_context:
            file = add_file.get(input("you want to add some context/files ?\n").lower())
        else:
            context += new_context
            file = add_file.get(input("you want to add some other context/files ?\n").lower())
    
    return context

model = SentenceTransformer("all-MiniLM-L6-v2")

def embeddings(question):
    question_embedding = model.encode(question).astype("float32")
    
    if question_embedding is None or not question_embedding.size:
        return ""
    index, contents = refresh_index()
    
    if index == None:
        return None
    
    _, indices = index.search(np.array([question_embedding]), 3)

    selected = [contents[i] for i in indices[0]]
        
    return "\n\n".join(selected) if selected else None

def refresh_index():
    db_path = os.path.expanduser("~/local_retrieval_assistant/test.db")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if not os.path.exists(db_path):
        open(db_path, "w").close()

    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dict (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            tags TEXT
        )
    """)
    cursor.execute("SELECT id, content FROM dict")
    rows = cursor.fetchall()
    
    ids = []
    contents = []
    embeddings = []
    
    for row in rows:
        id_, text = row
        vec = model.encode(text)
        ids.append(id_)
        contents.append(text)
        embeddings.append(vec)

    embedding_matrix = np.array(embeddings).astype("float32")

    if len(embeddings) == 0:
        return None, []

    print("Embedding matrix shape:", embedding_matrix.shape)
    
    index = faiss.IndexFlatL2(embedding_matrix.shape[1])
    index.add(embedding_matrix)
    
    connect.close()
    
    return index, contents
