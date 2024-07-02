from pydantic import BaseModel, Field
from config import settings
import uuid

class Setup(BaseModel):
    name: str = Field('example', example='example')
    attributes: list = Field([], example=[])
    size: int = Field(10, example=10)
    revocation: bool = Field(False, example=False)
    publish: bool = Field(False, example=False)
