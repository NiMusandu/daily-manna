import os
import requests

ULTRA_TOKEN = os.getenv("ULTRA_TOKEN")
ULTRA_INSTANCE = os.getenv("ULTRA_INSTANCE")

def send_whatsapp_message(to, message):
    url = f"https://api.ultramsg.com/{ULTRA_INSTANCE}/messages/chat"
    payload = {
        "token": ULTRA_TOKEN,
        "to": to,
        "body": message
    }
    try:
        response = requests.post(url, data=payload)
        print(f"✅ Sent to {to}: {message}")
    except Exception as e:
        print(f"❌ Error: {e}")
