import json
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

# Load the plan once on startup
with open("reading_plan.json", "r", encoding="utf-8") as f:
    reading_plan = json.load(f)

def generate_esv_link(reference: str) -> str:
    first_ref = reference.split(";")[0].strip()
    return f"https://www.esv.org/{first_ref.replace(' ', '%20')}/"

@router.get("/today-reading")
def today_reading():
    today = datetime.now().timetuple().tm_yday
    try:
        day_plan = reading_plan[today - 1]
        full_ref = f"{day_plan['old_testament']}; {day_plan['new_testament']}; {day_plan['psalm_or_gospel']}"
        return {
            "day": day_plan["day"],
            "date": day_plan["date"],
            "reading": full_ref,
            "link": generate_esv_link(full_ref)
        }
    except IndexError:
        return {"error": "Day out of range"}
