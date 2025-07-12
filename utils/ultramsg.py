import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

async def send_whatsapp_message(to_number: str, message: str):
    print("📤 Sending to:", to_number)
    print("💬 Message:", message)

    if not ULTRAMSG_INSTANCE_ID or not ULTRAMSG_TOKEN:
        print("❌ Missing UltraMsg instance ID or token.")
        return

    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": to_number,
        "body": message
    }

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, data=payload)
            print("📬 WhatsApp API response:", res.text)
        except Exception as e:
            print("❌ WhatsApp send error:", str(e))
