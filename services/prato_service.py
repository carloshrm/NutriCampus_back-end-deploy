from sqlalchemy.orm import Session, joinedload
from model.refeicao import Prato, Ingrediente
from database import get_db
from fastapi import Depends

class PratoService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def buscar_todos_pratos(self):
        return self.db.query(Prato).options(joinedload(Prato.ingredientes)).all()

    def buscar_prato_por_id(self, id: int):
        return self.db.query(Prato).options(joinedload(Prato.ingredientes)).filter(Prato.id_prato == id).first()

    def buscar_ingredientes_por_prato_id(self, id: int):
        return self.db.query(Ingrediente).filter(Ingrediente.id_prato == id).all()
