from sqlalchemy import Column, Float, Integer, String
from database import Base

class Usuario(Base):
  __tablename__ = 'usuario'

  id = Column(Integer, primary_key=True, autoincrement=True)
  nome = Column(String, nullable=False)
  email = Column(String, nullable=False)
  senha = Column(String, nullable=False)
  data_nascimento = Column(String, nullable=False)
  peso = Column(Float, nullable=False)
  altura = Column(Float, nullable=False)
  atividade = Column(Integer ,nullable=False)
  sexo = Column(String(1), nullable=False)