from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from model.refeicao import Prato, Ingrediente
from services.prato_service import PratoService
from database import get_db
from http import HTTPStatus

router = APIRouter()

@router.get("/pratos/")
async def listar_todos_pratos(db: Session = Depends(get_db)):
    """
    Lista todos os pratos disponíveis no banco de dados.
    """
    pratos = PratoService(db).buscar_todos_pratos()
    if not pratos:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Nenhum prato encontrado.")
    return pratos

@router.get("/pratos/{id}")
async def get_prato(id: int, db: Session = Depends(get_db)):
    """
    Retorna um prato específico pelo ID.
    """
    if id <= 0:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="ID inválido.")

    prato = PratoService(db).buscar_prato_por_id(id)
    if not prato:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Prato não encontrado.")
    
    return prato

@router.get("/pratos/{id}/ingredientes")
async def get_ingredientes_por_prato(id: int, db: Session = Depends(get_db)):
    """
    Retorna os ingredientes de um prato específico pelo ID do prato.
    """
    ingredientes = PratoService(db).buscar_ingredientes_por_prato_id(id)
    if not ingredientes:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Nenhum ingrediente encontrado para o prato especificado.")
    
    return ingredientes
