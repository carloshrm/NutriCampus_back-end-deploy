import google.generativeai as genai
import os
from sqlalchemy.orm import Session
from model.refeicao import Prato, Ingrediente
from dotenv import load_dotenv
from database import get_db

load_dotenv()

genai_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=genai_api_key)

# Função para converter quantidades de kg, ml e L para gramas
def converter_para_gramas(quantidade_str):
    if 'kg' in quantidade_str:
        return float(quantidade_str.replace('kg', '').strip()) * 1000  # 1kg = 1000g
    elif 'L' in quantidade_str:
        return float(quantidade_str.replace('L', '').strip()) * 1000  # 1L = 1000g (assumindo densidade de água)
    elif 'ml' in quantidade_str:
        return float(quantidade_str.replace('ml', '').strip())  # 1ml = 1g (assumindo densidade de água)
    elif 'g' in quantidade_str:
        return float(quantidade_str.replace('g', '').strip())  # Quantidade já em gramas
    else:
        return 0  # Caso não tenha unidade, retorna 0

def gerar_ingredientes(prato_nome):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Gere uma lista de ingredientes simples e direta com as respectivas quantidades para preparar o prato '{prato_nome}'.
    Não use markdown. Cada linha deve conter o nome do ingrediente seguido da quantidade em gramas. 
    Exemplo: tomate 300g (opcional)
    """
    
    response = model.generate_content(prompt)
    
    ingredientes_text = response.text.strip()
    if not ingredientes_text:
        print(f"Resposta vazia ou inválida da API Gemini para '{prato_nome}'.")
        return []
    
    print(f"Resposta do Gemini para '{prato_nome}':\n{ingredientes_text}")
    
    ingredientes = []
    for linha in ingredientes_text.split('\n'):
        if linha:
            try:
                opcional = "(opcional)" in linha  # Verifica se o ingrediente é opcional
                linha = linha.replace("(opcional)", "").strip()  # Remove a tag "(opcional)"
                
                # Divide a linha em nome e quantidade (sempre último elemento é numérico ou uma unidade)
                partes = linha.split()
                
                # Tentar pegar o último elemento como quantidade, caso contrário, assumir que é opcional
                try:
                    quantidade_str = partes[-1]
                    quantidade = converter_para_gramas(quantidade_str)  # Converte para gramas
                    nome_ingrediente = ' '.join(partes[:-1])  # Nome do ingrediente
                except ValueError:
                    # Se não houver quantidade válida, assume como opcional e quantidade 0
                    nome_ingrediente = ' '.join(partes)
                    quantidade = 0
                    opcional = True

                # Adiciona o ingrediente na lista
                ingredientes.append({
                    "nome": nome_ingrediente.strip(),
                    "quantidade": quantidade,
                    "opcional": opcional
                })
            except ValueError:
                print(f"Erro ao processar linha: {linha}")
                continue
    
    return ingredientes

def salvar_ingredientes_no_banco(session: Session, prato_id, ingredientes):
    for ing in ingredientes:
        novo_ingrediente = Ingrediente(
            nome_ingrediente=ing['nome'],
            quantidade=ing['quantidade'],
            calorias=ing.get('calorias', 0.0),  # Valor padrão 0.0 se calorias não for fornecido
            opcional=ing['opcional'],  # Define se o ingrediente é opcional
            id_prato=prato_id
        )
        session.add(novo_ingrediente)
    
    session.commit()

def gerar_ingredientes_para_todos_os_pratos(session: Session):
    pratos = session.query(Prato).all()

    if pratos:
        for prato in pratos:
            print(f"Gerando ingredientes para o prato: {prato.nome_prato}")
            ingredientes = gerar_ingredientes(prato.nome_prato)
            
            if ingredientes:
                salvar_ingredientes_no_banco(session, prato.id_prato, ingredientes)
                print(f"Ingredientes para o prato '{prato.nome_prato}' adicionados com sucesso.")
            else:
                print(f"Nenhum ingrediente foi gerado para o prato '{prato.nome_prato}'.")
    else:
        print("Nenhum prato encontrado no banco de dados.")

if __name__ == "__main__":
    db = next(get_db())

    try:
        gerar_ingredientes_para_todos_os_pratos(db)
    except Exception as e:
        print(f"Erro ao gerar ingredientes: {e}")
        db.rollback()  # Fazer rollback em caso de exceção
    finally:
        db.close()
