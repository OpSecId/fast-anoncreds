from fastapi import APIRouter, Security
from fastapi.responses import JSONResponse
from app.auth.handler import get_api_key
from app.models.web_requests import RegisterClient
from app.controllers.askar import AskarController
from config import settings
from datetime import datetime
import uuid
import secrets
import hashlib

router = APIRouter()


@router.get("", summary="List clients")
async def list_clients(apiKey: str = Security(get_api_key)):
    clients = await AskarController().list_profiles()
    return JSONResponse(status_code=200, content=clients)


@router.post("", summary="Register client")
async def register_client(
    request_body: RegisterClient, apiKey: str = Security(get_api_key)
):
    request_body = request_body.model_dump(by_alias=True, exclude_none=True)
    # client_id = str(uuid.uuid5(uuid.NAMESPACE_URL, request_body["did"]))
    client_id = str(uuid.uuid5(uuid.NAMESPACE_URL, request_body["did"])) if 'did' in request_body else str(uuid.uuid4())
    client_secret = secrets.token_urlsafe()
    client_hash = hashlib.md5(client_secret.encode()).hexdigest()
    client_info = {"client_id": client_id, "client_secret": client_secret}
    await AskarController().create_profile(client_id)

    # await AskarController(client_id).store("client", "did", request_body["did"])
    await AskarController(client_id).store("client", "hash", client_hash)
    
    did_doc = {
        '@context': 'https://www.w3.org/ns/did/v1',
        'id': f'{settings.DID_WEB}:{client_id}',
        'verificationMethod': [],
        'service': []
    }
    await AskarController(client_id).store("client", "didDoc", did_doc)

    return JSONResponse(status_code=201, content=client_info)
