from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Settings(BaseSettings):
    PROJECT_TITLE: str = "fast-anoncreds"
    PROJECT_VERSION: str = "v0"
    PROJECT_DESCRIPTION: str = """
    VC-API implementation of the anoncreds-rs python wrapper with did:web method
    """
    PROJECT_CONTACT: dict = {
        "name": "OpSecId",
        "url": "https://github.com/OpSecId",
    }
    PROJECT_LICENSE_INFO: dict = {
        "name": "Apache License",
        "url": "https://github.com/OpSecId/fast-anoncreds/blob/main/LICENSE",
    }

    DOMAIN: str = os.environ["DOMAIN"]
    DID_WEB: str = f"did:web:{DOMAIN}"
    HTTPS_BASE: str = f"https://{DOMAIN}"
    DOCS: str = os.environ["DOCS"]
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    POSTGRES_URI: str = os.environ["POSTGRES_URI"]


settings = Settings()
