from services.user import register_user
from utils.whatsapp import send_whatsapp_message

async def handle_incoming_message(payload):
    text = payload["data"].get("body", "").strip().upper()
    phone = payload["data"].get("author") or payload["data"].get("from")

    if text == "START":
        response = await register_user(payload)
        await send_whatsapp_message(phone, response["message"])
        return {"status": "registered"}

    return {"status": "unknown_command"}
