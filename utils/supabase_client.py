# utils/supabase_client.py

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # ✅ Load env vars from .env file

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL or SUPABASE_KEY not set in environment.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
