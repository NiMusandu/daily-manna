import re
from datetime import datetime
from utils.supabase_client import supabase
from utils.ultramsg import send_whatsapp_message


def normalize_user_id(raw_id: str) -> str:
    return raw_id if "@c.us" in raw_id else raw_id + "@c.us"


async def register_user(user_id: str, name: str):
    print(f"📌 Registering user: {user_id}")
    existing = supabase.table("users").select("*").eq("user_id", user_id).execute()

    if existing.data:
        print("👤 Already registered")
        return {"message": f"👋 Welcome back, {name}!"}

    supabase.table("users").insert({
        "user_id": user_id,
        "phone": user_id.split("@")[0],  # ✅ ensure "phone" is not null
        "name": name,
        "created_at": datetime.utcnow().isoformat(),
        "reminder_time": "07:00",
        "reminder_active": True
    }).execute()

    print("✅ Registered successfully")
    return {"message": f"✅ You're now registered, {name}!"}


async def handle_incoming_message(payload):
    data = payload.get("data", {})
    user_id = normalize_user_id(data.get("author") or data.get("from"))
    message = data.get("body", "").strip()
    command = message.upper()
    name = data.get("pushname", "Friend")

    print(f"📨 {command} from {user_id}")

    if command == "START":
        response = await register_user(user_id, name)
        return await send_whatsapp_message(user_id, response["message"])

    return await send_whatsapp_message(user_id, "❓ I didn’t understand that. Send START.")
