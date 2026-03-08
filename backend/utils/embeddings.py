from sentence_transformers import SentenceTransformer
import numpy as np

EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def embed_texts(texts):
    vectors = EMBED_MODEL.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return [v.tolist() for v in vectors]

def embed_query(text: str):
    vec = EMBED_MODEL.encode([text], show_progress_bar=False, convert_to_numpy=True)[0]
    return vec.tolist()