# utils/scheduler.py

from supabase import create_client
from datetime import datetime
import os

from utils.whatsapp import send_whatsapp_message
from utils.reading_plan import get_reading_for_day

# Initialize Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# 🔁 Send reminders to users at their preferred time
async def send_daily_reminders():
    now = datetime.utcnow()
    current_time = now.strftime("%H:%M")  # Format: HH:MM (e.g. "06:00")

    print(f"🕒 Checking reminders for {current_time} UTC...")

    # Query users who requested reminders at this time
    response = supabase.table("users").select("phone", "start_date").eq("reminder_time", current_time).execute()

    if not response.data:
        print("📭 No users scheduled for this time.")
        return

    for user in response.data:
        phone = user["phone"]
        start_date = datetime.fromisoformat(user["start_date"])
        day_number = (now.date() - start_date.date()).days + 1

        reading = get_reading_for_day(day_number)
        message = (
            "⏰ *Your Daily Manna Reminder!*\n\n"
            "Don't forget to read today's passage:\n\n"
            f"{reading}"
        )

        await send_whatsapp_message(phone, message)
        print(f"✅ Reminder sent to {phone}")
