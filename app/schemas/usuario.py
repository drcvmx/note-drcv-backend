from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    username: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    fondo_url: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    fondo_url: Optional[str] = None
    creado_en: datetime
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
