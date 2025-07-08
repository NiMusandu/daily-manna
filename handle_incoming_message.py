# routes/message_handler.py
from utils.supabase_client import supabase
from utils.ultramsg import send_whatsapp_message

async def handle_incoming_message(payload):
    data = payload.get("data")
    if not data:
        raise ValueError("Missing 'data' in payload")

    user_number = data.get("from", "").split("@")[0]
    message = data.get("body", "").strip()
    command = message.upper()

    print(f"📩 Incoming from {user_number}: {message}")

    if command.startswith("READ"):
        supabase.table("progress").upsert({
            "user_id": user_number,
            "days_completed": 1  # Optional: update this with logic to increment
        }).execute()
        return "✅ Your Bible reading progress has been recorded. Keep going!"

    elif command.startswith("REFLECT"):
        reflection_text = message[7:].strip()
        supabase.table("reflections").insert({
            "user_id": user_number,
            "reflection": reflection_text
        }).execute()
        return "🙏 Reflection saved. May God bless your meditation."

    elif command.startswith("STATS"):
        response = supabase.table("progress").select("*").eq("user_id", user_number).execute()
        if response.data:
            days = response.data[0].get("days_completed", 0)
            return f"📊 You’ve completed {days} day(s) of Bible reading. Keep going!"
        else:
            return "📊 No progress found. Start by sending READ after reading your Bible."

    else:
        return "🤖 Unknown command. Send READ, REFLECT <your message>, or STATS."

import re

elif message_text.startswith("REMIND"):
    match = re.search(r"REMIND\s+(\d{1,2}):(\d{2})", message_text)
    if match:
        hour, minute = match.groups()
        reminder_time = f"{int(hour):02d}:{minute}"

        supabase.table("users").update({
            "reminder_time": reminder_time,
            "reminder_active": True
        }).eq("phone", user_number).execute()

        return f"✅ Reminder set for *{reminder_time}* daily!"
    else:
        return "❌ Invalid format. Use: REMIND 6:30AM"

elif message_text == "STOP REMINDER":
    supabase.table("users").update({
        "reminder_active": False
    }).eq("phone", user_number).execute()

    return "🛑 Daily reminders turned *off*."


    # === Bible Version Selection ===
    supported_versions = ["KJV", "NIV", "ESV"]
    if message in supported_versions:
        # Update preferred_version
        supabase.table("users").update({
            "preferred_version": message
        }).eq("user_id", user_number).execute()

        confirmation = f"✅ Bible version set to *{message}*.\n\n⏰ Now, reply with your preferred reminder time (e.g., 6:30AM)."
        await send_whatsapp_message(user_number, confirmation)
        return {"status": "version_set"}

    # === Catch unsupported single-word replies ===
    if len(message.split()) == 1 and message.isalpha():
        fallback = "❗ I didn't recognize that Bible version.\nPlease reply with one of: *KJV*, *NIV*, or *ESV*."
        await send_whatsapp_message(user_number, fallback)
        return {"status": "invalid_version"}
