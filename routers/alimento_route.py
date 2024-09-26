from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
from model.alimento import Alimento
from services.alimento_service import Alimento_Service
from http import HTTPStatus
router = APIRouter()


@router.get("/alimento/{id}")
async def get_alimento(id: str, alimento_service: Alimento_Service = Depends(Alimento_Service)):
    if not id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ID não informado.")

    alimento_encontrado = alimento_service.get_by_id(id);
    if not alimento_encontrado:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Alimento não encontrado.")
    
    return alimento_encontrado
