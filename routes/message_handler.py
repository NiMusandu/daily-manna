# routes/message_handler.py

from fastapi.responses import JSONResponse
from supabase import create_client
from datetime import datetime
import os

from utils.whatsapp import send_whatsapp_message
from utils.reading_plan import get_reading_for_day

# Initialize Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

async def handle_incoming_message(payload: dict):
    data = payload.get("data", {})
    message_body = data.get("body", "").strip().upper()
    phone = data.get("from", "").replace("@c.us", "")
    pushname = data.get("pushname", "Friend")

    if message_body == "START":
        return await handle_start(phone, pushname)
    
    elif message_body == "READ":
        return await handle_read(phone)
    
    return JSONResponse(content={"message": f"Command '{message_body}' received."}, status_code=200)

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

    # Optional: prevent duplicate logging
    supabase.table("progress").insert({
        "phone": phone,
        "day": day_number,
        "date_read": today.isoformat()
    }).execute()

    await send_whatsapp_message(phone, reading)
    return JSONResponse(content={"message": "Reading sent."}, status_code=200)
