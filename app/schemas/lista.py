from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ItemListaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    completado: bool = False

class ItemListaCreate(ItemListaBase):
    pass

class ItemListaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    completado: Optional[bool] = None

class ItemListaResponse(ItemListaBase):
    id: int
    lista_id: int
    
    class Config:
        from_attributes = True


class ListaBase(BaseModel):
    titulo: str

class ListaCreate(ListaBase):
    pass

class ListaUpdate(BaseModel):
    titulo: Optional[str] = None

class ListaResponse(ListaBase):
    id: int
    usuario_id: int
    creado_en: datetime
    items: List[ItemListaResponse] = []
    
    class Config:
        from_attributes = True
