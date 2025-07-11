# services/user.py

import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL or SUPABASE_KEY not set in environment.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Function to register a new user from WhatsApp payload
async def register_user(payload: dict) -> dict:
    data = payload.get("data", {})
    phone = data.get("author") or data.get("from")
    name = data.get("pushname", "Friend")

    if not phone:
        return {"message": "❌ No phone number found in payload."}

    # Check if user already exists
    result = supabase.table("users").select("*").eq("phone", phone).execute()
    if result.data:
        return {"message": f"👋 Welcome back, {name}!"}

    # Insert new user
    user_data = {
        "phone": phone,
        "name": name,
        "joined_at": datetime.utcnow().isoformat()
    }

    response = supabase.table("users").insert(user_data).execute()

    if response.error:
        return {"message": "❌ Failed to register user."}
    
    return {"message": f"🎉 Hello {name}, you've been registered for Daily Manna!"}
