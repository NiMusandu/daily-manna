# main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router
from routes.join import router as join_router
import schedule
import threading
import time
from utils.ultramsg import send_whatsapp_message
from fastapi.responses import HTMLResponse

app = FastAPI()

# Include routers AFTER app is defined
app.include_router(whatsapp_router, prefix="/webhook")
app.include_router(join_router)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Welcome to Daily Manna 📖</h1>
    <p>This is the backend API for our WhatsApp Bible reading agent.</p>
    <p>Visit <a href='https://wa.me/254722000001?text=START'>our WhatsApp bot</a> to begin.</p>
    """

# Optional daily reminder via internal scheduler (not used in Render background services)
def send_daily_reminder():
    message = "📖 *Daily Bible Reading Reminder*\nDon't forget to read today's passage.\nReply *READ* when done!"
    send_whatsapp_message("254721420119", message)

def run_scheduler():
    schedule.every().day.at("06:00").do(send_daily_reminder)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.on_event("startup")
async def startup_event():
    print("✅ Daily Manna backend is live.")
    # Uncomment if running the reminder scheduler from here
    # threading.Thread(target=run_scheduler, daemon=True).start()
sssss