from dotenv import load_dotenv
load_dotenv()

from routes.whatsapp import router as whatsapp_router

app.include_router(whatsapp_router, prefix="/webhook")


# main.py
from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router

app = FastAPI()

app.include_router(whatsapp_router)

@app.get("/")
def root():
    return {"message": "Daily Manna WhatsApp Bot is live."}


from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router
import schedule
import threading
import time
from utils.ultramsg import send_whatsapp_message  # Make sure this exists
from utils.scheduler import start_scheduler  # Optional if separate scheduler module

app = FastAPI()
app.include_router(whatsapp_router)

# Sample reminder job
def send_daily_reminder():
    message = "📖 *Daily Bible Reading Reminder*\nDon't forget to read today's passage.\nReply *READ* when done!"
    send_whatsapp_message("254721420119", message)  # Replace with dynamic logic later

# Start scheduler thread
def run_scheduler():
    schedule.every().day.at("06:00").do(send_daily_reminder)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.on_event("startup")
async def startup_event():
    print("✅ Daily Bible reading scheduler started (6:00 AM).")
    threading.Thread(target=run_scheduler, daemon=True).start()

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Welcome to Daily Manna 📖</h1>
    <p>This is the backend API for our WhatsApp Bible reading agent.</p>
    <p>Visit <a href='https://wa.me/254721420119?text=START'>our WhatsApp bot</a> to begin.</p>
    """

from routes.join import router as join_router
app.include_router(join_router)
