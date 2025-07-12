from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from routes.whatsapp import router as whatsapp_router
from routes.join import router as join_router
from utils.scheduler import send_daily_reminders

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(whatsapp_router, prefix="/webhook")
app.include_router(join_router)

# Initialize and configure the scheduler
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    print("✅ Daily Manna backend is live.")
    # Run send_daily_reminders every hour at minute 0 and second 0
    scheduler.add_job(send_daily_reminders, CronTrigger(minute="0", second="0"))
    scheduler.start()

# ✅ Root route using JSONResponse
@app.get("/", response_class=JSONResponse)
def home():
    return {"message": "✅ Daily Manna backend is running."}
