from pydantic import BaseModel

class Usuario_DTO(BaseModel):
  nome: str
  email: str
  senha: str
  data_nascimento: str
  altura: float
  peso: float
  atividade: int
  sexo: str