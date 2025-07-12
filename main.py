# main.py

from fastapi import FastAPI
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ App initialization
app = FastAPI()

# ✅ Import and include your routes
from routes.whatsapp import router as whatsapp_router
app.include_router(whatsapp_router)
# (Optional: other routers can go here)

@app.get("/")
async def home():
    return {"message": "✅ Daily Manna backend is running."}
