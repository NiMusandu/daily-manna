from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from services.message_handler import handle_incoming_message

router = APIRouter()

@router.post("/webhook")  # ✅ Matches /webhook exactly
async def webhook(request: Request):
    try:
        payload = await request.json()
        print(f"📥 Incoming WhatsApp Payload: {payload}")
        await handle_incoming_message(payload)
        return JSONResponse(content={"status": "ok"}, status_code=200)
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return JSONResponse(content={"error": "Webhook failed"}, status_code=500)
