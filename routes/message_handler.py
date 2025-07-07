from datetime import datetime, timedelta
from utils.supabase_client import supabase
from utils.ultramsg import send_whatsapp_message

# Constants
TOTAL_DAYS = 365

async def handle_incoming_message(payload):
    data = payload.get("data")
    if not data:
        raise ValueError("Missing 'data' in payload")

    user_number = data.get("from", "").split("@")[0]
    message = data.get("body", "").strip()
    command = message.upper()

    print(f"📩 Incoming from {user_number}: {message}")

    if command.startswith("READ"):
        # Fetch progress or create new
        response = supabase.table("progress").select("*").eq("user_id", user_number).execute()
        user_data = response.data[0] if response.data else None

        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)

        if user_data:
            last_read_date = datetime.strptime(user_data["last_read_date"], "%Y-%m-%d").date()
            streak = user_data.get("streak", 0)

            if last_read_date == yesterday:
                streak += 1
            elif last_read_date == today:
                # Already marked today — no increment
                return "✅ You've already recorded today's reading. Keep it up!"
            else:
                streak = 1  # reset streak

            days_completed = user_data.get("days_completed", 0) + 1

            supabase.table("progress").update({
                "days_completed": days_completed,
                "last_read_date": today.isoformat(),
                "streak": streak
            }).eq("user_id", user_number).execute()

        else:
            # First time reader
            supabase.table("progress").insert({
                "user_id": user_number,
                "days_completed": 1,
                "last_read_date": today.isoformat(),
                "streak": 1
            }).execute()

        return "📖 Reading recorded! God bless your consistency."

    elif command == "STATS":
        response = supabase.table("progress").select("*").eq("user_id", user_number).execute()
        if not response.data:
            return "ℹ️ You haven’t started your reading journey. Send 'READ' to begin!"

        user = response.data[0]
        completed = user.get("days_completed", 0)
        streak = user.get("streak", 0)
        percent = round((completed / TOTAL_DAYS) * 100, 1)

        return (
            "📊 *Your Reading Stats*\n\n"
            f"✅ Days Completed: {completed}\n"
            f"🔥 Streak: {streak} days\n"
            f"📈 Completion: {percent}%\n\n"
            "🕊️ Keep pressing on!"
        )

    elif command.startswith("REFLECT"):
        reflection_text = message[7:].strip()
        supabase.table("reflections").insert({
            "user_id": user_number,
            "reflection": reflection_text
        }).execute()
        return "🙏 Reflection saved. May God bless your meditation."

    else:
        return (
            "🤖 Unknown command.\n\n"
            "Send:\n"
            "- READ to log your Bible reading\n"
            "- REFLECT <message> to submit a reflection\n"
            "- STATS to view your progress"
        )
