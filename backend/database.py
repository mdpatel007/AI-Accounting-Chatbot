import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
chat_collection = db["chat_history"]

def save_chat(user_id: str, user_message:str,bot_reply:str):
    chat_collection.insert_one({
        "user_id": user_id,
        "user_message": user_message,
        "bot_reply": bot_reply
    })

def get_chats_by_user(user_id: str, limit: int = 10):
    chats = chat_collection.find({"user_id": user_id}, {"_id": 0}).sort("_id", -1).limit(limit)
    return list(chats)

def clear_user_history(user_id: str):
    chat_collection.delete_many({"user_id": user_id})