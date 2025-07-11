async def register_user(user_id: str, name: str):
    from datetime import datetime

    data = {
        "user_id": user_id,
        "name": name,
        "created_at": datetime.utcnow().isoformat(),
        "reminder_time": "07:00",
        "reminder_active": True
    }

    print("📝 Trying to insert this payload into Supabase users table:")
    print(data)

    try:
        result = supabase.table("users").insert(data).execute()
        print("✅ Insert result:", result)
        return {"message": f"✅ You're now registered, {name}!"}
    except Exception as e:
        print("❌ Supabase insert failed with:", e)
        raise
