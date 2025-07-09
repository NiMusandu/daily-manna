import os
import httpx

ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")
ULTRAMSG_API_URL = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"

async def send_whatsapp_message(to_number: str, message: str):
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": to_number,
        "body": message,
        "priority": 10,
        "referenceId": "daily-manna"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(ULTRAMSG_API_URL, data=payload)
            response.raise_for_status()
            print("📤 Sent message:", response.json())
        except httpx.HTTPStatusError as http_err:
            print("❌ HTTP error while sending message:", http_err.response.text)
        except Exception as e:
            print("❌ Failed to send WhatsApp message:", str(e))
