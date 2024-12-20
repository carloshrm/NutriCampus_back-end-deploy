from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Refeicao(Base):
    __tablename__ = 'refeicao'

    id_refeicao = Column(Integer, primary_key=True, autoincrement=True)
    data_refeicao = Column(TIMESTAMP, nullable=False)
    tipo_refeicao = Column(String, nullable=False)  # Tipo de refeição (almoço, jantar, etc.)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))

    # Relacionamento: uma refeição pode ter vários pratos
    pratos = relationship('Prato', back_populates='refeicao')

class Consumo(Base):
    __tablename__ = 'consumo'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_refeicao = Column(Integer, ForeignKey('refeicao.id_refeicao'))
    id_prato = Column(Integer, ForeignKey('prato.id_prato'))
    quantidade = Column(Float, nullable=False)

class Prato(Base):
    __tablename__ = 'prato'

    id_prato = Column(Integer, primary_key=True, autoincrement=True)
    nome_prato = Column(String, nullable=False, unique=True)
    link_receita = Column(String, nullable=True)
    id_refeicao = Column(Integer, ForeignKey('refeicao.id_refeicao'))

    # Relacionamento: um prato pertence a uma refeição
    refeicao = relationship('Refeicao', secondary='consumo', back_populates='pratos')

    # Relacionamento: um prato pode ter vários ingredientes
    ingredientes = relationship('Ingrediente', back_populates='prato', cascade="all, delete-orphan")

class Map_Alimento(Base):
    __tablename__ = 'map_alimento'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_alimento = Column(Integer, ForeignKey('alimento._id'))
    quantidade = Column(Float, nullable=False)
    alimento = relationship('Alimento')

    id_prato = Column(Integer, ForeignKey('prato.id_prato'))
    prato = relationship('Prato')

class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id_ingrediente = Column(Integer, primary_key=True, autoincrement=True)
    nome_ingrediente = Column(String, nullable=False)
    quantidade_original = Column(Float, nullable=True)
    unidade_original = Column(String, nullable=True)
    a_gosto = Column(Boolean, default=False)
    quantidade_normalizada = Column(Float, nullable=True)
    unidade_normalizada = Column(String, nullable=True)
    calorias = Column(Float, nullable=True)
    id_prato = Column(Integer, ForeignKey("prato.id_prato", ondelete="CASCADE"))
    # Relacionamento: um ingrediente pertence a um prato
    prato = relationship('Prato', back_populates='ingredientes')
