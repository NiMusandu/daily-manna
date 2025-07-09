# main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.scheduler import send_daily_reminders

# Route imports
from routes.whatsapp import router as whatsapp_router
from routes.join import router as join_router

# Initialize FastAPI app
app = FastAPI()

# Register routers
app.include_router(whatsapp_router, prefix="/webhook")
app.include_router(join_router)

# Initialize scheduler
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    print("✅ Daily Manna backend is live.")
    scheduler.add_job(send_daily_reminders, CronTrigger(minute="0", second="0"))  # runs hourly at XX:00:00
    scheduler.start()

# Homepage
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1>Welcome to Daily Manna 📖</h1>
    <p>This is the backend API for our WhatsApp Bible reading agent.</p>
    <p>Visit <a href='https://wa.me/254707626058?text=START'>our WhatsApp bot</a> to begin.</p>
    """

# Optional: basic webhook echo (not needed if routed properly)
@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        print("📥 Incoming Webhook Payload:", payload)
        return JSONResponse(content={"status": "received"}, status_code=200)
    except Exception as e:
        print("❌ Error handling webhook:", str(e))
        return JSONResponse(content={"error": "Invalid payload"}, status_code=400)
