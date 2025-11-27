from sentence_transformers import SentenceTransformer
from tiktoken import get_encoding
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
encoding = get_encoding("cl100k_base")

def chunk_text(text, max_tokens=500, overlap=50):
    text = text.strip()
    if not text:
        return []
    
    tokens = encoding.encode(text)
    
    if len(tokens) <= max_tokens:
        return [encoding.decode(tokens)]
    
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk = tokens[start:end]
        chunks.append(encoding.decode(chunk))
        start += max_tokens - overlap
    return chunks

def generate(text):
    text = text.strip()
    if not text:
        return []
    
    embeddings = []
    chunks = chunk_text(text)
    if not chunks:
        return [] 
    
    for chunk in chunks:
        embedding = model.encode(chunk, convert_to_numpy=True, normalize_embeddings=True)
        embeddings.append(embedding)
    return np.array(embeddings)
