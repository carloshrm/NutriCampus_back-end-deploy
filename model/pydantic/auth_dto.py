
from pydantic import BaseModel

class Signin(BaseModel):
    email: str
    senha: str

class JWT(BaseModel):
    access_token: str
    token_type: str

class JWTPayload(BaseModel):
    usuario_id: str | None = None