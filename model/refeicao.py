from sqlalchemy import Column, ForeignKey, Integer, String, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class Refeicao(Base):
    __tablename__ = 'refeicao'

    id_refeicao = Column(Integer, primary_key=True, autoincrement=True)
    data_refeicao = Column(TIMESTAMP, nullable=False)
    tipo_refeicao = Column(String, nullable=False)  # Tipo de refeição (almoço, jantar, etc.)

    # Relacionamento: uma refeição pode ter vários pratos
    pratos = relationship('Prato', back_populates='refeicao')

class Prato(Base):
    __tablename__ = 'prato'

    id_prato = Column(Integer, primary_key=True, autoincrement=True)
    nome_prato = Column(String, nullable=False)
    id_refeicao = Column(Integer, ForeignKey('refeicao.id_refeicao'))

    # Relacionamento: um prato pertence a uma refeição
    refeicao = relationship('Refeicao', back_populates='pratos')

    # Relacionamento: um prato pode ter vários ingredientes
    ingredientes = relationship('Ingrediente', back_populates='prato')

class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id_ingrediente = Column(Integer, primary_key=True, autoincrement=True)
    nome_ingrediente = Column(String, nullable=False)
    calorias = Column(Float, nullable=False)
    quantidade = Column(Float, nullable=False)
    id_prato = Column(Integer, ForeignKey('prato.id_prato'))

    # Relacionamento: um ingrediente pertence a um prato
    prato = relationship('Prato', back_populates='ingredientes')
