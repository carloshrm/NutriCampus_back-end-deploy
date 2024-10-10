from fastapi.params import Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
from model.alimento import Alimento

class Alimento_Service:

  def __init__(self, db: Session = Depends(get_db)):
    self.db = db

  def get_by_id(self, id):
    return self.db.query(Alimento).options(
      joinedload(Alimento.graxos), 
      joinedload(Alimento.aminoacidos), 
      joinedload(Alimento.centesimal)).filter(Alimento._id == id).first()

  def get_by_name(self, name):
    name = name.lower()
    return self.db.query(Alimento).options(
      joinedload(Alimento.graxos), 
      joinedload(Alimento.aminoacidos), 
      joinedload(Alimento.centesimal)).filter(name in Alimento._nome.split(';')).first()