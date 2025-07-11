# utils/ultramsg.py

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

async def send_whatsapp_message(to_number: str, message: str):
    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": to_number,
        "body": message
    }

    print(f"📤 Sending message to {to_number}")
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, data=payload)
            print("📬 WhatsApp send response:", res.text)
            if res.status_code != 200:
                print("❌ Failed to send:", res.status_code, res.text)
        except Exception as e:
            print("❌ WhatsApp send error:", str(e))
