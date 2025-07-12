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

    # ✅ ONLY process real incoming messages from user
    if event_type != "message_received":
        print("📭 Skipping event type:", event_type)
        return

    # ✅ Ignore messages that bot sends (even if event_type is "message_received")
    if data.get("fromMe") or data.get("self") or data.get("ack") or data.get("type") != "chat":
        print("📭 Ignoring bot/self/ack/non-chat message:", data.get("body"))
        return

    raw_id = data.get("author") or data.get("from")
    user_id = normalize_user_id(raw_id)
    message = data.get("body", "").strip()
    command = message.upper()
    name = data.get("pushname", "Friend")

    # ✅ Ignore bot fallback messages (anti-loop)
    fallback_signature = "I didn’t understand that"
    if fallback_signature.lower() in message.lower():
        print("🛑 Preventing fallback message loop.")
        return

    print(f"📨 {command} from {user_id}")

    # ✅ Manual reset
    if command == "RESET":
        supabase.table("users").delete().eq("user_id", user_id).execute()
        supabase.table("progress").delete().eq("user_id", user_id).execute()
        supabase.table("reflections").delete().eq("user_id", user_id).execute()
        return await send_whatsapp_message(user_id, "🔄 Your data has been reset.")

    if command == "START":
        response = await register_user(user_id, name)
        return await send_whatsapp_message(user_id, response["message"])

    if command.startswith("READ"):
        supabase.table("progress").upsert({
            "user_id": user_id,
            "days_completed": 1
        }).execute()
        return await send_whatsapp_message(user_id, "✅ Your Bible reading has been recorded!")

    if command.startswith("REFLECT"):
        reflection_text = message[7:].strip()
        supabase.table("reflections").insert({
            "user_id": user_id,
            "reflection": reflection_text
        }).execute()
        return await send_whatsapp_message(user_id, "📝 Reflection saved.")

    if command == "STATS":
        response = supabase.table("progress").select("*").eq("user_id", user_id).execute()
        if response.data:
            days = response.data[0].get("days_completed", 0)
            return await send_whatsapp_message(user_id, f"📊 You’ve read for {days} day(s). Keep going!")
        return await send_whatsapp_message(user_id, "📊 No progress yet. Send READ to log your Bible reading.")

    if command.startswith("REMIND"):
        match = re.search(r"REMIND\s+(\d{1,2}):(\d{2})", message)
        if match:
            hour, minute = match.groups()
            reminder_time = f"{int(hour):02d}:{minute}"
            supabase.table("users").update({
                "reminder_time": reminder_time,
                "reminder_active": True
            }).eq("user_id", user_id).execute()
            return await send_whatsapp_message(user_id, f"⏰ Reminder set for *{reminder_time}*.")
        return await send_whatsapp_message(user_id, "❌ Invalid format. Use: REMIND 6:30")

    if command == "STOP REMINDER":
        supabase.table("users").update({
            "reminder_active": False
        }).eq("user_id", user_id).execute()
        return await send_whatsapp_message(user_id, "🛑 Reminders turned off.")

    if command in ["KJV", "NIV", "ESV"]:
        supabase.table("users").update({
            "preferred_version": command
        }).eq("user_id", user_id).execute()
        return await send_whatsapp_message(user_id, f"✅ Bible version set to *{command}*.")

    # ⏰ Accepts 6:30 or 6:30 PM
    time_pattern = re.compile(r"^([0-1]?[0-9]|2[0-3]):([0-5][0-9])\s?(AM|PM)?$", re.IGNORECASE)
    match = time_pattern.match(message)
    if match:
        hour, minute = int(match.group(1)), int(match.group(2))
        meridian = match.group(3)

        if meridian:
            if meridian.upper() == "PM" and hour != 12:
                hour += 12
            elif meridian.upper() == "AM" and hour == 12:
                hour = 0

        reminder_time = f"{hour:02d}:{minute:02d}"
        supabase.table("users").update({
            "reminder_time": reminder_time
        }).eq("user_id", user_id).execute()

        return await send_whatsapp_message(user_id, f"⏰ Reminder set to *{reminder_time}*.")

    # Fallback
    return await send_whatsapp_message(user_id, "❓ I didn’t understand that. Send START, READ, REFLECT <text>, STATS, or REMIND <time>.")
