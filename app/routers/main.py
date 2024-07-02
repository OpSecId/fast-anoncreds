from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from config import settings
from app.plugins.askar import AskarController
from app.models.web_requests import Setup
from anoncreds import (
    Schema,
    CredentialDefinition,
    RevocationRegistryDefinition,
    RevocationStatusList,
)
import base64
import json
import uuid

router = APIRouter()


@router.get("/")
async def return_object(
    schema: str = None,
    definition: str = None,
    revocation: str = None,
    verification: str = None,
    accumulator: str = None,
):
    if schema:
        return JSONResponse(
            status_code=200, content=await AskarController().fetch("schema", schema)
        )
    if definition:
        return JSONResponse(
            status_code=200,
            content=await AskarController().fetch("credDef", definition),
        )
    if revocation:
        return JSONResponse(
            status_code=200,
            content=await AskarController().fetch("revRegDef", revocation),
        )
    if accumulator:
        return JSONResponse(
            status_code=200,
            content=await AskarController().fetch("revList", accumulator),
        )
    if verification:
        return JSONResponse(
            status_code=200,
            content=await AskarController().fetch("verDoc", verification),
        )
    return RedirectResponse(url=settings.DOCS)


@router.post("/")
async def setup(request_body: Setup):
    name = vars(request_body)["name"]
    size = vars(request_body)["size"]
    attributes = vars(request_body)["attributes"]
    revocation = vars(request_body)["revocation"]

    schema = Schema.create(name, "1.0", settings.DID_WEB, attributes)
    schema_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(schema.to_dict())))
    schema_id = f"{settings.HTTPS_BASE}?schema={schema_uuid}"
    await AskarController().force_store("schema", schema_uuid, schema.to_dict())
    cred_def_tag = name
    cred_def_pub, cred_def_priv, cred_def_correctness = CredentialDefinition.create(
        schema_id,
        schema.to_dict(),
        settings.DID_WEB,
        cred_def_tag,
        "CL",
        support_revocation=revocation,
    )
    cred_def_uuid = str(
        uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(cred_def_pub.to_dict()))
    )
    cred_def_id = f"{settings.HTTPS_BASE}?definition={cred_def_uuid}"
    await AskarController().force_store("credDef", cred_def_uuid, cred_def_pub.to_dict())
    anoncreds_objects = {
        "schema": schema.to_dict(),
        "cred_def_pub": cred_def_pub.to_dict(),
        "cred_def_priv": cred_def_priv.to_dict(),
        "cred_def_correctness": cred_def_correctness.to_dict(),
    }
    public_keys = (
        cred_def_pub.to_dict()["value"]["primary"] | cred_def_correctness.to_dict()
    )
    if revocation:
        public_keys |= cred_def_pub.to_dict()["value"]["revocation"]
        rev_tag = name
        (rev_reg_def_pub, rev_reg_def_private) = RevocationRegistryDefinition.create(
            cred_def_id, cred_def_pub, settings.DID_WEB, rev_tag, "CL_ACCUM", size
        )
        rev_reg_def_uuid = str(
            uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(rev_reg_def_pub.to_dict()))
        )
        rev_reg_def_id = f"{settings.HTTPS_BASE}?revocation={rev_reg_def_uuid}"
        await AskarController().force_store(
            "revRegDef", rev_reg_def_uuid, rev_reg_def_pub.to_dict()
        )
        anoncreds_objects["rev_reg_def_pub"] = rev_reg_def_pub.to_dict()
        anoncreds_objects["rev_reg_def_private"] = rev_reg_def_private.to_dict()
        time_create_rev_status_list = 12
        revocation_status_list = RevocationStatusList.create(
            cred_def_pub,
            rev_reg_def_id,
            rev_reg_def_pub,
            rev_reg_def_private,
            settings.DID_WEB,
            True,
            time_create_rev_status_list,
        )
        rev_list_uuid = str(
            uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(revocation_status_list.to_dict()))
        )
        rev_list_id = f"{settings.HTTPS_BASE}?accumulator={rev_list_uuid}"
        await AskarController().force_store(
            "revList", rev_list_uuid, revocation_status_list.to_dict()
        )
        anoncreds_objects['revocation_status_list'] = revocation_status_list.to_dict()
    verification_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(public_keys)))
    verification_id = f"{settings.HTTPS_BASE}?verification={verification_uuid}"
    verification_document = {
        "id": verification_id,
        "type": "AnonCreds-CL",
        "publicKeys": public_keys,
    }
    await AskarController().force_store("verDoc", verification_uuid, verification_document)
    anoncreds_objects["identifiers"] = {
        "schema": schema_id,
        "credentialDefinition": cred_def_id,
        "revocationRegistry": rev_reg_def_id,
        "revocationList": rev_list_id,
        "verificationDocument": verification_id
    }
    return JSONResponse(status_code=201, content=anoncreds_objects)
