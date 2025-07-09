from fastapi import APIRouter, Request
from routes.message_handler import handle_incoming_message

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    try:
        payload = await request.json()  # ✅ DEFINE payload here
        print(f"📥 Incoming WhatsApp Payload: {payload}")

        response = await handle_incoming_message(payload)  # ✅ USE payload here

        return response
    except Exception as e:
        print(f"❌ Failed to process WhatsApp webhook: {e}")
        return {"error": "Webhook processing failed"}
