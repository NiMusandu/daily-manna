from dotenv import load_dotenv
load_dotenv()


import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # ✅ This MUST be before reading os.getenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL or SUPABASE_KEY not set in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_user_reflection(user_id: str, date: str, message: str):
    response = supabase.table("reflections").insert({
        "user_id": user_id,
        "date": date,
        "message": message
    }).execute()

    if response.error:
        print("❌ Error saving reflection:", response.error)
    else:
        print("✅ Reflection saved successfully.")


import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL or SUPABASE_KEY not set in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

