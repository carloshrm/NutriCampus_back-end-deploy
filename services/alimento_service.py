from fastapi.params import Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
from model.alimento import Alimento
from scraping.TACO.script import _remover_acentos
class Alimento_Service:

  def __init__(self, db: Session = Depends(get_db)):
    self.db = db

  def get_by_id(self, id):
    return self.db.query(Alimento).options(
      joinedload(Alimento.graxos), 
      joinedload(Alimento.aminoacidos), 
      joinedload(Alimento.centesimal)).filter(Alimento._id == id).first()

  def get_by_name(self, name):
    name = _remover_acentos(name.lower()).split(' ')
    return self.db.query(Alimento).options(
      joinedload(Alimento.graxos), 
      joinedload(Alimento.aminoacidos), 
      joinedload(Alimento.centesimal)).filter(Alimento._nome.contains(name)).all()