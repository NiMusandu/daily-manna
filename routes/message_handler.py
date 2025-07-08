from dotenv import load_dotenv
load_dotenv()

# routes/message_handler.py
from supabase import create_client
from utils.supabase_config import supabase_url, supabase_key
from utils.whatsapp import send_whatsapp_message

supabase = create_client(supabase_url, supabase_key)

async def handle_incoming_message(data):
    message = data['message']['body'].strip().upper()
    phone = data['message']['from']

    if message == "START":
        # Check if user exists
        response = supabase.table("users").select("*").eq("phone", phone).execute()
        if not response.data:
            # Register new user
            supabase.table("users").insert({
                "phone": phone,
                "start_date": "now()",  # Or calculate current date
                "reminder_time": None,
                "bible_version": None,
                "name": None,
            }).execute()

        # Send onboarding message
        await send_whatsapp_message(phone, 
            "🙏 Welcome to *Daily Manna*! Let's get you started.\n\n💬 What's your name?")


from supabase import create_client
from datetime import datetime
import os

# Supabase setup
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

async def handle_incoming_message(payload):
    user_number = payload['data']['from'].split('@')[0]  # Extract phone number
    message = payload['data']['body'].strip().upper()  # Normalize message

    # === START Command ===
    if message == "START":
        # Check if user exists
        existing = supabase.table("users").select("user_id").eq("user_id", user_number).execute()

        if not existing.data:
            # Create new user
            supabase.table("users").insert({
                "user_id": user_number,
                "joined_at": datetime.utcnow().isoformat(),
                "preferred_version": "KJV",
                "reminder_time": None
            }).execute()

            welcome = (
                f"👋 *Welcome to Daily Manna!*\n\n"
                "You're now registered for the Daily Bible Reading journey. 📖✨\n\n"
                "📌 To get started:\n"
                "1. Choose your Bible version (e.g., KJV, NIV, ESV)\n"
                "2. Set a daily reminder time (e.g., 6:30AM)\n\n"
                "Reply with your preferred *Bible version* to continue."
            )
        else:
            welcome = (
                "👋 Welcome back!\nYou're already registered for Daily Manna.\n"
                "Reply READ to get today's reading or HELP for available commands."
            )

        from utils.whatsapp import send_whatsapp_message
        await send_whatsapp_message(user_number, welcome)
        return {"status": "onboarded"}

    # === Future Commands (READ, STATS, REFLECT, etc.) ===
    # Add your existing logic here...


# routes/message_handler.py (continued)

async def handle_incoming_message(data):
    message = data['message']['body'].strip()
    phone = data['message']['from']

    user_response = supabase.table("users").select("*").eq("phone", phone).execute()
    user = user_response.data[0] if user_response.data else None

    if message.upper() == "START":
        if not user:
            supabase.table("users").insert({
                "phone": phone,
                "start_date": "now()",  # optional
                "reminder_time": None,
                "bible_version": None,
                "name": None,
            }).execute()

        await send_whatsapp_message(phone, 
            "🙏 Welcome to *Daily Manna*! Let's get you started.\n\n💬 What's your name?")
        return

    # Check if user has no name => treat message as name
    if user and user["name"] is None:
        supabase.table("users").update({"name": message}).eq("phone", phone).execute()
        await send_whatsapp_message(phone,
            f"✅ Thanks {message}!\n📖 What version of the Bible would you like to use?\nOptions: *KJV*, *NIV*, *ESV*")
        return

