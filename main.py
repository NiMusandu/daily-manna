# main.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router
from routes.join import router as join_router
from fastapi.responses import HTMLResponse

app = FastAPI()

# Include routers after defining app
app.include_router(whatsapp_router, prefix="/webhook")
app.include_router(join_router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Welcome to Daily Manna 📖</h1>
    <p>This is the backend API for our WhatsApp Bible reading agent.</p>
    <p>Visit <a href='https://wa.me/254707626058?text=START'>our WhatsApp bot</a> to begin.</p>
    """

@app.on_event("startup")
async def startup_event():
    print("✅ Daily Manna backend is live.")
