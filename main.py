from fastapi import FastAPI
from routes import whatsapp
from routes.twilio_webhook import router as twilio_router

app = FastAPI(title="MyChatCV API")

# To include WhatsApp bot route
app.include_router(whatsapp.router, prefix="/api/whatsapp")
# To include the Twilio webhook route
app.include_router(twilio_router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to MyChatCV API"
    }