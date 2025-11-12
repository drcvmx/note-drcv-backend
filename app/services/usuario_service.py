from sqlalchemy.orm import Session
from app.db.models import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional
from fastapi import HTTPException, status

class UsuarioService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)
    
    def get_usuario(self, usuario_id: int) -> Optional[Usuario]:
        return self.repository.get_by_id(usuario_id)
    
    def get_usuario_by_username(self, username: str) -> Optional[Usuario]:
        return self.repository.get_by_username(username)
    
    def create_usuario(self, usuario_data: UsuarioCreate) -> Usuario:
        """
        Regla 3: Integridad de Login
        - Verificar que username y email no existan
        - Hashear la contraseña antes de guardar
        """
        # Verificar si el usuario ya existe
        if self.repository.get_by_username(usuario_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El username ya está en uso"
            )
        if self.repository.get_by_email(usuario_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso"
            )
        
        # Crear usuario con contraseña hasheada
        usuario = Usuario(
            nombre=usuario_data.nombre,
            email=usuario_data.email,
            username=usuario_data.username,
            password_hash=get_password_hash(usuario_data.password)
        )
        return self.repository.create(usuario)
    
    def update_usuario(self, usuario_id: int, usuario_data: UsuarioUpdate, current_user_id: int) -> Optional[Usuario]:
        """
        Regla 2: Propiedad Exclusiva
        - Solo el usuario puede modificar sus propios datos
        """
        # Verificar propiedad
        if usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este usuario"
            )
        
        usuario = self.repository.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar email único si se está actualizando
        if usuario_data.email is not None and usuario_data.email != usuario.email:
            if self.repository.get_by_email(usuario_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está en uso"
                )
            usuario.email = usuario_data.email
        
        if usuario_data.nombre is not None:
            usuario.nombre = usuario_data.nombre
        if usuario_data.fondo_url is not None:
            usuario.fondo_url = usuario_data.fondo_url
        
        return self.repository.update(usuario)
    
    def authenticate_usuario(self, username: str, password: str) -> Optional[Usuario]:
        """
        Regla 3: Integridad de Login
        - Verificar contraseña hasheada
        """
        usuario = self.repository.get_by_username(username)
        if not usuario:
            return None
        if not verify_password(password, usuario.password_hash):
            return None
        return usuario

