# main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.scheduler import send_daily_reminders
from routes.whatsapp import router as whatsapp_router
from routes.join import router as join_router  # Optional if you use a separate /join route

load_dotenv()  # ✅ Load environment variables

app = FastAPI()

# ✅ Mount routers
app.include_router(whatsapp_router, prefix="/webhook")  # This will respond at POST /webhook
app.include_router(join_router)  # Optional if using another route like /join

# ✅ Daily reminder scheduler
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    print("✅ Daily Manna backend is live.")
    scheduler.add_job(send_daily_reminders, CronTrigger(minute="0", second="0"))  # runs hourly at XX:00:00
    scheduler.start()

# ✅ Homepage health check
@app.get("/", response_class=JSONResponse)
async def home():
    return {"message": "✅ Daily Manna backend is running."}
