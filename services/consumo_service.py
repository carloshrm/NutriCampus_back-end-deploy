from sqlalchemy.orm import Session, joinedload
from model.refeicao import Consumo, Prato, Refeicao
from database import get_db
from fastapi import Depends
from datetime import date

class Consumo_Service:
    def __init__(self, db: Session = Depends(get_db)):
      self.db = db

    def get_consumo(self, id_usuario):
      return self.db.query(Consumo).options(joinedload(Prato.id_prato), joinedload(Refeicao.id_refeicao)).filter(Refeicao.id_usuario == id_usuario).all()

    def get_consumo_por_data(self, id_usuario, data_inicio, data_fim):

      if data_inicio:
        if not data_fim:
          data_fim = date.today().isoformat()
        return self.db.query(Consumo).options(joinedload(Prato.id_prato), joinedload(Refeicao.id_refeicao)).filter(Refeicao.id_usuario == id_usuario and Refeicao.data_refeicao.between(data_inicio, data_fim)).all()
      else:
        return self.get_consumo(id_usuario)

    def add_consumo(self, consumo: Consumo):
      self.db.add(consumo)
      self.db.commit()
      self.db.refresh(consumo)
      return consumo

