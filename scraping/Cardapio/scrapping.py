import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import psycopg2
import os
from dotenv import load_dotenv  # Importando dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função auxiliar para separar as palavras corretamente
def separa(texto):
    resultado = []
    palavra_atual = texto[0]

    for i in range(1, len(texto)):
        char = texto[i]
        char_anterior = texto[i - 1]

        if char.isupper() and char_anterior != ' ' and char_anterior.islower():
            resultado.append(palavra_atual)
            palavra_atual = char
        else:
            palavra_atual += char

    resultado.append(palavra_atual)
    return resultado

# Função auxiliar para separar arroz branco e arroz integral
def separar_arroz(arroz_lista):
    arroz_branco = 'Não Encontrado'
    arroz_integral = 'Não Encontrado'
    for arroz in arroz_lista:
        if 'Branco' in arroz:
            arroz_branco = arroz
        elif 'Integral' in arroz:
            arroz_integral = arroz
    return arroz_branco, arroz_integral

# Função para salvar os dados no banco de dados PostgreSQL
def salvar_no_banco(campus_data):
    # Conexão com o banco de dados PostgreSQL usando variáveis de ambiente
    conn = psycopg2.connect(
        dbname=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
    )
    cursor = conn.cursor()

    # Criação da tabela com colunas separadas para arroz branco e integral
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS cardapios (
            id SERIAL PRIMARY KEY,
            campus VARCHAR(100),
            data DATE,
            refeicao VARCHAR(50),
            prato_principal TEXT,
            prato_veg TEXT,
            arroz_branco TEXT,
            arroz_integral TEXT,
            feijao TEXT,
            guarnicao TEXT,
            salada TEXT
        );
    """)
    conn.commit()

    # Inserir os dados no banco de dados
    for campus, dias in campus_data.items():
        for dia in dias:
            data = dia['data']
            for refeicao, pratos in dia['cardapio'].items():
                # Extrair os pratos para as colunas apropriadas
                prato_principal = ', '.join(pratos.get('prato_principal', ['Não Encontrado']))
                prato_veg = ', '.join(pratos.get('prato_veg', ['Não Encontrado']))

                # Separar arroz branco e arroz integral
                arroz_lista = pratos.get('arroz', ['Não Encontrado'])
                arroz_branco, arroz_integral = separar_arroz(arroz_lista)

                feijao = ', '.join(pratos.get('feijao', ['Não Encontrado']))
                guarnicao = ', '.join(pratos.get('guarnicao', ['Não Encontrado']))
                salada = ', '.join(pratos.get('salada', ['Não Encontrado']))

                # Inserir uma única linha com todos os pratos
                cursor.execute("""
                    INSERT INTO cardapios (campus, data, refeicao, prato_principal, prato_veg, arroz_branco, arroz_integral, feijao, guarnicao, salada)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (campus, data, refeicao, prato_principal, prato_veg, arroz_branco, arroz_integral, feijao, guarnicao, salada))

    # Confirmar a transação e fechar a conexão
    conn.commit()
    cursor.close()
    conn.close()

# Função para fazer scraping e extrair os cardápios
def extrair_cardapios(urls):
    campus = {}
    data_atual = datetime.now()

    # Loop pelos campus para realizar o scraping
    for url in urls:
        # Inicializa a estrutura para o campus atual
        campus[url] = []
        urlFinal = f'https://proae.ufu.br/ru/cardapios/{url}/'
        r = requests.get(urlFinal)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')

            # Loop pelos últimos 5 dias (ou seja, segunda a sexta)
            for x in range(5):
                cardapio_dia = {
                    'almoco': {},
                    'jantar': {}
                }

                # Calcula o dia da semana a partir da data atual
                if data_atual.weekday() == 6:  # Se for domingo
                    numero_dia_semana = 0 - x % 7
                else:
                    numero_dia_semana = (data_atual.weekday()) - x % 7

                inicio_semana = data_atual - timedelta(days=numero_dia_semana)
                data_formatada = inicio_semana.strftime('%Y%m%d')

                # Procura a div do cardápio correspondente à data
                target_div = soup.find('div', {'about': f'/ru/cardapios/{data_formatada}-cardapio-restaurante-universitario-{url}'})
                if target_div is None:
                    target_div = soup.find('div', {'about': f'/ru/cardapios/{data_formatada}-cardapio-restaurante-universitario-{url}-0'})

                # Mapeia as classes de almoço e jantar
                mapeamento_informacoes_almoco = {
                    'prato_principal': 'field-name-field-principal-almoco',
                    'prato_veg': 'field-name-field-veg-almoco',
                    'arroz': 'field-name-field-arroz-almoco',
                    'feijao': 'field-name-field-feijao-almoco',
                    'guarnicao': 'field-name-field-guarnicao-almoco',
                    'salada': 'field-name-field-salada-almoco',
                }

                mapeamento_informacoes_jantar = {
                    'prato_principal': 'field-name-field-principal-jantar',
                    'prato_veg': 'field-name-field-veg-jantar',
                    'arroz': 'field-name-field-arroz-jantar',
                    'feijao': 'field-name-field-feijao-jantar',
                    'guarnicao': 'field-name-field-guarnicao-jantar',
                    'salada': 'field-name-field-salada-jantar',
                }

                # Preenche as informações de almoço
                for nome, classe in mapeamento_informacoes_almoco.items():
                    elementos = target_div.find('div', class_=classe)
                    if elementos:
                        texto_elemento = elementos.get_text(strip=True).split(':', 1)[1].strip()
                        cardapio_dia['almoco'][nome] = separa(texto_elemento)
                    else:
                        cardapio_dia['almoco'][nome] = f'{nome} Não Encontrado'

                # Preenche as informações de jantar
                for nome, classe in mapeamento_informacoes_jantar.items():
                    elementos = target_div.find('div', class_=classe)
                    if elementos:
                        texto_elemento = elementos.get_text(strip=True).split(':', 1)[1].strip()
                        cardapio_dia['jantar'][nome] = separa(texto_elemento)
                    else:
                        cardapio_dia['jantar'][nome] = f'{nome} Não Encontrado'

                # Adiciona o cardápio do dia ao campus
                campus[url].append({
                    'data': inicio_semana.strftime('%Y-%m-%d'),
                    'cardapio': cardapio_dia
                })

    return campus

# Função para salvar o resultado do scraping em um arquivo JSON
def salvar_json(campus_data, file_name='cardapios.json'):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(campus_data, json_file, ensure_ascii=False, indent=4)

def main():
    urls = {'santa-monica', 'monte-carmelo', 'umuarama'}

    campus_data = extrair_cardapios(urls)


    salvar_json(campus_data)


    salvar_no_banco(campus_data)


