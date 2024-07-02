from pydantic import BaseModel, Field
from config import settings


class Setup(BaseModel):
    name: str = Field("Example Name", example="Example Name")
    size: int = Field(10, example=10)
    attributes: list = Field(["exampleAttribute"], example=["exampleAttribute"])
    revocation: bool = Field(True, example=True)
