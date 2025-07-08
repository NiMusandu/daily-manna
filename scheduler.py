from config import ULTRA_INSTANCE, ULTRA_TOKEN

import json
from datetime import datetime
from whatsapp import send_whatsapp_message
from apscheduler.schedulers.background import BackgroundScheduler

# Load reading plan
with open("reading_plan.json", "r", encoding="utf-8") as f:
    plan = json.load(f)

# Get today's Bible reading
def get_reading_for_day(day: int) -> str:
    if 1 <= day <= 365:
        item = plan[day - 1]
        return f"{item['old_testament']}; {item['new_testament']}; {item['psalm_or_gospel']}"
    return "John 1"

def generate_esv_link(ref: str) -> str:
    formatted = ref.replace("; ", ",").replace(" ", "+")
    return f"https://www.esv.org/{formatted}/"

# Actual send function
def send_daily_reading(to_number: str):
    day_of_year = datetime.now().timetuple().tm_yday
    reference = get_reading_for_day(day_of_year)
    link = generate_esv_link(reference)
    message = f"📖 *Day {day_of_year} Bible Reading*\n\n{reference}\n\n🔗 Read here: {link}\n\nReply *READ* once done."
    send_whatsapp_message(to_number, message)

# Optional scheduler start (only if you're auto-running daily)
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: send_daily_reading("254721420119"), 'cron', hour=6, minute=0)
    scheduler.start()
    print("✅ Daily Bible reading scheduler started (6:00 AM).")
