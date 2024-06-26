from pydantic import BaseModel, Field
from config import settings
import uuid

EXAMPLE_CRED_DEF_ID = f"{settings.DID_WEB}#7ee0620ab8db88bcc485f1fd0d1358cf"
EXAMPLE_SCHEMA_NAME = "ExampleCredential"
EXAMPLE_ATTRIBUTES = ["email"]
EXAMPLE_CREDENTIAL = {
    "@context": [""],
    "type": ["VerifiableCredential"],
    "credentialSubject": {"email": "patrick.st-louis@opsecid.ca"},
}
EXAMPLE_KEY_PROOF = "eyJjIjogIjI2NjUwMjU1MjM5MTQ0Nzg3MjMwMzIyOTQ5MTI4OTIyNDM1NzU5MzE2NzIyMjk0OTQ4MTgyMzQzNjQyOTQ2Mzc2NDAwMzA2NzA2MzE2IiwgInh6X2NhcCI6ICI1NzcxMzIwNzY1OTExODY5MDA5MDkxMjQxMTU1ODkxMzA2Mjk3NTU3MjY4Mjg4ODUzODQ0NTI3ODMwODU4NjYyMzk1NjQyMTY0MzI5MjEzNDAzNzE2MDQzMjI3MDYwNzQ0MjU0OTA1NzM5MDg0ODc0MTE2NjI5NzA0NzIyNjk1MjU2ODUwMjY2NzAzNjIzNDIyNTIxNDM2NzIyMDQyMjM1MjQ5NjU5ODA1MjU2MzE4MzQxNDk0MzY2MzQ2NDQzNTE1NzAwNTQ2Nzk1Njc1Njc4ODQxNTU5ODUxNTQzMTcwNTM1MTA5MjExODM5MzAzNDYxMTkzOTA1MzAyNDQwMjEzMDI5OTUyNTU5NTc2OTgwOTU1MDk4MjU4MDQ1OTI0MTA2NzUwNzEwNzk1MDc4NjE5NDAyMDQ1MDgxMDYyOTk1MzEyNDI2MTcxNTQ5MDg0OTAyMDAwNjc1ODA3NjY4NDY1MjU4OTk2OTQ2NzIxMDkyMjA0MDQwNzU5MjA0Njc2MDk5MTU5MzQ0Njg3MDkzMTkyMTk1MzAyODAzMTY3NTA4Mzc5NTQwMzk2MDg3MTk3ODQxNDQ2NDQ1NTE0NzEwNjUxMjA2ODk0MzAwMzM1MzUzNjU2MTcwMDY2Mzg3MjYyODQyNDQ4NzQ2NjMxODkzMjUwODg1MzMzMjQ2Nzg2MDkwOTg4MTY2MjUyMjExOTA4Mjc3MDU1Njg0MjQ4Mzk0MDI3NTAyNzE4MzYxMjM2MzE1MTYxMTY1Mjk4ODA3MDgyMDUzNDkwODM4NTQyNTQzMzMyMjY2ODkzMDM0NDE4Njc1NTE4ODMxNjQ1NTE1Mzg5Mzk2MjEyNTQ2MDkxMzkyNzc2ODM4NjcxMTA3NDg0NjQ4NDM4MjE3NjcxMzE1ODg1MzUxNDc3ODM3ODMxNjI4OTA4OTcxNDgiLCAieHJfY2FwIjogW1sibWFzdGVyX3NlY3JldCIsICIyNDUyMjc5NTI4MjQ3OTg2MjkzODc4MDY1NzYxNjgzOTYwODQ2NTg0ODMxNzEyNzE3MTgyOTA1NjM4NzM3NTY1OTY4NzAyMDYwODMxNTc0MjU3NDgyMDY2MjM1MjYxNjI2ODgzODUxMDA4NTAwMTQxNDYxMzI4Nzg2NTU1MzQ4NTYzNjQyMjg5MTc3MDA5MTk2Njc3MDI2MjE5MTg3MzI4NzI5ODE0MTE4OTczNzY5NDMwOTkyMzE1MjcyMzY5OTg5MzQ4OTA4OTcxODY4MTA3NzcwNzY4NzIwNDEwNDIwNDkzODQ4NjQxMTc5MTE2MjcxNjE5NTcxMzQyNDU2ODE2MjY2MjAyODQ1NzY3Mzg1NDg3MDY3NDgwMDYyNTc4MTY2MTY3NzgzODUzNzAzODI3Njc2OTI0MDU4ODI1MjM5NTQzNzMyNTUyMzgwNTI5ODMzNjk5MTg0NzMxNjQyOTgxOTE5MDQzODkyMTg5MjAxMzA0MTkxMjQ2ODc4NDYzMzQyMTU1OTIxOTQ5ODA4MzExNTIyNDY1MTQ5OTQzOTA2OTUyNDk4MDgxNzAzMTEzNjUxNTMwMDU0MDA1MTIzODc2Mzg1Mjc0MDg0MzY3NjU2NjE0MTAwODc0MDg3MzY1OTg2MDcwMjUwMzgzOTIzMzY5Njk2NDExODkyMzYwNDY0OTQ0NTY5Mjg3MjAwODIwNzA4OTYwNTQ0Mjk5NTgxMjQ1NDAwNTAwNjQxODQxNTU1OTIyMTE3MjYzMjY1NTc1NDk5NjYxMjkyNDI4NzcxNDA4MDgwNDcwOTU0OTI3NzQ5MDg4MDQxMTk0Mzc5MzM4NjI3ODM0NjI1Mzk1MDE1MTk0ODcxMDE0OTIzNzcwMzUwMzEwNTU0NjYzODE0NDcwNjIxMDUxODAxMDU2MTg0NDIxNTI1MjkiXSwgWyJlbWFpbCIsICIzNzY1Mjk4NTI4NDM0NzY4NTU1NjE4MzEzMTcxMDIwMjQyMzAzNzU3MzkyNjg0NjI0NDIwMjA5MDIwNjk0MzU3MDAxMzUyNDEyNTE0Mzk0OTYxNDc3OTk3MDYyOTEwMDkyMTQ1MDI4NjYzOTk4Njk1MzE4Nzc3OTU1NzU1MjY3OTQ5MDc5OTY3MzU1NTA2NTY2NTcyMDQ5NzQyMDUyNTA0MDkyODkyMDg2Mzc1ODU1OTgyNzYzNzczNjcwMjMyNTIyMTYzMDc3Mjc1NjYzMzc2NjY4MTkxMzcxOTE3MDk1OTkyNjYyMDMzNDE0OTIyMzc1NTc1NDc3NjczNjY4NzgyNDc5NTIzODg4MzkyNTkzMzkxMDIwNjM5NDYzNTU2OTE1NDEyNjgwMDYyNzcyNjgzOTc2MzgxMjcwMzk4NzUxMTgzMDI5ODQ1MDk0MjQ3MzUwMTYyMTA1ODQxMTY5NjE0NDUwODM2NTI4MzcwMTEyNjkxMzY0NjAzNTk1OTE0MDcyNjAxMDM3NTY1ODMzMjA2MTcxNTg0MDczNTc1MDkyMTI2MTQ1MTY1NjE5NjM0NTQ1NTcwMDQ2ODUzNzY0NjcxMTQyMzA5NjU5NTE2MjQwNDAyNTcwMzc5ODExOTMwODU3NDY0NDcxNjEwNTM3NDU1NTc5NDM1MTQzODE2MjY4NzM5MTE2MjMwMTU0OTQxNzM0NzA1MzI4MTU3NzYyMTQ4NDA3OTMyNDc2NjI1NzE4MDA0MDcxODg4MzAwNjc5MjAyMjA4NjYxOTA2MDQ5OTI3MDE1NjA4MzEwNzc3NzYxMTg5MjgwMDcxNjEyMzQ2NDYxOTExNzg3ODA2NTE4NDc0ODE2OTIxMDE4NjI4MTAyMTg2NDU0OTM0MDg1MjExMzQyMDUyMDM2MDYxMTk3NzQ3NTEwMDAiXV19"
EXAMPLE_BLINDED_LINK = "eyJ1IjogIjUyMDAxOTAyMjM0NzkyMzA1MjE0Mzc3Njk3NDE3MjA3NzYyMDM5ODUxMzcwNDI5ODUzMDI1OTgzOTY0NjQ3MTAyNjc1MTY0ODU1OTIzMjMzNjc1NjQ1MDAzOTI0NTI3NDQyMzA5MTg2ODc3MTE4MTk5MTYzNDM5NzU0ODQwNzkxNDk0MzM5NzQ5MjY5Nzc3MDA4MDY2MTE4OTkzMzk4MDA0MDcxMDU1NjA4MjE0NDcyNDU4NDkxNjQwOTE0NDIzMzMzOTY1NjA0MTg2NzE2MDA1MTI0Nzc2MDM1NjExMDg5MTAxNzk1MDYyMzk1MjM4ODE2NTgzNjc4MjE4OTU0OTI0NjU5NDU4Mzc4NTA5OTY0MDM3NDM1ODMxNTY1ODQ0MjkwOTQxNjE1Njg0NDEwNjg3MDc1ODg4NDc2ODAyNzMwNDIzMTI1NjM1NTY0NjUxNTcyMzEzNzUwOTE4NTY5MjMzMzMxMjY3Mzc1NjQ1MDk1NjY0NTgyMzY2MDQzNTE0ODMzNDY1OTAwMjYwMTY2NjU2MTc1Njk1NDY0OTQ5MDU0NzcwOTA2ODI3MTk3NjkzMzMzMTY1NTY4OTc1MzA1NDk0ODEwMjY4NDIxODY4MDMwMjUxNDcxMTM0ODU3NjU1MDQ3MDc2MTc1NTYzMjgwMDc5NzUyNDU5MDQwNTE3NTIxMjMzMDI4OTU3NDkyMDEzMDU5Nzk2NDMzODQ3NjQzODU3MzUyOTA4NjUxNDg4NTE2NDE4NDYyOTk4NjExNDk3MzEwMzIxMzM5NTUxNjk3NTE2MTAyNTU5MjI5NTc1NjQxNTc1NDQ2OTkxIiwgInVyIjogbnVsbCwgImhpZGRlbl9hdHRyaWJ1dGVzIjogWyJtYXN0ZXJfc2VjcmV0Il0sICJjb21taXR0ZWRfYXR0cmlidXRlcyI6IHt9fQ=="
EXAMPLE_BLINDED_LINK_PROOF = "eyJjIjogIjEwMTQyNzg5NDY3OTgzNTAyNTM0NjIwNzIwNTI2MTAzNTYxNTEzMTcwMjQxNTA1MzYyNTg5NTIyMDAxMzg3MzIyNzMyMDA5OTkwNjQ2OCIsICJ2X2Rhc2hfY2FwIjogIjExNTQ1MDM2MzI1NTE3ODI5MDgxNTAyOTcyMTg1ODYyNTk5NTUyNDQ0ODczNDY0MTIwMDc1NjQ5NTU0NTg5NTE1ODk4MjE0NzIzMjA4MjQ2OTg3ODg1MzMyODE3MjY3OTc5NzMzMTEzNDI1MTE4Mzg0MzgyMjgyODM1MzM1NTczMTgzNDU5MDgzODc4MTQ0NjM1MjU2ODc5Njc4NjcyNjIyMTMyNDU4NDY3OTAwNzQ2OTAwOTc5NTQ2Mjg3OTM5OTMxNDM3MzQ4NzE1ODcwMzg4MzkwOTcwNDAwOTEyMTY5NzU3Mzg2NDIxOTI1ODE1Mzk0MDQ2OTA3Njk4OTc0NjEwMjk0MTMyMDQ0OTI1ODk0ODExNzcxMzc2NTMwODA0OTQ0OTQwNzM3NDE1MTUyMjEyMDM4Mzk3NTE2MzM2MzA1Mjg5NjE0MDIxODcwOTUyMzI4MzgwNzQyMzkxNDM2ODc5Mjk0ODAyOTA0NDM4MjMyOTI1Mjg3NzUyMjY3OTc0MTIxMDYyNDUzNjY1MzE2OTk1MjA0NDM0NDA1OTYyNjg4NjY3MzU2MjY2MTY1ODEyNDE1MzcxOTU0OTY5MTIyNzM0ODAwMjEyMTU3NTkyNzU3NDQ2MDA1NjQzMTIyNzkzNTM0NDgzNzgyOTExNzM4MzcyODkyODQwMjY1MzQyNDM1NTU1MDY2NDE5NDY2NTY3MDY1NDA3NDQ0Mzk5MTAyMDk1NTQ0NzM3NDMzNjIxNjYyMzUxNjQwNjEzMDU0NzYwNTE2OTUzMDg1MDA2NjgyMzIzMjgwMDc1MTY4MTgyNjc1MTA1MTcwNzU3ODkxNTYyODA1NDY0MTEwMDA0NDQ0NzAxNDczMTI5NTc1NDc5MjIzMjM1MjA5NjI5NDg1ODE1Njc3MTA1ODAwMjQ0NzAxOTQzMTYxOTQ2NzU2NTEzOTQxODg2MDQ3NDk5OTQ3MzAiLCAibV9jYXBzIjogeyJtYXN0ZXJfc2VjcmV0IjogIjQ4NDAyNTI5MjM5NDkwMzc4NzQ5MTA1NzU5MjI0OTE0NjQ2NzQwOTcyODkzMjY2MTA1OTE0MzMzOTYyNjE2NzYwNTYwMDU4NDE4MjAxMzY3NDQ5ODUxNTM3MDUzMTgxNTExMjIyOTM1NTY2NzkyNDc0MzgzMzM2MjM2NjkzNjMzMDM4NzA3Mjg3NjkyMTk1NTc2ODM3MjcwMTYzODc2NzkzNTk3ODMyOTM0NzM4OTYwNDMifSwgInJfY2FwcyI6IHt9fQ=="


