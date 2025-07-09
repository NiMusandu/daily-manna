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
    message_body = data.get("body", "").strip()
    phone = data.get("from", "").replace("@c.us", "")
    pushname = data.get("pushname", "Friend")

    upper_body = message_body.upper()

    if upper_body == "START":
        return await handle_start(phone, pushname)
    
    elif upper_body == "READ":
        return await handle_read(phone)
    
    elif upper_body in ["STAT", "STATS"]:
        return await handle_stats(phone)

    elif upper_body.startswith("REMIND"):
        return await handle_remind(phone, message_body)

    elif upper_body == "STOP REMINDER":
        return await handle_stop_reminder(phone)

    elif upper_body.startswith("REFLECT"):
        return await handle_reflect(phone, message_body)

    elif upper_body == "MY REFLECTIONS":
        return await handle_my_reflections(phone)

    # Fallback: unknown command
    await send_whatsapp_message(phone, "🤖 Unknown command. Try *START*, *READ*, *REFLECT <msg>*, *MY REFLECTIONS*, *REMIND HH:MM*, *STATS* or *HELP*.")
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
    return JSONResponse(content={"message": "Stats sent"}, status_code=200)

# ⏰ REMIND command
async def handle_remind(phone: str, message: str):
    match = re.search(r"REMIND\s+(\d{1,2}):(\d{2})", message.upper())
    if not match:
        await send_whatsapp_message(phone,
            "⏰ Please use the correct format:\n\n*REMIND HH:MM*\nFor example:\nREMIND 07:30"
        )
        return JSONResponse(content={"message": "Invalid REMIND format"}, status_code=200)

    hour, minute = match.groups()
    hour = hour.zfill(2)  # pad single-digit hour
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

# ✍️ REFLECT command
async def handle_reflect(phone: str, message: str):
    reflection = message[7:].strip()
    if not reflection:
        await send_whatsapp_message(phone, "✍️ Please type your reflection after the word REFLECT.\nExample:\nREFLECT God reminded me that...")
        return JSONResponse(content={"message": "Empty reflection"}, status_code=200)

    # Get day number
    user = supabase.table("users").select("start_date").eq("phone", phone).execute()
    if not user.data:
        await send_whatsapp_message(phone, "⚠️ You're not registered. Send *START* first.")
        return JSONResponse(content={"error": "User not registered"}, status_code=400)

    start_date = datetime.fromisoformat(user.data[0]["start_date"])
    today = datetime.utcnow()
    day_number = (today.date() - start_date.date()).days + 1

    supabase.table("reflections").insert({
        "phone": phone,
        "message": reflection,
        "day_number": day_number,
        "timestamp": today.isoformat()
    }).execute()

    await send_whatsapp_message(phone, "✅ Reflection saved! You can view past ones using *MY REFLECTIONS*.")
    return JSONResponse(content={"message": "Reflection saved"}, status_code=200)

# 📚 MY REFLECTIONS command
async def handle_my_reflections(phone: str):
    reflections = supabase.table("reflections").select("*").eq("phone", phone).order("timestamp", desc=True).limit(5).execute()

    if not reflections.data:
        await send_whatsapp_message(phone, "📝 You haven’t written any reflections yet. Try:\n*REFLECT I felt comforted by today’s verse.*")
        return JSONResponse(content={"message": "No reflections found"}, status_code=200)

    message_lines = ["📝 *Your Last 5 Reflections:*"]
    for r in reflections.data:
        date = r["timestamp"].split("T")[0]
        snippet = r["message"][:80] + "..." if len(r["message"]) > 80 else r["message"]
        message_lines.append(f"📅 Day {r.get('day_number', '?')} ({date}):\n_{snippet}_\n")

    await send_whatsapp_message(phone, "\n".join(message_lines))
    return JSONResponse(content={"message": "Reflections sent"}, status_code=200)
