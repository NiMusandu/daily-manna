# ✅ Load .env before anything else
from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# ✅ Import routes and scheduler function
from routes.whatsapp import router as whatsapp_router
from utils.scheduler import send_daily_reminders

# ✅ Check if required env vars are present
ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

if not ULTRAMSG_INSTANCE_ID or not ULTRAMSG_TOKEN:
    raise EnvironmentError("❌ ULTRAMSG_INSTANCE_ID or ULTRAMSG_TOKEN not set in .env")

# ✅ FastAPI app init
app = FastAPI()

# ✅ Include router correctly
app.include_router(whatsapp_router)

# ✅ Start the scheduler on boot
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    print("✅ Daily Manna backend is live.")
    scheduler.add_job(send_daily_reminders, CronTrigger(minute="0", second="0"))
    scheduler.start()

# ✅ Homepage route
@app.get("/", response_class=HTMLResponse)
async def home():
    return {
        "message": "✅ Daily Manna backend is running."
    }
