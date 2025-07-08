# utils/whatsapp.py

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
        print(f"✅ Message sent to {to}: {message}")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")


import requests
import os

def send_whatsapp_message(phone: str, message: str):
    url = f"https://api.ultramsg.com/instance{os.getenv('ULTRA_INSTANCE')}/messages/chat"
    payload = {
        "token": os.getenv("ULTRA_TOKEN"),
        "to": phone,
        "body": message
    }
    response = requests.post(url, data=payload)
    print(f"📤 Sent WhatsApp message to {phone} → Status: {response.status_code}")
    return response.json()
