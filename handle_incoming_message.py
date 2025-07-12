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
        "phone": user_id.replace("@c.us", ""),
        "name": name,
        "created_at": datetime.utcnow().isoformat(),
        "reminder_time": "07:00",
        "reminder_active": True
    }).execute()

    print("✅ Registered successfully")
    return {"message": f"✅ You're now registered, {name}!"}


async def handle_incoming_message(payload):
    data = payload.get("data", {})
    event_type = payload.get("event_type")

    # ✅ 1. Only process user-sent messages
    if event_type != "message_received":
        print("📭 Skipping non-user event:", event_type)
        return

    # ✅ 2. Skip bot/self messages
    if data.get("fromMe") or data.get("self") or data.get("ack"):
        print("📭 Skipping bot/self/ack message:", data.get("body"))
        return

    user_id = normalize_user_id(data.get("author") or data.get("from"))
    message = data.get("body", "").strip()
    command = message.upper()
    name = data.get("pushname", "Friend")

    # ✅ 3. Prevent responding to fallback loop
    if "i didn’t understand" in command.lower():
        print("🚫 Preventing fallback loop.")
        return

    print(f"📨 {command} from {user_id}")

    # ✅ 4. RESET command (manual clearing)
    if command == "RESET":
        supabase.table("users").delete().eq("user_id", user_id).execute()
        supabase.table("progress").delete().eq("user_id", user_id).execute()
        supabase.table("reflections").delete().eq("user_id", user_id).execute()
        return await send_whatsapp_message(user_id, "🔄 Your Daily Manna data has been reset.")

    # START – Register the user
    if command == "START":
        response = await register_user(user_id, name)
        return await send_whatsapp_message(user_id, response["message"])

    # READ – Log Bible reading
    if command.startswith("READ"):
        supabase.table("progress").upsert({
            "user_id": user_id,
            "days_completed": 1
        }).execute()
        return await send_whatsapp_message(user_id, "✅ Bible reading recorded. Keep going!")

    # REFLECT – Save reflection
    if command.startswith("REFLECT"):
        reflection_text = message[7:].strip()
        supabase.table("reflections").insert({
            "user_id": user_id,
            "reflection": reflection_text
        }).execute()
        return await send_whatsapp_message(user_id, "🙏 Reflection saved. Stay blessed.")

    # STATS – Show progress
    if command == "STATS":
        response = supabase.table("progress").select("*").eq("user_id", user_id).execute()
        if response.data:
            days = response.data[0].get("days_completed", 0)
            return await send_whatsapp_message(user_id, f"📊 You’ve completed {days} day(s) of reading.")
        return await send_whatsapp_message(user_id, "📊 No progress found. Send READ to start tracking.")

    # REMIND – Set reminder
    if command.startswith("REMIND"):
        match = re.search(r"REMIND\s+(\d{1,2}):(\d{2})", message)
        if match:
            hour, minute = match.groups()
            reminder_time = f"{int(hour):02d}:{minute}"
            supabase.table("users").update({
                "reminder_time": reminder_time,
                "reminder_active": True
            }).eq("user_id", user_id).execute()
            return await send_whatsapp_message(user_id, f"✅ Reminder set for *{reminder_time}* daily!")
        return await send_whatsapp_message(user_id, "❌ Invalid format. Use: REMIND 6:30")

    # STOP REMINDER
    if command == "STOP REMINDER":
        supabase.table("users").update({
            "reminder_active": False
        }).eq("user_id", user_id).execute()
        return await send_whatsapp_message(user_id, "🛑 Reminders turned off.")

    # Bible version
    if command in ["KJV", "NIV", "ESV"]:
        supabase.table("users").update({
            "preferred_version": command
        }).eq("user_id", user_id).execute()
        return await send_whatsapp_message(user_id, f"✅ Bible version set to *{command}*.")

    # TIME SETTER (e.g. 6:30 AM)
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

        reminder_time = f"{hour:02d}:{minute}"
        supabase.table("users").update({
            "reminder_time": reminder_time
        }).eq("user_id", user_id).execute()

        return await send_whatsapp_message(user_id, f"⏰ Reminder set to *{reminder_time}*.")

    # Fallback – unknown command
    return await send_whatsapp_message(user_id, "❓ I didn’t understand that. Send START, READ, REFLECT <text>, STATS, or REMIND <time>.")
