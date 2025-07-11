# main.py

from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router

app = FastAPI()

# Include WhatsApp webhook route
app.include_router(whatsapp_router)

# Optional: health check route
@app.get("/")
def home():
    return {
        "message": "📖 Welcome to the Daily Manna WhatsApp API"
    }
