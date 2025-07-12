# utils/scheduler.py

from datetime import datetime
from utils.supabase_client import supabase
from utils.ultramsg import send_whatsapp_message

async def send_daily_reminders():
    current_time = datetime.utcnow().strftime("%H:%M")
    print(f"🕒 Checking reminders for {current_time} UTC...")

    try:
        users = supabase.table("users") \
            .select("user_id", "name", "reminder_time", "reminder_active") \
            .eq("reminder_time", current_time) \
            .eq("reminder_active", True) \
            .execute()

        for user in users.data:
            user_id = user["user_id"]
            name = user.get("name", "Friend")
            message = f"📖 Good morning {name}! Don’t forget to read your Daily Manna today."

            await send_whatsapp_message(user_id, message)

        print(f"✅ Reminders sent to {len(users.data)} users.")
    except Exception as e:
        print("❌ Error sending reminders:", str(e))
