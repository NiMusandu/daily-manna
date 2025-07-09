from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/join")
async def join_redirect():
    return RedirectResponse("https://wa.me/2547XXXXXXX?text=START")
