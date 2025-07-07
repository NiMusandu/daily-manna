import json

# Load the generated reading plan
with open("reading_plan.json", "r", encoding="utf-8") as f:
    plan = json.load(f)

def get_reading_for_day(day: int) -> str:
    if 1 <= day <= 365:
        item = plan[day - 1]
        combined = f"{item['old_testament']}; {item['new_testament']}; {item['psalm_or_gospel']}"
        return combined
    return "John 1"

def generate_esv_link(ref: str) -> str:
    formatted = ref.replace("; ", ",").replace(" ", "+")
    return f"https://www.esv.org/{formatted}/"

# Example usage
day = 21
reference = get_reading_for_day(day)
link = generate_esv_link(reference)

print(f"📖 Day {day} Reading: {reference}")
print(f"🔗 Read here: {link}")


