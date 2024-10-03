import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from services.usuario_service import Usuario_Service
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRES_DELTA_MINUTES = os.getenv("JWT_EXPIRES_DELTA_MINUTES")

class Auth_Service:
  def __init__(self):
      self.password_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

  def check_password(self, plain_password, hashed_password):
      return self.password_ctx.verify(plain_password, hashed_password)

  def get_password_hash(self, password):
      return self.password_ctx.hash(password)

  def make_token(self, payload_info: dict):
      token_payload = payload_info.copy()
      expire = datetime.now(timezone.utc) + timedelta(minutes=30 if not JWT_EXPIRES_DELTA_MINUTES else int(JWT_EXPIRES_DELTA_MINUTES))

      token_payload.update({"exp": expire})
      token = jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
      return token

  def decode_token(self, token: str):
      return jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)