from sqlalchemy.orm import Session
from app.db.models import PasswordResetToken
from datetime import datetime, timezone
from typing import Optional

class PasswordResetRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, token_data: PasswordResetToken) -> PasswordResetToken:
        """Crear un nuevo token de reseteo"""
        self.db.add(token_data)
        self.db.commit()
        self.db.refresh(token_data)
        return token_data
    
    def get_by_token(self, token: str) -> Optional[PasswordResetToken]:
        """Obtener token por su valor"""
        return self.db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token
        ).first()
    
    def get_valid_token(self, token: str) -> Optional[PasswordResetToken]:
        """Obtener token válido (no usado y no expirado)"""
        now = datetime.now(timezone.utc)
        return self.db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.usado == False,
            PasswordResetToken.expira_en > now
        ).first()
    
    def mark_as_used(self, token: str) -> bool:
        """Marcar token como usado"""
        token_obj = self.get_by_token(token)
        if token_obj:
            token_obj.usado = True
            self.db.commit()
            return True
        return False
    
    def delete_expired_tokens(self) -> int:
        """Eliminar tokens expirados (limpieza)"""
        now = datetime.now(timezone.utc)
        deleted = self.db.query(PasswordResetToken).filter(
            PasswordResetToken.expira_en < now
        ).delete()
        self.db.commit()
        return deleted
    
    def delete_user_tokens(self, usuario_id: int) -> int:
        """Eliminar todos los tokens de un usuario"""
        deleted = self.db.query(PasswordResetToken).filter(
            PasswordResetToken.usuario_id == usuario_id
        ).delete()
        self.db.commit()
        return deleted
