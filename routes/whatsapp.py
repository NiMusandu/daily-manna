from fastapi import APIRouter, Request
from routes.message_handler import handle_incoming_message

router = APIRouter()

@router.post("/")
async def whatsapp_webhook(request: Request):
    try:
        payload = await request.json()
        print(f"📥 Incoming WhatsApp Payload: {payload}")

        return await handle_incoming_message(payload)

    except Exception as e:
        print(f"❌ Failed to process WhatsApp webhook: {e}")
        return {"error": "Webhook processing failed"}
