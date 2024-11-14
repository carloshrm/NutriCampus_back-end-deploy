import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from scraping.TACO import script as TACOScraping
from scraping.Cardapio import scrapping as CardapioScraping
from scraping.receitas import prato as PratoMapeamento
from scraping.ingredientes import main as IngredientesteScraping
#from scraping.ingredientes import verificar_ingredientes as GeminiAction

load_dotenv()

user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
host = os.getenv("HOST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"

JOB_NAME = 'z-timer'

def run_all_scrapes():
  print("Rodando todos os scrapes")
  try:
    print("Rodando TACOScraping.executar_scraping()")
    TACOScraping.executar_scraping()
  except:
    print("Erro ao executar scraping da tabela TACO.")

  try:
    print("Rodando CardapioScraping.main()")
    CardapioScraping.main()
  except:
    print("Erro ao executar scraping de cardapio da UFU")

  try:
    print("Rodando mapeamento_prato()")
    PratoMapeamento.main()
  except:
    print("Erro ao executar mapeamento dos prato baseado em Cardapios")
    
  try:
    print("Rodando ingredientesScraping main()")
    IngredientesteScraping.main()
    #GeminiAction.processar_ingredientes_com_gemini()
  except:
    print("Erro ao executar ingredientesScraping main()")  


def setup_scrape_jobs():
  scheduler = BackgroundScheduler()
  scheduler.add_jobstore('sqlalchemy', url=SQLALCHEMY_DATABASE_URL)
  scheduler.start()

  if not scheduler.get_job(JOB_NAME):
    run_all_scrapes()
    scheduler.add_job(run_all_scrapes, 'cron', minutes=2, id=JOB_NAME, coalesce=True)
