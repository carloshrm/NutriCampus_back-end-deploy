from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from model.refeicao import Prato, Ingrediente, Map_Alimento
from model.pydantic.refeicao_dto import Map_Alimento_DTO
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

@router.get("/pratos/nome/{nome}")
async def buscar_prato_por_nome(nome: str, db: Session = Depends(get_db)):
    """
    Busca um prato pelo nome.
    """
    pratos = PratoService(db).buscar_prato_por_nome(nome)
    if not pratos:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Prato não encontrado.")
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

@router.post("/pratos/", status_code=HTTPStatus.CREATED)
async def criar_prato(prato_data: dict, db: Session = Depends(get_db)):
    """
    Cria um novo prato.
    """
    prato = PratoService(db).criar_prato(prato_data)
    return prato

@router.post("/pratos/{id}/map")
async def mapear_alimento(id: int, alimentos: List[Map_Alimento_DTO], db: Session = Depends(get_db)):
    prato = PratoService(db).mapear_alimentos(id, alimentos)
    return prato

@router.put("/pratos/{id}", status_code=HTTPStatus.OK)
async def atualizar_prato(id: int, prato_data: dict, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um prato específico pelo ID.
    """
    prato = PratoService(db).atualizar_prato(id, prato_data)
    if not prato:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Prato não encontrado.")
    return prato

@router.delete("/pratos/{id}", status_code=HTTPStatus.NO_CONTENT)
async def deletar_prato(id: int, db: Session = Depends(get_db)):
    """
    Deleta um prato específico pelo ID.
    """
    prato = PratoService(db).deletar_prato(id)
    if not prato:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Prato não encontrado.")
    return {"message": "Prato deletado com sucesso"}

@router.post("/ingredientes", status_code=HTTPStatus.CREATED)
async def criar_ingrediente(ingrediente_data: dict, db: Session = Depends(get_db)):
    """
    Cria um novo ingrediente associado a um prato.
    """
    id_prato = ingrediente_data.get("id_prato")
    if not id_prato:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Prato ID é necessário.")
    
    novo_ingrediente = Ingrediente(**ingrediente_data)
    db.add(novo_ingrediente)
    db.commit()
    db.refresh(novo_ingrediente)
    return novo_ingrediente

@router.put("/ingredientes/{id}", status_code=HTTPStatus.OK)
async def atualizar_ingrediente(id: int, ingrediente_data: dict, db: Session = Depends(get_db)):
    """
    Atualiza os dados de um ingrediente específico pelo ID.
    """
    ingrediente = PratoService(db).atualizar_ingrediente(id, ingrediente_data)
    if not ingrediente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Ingrediente não encontrado.")
    return ingrediente

@router.delete("/ingredientes/{id}", status_code=HTTPStatus.NO_CONTENT)
async def deletar_ingrediente(id: int, db: Session = Depends(get_db)):
    """
    Deleta um ingrediente específico pelo ID.
    """
    ingrediente = PratoService(db).deletar_ingrediente(id)
    if not ingrediente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Ingrediente não encontrado.")
    return {"message": "Ingrediente deletado com sucesso"}
