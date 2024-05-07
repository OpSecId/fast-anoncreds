from fastapi import APIRouter, Depends, Request
from config import settings
from app.models.web_requests import (
    DefineCredential,
    OfferCredential,
    RequestCredential,
    IssueCredential,
)
import json
import base64
import uuid
import brotli
from app.controllers.askar import AskarController
from app.auth.bearer import JWTBearer
from anoncreds import (
    generate_nonce,
    CredentialDefinition,
    CredentialOffer,
    CredentialRequest,
    Schema,
    W3cCredential,
)
from pprint import pprint

router = APIRouter()


@router.post("/define", dependencies=[Depends(JWTBearer())])
async def define_credential(request_body: DefineCredential, request: Request):
    access_token = request.headers.get("Authorization")
    decoded_token = base64.b64decode(access_token.split(".")[1] + "==").decode()
    client_id = json.loads(decoded_token)["client_id"]

    # issuer_did = await AskarController(client_id).fetch("client", "did")
    issuer_did = f'{settings.DID_WEB}:{client_id}'
    recreate = vars(request_body)["recreate"]
    schema_name = vars(request_body)["type"]
    schema_version = "1.0"
    attributes = vars(request_body)["attributes"]
    # attributes.append('id') if 'id' not in attributes else attributes

    schema = Schema.create(schema_name, schema_version, issuer_did, attributes)
    await AskarController(client_id).update(
        "schemas", schema_name, schema.to_dict()
    ) if recreate else await AskarController(client_id).store(
        "schemas", schema_name, schema.to_dict()
    )

    # schema_id = f"{settings.HTTPS_BASE}/schemas/{schema_name}?author={client_id}"
    # schema_id = f"did:vdr:{settings.DOMAIN}:{client_id}/schemas/{schema_name}"
    # schema_id = f"{issuer_did}:schemas:{schema_name}"
    cred_def_tag = schema_name
    schema_id = f'{settings.DID_WEB}:{client_id}:definitions:{cred_def_tag}#schema'
    cred_def_pub, cred_def_priv, cred_def_correctness = CredentialDefinition.create(
        schema_id,
        schema.to_dict(),
        issuer_did,
        cred_def_tag,
        "CL",
        support_revocation=False,
    )
    cred_def_hash = str(uuid.uuid5(
        uuid.NAMESPACE_URL, json.dumps(cred_def_pub.to_dict(), separators=(",", ":"))
    ))
    cred_def_id = f"{issuer_did}#{cred_def_hash}"
    await AskarController(client_id).update(
        "cred_def_pub", cred_def_tag, cred_def_pub.to_dict()
    ) if recreate else await AskarController(client_id).store(
        "cred_def_pub", cred_def_tag, cred_def_pub.to_dict()
    )
    await AskarController(client_id).update(
        "cred_def_priv", cred_def_tag, cred_def_priv.to_dict()
    ) if recreate else await AskarController(client_id).store(
        "cred_def_priv", cred_def_tag, cred_def_priv.to_dict()
    )
    await AskarController(client_id).update(
        "cred_def_correctness", cred_def_tag, cred_def_correctness.to_dict()
    ) if recreate else await AskarController(client_id).store(
        "cred_def_correctness", cred_def_tag, cred_def_correctness.to_dict()
    )

    # cred_def_endpoint = f"{settings.HTTPS_BASE}/definitions/{cred_def_tag}?issuer={client_id}"
    # cred_def_endpoint = f"did:vdr:{settings.DOMAIN}:{client_id}/definitions/{cred_def_tag}"
    cred_def_endpoint = f"{issuer_did}:definitions:{cred_def_tag}"

    service = {
        "id": cred_def_id,
        "type": "AnonCredsVDR",
        "serviceEndpoint": cred_def_endpoint,
    }
    jwk = cred_def_pub.to_dict()['value']['primary']
    jwk['n'] = 'u'+base64.urlsafe_b64encode(int(jwk['n']).to_bytes(256+1, byteorder='big')).decode().rstrip('=')
    jwk['s'] = 'u'+base64.urlsafe_b64encode(int(jwk['s']).to_bytes(256+1, byteorder='big')).decode().rstrip('=')
    jwk['rctxt'] = 'u'+base64.urlsafe_b64encode(int(jwk['rctxt']).to_bytes(256+1, byteorder='big')).decode().rstrip('=')
    jwk['z'] = 'u'+base64.urlsafe_b64encode(int(jwk['z']).to_bytes(256+1, byteorder='big')).decode().rstrip('=')
    for item in jwk['r']:
        jwk['r'][item] = 'u'+base64.urlsafe_b64encode(int(jwk['r'][item]).to_bytes(256+1, byteorder='big')).decode().rstrip('=')
    jwk = {"typ": "CL-RSA", "kid": cred_def_hash} | jwk
    verification_method = {
        "id": cred_def_id,
        "type": 'JsonWebKey',
        # "controller": f"did:web:{settings.DOMAIN}:{client_id}",
        "controller": issuer_did,
        "publicKeyJwk": jwk
    }
    await AskarController(client_id).update(
        "verificationMethods", cred_def_tag, verification_method
    ) if recreate else await AskarController(client_id).store(
        "verificationMethods", cred_def_tag, verification_method
    )
    did_doc = await AskarController(client_id).fetch("client", "didDoc")
    did_doc['service'].append(service)
    await AskarController(client_id).update("client", "didDoc", did_doc)
    return {
        'service': service,
        # 'verificationMethod': verification_method
        }


