from pydantic import BaseModel, ConfigDict
from typing import List

class Prato_DTO(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  
  id_prato: int
  quantidade: float

class Refeicao_DTO(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  tipo_refeicao: str
  pratos: List[Prato_DTO]

class Consumo_DTO(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  id_refeicao: int
  id_prato: int
  quantidade: float

class Map_Alimento_DTO(BaseModel):
  id_alimento: int
  quantidade: float
