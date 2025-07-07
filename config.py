import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from current project root
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Fetch environment variables
ULTRA_INSTANCE = os.getenv("ULTRA_INSTANCE")
ULTRA_TOKEN = os.getenv("ULTRA_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# ✅ Debug print to verify
print("✅ ULTRA_INSTANCE:", ULTRA_INSTANCE)
print("✅ ULTRA_TOKEN:", (ULTRA_TOKEN[:5] + "...") if ULTRA_TOKEN else "❌ Missing")
print("✅ SUPABASE_URL:", SUPABASE_URL)
print("✅ SUPABASE_KEY:", (SUPABASE_KEY[:8] + "...") if SUPABASE_KEY else "❌ Missing")