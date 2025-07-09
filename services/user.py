from datetime import datetime
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def register_user(payload):
    phone = payload["data"].get("author") or payload["data"].get("from")
    name = payload["data"].get("pushname", "Friend")

    # Check if user exists
    result = supabase.table("users").select("*").eq("phone", phone).execute()
    if result.data and len(result.data) > 0:
        return {"message": f"👋 Welcome back, {name}!"}

    # Register new user
    supabase.table("users").insert({
        "phone": phone,
        "name": name,
        "joined_at": datetime.utcnow().isoformat()
    }).execute()

    return {"message": f"🎉 Hello {name}, you've been registered for Daily Manna!"}
