from fastapi import APIRouter, Request
from services.message_handler import handle_incoming_message  # ✅ correct import

router = APIRouter()

@router.post("/webhook")  # ✅ correct endpoint
async def webhook(request: Request):
    try:
        payload = await request.json()
        print(f"📥 Incoming WhatsApp Payload: {payload}")
        response = await handle_incoming_message(payload)
        return response
    except Exception as e:
        print(f"❌ Failed to process WhatsApp webhook: {e}")
        return {"error": "Webhook failed"}
