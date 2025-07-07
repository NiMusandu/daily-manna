# utils/scheduler.py
import schedule
import time
import threading
from utils.supabase_client import supabase
from utils.ultramsg import send_whatsapp_message
from bible_readings import BIBLE_READING_PLAN  # Assume this is your 365-day plan

def send_daily_readings():
    print("📅 Running daily reading scheduler...")
    users = supabase.table("users").select("*").execute().data

    for user in users:
        user_id = user["id"]
        phone = user["phone"]
        day = user.get("days_completed", 0)

        if day < len(BIBLE_READING_PLAN):
            passage = BIBLE_READING_PLAN[day]
            message = f"📖 *Day {day + 1} Bible Reading*\n{passage}"
            send_whatsapp_message(phone, message)

            # update user progress
            supabase.table("users").update({"days_completed": day + 1}).eq("id", user_id).execute()
            print(f"✅ Sent to {phone}: {passage}")
        else:
            print(f"🎉 {phone} has completed all 365 readings!")

def start_scheduler():
    schedule.every().day.at("06:00").do(send_daily_readings)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)

    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    print("✅ Daily Bible reading scheduler started (6:00 AM).")
