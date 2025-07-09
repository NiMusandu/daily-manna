# utils/reading_plan.py

reading_plan = {
    1: "📖 *Day 1 Reading*\nGenesis 1–2\nJohn 1:1–18",
    2: "📖 *Day 2 Reading*\nGenesis 3–5\nJohn 1:19–51",
    3: "📖 *Day 3 Reading*\nGenesis 6–9\nJohn 2\n\n...",
    # ... add up to 365 days
}

def get_reading_for_day(day: int) -> str:
    return reading_plan.get(day, "🎉 You've completed the plan or no reading found for today.")
