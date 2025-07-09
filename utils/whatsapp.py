import httpx
import os

ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

ULTRAMSG_API_URL = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"

async def send_whatsapp_message(to_number: str, message: str):
    async with httpx.AsyncClient() as client:
        payload = {
            "token": ULTRAMSG_TOKEN,
            "to": to_number,
            "body": message,
            "priority": 10,
            "referenceId": "daily-manna"
        }
        try:
            res = await client.post(ULTRAMSG_API_URL, data=payload)
            print("📤 Sent message:", res.json())
        except Exception as e:
            print("❌ Failed to send WhatsApp message:", str(e))
