from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from model.pydantic.auth_dto import JWT, Signin
from model.pydantic.usuario_dto import Usuario_DTO
from model.usuario import Usuario
from services.auth_service import Auth_Service, oauth2_scheme
from services.usuario_service import Usuario_Service

router = APIRouter()

async def get_user_current(token: str  = Depends(oauth2_scheme), usuario_service: Usuario_Service = Depends(), auth_service: Auth_Service = Depends()):
    try:
      payload = auth_service.decode_token(token)
      id = payload.get("sub")
      if not payload or not id:
        raise InvalidTokenError()

    except InvalidTokenError:
      raise HTTPException(status.HTTP_401_UNAUTHORIZE, detail="Token inválido")

    user = usuario_service.get_by_id(id)
    if not user:
      raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return user


@router.get("/auth/me")
async def get_me(current_user: Usuario_DTO = Depends(get_user_current)):
  return current_user


@router.post("/auth/signin")
async def usuario_signin(credentials: Signin, auth_service: Auth_Service = Depends(), usuario_service: Usuario_Service = Depends()):
  user = usuario_service.get_by_email(credentials.email)
  if not user:
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos")
  
  if not auth_service.check_password(credentials.senha, user.senha):
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos")
  
  token = auth_service.make_token({"sub": user.id})
  return JWT(access_token=token, token_type="bearer")


@router.post("/auth/signup")
async def usuario_signup(usuario: Usuario_DTO, usuario_service: Usuario_Service = Depends(), auth_service: Auth_Service = Depends()):
  usuario_existente = usuario_service.get_by_email(usuario.email)
  if usuario_existente:
    raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

  usuario.senha = auth_service.get_password_hash(usuario.senha)
  novo_usuario = Usuario(**usuario.model_dump())
  usuario_criado = usuario_service.create(novo_usuario)
  token = auth_service.make_token({"sub": usuario_criado.id})
  return JWT(access_token=token, token_type="bearer")