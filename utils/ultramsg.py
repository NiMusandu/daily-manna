import httpx
import os
from dotenv import load_dotenv

load_dotenv()

ULTRA_TOKEN = os.getenv("ULTRA_TOKEN")
ULTRA_INSTANCE_ID = os.getenv("ULTRA_INSTANCE")

BASE_URL = f"https://api.ultramsg.com/{ULTRA_INSTANCE_ID}/messages/chat"

async def send_whatsapp_message(to: str, message: str):
    async with httpx.AsyncClient() as client:
        payload = {
            "token": ULTRA_TOKEN,
            "to": f"+{to}",  # Ensure it's in international format
            "body": message
        }
        response = await client.post(BASE_URL, data=payload)
        print(f"✅ WhatsApp API response: {response.text}")
        return response.json()
