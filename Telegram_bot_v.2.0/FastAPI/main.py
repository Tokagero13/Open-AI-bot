from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from cryptography.fernet import Fernet

app = FastAPI(
    title="Telegram Bot creator"
)

@app.get("/")
async def root():
    return {"message": "Tomato"}

class BotParameters(BaseModel):
    user_id: int
    open_ai_api_key: str
    open_ai_assistant_id: str
    bot_token: str

@app.post("/create_bot")
async def create_bot(bot_params: BotParameters):
    return {'status': 200, 'data': 'Bot created successfully', 'bot_params': bot_params.dict()}

#launch localhost ///$ uvicorn main2:app --reload