from sqlalchemy.orm import Session
from app.db.models import PasswordResetToken
from app.repositories.password_reset_repository import PasswordResetRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.email_service import EmailService
from app.core.security import get_password_hash
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from typing import Optional
import secrets

class PasswordResetService:
    def __init__(self, db: Session):
        self.db = db
        self.reset_repository = PasswordResetRepository(db)
        self.usuario_repository = UsuarioRepository(db)
        self.email_service = EmailService()
    
    def request_password_reset(self, email: str) -> dict:
        """
        Solicitar reseteo de contraseña
        
        Nota de seguridad: Siempre retorna éxito para no revelar si el email existe
        """
        # Buscar usuario por email
        usuario = self.usuario_repository.get_by_email(email)
        
        if usuario:
            # Invalidar tokens anteriores del usuario
            self.reset_repository.delete_user_tokens(usuario.id)
            
            # Generar token seguro
            token = secrets.token_urlsafe(32)
            
            # Token válido por 1 hora
            expira_en = datetime.now(timezone.utc) + timedelta(hours=1)
            
            # Guardar token en BD
            reset_token = PasswordResetToken(
                usuario_id=usuario.id,
                token=token,
                expira_en=expira_en
            )
            self.reset_repository.create(reset_token)
            
            # Enviar email
            self.email_service.send_password_reset_email(
                to_email=usuario.email,
                reset_token=token,
                username=usuario.username
            )
        
        # Siempre retornar éxito (seguridad)
        return {
            "message": "Si el email existe, recibirás un enlace de recuperación"
        }
    
    def validate_reset_token(self, token: str) -> dict:
        """
        Validar si un token es válido
        """
        reset_token = self.reset_repository.get_valid_token(token)
        
        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido o expirado"
            )
        
        return {
            "valid": True,
            "message": "Token válido"
        }
    
    def reset_password(self, token: str, new_password: str) -> dict:
        """
        Resetear la contraseña usando el token
        """
        # Validar token
        reset_token = self.reset_repository.get_valid_token(token)
        
        if not reset_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido o expirado"
            )
        
        # Obtener usuario
        usuario = self.usuario_repository.get_by_id(reset_token.usuario_id)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Validar contraseña (mínimo 8 caracteres)
        if len(new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 8 caracteres"
            )
        
        # Actualizar contraseña
        usuario.password_hash = get_password_hash(new_password)
        self.usuario_repository.update(usuario)
        
        # Marcar token como usado
        self.reset_repository.mark_as_used(token)
        
        # Enviar email de confirmación
        self.email_service.send_password_changed_confirmation(
            to_email=usuario.email,
            username=usuario.username
        )
        
        return {
            "message": "Contraseña actualizada exitosamente"
        }
    
    def cleanup_expired_tokens(self) -> int:
        """
        Limpiar tokens expirados (puede ejecutarse como tarea programada)
        """
        return self.reset_repository.delete_expired_tokens()
