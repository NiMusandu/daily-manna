from config import ULTRA_INSTANCE, ULTRA_TOKEN

import asyncio
from datetime import datetime
from supabase import create_client
from utils.whatsapp import send_whatsapp_message
import os

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def send_daily_readings():
    while True:
        now = datetime.now().strftime("%H:%M")
        
        # Fetch users with active reminders
        result = supabase.table("users").select("*").eq("reminder_active", True).execute()
        users = result.data if result.data else []

        for user in users:
            if user.get("reminder_time") == now:
                phone = user["phone"]
                message = "📖 Good morning! Here's your Daily Manna reading for today. Type *READ* to view it."

                print(f"📤 Sending reminder to {phone} at {now}")
                send_whatsapp_message(phone, message)

        await asyncio.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    print("✅ Daily Reminder Scheduler started.")
    asyncio.run(send_daily_readings())
