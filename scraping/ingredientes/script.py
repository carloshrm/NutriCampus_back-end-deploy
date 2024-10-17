import requests
import re
from bs4 import BeautifulSoup
from unidecode import unidecode
from dotenv import load_dotenv
import os

load_dotenv()

# Função para converter unidades para o singular
def converter_para_singular(unidade):
    plurais_para_singular = {
        'xicaras': 'xicara',
        'colheres': 'colher',
        'colheres de cha': 'colher (cha)',
        'colheres de sopa': 'colher (sopa)',
        'colher de chas': 'colher (cha)',
        'colher de sopas': 'colher (sopa)',
        'gramas': 'grama',
        'kgs': 'kg',
        'mls': 'ml',
        'litros': 'litro',
        'folhas': 'folha',
        'dentes': 'dente',
        'pitadas': 'pitada',
        'gotas': 'gota',
        'latas': 'lata',
        'copos': 'copo',
        'unidades': 'unidade'
    }
    unidade = unidade.strip().lower()
    unidade_singular = plurais_para_singular.get(unidade, unidade)
    return unidade_singular

# Função de Conversão de Unidades
def converter_para_unidade_padrao(quantidade, unidade_original):
    conversoes = {
        'xicara': ('ml', 240),
        'xicara (cha)': ('ml', 240),
        'colher (sopa)': ('ml', 15),
        'colher (cha)': ('ml', 5),
        'colher': ('ml', 15),  # Assumindo colher como colher de sopa
        'grama': ('g', 1),
        'kg': ('g', 1000),
        'g': ('g', 1),
        'ml': ('ml', 1),
        'litro': ('ml', 1000),
        'folha': ('unitario', 1),
        'dente': ('unitario', 1),
        'pitada': ('unitario', 1),
        'gota': ('unitario', 1),
        'lata': ('unitario', 1),
        'copo': ('ml', 250),
        'unidade': ('unitario', 1),
        'unitario': ('unitario', 1)
    }
    unidade_original_lower = unidade_original.lower() if unidade_original else ''
    if unidade_original_lower in conversoes:
        unidade_padrao, fator = conversoes[unidade_original_lower]
        quantidade_normalizada = quantidade * fator
        return quantidade_normalizada, unidade_padrao
    else:
        return quantidade, unidade_original  # Unidade não reconhecida, retorna como está

# Função para avaliar quantidades (incluindo frações)
def avaliar_quantidade(quantidade_str):
    quantidade_str = quantidade_str.replace(',', '.').strip()
    try:
        if ' ' in quantidade_str:
            partes = quantidade_str.split(' ')
            inteiro = float(partes[0])
            frac_str = partes[1]
            numerador, denominador = map(float, frac_str.split('/'))
            return inteiro + (numerador / denominador)
        elif '/' in quantidade_str:
            numerador, denominador = map(float, quantidade_str.split('/'))
            return numerador / denominador
        else:
            return float(quantidade_str)
    except:
        return None  # Retorna None se não for possível avaliar


