# main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse

# Route imports (assumes you have routes/whatsapp.py and routes/join.py)
from routes.whatsapp import router as whatsapp_router
from routes.join import router as join_router

# Initialize the FastAPI app
app = FastAPI()

# ✅ Register routes after app is defined
app.include_router(whatsapp_router, prefix="/webhook")
app.include_router(join_router)

# Homepage
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1>Welcome to Daily Manna 📖</h1>
    <p>This is the backend API for our WhatsApp Bible reading agent.</p>
    <p>Visit <a href='https://wa.me/254707626058?text=START'>our WhatsApp bot</a> to begin.</p>
    """

# Optional fallback or debug endpoint
@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        print("📥 Incoming Webhook Payload:", payload)

        # You can remove this if your logic is fully handled in routes/whatsapp.py
        return JSONResponse(content={"status": "received"}, status_code=200)

    except Exception as e:
        print("❌ Error handling webhook:", str(e))
        return JSONResponse(content={"error": "Invalid payload"}, status_code=400)

# Startup event hook
@app.on_event("startup")
async def startup_event():
    print("✅ Daily Manna backend is live.")

