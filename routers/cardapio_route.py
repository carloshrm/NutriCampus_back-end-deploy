from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.cardapio_service import Cardapio_Service
from database import get_db

# Criação do router
router = APIRouter()

@router.get("/cardapios/")
def listar_todos_cardapios(service: Session = Depends(Cardapio_Service)):
    return service.buscar_todos_cardapios()

@router.get("/cardapios/campus/{campus}")
def listar_cardapios_por_campus(campus: str, service: Session = Depends(Cardapio_Service)):
    return service.buscar_cardapio_por_campus(campus)

@router.get("/cardapios/data/{data}")
def listar_cardapios_por_data(data: str, service: Session = Depends(Cardapio_Service)):
    return service.buscar_cardapio_por_data(data)

@router.get("/cardapio-refeicao/{campus}/{refeicao}")
def listar_cardapios_por_refeicao(refeicao: str, service: Session = Depends(Cardapio_Service)):
    return service.buscar_cardapio_por_refeicao(refeicao)

@router.get("/cardapio-dia/{campus}/{data}")
def listar_cardapios_por_campus_e_data(campus: str, data: str, service: Session = Depends(Cardapio_Service)):
    return service.buscar_cardapio_por_campus_e_data(campus, data)

