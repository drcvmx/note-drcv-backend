from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotaBase(BaseModel):
    titulo: str
    contenido: str

class NotaCreate(NotaBase):
    pass

class NotaUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None

class NotaResponse(NotaBase):
    id: int
    usuario_id: int
    creado_en: datetime
    actualizado_en: datetime
    
    class Config:
        from_attributes = True
