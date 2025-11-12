from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CarpetaBase(BaseModel):
    nombre: str
    carpeta_padre_id: Optional[int] = None

class CarpetaCreate(CarpetaBase):
    pass

class CarpetaUpdate(BaseModel):
    nombre: Optional[str] = None
    carpeta_padre_id: Optional[int] = None

class CarpetaResponse(CarpetaBase):
    id: int
    usuario_id: int
    
    class Config:
        from_attributes = True

# Para respuestas con jerarquía
class CarpetaWithChildren(CarpetaResponse):
    subcarpetas: List['CarpetaWithChildren'] = []
    
    class Config:
        from_attributes = True
