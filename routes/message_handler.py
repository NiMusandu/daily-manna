# routes/whatsapp.py

from fastapi import APIRouter, Request

router = APIRouter()

async def handle_incoming_message(payload):
    # your logic here
    return {"message": "Handled"}

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




