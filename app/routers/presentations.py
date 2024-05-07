from fastapi import APIRouter, Depends, Request
from config import settings
from app.models import *
from app.auth.bearer import JWTBearer

router = APIRouter()


@router.post("/request", dependencies=[Depends(JWTBearer())])
async def request_presentation(request: Request):
    return ""


@router.post("/create", dependencies=[Depends(JWTBearer())])
async def create_presentation(request: Request):
    return ""


@router.post("/verify", dependencies=[Depends(JWTBearer())])
async def verify_presentation(request: Request):
    return ""
