# main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from utils.supabase_client import supabase  # ✅ Single source of truth

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.scheduler import send_daily_reminders

from routes.whatsapp import router as whatsapp_router
from routes.join import router as join_router

# Optional: check the role on startup to verify service key
role_check = supabase.rpc("auth.role").execute()
print("🔐 Supabase role:", role_check.data)

app = FastAPI()

# Include routes
app.include_router(whatsapp_router, prefix="/webhook")
app.include_router(join_router)

# Scheduler setup
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    print("✅ Backend is live.")
    scheduler.add_job(send_daily_reminders, CronTrigger(minute="0", second="0"))
    scheduler.start()

@app.get("/")
def home():
    return {"message": "📖 Welcome to Daily Manna backend"}
