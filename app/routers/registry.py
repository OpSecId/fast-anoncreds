from fastapi import APIRouter, Depends, Request
from config import settings
from app.controllers.askar import AskarController
from app.auth.bearer import JWTBearer
from app.models.web_requests import ActivateDefinition
import base64
import json

router = APIRouter()


@router.get("/{client_id}/did.json")
async def get_schema(client_id: str):
    did_doc = await AskarController(client_id).fetch("client", "didDoc")
    return did_doc


@router.get("/{client_id}/schemas/{schema_name}")
async def get_schema(client_id: str, schema_name: str):
    schema = await AskarController(client_id).fetch("schemas", schema_name)
    return schema


@router.get("/{client_id}/definitions/{cred_def_tag}/did.json")
async def get_cred_def(client_id: str, cred_def_tag: str):
    service = {
        "id": f'{settings.DID_WEB}:{client_id}:definitions:{cred_def_tag}#schema',
        "type": "AnonCredsVDR",
        "serviceEndpoint": f"{settings.HTTPS_BASE}/{client_id}/schemas/{cred_def_tag}",
    }
    verification_method = await AskarController(client_id).fetch("verificationMethods", cred_def_tag)
    did_doc = {
        '@context': 'https://www.w3.org/ns/did/v1',
        'id': f'{settings.DID_WEB}:{client_id}:definitions:{cred_def_tag}',
        'controller': f'{settings.DID_WEB}:{client_id}',
        'verificationMethod': [verification_method],
        'service': [service]
    }
    return did_doc


@router.post("/definitions/{cred_def_tag}", dependencies=[Depends(JWTBearer())])
async def activate_cred_def(cred_def_tag: str, request_body: ActivateDefinition, request: Request):
    access_token = request.headers.get("Authorization")
    decoded_token = base64.b64decode(access_token.split(".")[1] + "==").decode()
    client_id = json.loads(decoded_token)["client_id"]
    issuer_did = await AskarController(client_id).fetch("client", "did")
    jwt = vars(request_body)["jwt"]
    cred_def = await AskarController(issuer_did).fetch("cred_def_pub", cred_def_tag)
    jwt_payload = json.loads(jwt.split('.')[1])
    if jwt_payload == cred_def:
        await AskarController(issuer_did).update("cred_def_pub", cred_def_tag, [jwt])
        return {"message": "Cred Def Verified"}
    return {"message": "Cred Def Invalid"}
