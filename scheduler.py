from dotenv import load_dotenv
load_dotenv()

from config import ULTRA_INSTANCE, ULTRA_TOKEN
import asyncio
import datetime
from utils.whatsapp import send_whatsapp_message
from utils.bible import get_daily_reading  # Assuming this returns today's reading
from supabase import create_client
import os

# Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

async def send_daily_readings():
    print("✅ Daily Reminder Scheduler started.")
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        response = supabase.table("users").select("*").eq("reminder_time", current_time).execute()
        users_to_notify = response.data or []

        for user in users_to_notify:
            user_id = user["user_id"]
            bible_version = user.get("bible_version", "KJV")
            reading = get_daily_reading(bible_version)

            await send_whatsapp_message(user_id, f"📖 *Your Daily Manna ({bible_version})*\n\n{reading}")
            print(f"✅ Sent reading to {user_id} at {current_time}")

        await asyncio.sleep(60)

# ✅ Required entry point
if __name__ == "__main__":
    asyncio.run(send_daily_readings())
