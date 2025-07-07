from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_progress(user_number):
    """Log or update the user's progress."""
    try:
        # Check if user already exists
        existing = supabase.table("progress").select("*").eq("user_id", user_number).execute()

        if existing.data:
            # Update progress by incrementing days_completed
            current = existing.data[0]["days_completed"]
            supabase.table("progress").update({
                "days_completed": current + 1
            }).eq("user_id", user_number).execute()
        else:
            # Insert new user progress
            supabase.table("progress").insert({
                "user_id": user_number,
                "days_completed": 1
            }).execute()
    except Exception as e:
        print(f"❌ Error logging progress: {e}")