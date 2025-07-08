# utils/bible.py

from datetime import datetime

def get_daily_reading():
    # For now, return a dummy verse based on the day number
    day_number = datetime.utcnow().timetuple().tm_yday
    # You can replace this with actual logic later
    return f"Day {day_number}: John 3:16 — For God so loved the world..."
