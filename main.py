from fastapi import FastAPI
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from routes.whatsapp import router as whatsapp_router
from routes.join import router as join_router
from utils.scheduler import send_daily_reminders

load_dotenv()

app = FastAPI()

# ✅ Register routers (no prefix for /webhook)
app.include_router(whatsapp_router)
app.include_router(join_router)

# ✅ Scheduler setup
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    print("✅ Daily Manna backend is live.")
    scheduler.add_job(send_daily_reminders, CronTrigger(minute="0", second="0"))
    scheduler.start()

@app.get("/")
async def home():
    return {
        "message": "📖 Welcome to Daily Manna backend!",
        "whatsapp_bot": "https://wa.me/254707626058?text=START"
    }
