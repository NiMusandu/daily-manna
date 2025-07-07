# ✅ utils/user.py
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def register_user(phone: str, status: str = "active"):
    # Check if user exists
    result = supabase.table("users").select("*").eq("phone", phone).execute()
    if not result.data:
        supabase.table("users").insert({"phone": phone, "status": status}).execute()
    else:
        # Update status
        supabase.table("users").update({"status": status}).eq("phone", phone).execute()

def update_reminder_time(phone: str, time: str) -> bool:
    try:
        supabase.table("users").update({
            "reminder_time": time,
            "status": "active"
        }).eq("phone", phone).execute()
        return True
    except:
        return False