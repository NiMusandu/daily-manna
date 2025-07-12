# utils/ultramsg.py

import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read values from .env
ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

async def send_whatsapp_message(to_number: str, message: str):
    print("📤 Sending to:", to_number)
    print("💬 Message:", message)

    # Validate credentials
    if not ULTRAMSG_INSTANCE_ID or not ULTRAMSG_TOKEN:
        print("❌ Missing UltraMsg instance ID or token.")
        return

    # Properly format the endpoint
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat?token={ULTRAMSG_TOKEN}"

    payload = {
        "to": to_number,
        "body": message
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload)
            print("📬 WhatsApp API response:", response.text)
    except Exception as e:
        print("❌ WhatsApp send error:", str(e))
