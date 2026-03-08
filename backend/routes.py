from fastapi import APIRouter, UploadFile, File
from backend.models import ChatRequest, ChatResponse, QueryRequest
from backend.groq_client import get_groq_response
from backend.database import save_chat, get_chats_by_user, clear_user_history
from backend.utils.file_parser import extract_text_from_txt
from backend.utils.chunking import fixed_size_chunking
from backend.utils.embeddings import embed_query
from backend.utils.vectorstore import add_chunks, query_chunks
from backend.utils import llm_helper

router = APIRouter()

@router.post("/process_file")
async def process_file(file: UploadFile = File(...)):
    text = ""

    if file.filename.endswith(".txt") or file.filename.endswith(".md"):
        text = extract_text_from_txt(file.file)
    else:
        return {"message": "Only TXT or Markdown files are supported."}

    if not text:
        return {"message": "No text extracted from file."}

    chunks = fixed_size_chunking(text, chunk_size=500, overlap=25) 

    # Store in Chroma
    metadatas = [{"source": file.filename, "chunk": i} for i in range(len(chunks))]
    add_chunks("documents", chunks, metadatas)

    return {
        "message": "File processed and stored in vector DB",
        "text_preview": text[:1000]  
    }

@router.post("/query_vector") 
def query_vector(req: QueryRequest):
    #conver into vec
    query_vec = embed_query(req.query)

    # Search in Chroma
    results = query_chunks(req.collection_name, query_vec, top_k=req.top_k)

    retrieved_texts = results.get("documents", [[]])[0]
    retrieved_scores = results.get("distances", [[]])[0]

    print("User Query:", req.query)
    print("Retrieved:", retrieved_texts)
    print("Scores:", retrieved_scores)

    # Threshold to decide relevance distance lower = better
    threshold = 0.95
    relevant_chunks = [
        {"text_snippet": txt, "score": float(score)}
        for txt, score in zip(retrieved_texts, retrieved_scores)
        if score < threshold
    ]

    # Remove duplicate chunks
    seen_texts = set()
    unique_chunks = []
    for c in relevant_chunks:
        if c["text_snippet"] not in seen_texts:
            unique_chunks.append(c)
            seen_texts.add(c["text_snippet"])

    relevant_chunks = unique_chunks

    # PDF related
    if relevant_chunks:
        bot_reply = llm_helper.answer_with_context(
            req.user_id, 
            req.query, 
            [c["text_snippet"] for c in relevant_chunks],
            include_history=True
        )
        save_chat(req.user_id, req.query, bot_reply)
        return {    
            "answer": bot_reply,
            "retrieved_chunks": relevant_chunks,
            "irrelevant_to_pdf": False
        }

    # outside pdf
    else:
        bot_reply = llm_helper.answer_without_context(req.user_id, req.query)
        save_chat(req.user_id, req.query, bot_reply)
        return {
            "answer": bot_reply,
            "retrieved_chunks": [],
            "irrelevant_to_pdf": True
        }

@router.post("/chat", response_model=ChatResponse)
def chat_completion(request: ChatRequest):
    bot_reply = get_groq_response(request.user_id, request.message)
    save_chat(request.user_id, request.message, bot_reply)
    return ChatResponse(reply=bot_reply)

@router.get("/history/{user_id}")
def fetch_history(user_id: str):
    return {"history": get_chats_by_user(user_id, limit=20)}

@router.delete("/history/{user_id}")
def clear_history(user_id: str):
    clear_user_history(user_id)
    return {"message": "User history cleared."}
