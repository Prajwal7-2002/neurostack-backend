import numpy as np
from pathlib import Path
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from numpy.linalg import norm

from .loader import build_corpus

BASE = Path(__file__).resolve().parent.parent

# Load corpus
TEXTS, META = build_corpus()

# BM25
BM25 = BM25Okapi([t.split() for t in TEXTS])

# Embeddings
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

EMB_DIR = BASE / "embeddings"
EMB_DIR.mkdir(exist_ok=True)
NPY_PATH = EMB_DIR / "embeddings.npy"
FAISS_PATH = EMB_DIR / "faiss.index"

TOP_K = 6
MIN_SCORE_THRESHOLD = 0.35


def compute_embeddings():
    if NPY_PATH.exists() and FAISS_PATH.exists():
        return np.load(NPY_PATH)

    embs = MODEL.encode(TEXTS, convert_to_numpy=True)
    np.save(NPY_PATH, embs)

    faiss.normalize_L2(embs)
    index = faiss.IndexFlatIP(embs.shape[1])
    index.add(embs)
    faiss.write_index(index, str(FAISS_PATH))

    return embs


EMBS = compute_embeddings()
FAISS_INDEX = faiss.read_index(str(FAISS_PATH))


def retrieve(query, top_k=6):
    # semantic
    q_emb = MODEL.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = FAISS_INDEX.search(q_emb.astype("float32"), top_k)

    semantic = [{
        "text": TEXTS[i],
        "score": float(s),
        "idx": int(i),
        "meta": META[i]
    } for s, i in zip(D[0], I[0])]

    # lexical
    scores = BM25.get_scores(query.split())
    lex_sorted = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    lexical = [{
        "text": TEXTS[i],
        "score": float(s),
        "idx": int(i),
        "meta": META[i]
    } for i, s in lex_sorted]

    combined = semantic + lexical
    combined = sorted(combined, key=lambda x: x["score"], reverse=True)

    return [c for c in combined if c["score"] >= MIN_SCORE_THRESHOLD][:top_k]
