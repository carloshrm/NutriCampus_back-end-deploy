from fastapi.params import Depends
from sqlalchemy.orm import Session
from model.Cardapio import Cardapio
from database import get_db

class Cardapio_Service:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def buscar_todos_cardapios(self):
        """Busca todos os cardápios no banco de dados."""
        return self.db.query(Cardapio).all()

    def buscar_cardapio_por_campus(self, campus: str):
        """Busca os cardápios por campus."""
        return self.db.query(Cardapio).filter(Cardapio.campus == campus).all()

    def buscar_cardapio_por_data(self, data: str):
        """Busca os cardápios por data específica."""
        return self.db.query(Cardapio).filter(Cardapio.data == data).all()

    def buscar_cardapio_por_refeicao(self, refeicao: str):
        """Busca os cardápios por tipo de refeição (almoço, jantar)."""
        return self.db.query(Cardapio).filter(Cardapio.refeicao == refeicao).all()
