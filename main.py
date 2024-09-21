from fastapi import FastAPI
from database import Base, engine
from scraping import timer

Base.metadata.create_all(bind=engine)

app = FastAPI()
timer.setup_scrape_jobs()

@app.get("/")
def read_root():
    return {"Hello":"World"}
    

