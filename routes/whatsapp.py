# routes/whatsapp.py

from fastapi import APIRouter, Request
from routes.message_handler import handle_incoming_message

router = APIRouter()

@router.post("/")  # This handles POST to /webhook if router prefix is /webhook
async def whatsapp_webhook(request: Request):
    try:
        response = await handle_incoming_message(payload)
        print("📥 Incoming WhatsApp Payload:", payload)
        result = await handle_incoming_message(payload)
        return {"status": "ok", "reply": result.get("reply", "handled")} if result else {"status": "ok"}
    except Exception as e:
        print("❌ Failed to process WhatsApp webhook:", e)
        return {"status": "error", "detail": str(e)}
