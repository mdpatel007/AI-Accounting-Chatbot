import requests
import os
from dotenv import load_dotenv
from backend.database import get_chats_by_user

load_dotenv()

GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a helpful assistant. Always consider system instructions, "
        "user queries, and prior conversation history before responding."
    ),
}

def get_groq_response(user_id: str, user_message: str, model: str = "openai/gpt-oss-20b"):
    if not GROQ_API_URL:
        raise ValueError("GROQ_API_URL is not set in environment variables.")
    
    # history = get_chats_by_user(user_id, limit=10)
    history = []

    # Convert history into OpenAI-style messages
    messages = [SYSTEM_MESSAGE]
    for chat in history:
        messages.append({"role": "user", "content": chat["user_message"]})
        messages.append({"role": "assistant", "content": chat["bot_reply"]})

    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    return result["choices"][0]["message"]["content"]
