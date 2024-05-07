from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
import time
from typing import Dict
from config import settings
import jwt, hashlib
from app.validations import ValidationException
import uuid

api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == settings.SECRET_KEY:
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key",
    )


def token_response(token: str):
    return {"access_token": token}


def signJWT(client_id: str) -> Dict[str, str]:
    payload = {"client_id": client_id, "expires": int(time.time()) + 600}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return decoded_token if decoded_token["expires"] >= int(time.time()) else None
    except:
        return {}
