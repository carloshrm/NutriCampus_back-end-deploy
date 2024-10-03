from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.cardapio_service import Cardapio_Service
from database import get_db

# Criação do router
router = APIRouter()

@router.get("/cardapios/")
def listar_todos_cardapios(db: Session = Depends(get_db)):
    service = Cardapio_Service(db)
    return service.buscar_todos_cardapios()

@router.get("/cardapios/campus/{campus}")
def listar_cardapios_por_campus(campus: str, db: Session = Depends(get_db)):
    service = Cardapio_Service(db)
    return service.buscar_cardapio_por_campus(campus)

@router.get("/cardapios/data/{data}")
def listar_cardapios_por_data(data: str, db: Session = Depends(get_db)):
    service = Cardapio_Service(db)
    return service.buscar_cardapio_por_data(data)

@router.get("/cardapios/refeicao/{refeicao}")
def listar_cardapios_por_refeicao(refeicao: str, db: Session = Depends(get_db)):
    service = Cardapio_Service(db)
    return service.buscar_cardapio_por_refeicao(refeicao)
