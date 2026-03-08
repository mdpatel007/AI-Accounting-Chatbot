from fastapi import FastAPI
from backend.routes import router
from backend.database import save_chat, get_chats_by_user, clear_user_history

app = FastAPI()

app.include_router(router)