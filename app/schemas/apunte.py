from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ApunteBase(BaseModel):
    titulo: str
    contenido: str

class ApunteCreate(ApunteBase):
    carpeta_id: int

class ApunteUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    carpeta_id: Optional[int] = None

class ApunteResponse(ApunteBase):
    id: int
    carpeta_id: int
    creado_en: datetime
    
    class Config:
        from_attributes = True
