# routes/whatsapp.py

from fastapi import APIRouter, Request

router = APIRouter()

async def handle_incoming_message(payload):
    # your logic here
    return {"message": "START command received"}

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

from utils.whatsapp import send_whatsapp_message  # you'd implement this

async def handle_incoming_message(payload):
    message = payload["data"].get("body", "").strip().upper()
    sender = payload["data"].get("author") or payload["data"].get("from")

    if message == "START":
        await send_whatsapp_message(sender, "🎉 Welcome to Daily Manna!")
    elif message == "READ":
        await send_whatsapp_message(sender, "📖 Today's Reading: John 3:16")
    else:
        await send_whatsapp_message(sender, "🤖 Unknown command. Try: START or READ")

    return {"status": "ok"}



