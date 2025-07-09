async def get_user_reading(user_id: str) -> str:
    # Match by user_id instead of phone
    result = supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    if not result.data:
        return "⚠️ You are not registered. Send START to begin."

    start_date = result.data["created_at"]
    day_num = calculate_day_number(start_date)

    reading = next((r["passage"] for r in READING_PLAN if r["day"] == day_num), None)
    if reading:
        return f"📖 Day {day_num} Reading:\n{reading}"
    return "✅ Congratulations! You've completed the 365-day plan!"