@router.post("/offer", dependencies=[Depends(JWTBearer())])
async def offer_credential(request_body: OfferCredential, request: Request):
    access_token = request.headers.get("Authorization")
    decoded_token = base64.b64decode(access_token.split(".")[1] + "==").decode()
    client_id = json.loads(decoded_token)["client_id"]
    
    attributes = vars(request_body)["credential"]["credentialSubject"]
    cred_def_id = vars(request_body)["options"]["verificationMethod"]
    cred_def_hash = cred_def_id.split("#")[-1]
    cred_def_tag = 'ExampleCredential'
    
    cred_def_pub = await AskarController(client_id).fetch("cred_def_pub", cred_def_tag)
    cred_def_correctness = await AskarController(client_id).fetch(
        "cred_def_correctness", cred_def_tag
    )
    cred_offer = CredentialOffer.create(
        cred_def_pub["schemaId"], cred_def_id, cred_def_correctness
    )
    key_proof = cred_offer.to_dict()["key_correctness_proof"]
    key_proof_compressed = brotli.compress(
        json.dumps(key_proof, separators=(",", ":")).encode()
    )
    key_proof_encoded = 'u'+base64.urlsafe_b64encode(key_proof_compressed).decode().rstrip('=')
    cred_offer = {
        "id": str(uuid.uuid4()),
        "credentialSubject": attributes,
        "credentialSchema": {"id": cred_def_pub["schemaId"]},
        "proof": {
            "verificationMethod": cred_def_id,
            "nonce": cred_offer.to_dict()["nonce"],
            "keyProof": key_proof_encoded,
        },
    }
    await AskarController(client_id).store("offer", cred_offer["id"], cred_offer)
    return {"credentialOffer": cred_offer}


