from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from services.alimento_service import Alimento_Service
from http import HTTPStatus
router = APIRouter()


@router.get("/alimento/{id}")
async def get_alimento(id: int, alimento_service: Alimento_Service = Depends(Alimento_Service)):
    if not id or id <= 0 or id >= 600:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ID inválido.")

    alimento_encontrado = alimento_service.get_by_id(id);
    if not alimento_encontrado:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Alimento não encontrado.")
    
    return alimento_encontrado

@router.get("/alimento/nome/{nome}")
async def get_alimento_por_nome(nome: str, alimento_service: Alimento_Service = Depends(Alimento_Service)):
    if not nome or len(nome) <= 0:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Nome inválido.")

    alimento_encontrado = alimento_service.get_by_name(nome);
    if not alimento_encontrado:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Alimento não encontrado.")
    
    return alimento_encontrado