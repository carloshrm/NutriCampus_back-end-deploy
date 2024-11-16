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

    def criar_prato(self, prato_data: dict):
        prato = Prato(**prato_data)
        self.db.add(prato)
        self.db.commit()
        self.db.refresh(prato)
        return prato

    def atualizar_prato(self, id: int, prato_data: dict):
        prato = self.buscar_prato_por_id(id)
        if not prato:
            return None
        for key, value in prato_data.items():
            setattr(prato, key, value)
        self.db.commit()
        self.db.refresh(prato)
        return prato

    def deletar_prato(self, id: int):
        prato = self.buscar_prato_por_id(id)
        if not prato:
            return None
        self.db.delete(prato)
        self.db.commit()
        return prato

    def criar_ingrediente(self, ingrediente_data: dict):
        ingrediente = Ingrediente(**ingrediente_data)
        self.db.add(ingrediente)
        self.db.commit()
        self.db.refresh(ingrediente)
        return ingrediente

    def atualizar_ingrediente(self, id: int, ingrediente_data: dict):
        ingrediente = self.db.query(Ingrediente).filter(Ingrediente.id_ingrediente == id).first()
        if not ingrediente:
            return None
        for key, value in ingrediente_data.items():
            setattr(ingrediente, key, value)
        self.db.commit()
        self.db.refresh(ingrediente)
        return ingrediente

    def deletar_ingrediente(self, id: int):
        ingrediente = self.db.query(Ingrediente).filter(Ingrediente.id_ingrediente == id).first()
        if not ingrediente:
            return None
        self.db.delete(ingrediente)
        self.db.commit()
        return ingrediente
