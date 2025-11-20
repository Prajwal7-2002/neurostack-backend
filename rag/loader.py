import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_PATH = BASE / "data" / "faqs.json"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

def load_faqs():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    if len(text) <= size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks

def build_corpus():
    docs = load_faqs()
    texts, meta = [], []

    for d in docs:
        q = clean_text(d.get("question", ""))
        a = clean_text(d.get("answer", ""))
        combined = q + "\n\n" + a

        for i, chunk in enumerate(chunk_text(combined)):
            texts.append(chunk)
            meta.append({
                "source_id": d["id"],
                "chunk_index": i,
                "question": q
            })

    return texts, meta
