from sqlalchemy import Column, Integer, String, Date
from database import Base

class Cardapio(Base):
    __tablename__ = "cardapios"  # Nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True)
    campus = Column(String, index=True)
    data = Column(Date)
    refeicao = Column(String)
    prato_principal = Column(String)
    prato_veg = Column(String)
    arroz_principal = Column(String)
    arroz_secundario = Column(String)
    feijao_principal = Column(String)
    feijao_secundario = Column(String)
    guarnicao = Column(String)
    salada = Column(String)