def processar_ingrediente(texto_limpo):
    # Verificar se o ingrediente é "opcional" e descartar se for
    if 'opcional' in texto_limpo.lower():
        return None

    # Verificar se o ingrediente é "a gosto"
    if 'a gosto' in texto_limpo.lower():
        return {
            'nome_ingrediente': texto_limpo.replace('a gosto', '').strip(),
            'quantidade': None,
            'unidade_original': None,
            'a_gosto': True
        }

    # Substituir frações unicode por texto
    substituicoes = {
        '½': '1/2',
        '⅓': '1/3',
        '⅔': '2/3',
        '¼': '1/4',
        '¾': '3/4',
        '⅛': '1/8',
    }
    for k, v in substituicoes.items():
        texto_limpo = texto_limpo.replace(k, v)

    # Expressão regular para capturar variações de unidades
    pattern = r'^(\d+\s+\d+/\d+|\d+/\d+|\d+(?:[\.,]\d+)?)\s+(.*?)\s+(?:de\s+)?(.*)$'
    
    match = re.match(pattern, texto_limpo, re.IGNORECASE)
    if match:
        quantidade_str = match.group(1)
        unidade_raw = match.group(2).strip()
        nome_ingrediente = match.group(3).strip()
    else:
        # Tentar outra expressão regular sem unidade
        pattern_sem_unidade = r'^(\d+\s+\d+/\d+|\d+/\d+|\d+(?:[\.,]\d+)?)(.*)$'
        match_sem_unidade = re.match(pattern_sem_unidade, texto_limpo, re.IGNORECASE)
        if match_sem_unidade:
            quantidade_str = match_sem_unidade.group(1)
            unidade_raw = ''
            nome_ingrediente = match_sem_unidade.group(2).strip()
        else:
            # Se não houver correspondência, assumir que é apenas o nome do ingrediente
            quantidade_str = None
            unidade_raw = None
            nome_ingrediente = texto_limpo.strip()

    # Converter quantidade para float
    quantidade = avaliar_quantidade(quantidade_str) if quantidade_str else None

    # Limpar e padronizar a unidade
    if unidade_raw is not None:
        unidade_clean = unidade_raw.lower()
        
        # Padronizar colheres
        if 'colher' in unidade_clean or 'colheres' in unidade_clean:
            if 'chá' in unidade_clean or 'cha' in unidade_clean:
                unidade_original = 'colher (cha)'
            elif 'sopa' in unidade_clean:
                unidade_original = 'colher (sopa)'
            else:
                # Se não especificado, assumir colher de sopa
                unidade_original = 'colher (sopa)'
        elif 'xícara' in unidade_clean or 'xicara' in unidade_clean:
            unidade_original = 'xicara (cha)'  # Assumindo que xícaras são geralmente de chá
        else:
            # Converter para singular outras unidades
            unidade_original = converter_para_singular(unidade_clean)

        # Remover a unidade do nome do ingrediente
        nome_ingrediente = re.sub(r'^.*?\bde\b', '', nome_ingrediente).strip()
    else:
        unidade_original = None

    # Se não houver unidade, mas houver quantidade, definir 'unitario' como unidade
    if quantidade is not None and (unidade_original is None or unidade_original == ''):
        unidade_original = 'unitario'

    # Converter a unidade para algo padronizado
    quantidade_normalizada, unidade_normalizada = converter_para_unidade_padrao(quantidade, unidade_original)

    return {
        'nome_ingrediente': nome_ingrediente.strip(),
        'quantidade': quantidade,
        'unidade_original': unidade_original,
        'a_gosto': False,
        'quantidade_normalizada': quantidade_normalizada,
        'unidade_normalizada': unidade_normalizada
    }

# Receita a ser buscada
receita = 'arroz branco'
lista_ingredientes = []

# Usando a API do DuckDuckGo para buscar a receita no site 'minhasreceitinhas.com.br'
url = "https://duckduckgo8.p.rapidapi.com/"
querystring = {"q": f"{receita} site:minhasreceitinhas.com.br"}

headers_api = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
    "x-rapidapi-host": os.getenv("RAPIDAPI_HOST")
}

# Fazendo a requisição à API do DuckDuckGo
response = requests.get(url, headers=headers_api, params=querystring)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    print("Requisição à API do DuckDuckGo bem-sucedida!")
    search_results = response.json().get('results', [])

    if search_results:
        link_encontrado = search_results[0].get('url')  # Pega o primeiro link da resposta
        print(f"Link encontrado: {link_encontrado}")
    else:
        print("Nenhum resultado encontrado.")
        link_encontrado = None
else:
    print('Requisição para a API falhou com status:', response.status_code)
    link_encontrado = None

# Verificar se a URL foi encontrada antes de continuar
if link_encontrado:
    try:
        headers_receita = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'pt-BR,pt;q=0.7',
            'Referer': 'https://www.google.com/'
        }

        print(f"Fazendo requisição para o link da receita: {link_encontrado}")
        requestReceita = requests.get(link_encontrado, headers=headers_receita)

        if requestReceita.status_code == 200:
            print("Requisição para a página da receita bem-sucedida!")
            soup = BeautifulSoup(requestReceita.text, 'html.parser')

            ingredientes = soup.find('ul', class_='recipe-content__steps')

            if ingredientes:
                for ingrediente in ingredientes.find_all('li'):
                    texto_limpo = unidecode(ingrediente.get_text(strip=True)
                                            .replace('Check', '')
                                            .replace('\r', '')).strip()
                    resultado = processar_ingrediente(texto_limpo)
                    if resultado:
                        lista_ingredientes.append(resultado)

                print('Lista de ingredientes:')
                for ingrediente in lista_ingredientes:
                    print(ingrediente)
            else:
                print('Lista de ingredientes não encontrada.')
        else:
            print(f"Requisição para a receita falhou com status: {requestReceita.status_code}")
    except Exception as e:
        print(f"Erro ao tentar acessar a URL: {e}")
else:
    print("Nenhuma URL válida foi encontrada nos resultados do DuckDuckGo.")
