import time
import requests
import json
from retriever import retrieve_documents
from joblib import Memory

# Together AI API Details
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = "tgp_v1_9r_LzAQF2qOpKABJjDmZOc3ffFA9noiL4zGEtGG_UFg"

# Cache to Avoid Recomputing Same Queries
memory = Memory(location="cache", verbose=0)

HEADERS = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}


@memory.cache
def query_together_ai(prompt, temperature=0.7, max_tokens=500):
    """Queries Together AI's API with retry on failure."""
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    for attempt in range(3):  # Retry up to 3 times
        response = requests.post(TOGETHER_API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]

        print(f"⚠️ API Error {response.status_code}, Retrying ({attempt + 1}/3)...")
        time.sleep(2)  # Wait before retrying

    return "❌ AI response failed after multiple attempts."


def generate_response(query, k=10, temperature=0.7):
    """Retrieves context and generates a response using Together AI."""
    # Convert k to integer if it's a list
    if isinstance(k, list):
        k = k[0] if k else 10
    k = int(k)  # Ensure k is an integer

    # Handle specific user queries
    query_lower = query.lower().strip()

    # Greetings and self-introduction
    if query_lower in ["hi", "hello", "who are you","Namaste","Good morning"]:
        return "Namaste, I'm a RAG-based chatbot trained on KIIT University's data by Sajan Kumar Sah. You can ask me anything about KIIT University!"

    # Questions about the creator
    if any(phrase in query_lower for phrase in ["who built you", "who made you", "who trained you"]):
        return "I was built and trained by Sajan Kumar Sah."

    if any(phrase in query_lower for phrase in ["How are you"]):
        return "I am Good . Tell me what do you wnat to know about KIIT? "

    # General questions (fallback to normal response)
    if "?" in query_lower:  # Simple heuristic for general questions
        context = retrieve_documents(query, k)
        context_text = "\n\n".join(context)
        prompt = f"Context:\n{context_text}\n\nUser: {query}\nAI:"
        return query_together_ai(prompt, temperature=temperature)

    # Default behavior for other queries
    context = retrieve_documents(query, k)
    context_text = "\n\n".join(context)
    prompt = f"Context:\n{context_text}\n\nUser: {query}\nAI:"
    return query_together_ai(prompt, temperature=temperature)