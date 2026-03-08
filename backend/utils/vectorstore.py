import os
import uuid
from pathlib import Path
from chromadb import PersistentClient  
from backend.utils.embeddings import embed_texts

CHROMA_DIR = os.getenv("CHROMA_DIR", "chroma_db")
Path(CHROMA_DIR).mkdir(exist_ok=True)

client = PersistentClient(path=CHROMA_DIR)

default_collection = client.get_or_create_collection("documents")

def create_collection_if_not_exists(name: str):
    return client.get_or_create_collection(name)

def add_chunks(collection_name: str, docs: list[str], metadatas: list[dict]):
    col = create_collection_if_not_exists(collection_name)
    embeddings = embed_texts(docs)
    ids = [f"{collection_name}_{uuid.uuid4().hex}" for _ in range(len(docs))]

    col.add(
        ids=ids,
        documents=docs,
        metadatas=metadatas,
        embeddings=embeddings
    )
    return True  

def query_chunks(collection_name: str, query_embedding: list[float], top_k: int = 3):
    col = create_collection_if_not_exists(collection_name)
    return col.query(query_embeddings=[query_embedding], n_results=top_k)