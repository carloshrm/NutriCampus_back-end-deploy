from fastapi import FastAPI
from database import Base, engine
from scraping import timer
from routers import alimento_route, usuario_route, cardapio_route, refeicao_route
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

timer.setup_scrape_jobs()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_route.router)
app.include_router(refeicao_route.router)
app.include_router(alimento_route.router)
app.include_router(cardapio_route.router)

@app.get("/")
def read_root():
    return {"Hello":"World"}
