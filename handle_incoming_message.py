import re
from datetime import datetime
import httpx
from utils.supabase_client import supabase
from utils.ultramsg_config import ULTRAMSG_INSTANCE_ID, ULTRAMSG_TOKEN  # Assuming you're importing tokens here

def normalize_user_id(raw_id: str) -> str:
    return raw_id if "@c.us" in raw_id else raw_id + "@c.us"

async def send_whatsapp_message(to_number: str, message: str):
    print("📤 Sending to:", to_number)
    print("💬 Message:", message)

    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": to_number,
        "body": message
    }

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, data=payload)
            print("📬 Ultramsg response:", res.text)
        except Exception as e:
            print("❌ WhatsApp send error:", str(e))

async def register_user(user_id: str, name: str):
    print("📌 Registering user:", user_id)
    existing = supabase.table("users").select("*").eq("user_id", user_id).execute()

    if existing.data:
        print("👤 Already registered")
        return {"message": f"👋 Welcome back, {name}!"}

    supabase.table("users").insert({
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat(),
        "reminder_time": "07:00",
        "reminder_active": True
    }).execute()

    print("✅ Registered successfully")
    return {"message": f"✅ You're now registered, {name}!"}

async def handle_incoming_message(payload):
    data = payload.get("data", {})
    raw_id = data.get("author") or data.get("from")
    user_id = normalize_user_id(raw_id)
    message = data.get("body", "").strip()
    command = message.upper()
    name = data.get("pushname", "Friend")

    print(f"📨 {command} from {user_id}")

    if command == "START":
        response = await register_user(user_id, name)
        return await send_whatsapp_message(user_id, response["message"])

    elif command.startswith("READ"):
        supabase.table("progress").upsert({
            "user_id": user_id,
            "days_completed": 1
        }).execute()
        return await send_whatsapp_message(user_id, "✅ Your Bible reading progress has been recorded. Keep going!")

    elif command.startswith("REFLECT"):
        reflection_text = message[7:].strip()
        supabase.table("reflections").insert({
            "user_id": user_id,
            "reflection": reflection_text
        }).execute()
        return await send_whatsapp_message(user_id, "🙏 Reflection saved. May God bless your meditation.")

    elif command == "STATS":
        response = supabase.table("progress").select("*").eq("user_id", user_id).execute()
        if response.data:
            days = response.data[0].get("days_completed", 0)
            return await send_whatsapp_message(user_id, f"📊 You’ve completed {days} day(s) of Bible reading. Keep going!")
        else:
            return await send_whatsapp_message(user_id, "📊 No progress found. Start by sending READ after reading your Bible.")

    elif command.startswith("REMIND"):
        match = re.search(r"REMIND\s+(\d{1,2}):(\d{2})", message)
        if match:
            hour, minute = match.groups()
            reminder_time = f"{int(hour):02d}:{minute}"
            supabase.table("users").update({
                "reminder_time": reminder_time,
                "reminder_active": True
            }).eq("user_id", user_id).execute()
            return await send_whatsapp_message(user_id, f"✅ Reminder set for *{reminder_time}* daily!")
        else:
            return await send_whatsapp_message(user_id, "❌ Invalid format. Use: REMIND 6:30")

    elif command == "STOP REMINDER":
        supabase.table("users").update({
            "reminder_active": False
        }).eq("user_id", user_id).execute()
        return await send_whatsapp_message(user_id, "🛑 Daily reminders turned *off*.")

    supported_versions = ["KJV", "NIV", "ESV"]
    if command in supported_versions:
        supabase.table("users").update({
            "preferred_version": command
        }).eq("user_id", user_id).execute()
        return await send_whatsapp_message(user_id, f"✅ Bible version set to *{command}*.")

    time_pattern = re.compile(r"^([0-1]?[0-9]|2[0-3]):([0-5][0-9])\s?(AM|PM)?$", re.IGNORECASE)
    match = time_pattern.match(message)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        meridian = match.group(3)

        if meridian:
            meridian = meridian.upper()
            if meridian == "PM" and hour != 12:
                hour += 12
            elif meridian == "AM" and hour == 12:
                hour = 0

        reminder_time = f"{hour:02d}:{minute:02d}"
        supabase.table("users").update({
            "reminder_time": reminder_time
        }).eq("user_id", user_id).execute()

        return await send_whatsapp_message(user_id, f"⏰ Reminder time set to *{reminder_time}*. You’ll now receive your Daily Manna.")

    return await send_whatsapp_message(user_id, "❓ I didn’t understand that. Send READ, REFLECT <text>, STATS, or START.")
