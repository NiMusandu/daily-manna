# routes/whatsapp.py

from fastapi import APIRouter, Request
from routes.message_handler import handle_incoming_message

router = APIRouter()

@router.post("/")  # This will be mounted at /webhook if you set prefix="/webhook"
async def whatsapp_webhook(request: Request):
    try:
        data = await request.json()
        print("📥 RAW JSON DATA:", data)

        result = await handle_incoming_message(data)

        if result and "reply" in result:
            return {"status": "ok", "reply": result["reply"]}
        
        return {"status": "ok"}

    except Exception as e:
        print("❌ Error while handling WhatsApp webhook:", e)
        return {"status": "error", "detail": str(e)}
