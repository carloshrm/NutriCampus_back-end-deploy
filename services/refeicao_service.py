from fastapi.params import Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
from model.refeicao import Refeicao, Prato, Consumo
from datetime import date

class Refeicao_Service:

  def __init__(self, db: Session = Depends(get_db)):
    self.db = db

  def get_by_id(self, id):
    return self.db.query(Refeicao).filter(Refeicao.id_refeicao == id).options(joinedload(Refeicao.pratos_consumidos)).first()
  
  def get_by_user(self, id_usuario, data_inicio = None, data_fim = None):
    if data_inicio:
      if not data_fim:
        data_fim = date.today().isoformat()
      return self.db.query(Refeicao).filter(Refeicao.id_usuario == id_usuario and Refeicao.data_refeicao.between(data_inicio, date.today().isoformat())).all()
    else:
      return self.db.query(Refeicao).filter(Refeicao.id_usuario == id_usuario).all()
  
  def create(self, refeicao: Refeicao):
    self.db.add(refeicao)
    self.db.commit()
    self.db.refresh(refeicao)
    return refeicao