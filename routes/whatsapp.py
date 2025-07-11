async def send_whatsapp_message(to_number: str, message: str):
    print("📤 Sending to:", to_number)
    print("💬 Message:", message)

    url = f"https://api.ultramsg.com/{ULTRAMSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": to_number,
        "body": message
    }

    print("📤 Payload:", payload)  # ✅ log payload before sending

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=payload)
            print("📬 Ultramsg response:", response.status_code, response.text)  # ✅ log full response
        except Exception as e:
            print("❌ WhatsApp send error:", str(e))
