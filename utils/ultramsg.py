import os
import httpx

ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

async def send_whatsapp_message(to: str, message: str):
    if not ULTRAMSG_INSTANCE_ID or not ULTRAMSG_TOKEN:
        print("❌ Missing UltraMsg instance ID or token.")
        return

    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "to": to,
        "body": message,
        "priority": 10,
        "referenceId": ""
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{url}?token={ULTRAMSG_TOKEN}", data=payload)
            print("📬 WhatsApp API response:", response.text)
    except Exception as e:
        print("❌ Error sending WhatsApp message:", e)
