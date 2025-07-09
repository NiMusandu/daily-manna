# routes/message_handler.py

from fastapi.responses import JSONResponse
from supabase import create_client
from datetime import datetime
import os
import re

from utils.whatsapp import send_whatsapp_message
from utils.reading_plan import get_reading_for_day

# Initialize Supabase client
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


# 🚀 Main message dispatcher
async def handle_incoming_message(payload: dict):
    data = payload.get("data", {})
    message_body = data.get("body", "").strip().upper()
    phone = data.get("from", "").replace("@c.us", "")
    pushname = data.get("pushname", "Friend")

    if message_body == "START":
        return await handle_start(phone, pushname)
    
    elif message_body == "READ":
        return await handle_read(phone)
    
    elif message_body in ["STAT", "STATS"]:
        return await handle_stats(phone)

    elif message_body.startswith("REMIND"):
        return await handle_remind(phone, message_body)

    elif message_body in ["STOP REMINDER", "STOPREMINDER"]:
        return await handle_stop_reminder(phone)

    # Fallback: unknown command
    await send_whatsapp_message(phone, "🤖 Unknown command. Try *START*, *READ*, *REMIND HH:MM*, *STATS* or *HELP*.")
    return JSONResponse(content={"message": f"Unknown command '{message_body}'"}, status_code=200)


# 🧩 START command
async def handle_start(phone: str, name: str):
    existing = supabase.table("users").select("id").eq("phone", phone).execute()
    if existing.data:
        await send_whatsapp_message(phone, "📖 You're already registered. Type *READ* to continue.")
    else:
        supabase.table("users").insert({
            "phone": phone,
            "name": name,
            "start_date": datetime.utcnow().isoformat()
        }).execute()

        welcome_msg = (
            f"👋 Hello {name}!\n\n"
            "Welcome to *Daily Manna* 📖.\n"
            "You’ll receive a Bible passage every day.\n\n"
            "Type *READ* to get your first reading.\n"
            "Type *HELP* to see available commands."
        )
        await send_whatsapp_message(phone, welcome_msg)

    return JSONResponse(content={"message": "START command handled."}, status_code=200)


# 📖 READ command
async def handle_read(phone: str):
    result = supabase.table("users").select("start_date").eq("phone", phone).execute()
    if not result.data:
        await send_whatsapp_message(phone, "⚠️ You're not registered. Send *START* first.")
        return JSONResponse(content={"error": "User not registered"}, status_code=400)

    start_date_str = result.data[0]["start_date"]
    start_date = datetime.fromisoformat(start_date_str)
    today = datetime.utcnow()
    day_number = (today.date() - start_date.date()).days + 1

    reading = get_reading_for_day(day_number)

    supabase.table("progress").insert({
        "phone": phone,
        "day": day_number,
        "date_read": today.isoformat()
    }).execute()

    await send_whatsapp_message(phone, reading)
    return JSONResponse(content={"message": "Reading sent."}, status_code=200)


# 📊 STATS command
async def handle_stats(phone: str):
    result = supabase.table("progress").select("*").eq("phone", phone).execute()

    if not result.data:
        await send_whatsapp_message(phone, "😢 No reading history found. Type *READ* to start.")
        return JSONResponse(content={"message": "No stats"}, status_code=200)

    total_days = len(result.data)
    percent = round((total_days / 365) * 100, 1)

    message = (
        f"📊 *Your Daily Manna Stats*\n\n"
        f"✅ Days Read: *{total_days}*\n"
        f"🎯 Progress: *{percent}%* complete\n"
        f"🏅 Keep going! You're doing great."
    )

    await send_whatsapp_message(phone, message)
    return JSONResponse(content={"message": "Stats sent."}, status_code=200)


# ⏰ REMIND command
async def handle_remind(phone: str, message: str):
    # Match "REMIND HH:MM" exactly
    match = re.search(r"REMIND\s+(\d{1,2}):(\d{2})", message.upper())
        hour, minute = match.groups()
	time_str = f"{int(hour):02d}:{minute}"
    if not match:
        await send_whatsapp_message(phone,
            "⏰ Please use the correct format:\n\n*REMIND HH:MM*\nFor example:\nREMIND 07:30"
        )
        return JSONResponse(content={"message": "Invalid REMIND format"}, status_code=200)

    hour, minute = match.groups()
    time_str = f"{hour}:{minute}"

    supabase.table("users").update({"reminder_time": time_str}).eq("phone", phone).execute()

    await send_whatsapp_message(
        phone,
        f"✅ Great! We'll remind you every day at *{time_str} UTC*.\n\nTo stop, type *STOP REMINDER*."
    )
    return JSONResponse(content={"message": "Reminder time set"}, status_code=200)


# 🛑 STOP REMINDER
async def handle_stop_reminder(phone: str):
    supabase.table("users").update({"reminder_time": None}).eq("phone", phone).execute()
    await send_whatsapp_message(phone, "🚫 Reminder stopped. You won’t receive daily alerts.")
    return JSONResponse(content={"message": "Reminder stopped"}, status_code=200)