@router.post("/request", dependencies=[Depends(JWTBearer())])
async def request_credential(request_body: RequestCredential, request: Request):
    access_token = request.headers.get("Authorization")
    decoded_token = base64.b64decode(access_token.split(".")[1] + "==").decode()
    client_id = json.loads(decoded_token)["client_id"]
    
    cred_offer = vars(request_body)["credentialOffer"]
    schema_id = cred_offer["credentialSchema"]["id"]
    schema_name = schema_id.split(':')[-1].split('#')[0]
    issuer_did = cred_offer["proof"]["verificationMethod"].split("#")[0]
    
    cred_def_pub = await AskarController(client_id).fetch("cred_def_pub", schema_name)
    
    key_proof_encoded = cred_offer["proof"]["keyProof"]
    key_proof_compressed = base64.urlsafe_b64decode(key_proof_encoded[1:]+'==')
    key_proof = brotli.decompress(key_proof_compressed).decode()
    
    cred_def_pub = {
        "schemaId": schema_id,
        "type": "CL",
        "tag": schema_name,
        "issuerId": issuer_did,
        "value": {"primary": cred_def_pub["value"]["primary"]},
    }
    cred_offer = {
        "nonce": cred_offer["proof"]["nonce"],
        "schema_id": schema_id,
        "cred_def_id": cred_offer["proof"]["verificationMethod"],
        "key_correctness_proof": json.loads(key_proof),
    }
    
    link_secret_id = vars(request_body)["options"]["linkSecretId"]
    link_secret = await AskarController(client_id).fetch("link_secret", link_secret_id)
    entropy = generate_nonce()
    cred_request, cred_request_metadata = CredentialRequest.create(
        entropy, None, cred_def_pub, link_secret, link_secret_id, cred_offer
    )

    blinded_ms = cred_request.to_dict()["blinded_ms"]
    blinded_ms_compressed = brotli.compress(
        json.dumps(blinded_ms, separators=(",", ":")).encode()
    )
    blinded_ms_encoded = 'u'+base64.urlsafe_b64encode(blinded_ms_compressed).decode().rstrip('=')

    blinded_ms_proof = cred_request.to_dict()["blinded_ms_correctness_proof"]
    blinded_ms_proof_compressed = brotli.compress(
        json.dumps(blinded_ms_proof, separators=(",", ":")).encode()
    )
    blinded_ms_proof_encoded = 'u'+base64.urlsafe_b64encode(blinded_ms_proof_compressed).decode().rstrip('=')

    cred_request = {
        "id": vars(request_body)["credentialOffer"]["id"],
        "credentialSchema": vars(request_body)["credentialOffer"]["credentialSchema"],
        "credentialSubject": vars(request_body)["credentialOffer"]["credentialSubject"],
        "proof": {
            "verificationMethod": cred_offer["cred_def_id"],
            "nonce": cred_request.to_dict()["nonce"],
            "entropy": cred_request.to_dict()["entropy"],
            "keyProof": key_proof_encoded,
            "blindedLinkSecret": blinded_ms_encoded,
            "blindedLinkProof": blinded_ms_proof_encoded,
        },
    }
    return {"credentialRequest": cred_request}


@router.post("/issue", dependencies=[Depends(JWTBearer())])
async def issue_credential(request_body: IssueCredential, request: Request):
    access_token = request.headers.get("Authorization")
    decoded_token = base64.b64decode(access_token.split(".")[1] + "==").decode()
    client_id = json.loads(decoded_token)["client_id"]
    credential = vars(request_body)["credential"]
    options = vars(request_body)["options"]
    
    # credential['credentialSubject']['id'] = credential['credentialSubject']['id'] if 'id' in credential['credentialSubject'] else 'urn:anonymous'
    
    schema_id = credential["credentialSchema"]["id"]
    schema_name = schema_id.split(':')[-1].split('#')[0]
    cred_offer = await AskarController(client_id).fetch("offer", credential["id"])
    cred_def_pub = await AskarController(client_id).fetch("cred_def_pub", schema_name)
    cred_def_priv = await AskarController(client_id).fetch(
        "cred_def_priv", schema_name
    )

    key_proof = brotli.decompress(base64.urlsafe_b64decode(options["keyProof"][1:]+'==')).decode()
    blinded_ms = brotli.decompress(base64.urlsafe_b64decode(options["blindedLinkSecret"][1:]+'==')).decode()
    blinded_ms_proof = brotli.decompress(base64.urlsafe_b64decode(options["blindedLinkProof"][1:]+'==')).decode()

    cred_offer = {
        "nonce": cred_offer["proof"]["nonce"],
        "schema_id": credential["credentialSchema"]["id"],
        "cred_def_id": options["verificationMethod"],
        "key_correctness_proof": json.loads(key_proof),
    }
    cred_request = {
        "nonce": options["nonce"],
        "entropy": options["entropy"],
        "cred_def_id": options["verificationMethod"],
        "blinded_ms": json.loads(blinded_ms),
        "blinded_ms_correctness_proof": json.loads(blinded_ms_proof),
    }
    vc = W3cCredential.create(
        cred_def_pub,
        cred_def_priv,
        cred_offer,
        cred_request,
        credential["credentialSubject"],
        w3c_version="2.0",
    )
    vc = vc.to_dict()
    vc["@context"] = [vc["@context"][0]]
    vc['type'].append(schema_name)
    vc['credentialSchema'] = {'id': schema_id}
    vc['credentialSchema']['type'] = ['AnonCredsVDR']

    return {"verifiableCredential": vc}