EXAMPLE_OFFER_OPTIONS = {"verificationMethod": EXAMPLE_CRED_DEF_ID}
EXAMPLE_OFFER = {
    "credentialSubject": EXAMPLE_CREDENTIAL["credentialSubject"],
    "proof": {
        "nonce": "1075362810065105604429888",
        "keyProof": EXAMPLE_KEY_PROOF,
        "verificationMethod": EXAMPLE_CRED_DEF_ID,
    },
}
EXAMPLE_REQUEST_OPTIONS = {"linkSecretId": str(uuid.NAMESPACE_URL)}
EXAMPLE_ISSUANCE_OPTIONS = {
    "nonce": "",
    "entropy": "",
    "keyProof": EXAMPLE_KEY_PROOF,
    "blindedLink": EXAMPLE_BLINDED_LINK,
    "blindedLinkProof": EXAMPLE_BLINDED_LINK_PROOF,
    "credentialId": uuid.uuid4(),
    "verificationMethod": EXAMPLE_CRED_DEF_ID,
}
EXAMPLE_JWT = 'ey..ey'


class RegisterClient(BaseModel):
    did: str = Field(None, example=settings.DID_WEB)
    managed: bool = Field(False, example=False)

class DefineCredential(BaseModel):
    type: str = Field(None, example=EXAMPLE_SCHEMA_NAME)
    # version: str = Field(None, example='1.0')
    recreate: bool = Field(False, example=False)
    attributes: list = Field(None, example=EXAMPLE_ATTRIBUTES)

class ActivateDefinition(BaseModel):
    jwt: str = Field(None, example=EXAMPLE_JWT)

class OfferCredential(BaseModel):
    credential: dict = Field(None, example=EXAMPLE_CREDENTIAL)
    options: dict = Field(None, example=EXAMPLE_OFFER_OPTIONS)

class RequestCredential(BaseModel):
    credentialOffer: dict = Field(None, example=EXAMPLE_OFFER)
    options: dict = Field(None, example=EXAMPLE_REQUEST_OPTIONS)

class IssueCredential(BaseModel):
    credential: dict = Field(None, example=EXAMPLE_CREDENTIAL)
    options: dict = Field(None, example=EXAMPLE_ISSUANCE_OPTIONS)
