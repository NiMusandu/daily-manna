from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router

app = FastAPI()

# Do not add prefix, keep path as /webhook
app.include_router(whatsapp_router)

@app.get("/")
async def home():
    return {"message": "✅ Daily Manna backend is running."}
