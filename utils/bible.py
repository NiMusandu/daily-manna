# utils/bible.py

from datetime import datetime

def get_daily_reading():
    day_number = datetime.utcnow().timetuple().tm_yday
    return f"📖 Day {day_number}: John 3:16 — For God so loved the world..."
