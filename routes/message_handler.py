# routes/message_handler.py

from supabase import create_client
from utils.supabase_config import supabase_url, supabase_key
from utils.whatsapp import send_whatsapp_message
from datetime import datetime
import re

supabase = create_client(supabase_url, supabase_key)

async def handle_incoming_message(payload):
    print("📥 Incoming webhook payload:", payload)

    try:
        # For Ultramsg:
        user_number = payload["data"]["from"].split("@")[0]
        message = payload["data"]["body"].strip()
    except KeyError:
        print("❌ Payload format not recognized. Check provider.")
        return

    message_upper = message.upper()
    print(f"📱 From: {user_number}, Message: {message_upper}")

    # === START command
    if message_upper == "START":
        existing = supabase.table("users").select("*").eq("user_id", user_number).execute()
        print("🔎 Existing user check:", existing.data)

        if not existing.data:
            res = supabase.table("users").insert({
                "user_id": user_number,
                "joined_at": datetime.utcnow().isoformat(),
                "preferred_version": None,
                "reminder_time": None,
                "name": None
            }).execute()
            print("🆕 Insert result:", res)

            welcome = (
                f"👋 *Welcome to Daily Manna!*\n\n"
                "You're now registered for the Daily Bible Reading journey. 📖✨\n\n"
                "Reply with your *name* to begin."
            )
        else:
            welcome = (
                "👋 Welcome back to *Daily Manna*! 🙌\n"
                "Type READ to get today's reading.\n"
                "Type HELP to see all commands."
            )

        await send_whatsapp_message(user_number, welcome)
        return

    # === If user exists, continue onboarding
    user = supabase.table("users").select("*").eq("user_id", user_number).execute().data
    if not user:
        print("⚠️ Message received from unregistered user. Ask them to send START.")
        await send_whatsapp_message(user_number, "Please type *START* to begin.")
        return

    user = user[0]

    # === NAME
    if user.get("name") is None:
        supabase.table("users").update({"name": message}).eq("user_id", user_number).execute()
        await send_whatsapp_message(user_number, 
            f"✅ Thanks *{message}*! Now, choose your preferred Bible version:\n*KJV*, *NIV*, or *ESV*.")
        return

    # === Bible Version
    if user.get("preferred_version") is None:
        version = message_upper
        if version in ["KJV", "NIV", "ESV"]:
            supabase.table("users").update({"preferred_version": version}).eq("user_id", user_number).execute()
            await send_whatsapp_message(user_number, 
                f"📖 Awesome! You’ll be using the *{version}* version.\n\n⏰ What time should I send your daily reading?\nSend in *HH:MM AM/PM* or 24-hour format like *20:00*.")
        else:
            await send_whatsapp_message(user_number, "❌ Invalid version. Please reply with: *KJV*, *NIV*, or *ESV*")
        return

    # === Reminder Time
    if user.get("reminder_time") is None:
        time_input = message.replace(" ", "").upper()
        match_12hr = re.match(r"^(\d{1,2}):(\d{2})(AM|PM)$", time_input)
        match_24hr = re.match(r"^(\d{1,2}):(\d{2})$", time_input)

        if match_12hr:
            hr, minute, ampm = int(match_12hr[1]), int(match_12hr[2]), match_12hr[3]
            if ampm == "PM" and hr != 12:
                hr += 12
            elif ampm == "AM" and hr == 12:
                hr = 0
            reminder_time = f"{hr:02d}:{minute:02d}"
        elif match_24hr:
            hr, minute = int(match_24hr[1]), int(match_24hr[2])
            if hr > 23 or minute > 59:
                await send_whatsapp_message(user_number, "❌ Invalid time. Please send in HH:MM format like *06:30 AM* or *20:00*")
                return
            reminder_time = f"{hr:02d}:{minute:02d}"
        else:
            await send_whatsapp_message(user_number, "❌ Invalid time format. Please send in HH:MM format.")
            return

        supabase.table("users").update({"reminder_time": reminder_time}).eq("user_id", user_number).execute()
        await send_whatsapp_message(user_number, 
            f"✅ All set! You'll receive daily Bible readings at *{reminder_time}*.\n\nType *READ* anytime to get today's passage.")
        return

    # === Fallback
    await send_whatsapp_message(user_number, 
        "🙏 I'm not sure what you meant. Type *READ* for today’s Bible passage or *HELP* for commands.")
