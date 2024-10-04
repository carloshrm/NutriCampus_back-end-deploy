from sqlalchemy import CheckConstraint, Column, Float, Integer, String
from database import Base

class Usuario(Base):
  __tablename__ = 'usuario'

  id = Column(Integer, primary_key=True, autoincrement=True)
  nome = Column(String, nullable=False)
  email = Column(String, nullable=False)
  senha = Column(String, nullable=False)
  data_nascimento = Column(String, nullable=False)
  peso = Column(Float, CheckConstraint('peso > 0'),nullable=False)
  altura = Column(Float, CheckConstraint('altura > 0') ,nullable=False)
  atividade = Column(Integer, CheckConstraint('atividade >= 1 AND atividade <= 5'), nullable=False)
  sexo = Column(String(1), nullable=False)