from backend.groq_client import get_groq_response
from backend.database import get_chats_by_user  

def answer_with_context(user_id: str, query: str, chunks: list[str], include_history: bool = True) -> str:
    context = "\n\n".join(chunks)

    # Fetch last 10 msg
    context_history = ""
    if include_history:
        history = get_chats_by_user(user_id, limit=10)
        if history:
            context_history = "\n".join([f"User: {c['user_message']}\nBot: {c['bot_reply']}" for c in history])
    
    # prompt
    if context_history:
        prompt = f"""
        You are an AI accounting assistant for Hellobooks.

        Answer the user's accounting question using the provided context.

        If the answer is not in the context, say:
        "I could not find this information in the accounting knowledge base."

        Context:
        {context}

        Question:
        {query}

        Conversation history:
        {context_history}

        Answer: """
    else:
        prompt = f"""User Question: {query}
        Relevant PDF Chunks:
        {context}
        Answer in simple and clear human way."""
    return get_groq_response(user_id, prompt)

def answer_without_context(user_id: str, query: str) -> str:
    return get_groq_response(user_id, query)
    # return "This information is not available in the document."
