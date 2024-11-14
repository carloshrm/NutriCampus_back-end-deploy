from fastapi import APIRouter, Depends, HTTPException, status
from model.pydantic.auth_dto import JWT
from model.pydantic.refeicao_dto import Refeicao_DTO
from model.pydantic.usuario_dto import Usuario_DTO
from model.refeicao import Refeicao, Consumo
from routers.usuario_route import get_user_id
from services.refeicao_service import Refeicao_Service
from services.consumo_service import Consumo_Service
from services.prato_service import PratoService
from datetime import date

router = APIRouter()

@router.post("/refeicao/create")
async def refeicao_create(refeicao_dto: Refeicao_DTO, 
                          id_usuario: Usuario_DTO = Depends(get_user_id), 
                          refeicao_service: Refeicao_Service = Depends(Refeicao_Service), 
                          prato_service: PratoService = Depends(PratoService),
                          consumo_service: Consumo_Service = Depends(Consumo_Service)):
  
  refeicao_dto_info = refeicao_dto.model_dump()
  refeicao_criada =  refeicao_service.create(Refeicao(tipo_refeicao=refeicao_dto_info.get("tipo_refeicao"), id_usuario=id_usuario, data_refeicao=date.today().isoformat()))
  
  for prato in refeicao_dto_info.get("pratos"):
    consumo_service.add_consumo(Consumo(id_prato=prato.get("id_prato"), quantidade=prato.get("quantidade"), id_refeicao=refeicao_criada.id_refeicao))

  return refeicao_service.get_by_id(refeicao_criada.id_refeicao)

@router.get("/refeicao/consumo")
async def get_consumo_por_data(data_inicio: str, data_fim: str, consumo_service: Consumo_Service = Depends(Consumo_Service), id_usuario: Usuario_DTO = Depends(get_user_id)):
  return consumo_service.get_consumo(id_usuario, data_inicio, data_fim)

@router.get("/refeicao/{id}")
async def refeicao_get(id: str, refeicao_service: Refeicao_Service = Depends(Refeicao_Service), id_usuario: Usuario_DTO = Depends(get_user_id)):
  refeicao = refeicao_service.get_by_id(id)

  if refeicao.id_usuario != id_usuario:
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Acesso não autorizado.")
  
  return refeicao
