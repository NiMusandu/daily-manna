import os
import asyncio
import httpx
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")


async def send_whatsapp_message(to_number: str, message: str):
    if not ULTRAMSG_INSTANCE_ID or not ULTRAMSG_TOKEN:
        print("❌ Missing UltraMsg instance ID or token.")
        return

    print("📤 Sending to:", to_number)
    print("💬 Message:", message)

    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    params = {
        "token": ULTRAMSG_TOKEN
    }
    payload = {
        "to": to_number,
        "body": message
    }

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, params=params, data=payload)
            print("📬 WhatsApp API response:", res.text)
            if res.status_code != 200:
                print("❌ Failed to send. Status:", res.status_code)
        except Exception as e:
            print("❌ Exception:", str(e))


if __name__ == "__main__":
    # ✅ Replace with your own WhatsApp number (in international format)
    test_number = "254721420119@c.us"  # or "2547XXXXXXXX@c.us"
    test_message = "✅ Hello from UltraMsg test script!"

    asyncio.run(send_whatsapp_message(test_number, test_message))
