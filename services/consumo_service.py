from sqlalchemy.orm import Session, joinedload
from model.refeicao import Consumo, Prato, Refeicao, Map_Alimento
from database import get_db
from fastapi import Depends
from datetime import date

class Consumo_Service:
    def __init__(self, db: Session = Depends(get_db)):
      self.db = db

    def get_consumo(self, id_usuario):
      refs = self.db.query(Refeicao).filter(Refeicao.id_usuario == id_usuario).all()
      consumo = self.db.query(Consumo, Prato).filter(Consumo.id_refeicao.in_([ref.id_refeicao for ref in refs])).all()
      pratos = self.db.query(Prato).filter(Prato.id_prato.in_([c.id_prato for c in consumo])).all()
      map_alimento_pratos = self.db.query(Map_Alimento).filter(Map_Alimento.id_prato.in_([p.id_prato for p in pratos])).all()

      group_pratos = {}
      for al in map_alimento_pratos:
        if al.id_prato in group_pratos:
          group_pratos[al.id_prato].append(al)
        else:
          group_pratos[al.id_prato] = [al]

      return group_pratos

    def get_consumo_hoje(self, id_usuario):
      refs = self.db.query(Refeicao).filter(Refeicao.id_usuario == id_usuario and Refeicao.data_refeicao == date.today().isoformat()).all()
      consumo = self.db.query(Consumo).filter(Consumo.id_refeicao.in_([ref.id_refeicao for ref in refs])).all()
      pratos = self.db.query(Prato).filter(Prato.id_prato.in_([c.id_prato for c in consumo])).all()
      map_alimento_pratos = self.db.query(Map_Alimento).filter(Map_Alimento.id_prato.in_([p.id_prato for p in pratos])).all()

      group_pratos = {}
      for al in map_alimento_pratos:
        if al.id_prato in group_pratos:
          group_pratos[al.id_prato].append(al)
        else:
          group_pratos[al.id_prato] = [al]

      return group_pratos

    def get_consumo_por_data(self, id_usuario, data_inicio, data_fim):

      if data_inicio:
        if not data_fim:
          data_fim = date.today().isoformat()
        refs = self.db.query(Consumo).filter(Consumo.id_refeicao.in_([ref.id_refeicao for ref in self.db.query(Refeicao).filter(Refeicao.id_usuario == id_usuario and Refeicao.data_refeicao.between(data_inicio, data_fim)).all()])).all()
        consumo = self.db.query(Consumo).filter(Consumo.id_refeicao.in_([ref.id_refeicao for ref in refs])).all()
        pratos = self.db.query(Prato).filter(Prato.id_prato.in_([c.id_prato for c in consumo])).all()
        map_alimento_pratos = self.db.query(Map_Alimento).filter(Map_Alimento.id_prato.in_([p.id_prato for p in pratos])).all()

        group_pratos = {}
        for al in map_alimento_pratos:
          if al.id_prato in group_pratos:
            group_pratos[al.id_prato].append(al)
        else:
          group_pratos[al.id_prato] = [al]

        return group_pratos
      else:
        return self.get_consumo(id_usuario)

    def add_consumo(self, consumo: Consumo):
      self.db.add(consumo)
      self.db.commit()
      self.db.refresh(consumo)
      return consumo

