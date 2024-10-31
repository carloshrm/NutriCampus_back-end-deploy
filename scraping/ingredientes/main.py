import logging
from scraper import buscar_link_receita, obter_soup_da_receita, extrair_ingredientes
from sqlalchemy.orm import Session
from database import SessionLocal
from model.refeicao import Prato, Ingrediente

def salvar_ingredientes_no_banco(db: Session, id_prato: int, ingredientes: list):
    for ing in ingredientes:
        novo_ingrediente = Ingrediente(
            nome_ingrediente=ing['nome_ingrediente'],
            quantidade_original=ing['quantidade'],
            unidade_original=ing['unidade_original'],
            a_gosto=ing.get('a_gosto', False),
            quantidade_normalizada=ing.get('quantidade_normalizada'),
            unidade_normalizada=ing.get('unidade_normalizada'),
            calorias=0.0,
            id_prato=id_prato
        )
        db.add(novo_ingrediente)
    db.commit()

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Cria uma sessão com o banco de dados
    db = SessionLocal()

    try:
        # Busca todos os pratos (receitas) do banco de dados
        pratos = db.query(Prato).all()

        if not pratos:
            logging.warning("Nenhum prato encontrado no banco de dados.")
            return

        for prato in pratos:
            receita = prato.nome_prato
            logging.info(f"Processando a receita: {receita}")

            # Busca o link da receita usando o DuckDuckGo
            link_receita = buscar_link_receita(receita)
            if link_receita:
                # Atualiza o link da receita no prato
                prato.link_receita = link_receita
                db.commit()

                soup = obter_soup_da_receita(link_receita)
                if soup:
                    lista_ingredientes = extrair_ingredientes(soup)
                    if lista_ingredientes:
                        # Salva os ingredientes no banco de dados
                        salvar_ingredientes_no_banco(db, prato.id_prato, lista_ingredientes)
                        logging.info(f"Ingredientes da receita '{receita}' salvos com sucesso.")
                    else:
                        logging.warning(f"Nenhum ingrediente foi extraído para a receita '{receita}'.")
                else:
                    logging.error(f"Não foi possível obter o conteúdo da receita '{receita}'.")
            else:
                logging.error(f"Nenhuma URL válida foi encontrada para a receita '{receita}'.")

    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()