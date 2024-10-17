from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Função para pesquisar no DuckDuckGo
def search_duckduckgo(query):
    url = "https://duckduckgo8.p.rapidapi.com/"
    querystring = {"q": query + " site:minhasreceitinhas.com.br"}

    headers_api = {
        "x-rapidapi-key": "7331f09302msh1358e1c8749f727p1914d8jsnfb1bd32ec7c4",
        "x-rapidapi-host": "duckduckgo8.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers_api, params=querystring)

    if response.status_code == 200:
        search_results = response.json().get('results', [])
        if search_results:
            return search_results[0].get('url')  # Pega o primeiro link
        else:
            print("Nenhum resultado encontrado.")
            return None
    else:
        print('Requisição para a API falhou com status:', response.status_code)
        return None

# Função para scraping da página com Selenium
def scrape_website(website):
    print("Connecting to Scraping Browser...")
    
    service = Service(executable_path="./chromedriver.exe") 
    options = Options()
    options.add_argument("--headless")  # Para executar sem abrir o navegador
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(website)
    print("Navigated! Scraping page content...")
    html = driver.page_source
    driver.quit()  # Fechar o navegador após o scraping
    return html

# Função para extrair a <ul> dos ingredientes
def extract_ingredients_list(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Debug: Printar uma parte do conteúdo HTML bruto para inspecionar
    print("HTML bruto da página (primeiros 500 caracteres):")
    print(html_content[:500])
    
    # Isolando a <ul> que contém os ingredientes
    ingredients_list = soup.find('ul', class_='recipe-content__steps') 
    
    if ingredients_list:
        print("Lista de ingredientes encontrada!")
        print(ingredients_list.prettify())  # Imprimir a <ul> encontrada com formatação
        return str(ingredients_list)
    else:
        print('Lista de ingredientes não encontrada.')
        return None

# Template do prompt para o LLM
template = (
    "You are tasked with extracting specific information from the following HTML content: {dom_content}. "
    "Please extract the ingredients list in a structured format (quantity, unit, ingredient name) as follows:\n"
    "1. For each ingredient, extract it in the format: [quantity] [unit] [ingredient name].\n"
    "2. If the ingredient has no quantity or unit, leave those fields empty.\n"
    "3. Return the extracted ingredients as a list of bullet points."
)

# Modelo OllamaLLM
model = OllamaLLM(model="llama3.2")

# Função para processar o conteúdo com LLM (Ollama)
def parse_with_ollama(ingredients_html, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    response = chain.invoke(
        {"dom_content": ingredients_html, "parse_description": parse_description}
    )
    
    print(f"Parsed ingredients:")
    return response


def run_mvp_test():
    website = "https://minhasreceitinhas.com.br/receita/arroz-branco-soltinho/"

    if website:
        print(f"Link encontrado: {website}")
        
        # Etapa 2: Faz o scraping da página encontrada usando Selenium
        html_content = scrape_website(website)
        
        # Etapa 3: Extrai a <ul> que contém a lista de ingredientes
        ingredients_html = extract_ingredients_list(html_content)
        
        if ingredients_html:
            # Etapa 4: Usa o LLM para processar a <ul> e extrair os ingredientes
            parse_description = "Extraia os ingredientes de uma receita de arroz branco"
            parsed_results = parse_with_ollama(ingredients_html, parse_description)
            
            print("Resultado final extraído pelo LLM:")
            print(parsed_results)
        else:
            print("Não foi possível extrair os ingredientes da página.")
    else:
        print("Nenhum link válido encontrado para o termo pesquisado.")

# Executa o MVP
if __name__ == "__main__":
    run_mvp_test()
