from fastapi import FastAPI
from app.api import whatsapp

app = FastAPI(title="MyChatCV API")

# To include WhatsApp bot route
# app.include_router(whatsapp.router, prefix="/api/whatsapp")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to MyChatCV API"
    }