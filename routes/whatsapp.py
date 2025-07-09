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

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/")
async def whatsapp_webhook(request: Request):
    payload = await request.json()
    message_body = payload.get("data", {}).get("body", "").strip().upper()
    user_number = payload.get("data", {}).get("from", "")

    if message_body == "START":
        # TODO: Register user in Supabase, send welcome message via WhatsApp API
        print(f"🚀 New user {user_number} started the journey!")
        return JSONResponse(content={"message": "User START command processed."}, status_code=200)

    # Handle other commands
    return JSONResponse(content={"message": f"Command '{message_body}' received."}, status_code=200)
