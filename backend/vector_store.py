import faiss
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Paths
INDEX_PATH = Path("data/faiss.index")
META_PATH = Path("data/metadata.json")

# Load embedding model (lightweight & fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

EMBEDDING_DIM = 384

# Load or create index
if INDEX_PATH.exists():
    index = faiss.read_index(str(INDEX_PATH))
    metadata = json.loads(META_PATH.read_text())
else:
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    metadata = []


def add_story(story_text):
    embedding = model.encode([story_text])
    index.add(np.array(embedding))
    metadata.append(story_text)

    faiss.write_index(index, str(INDEX_PATH))
    META_PATH.write_text(json.dumps(metadata))


def search_similar(query, k=3):
    if index.ntotal == 0:
        return []

    embedding = model.encode([query])
    _, indices = index.search(np.array(embedding), k)

    return [metadata[i] for i in indices[0] if i < len(metadata)]