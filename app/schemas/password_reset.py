from pydantic import BaseModel, EmailStr

class PasswordResetRequest(BaseModel):
    """Schema para solicitar reseteo de contraseña"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Schema para confirmar reseteo con nueva contraseña"""
    token: str
    new_password: str

class PasswordResetResponse(BaseModel):
    """Schema de respuesta genérica"""
    message: str

class TokenValidationResponse(BaseModel):
    """Schema para validación de token"""
    valid: bool
    message: str
