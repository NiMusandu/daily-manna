async def register_user(user_id: str, name: str):
    from datetime import datetime
    print("📌 Registering user:", user_id)

    # Print existing check (if needed)
    existing = supabase.table("users").select("*").eq("user_id", user_id).execute()
    if existing.data:
        print("👤 Already registered")
        return {"message": f"👋 Welcome back, {name}!"}

    # Insert payload
    data = {
        "user_id": user_id,
        "name": name,
        "created_at": datetime.utcnow().isoformat(),
        "reminder_time": "07:00",
        "reminder_active": True
    }

    print("📝 Insert payload:", data)

    # Now try to insert
    try:
        supabase.table("users").insert(data).execute()
        print("✅ Registered successfully")
        return {"message": f"✅ You're now registered, {name}!"}
    except Exception as e:
        print("❌ Supabase insert error:", e)
        raise
