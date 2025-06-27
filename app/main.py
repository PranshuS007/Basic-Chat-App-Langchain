import dotenv, os
dotenv.load_dotenv()

from fastapi import FastAPI, Request
from pydantic import BaseModel
from chat_engine import conversation, memory

app = FastAPI()

class ChatInput(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Chatbot is live!"}

@app.post("/chat")
def chat(input: ChatInput):
    response = conversation.run(input=input.query)
    return {"response": response}



