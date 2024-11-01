import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from scraping.TACO import script as TACOScraping
from scraping.Cardapio import scrapping as CardapioScraping

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
    TACOScraping.executar_scraping()
  except:
    print("Erro ao executar scraping da tabela TACO.")

  CardapioScraping.main()
  # chamar outras tarefas de scraping

def setup_scrape_jobs():
  scheduler = BackgroundScheduler()
  scheduler.add_jobstore('sqlalchemy', url=SQLALCHEMY_DATABASE_URL)
  scheduler.start()

  if not scheduler.get_job(JOB_NAME):
    run_all_scrapes()
    scheduler.add_job(run_all_scrapes, 'cron', day_of_week='sun', hour=1, id=JOB_NAME, coalesce=True)
  