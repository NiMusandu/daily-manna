# utils/whatsapp.py

import os
import requests
from config import ULTRA_INSTANCE, ULTRA_TOKEN

def send_whatsapp_message(to, body):
    url = f"https://api.ultramsg.com/instance{ULTRA_INSTANCE}/messages/chat"
    payload = {
        "token": ULTRA_TOKEN,
        "to": to,
        "body": body
    }

    print("🔧 Sending WhatsApp message...")
    print("📍 URL:", url)
    print("📦 Payload:", payload)

    response = requests.post(url, data=payload)
    print("📨 HTTP Status:", response.status_code)
    print("🧾 Raw Response:", response.text)


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
