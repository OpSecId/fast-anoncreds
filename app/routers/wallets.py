from fastapi import APIRouter
from config import settings
from app.models import *
from mnemonic import Mnemonic
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

# @router.get("", tags=["Wallets"], summary="List wallets")
# async def list_wallets():
#     return ""


@router.post("", tags=["Wallets"], summary="Create wallet")
async def create_wallet():
    # mnemo = Mnemonic("english")
    # words = mnemo.generate(strength=256)
    # seed = mnemo.to_seed(words, passphrase="")
    # entropy = mnemo.to_entropy(words)

    link_secret = create_link_secret()
    link_secret_id = "default"
    link_secret = {"id": link_secret_id, "link_secret": link_secret}
    return link_secret
