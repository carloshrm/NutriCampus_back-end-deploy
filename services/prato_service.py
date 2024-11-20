from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from model.refeicao import Prato, Ingrediente
from database import get_db
from fastapi import Depends, HTTPException
from scraping.TACO.script import _remover_acentos

class PratoService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def buscar_todos_pratos(self):
        return self.db.query(Prato).options(joinedload(Prato.ingredientes)).all()

    def buscar_prato_por_id(self, id: int):
        return self.db.query(Prato).options(joinedload(Prato.ingredientes)).filter(Prato.id_prato == id).first()

    def buscar_prato_por_nome(self, nome: str):
        nome_limpo = nome.strip().lower()
        return self.db.query(Prato).filter(func.lower(Prato.nome_prato).like(f"%{nome_limpo}%")).all()

    def buscar_ingredientes_por_prato_id(self, id: int):
        return self.db.query(Ingrediente).filter(Ingrediente.id_prato == id).all()

    def criar_prato(self, prato_data: dict):
        prato = Prato(**prato_data)
        self.db.add(prato)
        self.db.commit()
        self.db.refresh(prato)
        return prato

    def atualizar_prato(self, id: int, prato_data: dict):
        prato = self.db.query(Prato).filter(Prato.id_prato == id).first()
        if not prato:
            raise HTTPException(status_code=404, detail="Prato não encontrado.")

        self.db.query(Ingrediente).filter(Ingrediente.id_prato == id).delete()

        for key, value in prato_data.items():
            if key != "ingredientes":  
                setattr(prato, key, value)

        if "ingredientes" in prato_data:
            for ingrediente_data in prato_data["ingredientes"]:
                novo_ingrediente = Ingrediente(**ingrediente_data)
                novo_ingrediente.id_prato = id
                self.db.add(novo_ingrediente)

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
