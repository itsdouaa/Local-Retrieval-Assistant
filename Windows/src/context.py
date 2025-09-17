from sentence_transformers import SentenceTransformer
import sqlite3
import faiss
import numpy as np
import file_loader
import os

def manager(question):
    add_file = {"yes": file_loader.main}
    
    context = []
    
    file = add_file.get(input("do you want to add some context/files ?\n").lower())
    while file:
        new_context = file()
        if not new_context:
            file = add_file.get(input("you want to add some context/files ?\n").lower())
        else:
            context += new_context
            file = add_file.get(input("you want to add some other context/files ?\n").lower())
    
    context += embeddings(question)
    return context

model = SentenceTransformer("all-MiniLM-L6-v2")

def embeddings(question):
    question_embedding = model.encode(question).astype("float32")
    
    if question_embedding is None or not question_embedding.size:
        return ""
    
    index, contents = refresh_index()
    
    if index is None:
        return None
    
    _, indices = index.search(np.array([question_embedding]), 3)

    selected = [contents[i] for i in indices[0] if i < len(contents)]
        
    return "\n\n".join(selected) if selected else None

def refresh_index():
    # Create database path in the same directory as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "test.db")
    
    connect = sqlite3.connect(db_path)
    cursor = connect.cursor()
    cursor.execute("SELECT id, content FROM dict")
    rows = cursor.fetchall()
    
    contents = []
    embeddings_list = []
    
    for row in rows:
        id_, text = row
        vec = model.encode(text)
        contents.append(text)
        embeddings_list.append(vec)

    if len(embeddings_list) == 0:
        connect.close()
        return None, []

    embedding_matrix = np.array(embeddings_list).astype("float32")
    
    index = faiss.IndexFlatL2(embedding_matrix.shape[1])
    index.add(embedding_matrix)
    
    connect.close()
    
    return index, contents