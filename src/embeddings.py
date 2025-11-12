from sentence_transformers import SentenceTransformer
from tiktoken import get_encoding
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, max_tokens=500, overlap=50):
    enc = get_encoding("cl100k_base")
    tokens = enc.encode(text)

    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk = tokens[start:end]
        chunks.append(enc.decode(chunk))
        start += max_tokens - overlap
    return chunks

def generate(text):
    embeddings = []
    chunks = chunk_text(text)
    for chunk in chunks:
        emb = model.encode(chunk, convert_to_numpy=True, normalize_embeddings=True)
        embeddings.append(emb)
    return embeddings
