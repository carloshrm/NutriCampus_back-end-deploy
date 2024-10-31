from pydantic import BaseModel, ConfigDict
from typing import List

class Ingrediente_DTO(BaseModel):
  nome_ingrediente: str
  quantidade: float
  id_alimento: int

class Prato_DTO(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  
  nome_prato: str
  ingredientes: List[Ingrediente_DTO]

class Refeicao_DTO(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  tipo_refeicao: str
  pratos: List[Prato_DTO]


