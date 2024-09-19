from sqlalchemy import Column, ForeignKey, Float, Integer, String, TIMESTAMP, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import text
from database import Base

class Alimento(Base):
  __tablename__ = 'alimento'

  _id = Column(Integer, primary_key=True, nullable=False)
  _nome = Column(String, nullable=False)
  umidade = Column(Float, server_default="0.0")
  energia_kcal = Column(Float, server_default="0.0")
  energia_kj = Column(Float, server_default="0.0")
  proteina = Column(Float, server_default="0.0")
  lipideos = Column(Float, server_default="0.0")
  colesterol = Column(Float, server_default="0.0")
  carboidrato = Column(Float, server_default="0.0")
  fibra_alimentar = Column(Float, server_default="0.0")
  cinzas = Column(Float, server_default="0.0")
  calcio = Column(Float, server_default="0.0")
  magnesio = Column(Float, server_default="0.0")
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

  centesimal = relationship('Alimento_Centesimal', backref=backref("Alimento"), uselist=False, cascade="all")
  graxos = relationship('Alimento_AcidosGraxos', backref=backref("Alimento"), uselist=False, cascade="all")
  aminoacidos = relationship('Alimento_Aminoacidos', backref=backref("Alimento"), uselist=False, cascade="all")

class Alimento_Centesimal(Base):
  __tablename__ = 'alimento_centesimal'

  _id = Column(String, primary_key=True, nullable=False)
  alimento_id = Column(Integer, ForeignKey('alimento._id'), unique=True)
  
  manganes = Column(Float, server_default="0.0")
  fosforo = Column(Float, server_default="0.0")
  ferro = Column(Float, server_default="0.0")
  sodio = Column(Float, server_default="0.0")
  potassio = Column(Float, server_default="0.0")
  cobre = Column(Float, server_default="0.0")
  zinco = Column(Float, server_default="0.0")
  retinol = Column(Float, server_default="0.0")
  re = Column(Float, server_default="0.0")
  rae = Column(Float, server_default="0.0")
  tiamina = Column(Float, server_default="0.0")
  riboflavina = Column(Float, server_default="0.0")
  piridoxina = Column(Float, server_default="0.0")
  niacina = Column(Float, server_default="0.0")
  vitamina_c = Column(Float, server_default="0.0")

class Alimento_AcidosGraxos(Base):
  __tablename__ = 'alimento_acidosgraxos'

  _id = Column(String, primary_key=True, nullable=False)
  alimento_id = Column(Integer, ForeignKey('alimento._id'), unique=True)

  saturados = Column(Float, server_default="0.0")
  mono_insaturados = Column(Float, server_default="0.0")
  poli_insaturados = Column(Float, server_default="0.0")
  _12_0 = Column(Float, server_default="0.0")
  _14_0 = Column(Float, server_default="0.0")
  _16_0 = Column(Float, server_default="0.0")
  _18_0 = Column(Float, server_default="0.0")
  _20_0 = Column(Float, server_default="0.0")
  _22_0 = Column(Float, server_default="0.0")
  _24_0 = Column(Float, server_default="0.0")
  _14_1 = Column(Float, server_default="0.0")
  _16_1 = Column(Float, server_default="0.0")
  _18_1 = Column(Float, server_default="0.0")
  _20_1 = Column(Float, server_default="0.0")
  _18_2n6 = Column(Float, server_default="0.0")
  _18_3n3 = Column(Float, server_default="0.0")
  _20_4 = Column(Float, server_default="0.0")
  _20_5 = Column(Float, server_default="0.0")
  _22_5 = Column(Float, server_default="0.0")
  _22_6 = Column(Float, server_default="0.0")
  _18_1t = Column(Float, server_default="0.0")
  _18_2t = Column(Float, server_default="0.0")

class Alimento_Aminoacidos(Base):
  __tablename__ = 'alimento_aminoacidos'

  _id = Column(String, primary_key=True, nullable=False)
  alimento_id = Column(Integer, ForeignKey('alimento._id'), unique=True)

  triptofano = Column(Float, server_default="0.0")
  treonina = Column(Float, server_default="0.0")
  isoleucina = Column(Float, server_default="0.0")
  leucina = Column(Float, server_default="0.0")
  lisina = Column(Float, server_default="0.0")
  metionina = Column(Float, server_default="0.0")
  cistina = Column(Float, server_default="0.0")
  fenilalanina = Column(Float, server_default="0.0")
  tirosina = Column(Float, server_default="0.0")
  valina = Column(Float, server_default="0.0")
  arginina = Column(Float, server_default="0.0")
  histidina = Column(Float, server_default="0.0")
  alanina = Column(Float, server_default="0.0")
  acido_aspartico = Column(Float, server_default="0.0")
  acido_glutamico = Column(Float, server_default="0.0")
  glicina = Column(Float, server_default="0.0")
  prolina = Column(Float, server_default="0.0")
  serina = Column(Float, server_default="0.0")