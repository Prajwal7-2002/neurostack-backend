# backend/rag/llm.py
import os
import requests

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

PROMPT_TEMPLATE = """
You are a helpful SaaS support assistant.
Answer ONLY from the provided context.
If the answer does not exist in the context, reply:
"I don't know based on the available documentation."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

def call_llm(question, context, max_tokens=200):
    if not GROQ_API_KEY:
        return None

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You MUST answer only using context."},
            {"role": "user",
             "content": PROMPT_TEMPLATE.format(context=context, question=question)}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.0
    }

    try:
        resp = requests.post(GROQ_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception:
        return None  # triggers fallback
