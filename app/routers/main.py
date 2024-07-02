from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config import settings
from app.models.web_requests import (
    Setup
)
from anoncreds import (
    Schema,
    CredentialDefinition,
    RevocationRegistryDefinition,
    RevocationStatusList,
)

router = APIRouter()


@router.post("")
async def setup(request_body: Setup):
    name = vars(request_body)["name"]
    attributes = vars(request_body)["r"]
    revocation = vars(request_body)["revocation"]
    size = vars(request_body)["size"]
    publish = vars(request_body)["publish"]
    
    schema = Schema.create(name, '1.0', settings.DID_WEB, attributes)
    schema_b64 = schema.to_dict()
    schema_id = f'{settings.HTTPS_BASE}?schema={schema_b64}'
    cred_def_tag = name
    cred_def_pub, cred_def_priv, cred_def_correctness = CredentialDefinition.create(
        schema_id,
        schema.to_dict(),
        settings.DID_WEB,
        cred_def_tag,
        "CL",
        support_revocation=revocation,
    )
    anoncreds_objects = {
        'schema': schema.to_dict(),
        'cred_def_pub': cred_def_pub.to_dict(),
        'cred_def_priv': cred_def_priv.to_dict(),
        'cred_def_correctness': cred_def_correctness.to_dict(),
    }
    cred_def_hash = 'xyz'
    cred_def_id = f'{settings.HTTPS_BASE}?definition={cred_def_hash}'
    if revocation:
        rev_tag = name
        (rev_reg_def_pub, rev_reg_def_private) = RevocationRegistryDefinition.create(
            cred_def_id, cred_def_pub, settings.DID_WEB, rev_tag, "CL_ACCUM", size
        )
        rev_reg_def_hash = 'xyz'
        rev_reg_id = f'{settings.HTTPS_BASE}?revocation={rev_reg_def_hash}'
        time_create_rev_status_list = 12
        revocation_status_list = RevocationStatusList.create(
            cred_def_pub,
            rev_reg_id,
            rev_reg_def_pub,
            rev_reg_def_private,
            settings.DID_WEB,
            True,
            time_create_rev_status_list,
        )
        anoncreds_objects['rev_reg_def_pub'] = rev_reg_def_pub.to_dict()
        anoncreds_objects['rev_reg_def_private'] = rev_reg_def_private.to_dict()
        anoncreds_objects['revocation_status_list'] = revocation_status_list.to_dict()
    if publish:
        cred_def_id = f'{settings.HTTPS_BASE}?verification={cred_def_hash}'
    return JSONResponse(status_code=200, content=anoncreds_objects)