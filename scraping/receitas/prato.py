from sqlalchemy.orm import Session
from model.Cardapio import Cardapio
from model.refeicao import Prato
from database import SessionLocal

def mapeamento_prato(db: Session):
    # Conjunto para armazenar nomes de pratos já verificados
    pratos_existentes = set(prato.nome_prato for prato in db.query(Prato).all())

    cardapios = db.query(Cardapio).all()

    for cardapio in cardapios:
        # Verifica e insere o prato principal
        if cardapio.prato_principal and cardapio.prato_principal not in pratos_existentes:
            novo_prato_principal = Prato(
                nome_prato=cardapio.prato_principal,
                link_receita=None,  # Link ainda não disponível
                id_refeicao=None 
            )
            db.add(novo_prato_principal)
            pratos_existentes.add(cardapio.prato_principal)

        # Verifica e insere o prato vegetariano
        if cardapio.prato_veg and cardapio.prato_veg not in pratos_existentes:
            novo_prato_veg = Prato(
                nome_prato=cardapio.prato_veg,
                link_receita=None,  # Link ainda não disponível
                id_refeicao=None 
            )
            db.add(novo_prato_veg)
            pratos_existentes.add(cardapio.prato_veg)

    # Commit após todas as inserções
    db.commit()

# Executa o código para popular a tabela Prato
def main():
    db = SessionLocal()
    try:
        mapeamento_prato(db)
        print("Tabela 'Prato' populada com sucesso a partir de 'Cardapios'.")
    except Exception as e:
        print(f"Erro ao popular a tabela 'Prato': {e}")
    finally:
        db.close()
