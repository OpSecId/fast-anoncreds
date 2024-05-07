from fastapi import APIRouter
from config import settings
from app.models import CreateSchemaInput
from anoncreds import (
    generate_nonce,
    create_link_secret,
    Credential,
    CredentialDefinition,
    CredentialOffer,
    CredentialRequest,
    CredentialRevocationConfig,
    CredentialRevocationState,
    PresentationRequest,
    Presentation,
    PresentCredentials,
    RevocationRegistryDefinition,
    RevocationStatusList,
    Schema,
)

router = APIRouter()


@router.post("", tags=["Schemas"], summary="Publish new schema to VDR")
async def create_schema(request_body: CreateSchemaInput):
    schema = vars(request_body)
    issuer_id = f"did:web:{settings.ENDPOINT}"
    schema_version = "1.0"
    schema = Schema.create(
        schema["name"], schema_version, issuer_id, schema["attributes"]
    )
    schema = schema.to_dict()
    return schema
