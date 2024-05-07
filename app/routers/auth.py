from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from app.controllers.askar import AskarController
from app.auth.handler import signJWT
from config import settings
from typing import Annotated
import time
import jwt


router = APIRouter()


@router.post("/token", summary="Request 0Auth 2 token")
async def request_oauth_token(
    client_id: Annotated[str, Form()], client_secret: Annotated[str, Form()]
):
    await AskarController(client_id).profile_exists()
    await AskarController(client_id).compare_hash(client_secret)
    return JSONResponse(status_code=200, content=signJWT(client_id))
