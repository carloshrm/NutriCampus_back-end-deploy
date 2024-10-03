from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario

class Usuario_Service:

  def __init__(self, db: Session = Depends(get_db)):
    self.db = db

  def get_by_id(self, id):
    return self.db.query(Usuario).filter(Usuario.id == id).first()
  
  def get_by_email(self, email):
    return self.db.query(Usuario).filter(Usuario.email == email).first()
  
  def create(self, usuario: Usuario):
    self.db.add(usuario)
    self.db.commit()
    self.db.refresh(usuario)
    return usuario