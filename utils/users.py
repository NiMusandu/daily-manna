from config import ULTRA_INSTANCE, ULTRA_TOKEN

from supabase_client import supabase
from datetime import datetime

def register_user(phone: str, name: str = None):
    existing = supabase.table("users").select("*").eq("phone", phone).execute()
    
    if existing.data:
        print("✅ User already exists.")
        return existing.data[0]
    
    new_user = {
        "phone": phone,
        "name": name,
        "joined_at": datetime.utcnow().isoformat(),
        "last_read_day": 0,
        "streak": 0,
        "reminder_time": "06:00:00"
    }

    response = supabase.table("users").insert(new_user).execute()
    print("🎉 New user registered:", response.data[0])
    return response.data[0]
