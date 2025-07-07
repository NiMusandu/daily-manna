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
