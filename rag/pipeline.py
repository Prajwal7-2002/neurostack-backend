# backend/rag/pipeline.py
from .retrieval import retrieve, MIN_SCORE_THRESHOLD
from .llm import call_llm

def run_rag(query: str, max_chunks=4):
    """
    RAG main pipeline.
    Returns dict:
    {
        "answer": str,
        "validated": bool,
        "chunks": [...],
        "reason": str (optional),
        "note": str (optional)
    }
    """

    # ---------------------------------------
    # 1) RETRIEVAL
    # ---------------------------------------
    candidates = retrieve(query)   # FIXED — no top_k argument

    if not candidates:
        return {
            "answer": "",
            "validated": False,
            "chunks": [],
            "reason": "no_relevant_documents"
        }

    # ---------------------------------------
    # 2) VALIDATION — MIN SCORE CHECK
    # ---------------------------------------
    top = candidates[0]
    if top["score"] < MIN_SCORE_THRESHOLD:
        return {
            "answer": "",
            "validated": False,
            "chunks": candidates,
            "reason": "low_relevance"
        }

    # ---------------------------------------
    # 3) SELECT CHUNKS
    # ---------------------------------------
    chosen = candidates[:max_chunks]
    context = "\n\n---\n\n".join([c["text"] for c in chosen])

    # ---------------------------------------
    # 4) CALL THE LLM
    # ---------------------------------------
    try:
        llm_answer = call_llm(query, context)

        # If LLM returns nothing → fallback
        if not llm_answer or llm_answer.strip() == "":
            fallback = chosen[0]["text"]
            return {
                "answer": fallback,
                "validated": True,
                "chunks": chosen,
                "note": "fallback_used_empty_or_none_llm"
            }

        # SUCCESS
        return {
            "answer": llm_answer.strip(),
            "validated": True,
            "chunks": chosen
        }

    except Exception as e:
        # ---------------------------------------
        # 5) TOTAL FAILURE → FALLBACK ANSWER
        # ---------------------------------------
        fallback = chosen[0]["text"]
        return {
            "answer": fallback,
            "validated": True,
            "chunks": chosen,
            "note": f"fallback_used_due_to_llm_error: {str(e)}"
        }
