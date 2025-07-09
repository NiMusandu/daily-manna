from dotenv import load_dotenv
load_dotenv()

# routes/message_handler.py
from datetime import datetime
import re
from supabase import create_client
from utils.supabase_config import supabase_url, supabase_key
from utils.whatsapp import send_whatsapp_message

supabase = create_client(supabase_url, supabase_key)

async def handle_incoming_message(data):
    message = data['message']['body'].strip()
    phone = data['message']['from']

    user_response = supabase.table("users").select("*").eq("phone", phone).execute()
    user = user_response.data[0] if user_response.data else None

    # === START ===
    if message.upper() == "START":
        if not user:
            supabase.table("users").insert({
                "phone": phone,
                "start_date": datetime.utcnow().isoformat(),
                "reminder_time": None,
                "bible_version": None,
                "name": None,
            }).execute()

        await send_whatsapp_message(phone, 
            "🙏 Welcome to *Daily Manna*! Let's get you started.\n\n💬 What's your name?")
        return

    # === NAME ===
    if user and user["name"] is None:
        supabase.table("users").update({"name": message}).eq("phone", phone).execute()
        await send_whatsapp_message(phone,
            f"✅ Thanks {message}!\n📖 What version of the Bible would you like to use?\nOptions: *KJV*, *NIV*, *ESV*")
        return

    # === BIBLE VERSION ===
    if user and user["bible_version"] is None:
        version = message.upper()
        if version in ["KJV", "NIV", "ESV"]:
            supabase.table("users").update({"bible_version": version}).eq("phone", phone).execute()
            await send_whatsapp_message(phone,
                f"📖 Great! You'll be using the *{version}* Bible.\n\n⏰ What time should I send your daily reading?\nFormat: *06:30 AM* or *20:00*")
        else:
            await send_whatsapp_message(phone,
                "❌ Invalid Bible version. Please choose one of: *KJV*, *NIV*, *ESV*")
        return

    # === REMINDER TIME ===
    if user and user["reminder_time"] is None:
        time_input = message.strip().upper().replace(" ", "")
        match_12hr = re.match(r"^(\d{1,2}):(\d{2})(AM|PM)$", time_input)
        match_24hr = re.match(r"^(\d{1,2}):(\d{2})$", time_input)

        if match_12hr:
            hr, minute, ampm = int(match_12hr[1]), int(match_12hr[2]), match_12hr[3]
            if ampm == "PM" and hr != 12: hr += 12
            if ampm == "AM" and hr == 12: hr = 0
            reminder_time = f"{hr:02d}:{minute:02d}"
        elif match_24hr:
            hr, minute = int(match_24hr[1]), int(match_24hr[2])
            if hr > 23 or minute > 59:
                await send_whatsapp_message(phone, "❌ Invalid time. Please use format like *06:30 AM* or *20:00*")
                return
            reminder_time = f"{hr:02d}:{minute:02d}"
        else:
            await send_whatsapp_message(phone, "❌ Invalid time. Please use format like *06:30 AM* or *20:00*")
            return

        supabase.table("users").update({"reminder_time": reminder_time}).eq("phone", phone).execute()
        await send_whatsapp_message(phone,
            f"✅ Awesome! You’ll get your daily reading at *{reminder_time}*.\n\nType *READ* to get today’s passage anytime.")
        return

    # === Unknown Input ===
    await send_whatsapp_message(phone,
        "🤖 Sorry, I didn't understand that. Type *READ* to get today's passage or *HELP* for a list of commands.")
