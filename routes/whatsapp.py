
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from services.message_handler import handle_incoming_message  # ✅ Import your handler

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    """
    Receives incoming WhatsApp webhook messages and routes them to the message handler.
    """
    try:
        payload = await request.json()
        print(f"📥 Incoming WhatsApp Payload: {payload}")

        if payload.get("event_type") == "message_received":
            await handle_incoming_message(payload)

        return JSONResponse(content={"status": "ok"}, status_code=200)

    except Exception as e:
        print(f"❌ Failed to process WhatsApp webhook: {e}")
        return JSONResponse(content={"error": "Webhook failed"}, status_code=500)
