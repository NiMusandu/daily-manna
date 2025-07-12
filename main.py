from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.whatsapp import router as whatsapp_router

app = FastAPI()

# Optional: Enable CORS (useful if calling this API from frontend in future)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the WhatsApp webhook router at "/webhook" without trailing slash conflict
app.include_router(whatsapp_router, prefix="/webhook", include_in_schema=False)

# Root route for confirmation
@app.get("/", response_class=JSONResponse)
def home():
    return {"message": "✅ Daily Manna backend is running."}
