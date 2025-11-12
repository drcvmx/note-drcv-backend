from sqlalchemy.orm import Session
from app.db.models import Carpeta
from app.repositories.carpeta_repository import CarpetaRepository
from app.schemas.carpeta import CarpetaCreate, CarpetaUpdate
from typing import List, Optional
from fastapi import HTTPException, status

class CarpetaService:
    def __init__(self, db: Session):
        self.repository = CarpetaRepository(db)
    
    def get_carpeta(self, carpeta_id: int, current_user_id: int) -> Optional[Carpeta]:
        """
        Regla 2: Propiedad Exclusiva
        """
        carpeta = self.repository.get_by_id(carpeta_id)
        if not carpeta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carpeta no encontrada"
            )
        
        # Verificar propiedad
        if carpeta.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a esta carpeta"
            )
        
        return carpeta
    
    def get_carpetas_by_usuario(self, usuario_id: int, current_user_id: int) -> List[Carpeta]:
        """
        Regla 2: Propiedad Exclusiva
        """
        if usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a estas carpetas"
            )
        
        return self.repository.get_all_by_usuario(usuario_id)
    
    def get_root_carpetas(self, current_user_id: int) -> List[Carpeta]:
        """Obtener carpetas raíz del usuario"""
        return self.repository.get_root_carpetas(current_user_id)
    
    def get_subcarpetas(self, carpeta_padre_id: int, current_user_id: int) -> List[Carpeta]:
        """Obtener subcarpetas de una carpeta"""
        # Verificar que la carpeta padre pertenece al usuario
        carpeta_padre = self.repository.get_by_id(carpeta_padre_id)
        if not carpeta_padre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carpeta padre no encontrada"
            )
        
        if carpeta_padre.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a esta carpeta"
            )
        
        return self.repository.get_subcarpetas(carpeta_padre_id)
    
    def create_carpeta(self, usuario_id: int, carpeta_data: CarpetaCreate) -> Carpeta:
        """
        Validar nombre no vacío
        """
        if not carpeta_data.nombre or carpeta_data.nombre.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de la carpeta no puede estar vacío"
            )
        
        # Si tiene carpeta padre, verificar que existe y pertenece al usuario
        if carpeta_data.carpeta_padre_id is not None:
            carpeta_padre = self.repository.get_by_id(carpeta_data.carpeta_padre_id)
            if not carpeta_padre:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Carpeta padre no encontrada"
                )
            
            if carpeta_padre.usuario_id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para crear subcarpetas en esta carpeta"
                )
        
        carpeta = Carpeta(
            usuario_id=usuario_id,
            nombre=carpeta_data.nombre.strip(),
            carpeta_padre_id=carpeta_data.carpeta_padre_id
        )
        return self.repository.create(carpeta)
    
    def update_carpeta(self, carpeta_id: int, carpeta_data: CarpetaUpdate, current_user_id: int) -> Optional[Carpeta]:
        """
        Regla 2: Propiedad Exclusiva
        Regla 4: Prevención de Bucle Recursivo
        """
        carpeta = self.repository.get_by_id(carpeta_id)
        if not carpeta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carpeta no encontrada"
            )
        
        # Verificar propiedad
        if carpeta.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar esta carpeta"
            )
        
        if carpeta_data.nombre is not None:
            if carpeta_data.nombre.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de la carpeta no puede estar vacío"
                )
            carpeta.nombre = carpeta_data.nombre.strip()
        
        # Si se cambia la carpeta padre
        if carpeta_data.carpeta_padre_id is not None:
            # Regla 4: Verificar bucle recursivo
            if self.repository.check_circular_reference(carpeta_id, carpeta_data.carpeta_padre_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede mover la carpeta: crearía una referencia circular"
                )
            
            # Verificar que la nueva carpeta padre existe y pertenece al usuario
            nueva_carpeta_padre = self.repository.get_by_id(carpeta_data.carpeta_padre_id)
            if not nueva_carpeta_padre:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Carpeta padre no encontrada"
                )
            
            if nueva_carpeta_padre.usuario_id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para mover la carpeta aquí"
                )
            
            carpeta.carpeta_padre_id = carpeta_data.carpeta_padre_id
        
        return self.repository.update(carpeta)
    
    def delete_carpeta(self, carpeta_id: int, current_user_id: int) -> bool:
        """
        Regla 2: Propiedad Exclusiva
        Regla 5: Borrado en Cascada (manejado por PostgreSQL)
        """
        carpeta = self.repository.get_by_id(carpeta_id)
        if not carpeta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carpeta no encontrada"
            )
        
        # Verificar propiedad
        if carpeta.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar esta carpeta"
            )
        
        return self.repository.delete(carpeta_id)
