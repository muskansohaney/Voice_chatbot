# assistant_app.py
import os
import json
import uuid
import time
import numpy as np
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv
import redis
import requests

from sentence_transformers import SentenceTransformer


import whisper

# Load model once globally (small is faster)
whisper_model = whisper.load_model("base")

def transcribe_audio(file_path: str) -> str:
    """
    Convert uploaded audio into text using Whisper.
    """
    try:
        result = whisper_model.transcribe(file_path)
        text = result.get("text", "").strip()
        return text if text else "(Could not understand audio)"
    except Exception as e:
        return f"Error during transcription: {str(e)}"


# Load env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
MEMORY_RET_K = int(os.getenv("MEMORY_RET_K", "5"))

# Initialize redis
r = redis.from_url(REDIS_URL, decode_responses=True)

# Embedding model (free)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")  # small and fast


def embed_text(text: str) -> List[float]:
    vec = embed_model.encode(text, normalize_embeddings=True)
    return vec.tolist()


def store_memory(text: str, role: str = "user", metadata: Dict = None):
    key = f"memory:{str(uuid.uuid4())}"
    emb = embed_text(text)
    item = {
        "id": key,
        "text": text,
        "embedding": json.dumps(emb),
        "role": role,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": json.dumps(metadata or {}),
    }
    r.hset(key, mapping=item)
    r.sadd("memory_index", key)
    return key


def fetch_all_memories():
    keys = list(r.smembers("memory_index") or [])
    mems = []
    for k in keys:
        m = r.hgetall(k)
        if m:
            m["embedding"] = json.loads(m["embedding"])
            mems.append(m)
    return mems


def cosine_sim(a: np.ndarray, b: np.ndarray):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def retrieve_relevant_memories(query: str, k: int = None):
    k = k or MEMORY_RET_K
    q_emb = np.array(embed_text(query))
    mems = fetch_all_memories()
    scored = []
    for m in mems:
        score = cosine_sim(q_emb, np.array(m["embedding"]))
        scored.append((score, m))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [m for s, m in scored[:k]]
    return top


# Groq wrapper: minimal; adapt to groq API spec.
def call_groq(prompt: str, max_tokens: int = 512, temperature: float = 0.7):
    """
    Calls the Groq API using OpenAI-compatible /chat/completions endpoint.
    Returns the assistant's response text.
    """

    if not GROQ_API_KEY:
        raise RuntimeError("❌ Missing GROQ_API_KEY in .env")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "llama-3.1-8b-instant",  # or "llama-3.1-70b-versatile"
        "messages": [
            {"role": "system", "content": "You are a helpful AI voice and text assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # ✅ Extract message safely
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"].strip()

        # fallback for unexpected shapes
        return json.dumps(data)

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error: {e}")
        print("Response:", resp.text)
        return "⚠️ Error: Bad request to Groq API."

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return "⚠️ Network error. Please check your internet or Groq server."

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return "⚠️ Something went wrong inside call_groq()."
    
    
def compose_prompt(user_text: str, relevant_memories: List[Dict], system_instructions: str = None) -> str:
    system = system_instructions or (
        "You are a helpful assistant with access to user memory. Use the memory to provide personalized answers. "
        "Be concise but polite."
    )
    memory_block = ""
    if relevant_memories:
        memory_block += "User memory (most relevant first):\n"
        for m in relevant_memories:
            ts = m.get("timestamp", "")
            role = m.get("role", "user")
            text = m.get("text", "")
            memory_block += f"- [{role} | {ts}] {text}\n"
        memory_block += "\n"

    prompt = f"{system}\n\n{memory_block}\nUser: {user_text}\nAssistant:"
    return prompt


# High-level handle function
def handle_user_input(user_text: str, store_this_interaction: bool = True):
    # 1) Retrieve relevant memories
    rel = retrieve_relevant_memories(user_text, k=MEMORY_RET_K)

    # 2) Compose prompt
    prompt = compose_prompt(user_text, rel)

    # 3) Call Groq
    assistant_response = call_groq(prompt)

    # 4) Store memories: user utterance + assistant response
    if store_this_interaction:
        store_memory(user_text, role="user", metadata={"source": "conversation"})
        store_memory(assistant_response, role="assistant", metadata={"source": "conversation"})

    return assistant_response, rel


# Example quick test
if __name__ == "__main__":
    print("Type message (ctrl-C to exit)")
    while True:
        text = input("You: ")
        resp, rel = handle_user_input(text)
        print("Assistant:", resp)
        print("Top memories returned:", [m["text"][:80] for m in rel])
