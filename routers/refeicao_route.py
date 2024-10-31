from fastapi import APIRouter, Depends, HTTPException, status
from model.pydantic.auth_dto import JWT
from model.pydantic.refeicao_dto import Refeicao_DTO
from model.pydantic.usuario_dto import Usuario_DTO
from model.refeicao import Ingrediente, Prato, Refeicao
from routers.usuario_route import get_user_id
from services.refeicao_service import Refeicao_Service
from datetime import date

router = APIRouter()

@router.post("/refeicao/create")
async def refeicao_create(refeicao_dto: Refeicao_DTO, id_usuario: Usuario_DTO = Depends(get_user_id), refeicao_service: Refeicao_Service = Depends(Refeicao_Service)):
  refeicao_info = refeicao_dto.model_dump()
  refeicao_info["pratos"] = [Prato(nome_prato = p.get("nome_prato"), ingredientes = [Ingrediente(**i) for i in p.get("ingredientes")]) for p in refeicao_info.get("pratos")]
  refeicao_model = Refeicao(**refeicao_info, id_usuario=id_usuario, data_refeicao=date.today().isoformat())
  return refeicao_service.create(refeicao_model)

@router.get("/refeicao/{id}")
async def refeicao_get(id: str, refeicao_service: Refeicao_Service = Depends(Refeicao_Service), id_usuario: Usuario_DTO = Depends(get_user_id)):
  refeicao = refeicao_service.get_by_id(id)

  if refeicao.id_usuario != id_usuario:
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
  
  return refeicao
