from typing import Union

from fastapi import FastAPI, HTTPException
from typing import List

import httpx
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
import asyncio
from cryptography.fernet import Fernet

app = FastAPI(
    title="Telegram Bot creator"
)

class BotParameters(BaseModel):
    user_id: int
    open_ai_api_key: str
    open_ai_assistant_id: str
    bot_token: str

# In-memory store for BotParameters instances
bot_parameters_store: List[BotParameters] = []

@app.post("/create_bot")
async def create_bot(bot_params: BotParameters):
    # Save the BotParameters instance to the in-memory store
    bot_parameters_store.append(bot_params)
    return {'status': 200, 'data': 'Bot created successfully', 'bot_params': bot_params.dict()}

@app.get("/get_bot/{user_id}")
async def get_bot(user_id: int):
    # Search for the BotParameters instance by user_id
    for bot in bot_parameters_store:
        if bot.user_id == user_id:
            return {'status': 200, 'data': bot.dict()}
    raise HTTPException(status_code=404, detail="Bot not found")

@app.get("/telegram_bot")
async def listen_message_telgram(request_list):
    last_update_id = None 

    async with httpx.AsyncClient() as client:
        while True:
            print("Waiting for message...")
            await asyncio.sleep(1)
            url = "https://api.telegram.org/bot{}/getUpdates".format(bot_token)
            params = {'offset': last_update_id} if last_update_id else {}
            response = await client.get(url, params=params)
            updates = await response.json()

            if 'result' in updates and updates['result']:
                for update in updates['result']:
                    last_update_id = update['update_id'] + 1
                    input = {
                        "user_message": update
                        }
                    print(f"\nGET USER MESSAGE INPUT: {json.dumps(input, indent=4)}")
                    request_list.append(input)
                    print("Collected in the |request_list|")
                    await asyncio.sleep(1)  # Simulate delay in collecting messages
            else:
                print("No new updates.")



#launch localhost ///$ uvicorn main2:app --reload