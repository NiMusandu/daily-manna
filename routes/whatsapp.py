from fastapi import APIRouter, Request
from routes.message_handler import handle_incoming_message

router = APIRouter()  # ✅ Define the router here

@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    try:
        data = await request.json()
        print("📥 RAW JSON DATA:", data)
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        return {"status": "error", "message": "JSON could not be parsed"}

    result = await handle_incoming_message(data)

    if result and "reply" in result:
        return {"status": "ok", "reply": result["reply"]}
    
    return {"status": "ok"}