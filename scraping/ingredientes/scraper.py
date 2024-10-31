import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
from unidecode import unidecode
from processador import processar_ingrediente
import logging
import os
from dotenv import load_dotenv

load_dotenv()


def buscar_link_receita(receita: str) -> Optional[str]:
    """
    Busca o link da receita usando a API do DuckDuckGo.

    Args:
        receita (str): Nome da receita.

    Returns:
        str ou None: URL da receita encontrada ou None se não encontrar.
    """
    url = "https://duckduckgo8.p.rapidapi.com/"
    querystring = {"q": f"{receita} site:minhasreceitinhas.com.br"}

    headers_api = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("RAPIDAPI_HOST")
    }

    try:
        response = requests.get(url, headers=headers_api, params=querystring)
        response.raise_for_status()
        logging.info("Requisição à API do DuckDuckGo bem-sucedida!")
        search_results = response.json().get('results', [])
        if search_results:
            link_encontrado = search_results[0].get('url')  # Pega o primeiro link da resposta
            logging.info(f"Link encontrado: {link_encontrado}")
            return link_encontrado
        else:
            logging.info("Nenhum resultado encontrado.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Requisição para a API falhou: {e}")
        return None


def obter_soup_da_receita(url_receita: str) -> Optional[BeautifulSoup]:
    """
    Faz a requisição para a página da receita e retorna o BeautifulSoup.

    Args:
        url_receita (str): URL da receita.

    Returns:
        BeautifulSoup ou None: Objeto BeautifulSoup da página ou None em caso de erro.
    """
    headers_receita = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'pt-BR,pt;q=0.7',
        'Referer': 'https://www.google.com/'
    }

    try:
        logging.info(f"Fazendo requisição para o link da receita: {url_receita}")
        response = requests.get(url_receita, headers=headers_receita)
        response.raise_for_status()
        logging.info("Requisição para a página da receita bem-sucedida!")
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        logging.error(f"Requisição para a receita falhou: {e}")
        return None


def extrair_ingredientes(soup: BeautifulSoup) -> List[Dict]:
    """
    Extrai a lista de ingredientes da página da receita.

    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup da página.

    Returns:
        List[Dict]: Lista de ingredientes processados.
    """
    lista_ingredientes = []
    ingredientes = soup.find('ul', class_='recipe-content__steps')

    if ingredientes:
        # Imprimir o texto original da ul
        texto_original = ingredientes.get_text(separator='\n', strip=True)
        logging.info('Texto original da ul:')
        logging.info(texto_original)

        for ingrediente in ingredientes.find_all('li'):
            texto_limpo = unidecode(ingrediente.get_text(strip=True)
                                    .replace('Check', '')
                                    .replace('\r', '')).strip()
            resultado = processar_ingrediente(texto_limpo)
            if resultado:
                lista_ingredientes.append(resultado)

        logging.info('Lista de ingredientes extraída com sucesso.')
    else:
        logging.warning('Lista de ingredientes não encontrada.')

    return lista_ingredientes
