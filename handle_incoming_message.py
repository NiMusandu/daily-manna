async def handle_incoming_message(payload):
    # ✅ Only respond to message_received events
    if payload.get("event_type") != "message_received":
        print("📭 Skipping event:", payload.get("event_type"))
        return

    data = payload.get("data", {})

    # ✅ Also ignore any bot-sent messages just in case
    if data.get("fromMe") or data.get("self") or data.get("ack"):
        print("📭 Skipping bot/self/ack message:", data.get("body"))
        return

    raw_id = data.get("author") or data.get("from")
    user_id = normalize_user_id(raw_id)
    message = data.get("body", "").strip()
    command = message.upper()
    name = data.get("pushname", "Friend")

    print(f"📨 {command} from {user_id}")

    # START – Register the user
    if command == "START":
        response = await register_user(user_id, name)
        return await send_whatsapp_message(user_id, response["message"])

    # ... rest of your logic unchanged
