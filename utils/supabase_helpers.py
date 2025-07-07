def get_or_create_user(supabase, phone):
    result = supabase.table("users").select("*").eq("phone", phone).execute()
    if not result.data:
        supabase.table("users").insert({"phone": phone, "days_completed": 0}).execute()
    return True

def log_user_progress(supabase, phone):
    existing = supabase.table("users").select("*").eq("phone", phone).execute()
    if existing.data:
        current = existing.data[0].get("days_completed", 0)
        supabase.table("users").update({"days_completed": current + 1}).eq("phone", phone).execute()
