import os
import httpx

ULTRA_TOKEN = os.getenv("ULTRA_TOKEN")
ULTRA_INSTANCE = os.getenv("ULTRA_INSTANCE")

async def send_whatsapp_message(phone_number, message):
    url = f"https://api.ultramsg.com/{ULTRA_INSTANCE}/messages/chat"
    payload = {
        "token": ULTRA_TOKEN,
        "to": phone_number,
        "body": message
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, data=payload)
