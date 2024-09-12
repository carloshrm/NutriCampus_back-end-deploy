from pydantic import BaseModel
import classes

class Mensagem(BaseModel):
    titulo: str
    conteudo: str