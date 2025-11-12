from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.password_reset import (
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordResetResponse,
    TokenValidationResponse
)
from app.services.password_reset_service import PasswordResetService

router = APIRouter()

@router.post("/forgot-password", response_model=PasswordResetResponse)
def forgot_password(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Solicitar reseteo de contraseña
    
    - Envía un email con un link para resetear la contraseña
    - El link expira en 1 hora
    - Por seguridad, siempre retorna éxito (no revela si el email existe)
    """
    service = PasswordResetService(db)
    result = service.request_password_reset(request.email)
    return result

@router.get("/validate-token/{token}", response_model=TokenValidationResponse)
def validate_token(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Validar si un token de reseteo es válido
    
    - Verifica que el token exista
    - Verifica que no haya expirado
    - Verifica que no haya sido usado
    """
    service = PasswordResetService(db)
    result = service.validate_reset_token(token)
    return result

@router.post("/reset-password", response_model=PasswordResetResponse)
def reset_password(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """
    Resetear la contraseña usando el token
    
    - Valida el token
    - Actualiza la contraseña
    - Marca el token como usado
    - Envía email de confirmación
    """
    service = PasswordResetService(db)
    result = service.reset_password(request.token, request.new_password)
    return result
