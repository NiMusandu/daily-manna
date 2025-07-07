from config import ULTRA_INSTANCE, ULTRA_TOKEN
import httpx

# ✅ Correct API URL with "instance" prefix
ULTRA_BASE_URL = f"https://api.ultramsg.com/instance{ULTRA_INSTANCE}/messages/chat"

def send_whatsapp_message(to_number: str, message: str):
    payload = {
        "token": ULTRA_TOKEN,
        "to": to_number,
        "body": message,
    }

    print("🔧 Sending WhatsApp message...")
    print("📍 URL:", ULTRA_BASE_URL)
    print("📦 Payload:", payload)

    try:
        response = httpx.post(ULTRA_BASE_URL, data=payload)
        print(f"📨 HTTP Status: {response.status_code}")
        print("🧾 Raw Response:", response.text)
    except Exception as e:
        print(f"❌ Error:", e)

if __name__ == "__main__":
    send_whatsapp_message("254721420119", "📖 This is a test message from Daily Manna!")
