import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from app.agent import chat

load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    messages: list

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    response = chat(request.messages)
    return {"response": response}
