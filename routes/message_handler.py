from fastapi.responses import JSONResponse
from supabase import create_client
import os
from datetime import datetime
from utils.whatsapp import send_whatsapp_message

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

async def handle_incoming_message(payload: dict):
    data = payload.get("data", {})
    message_body = data.get("body", "").strip().upper()
    phone = data.get("from", "").replace("@c.us", "")
    pushname = data.get("pushname", "Friend")

    if message_body == "START":
        return await handle_start(phone, pushname)

    # Future command routing (READ, HELP, REFLECT, etc.)
    return JSONResponse(content={"message": f"Command '{message_body}' received."}, status_code=200)

async def handle_start(phone: str, name: str):
    # Check if user exists
    existing = supabase.table("users").select("id").eq("phone", phone).execute()
    if existing.data:
        await send_whatsapp_message(phone, "📖 You're already registered. Type *READ* to continue.")
    else:
        # Create user
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
