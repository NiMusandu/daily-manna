from dotenv import load_dotenv
load_dotenv()

role = supabase.rpc("auth.role").execute()
print("🔐 Supabase role:", role.data)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from utils.scheduler import send_daily_reminders
from routes.whatsapp import router as whatsapp_router
from routes.join import router as join_router

app = FastAPI()

# ✅ No prefix here
app.include_router(whatsapp_router)
app.include_router(join_router)

# Scheduler for daily reminders
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    print("✅ Daily Manna backend is live.")
    scheduler.add_job(send_daily_reminders, CronTrigger(minute="0", second="0"))
    scheduler.start()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1>Welcome to Daily Manna 📖</h1>
    <p>This is the backend API for our WhatsApp Bible reading agent.</p>
    <p>Visit <a href='https://wa.me/254707626058?text=START'>our WhatsApp bot</a> to begin.</p>
    """
