from sqlalchemy.orm import Session
from app.db.models import Apunte
from app.repositories.apunte_repository import ApunteRepository
from app.repositories.carpeta_repository import CarpetaRepository
from app.schemas.apunte import ApunteCreate, ApunteUpdate
from typing import List, Optional
from fastapi import HTTPException, status

class ApunteService:
    def __init__(self, db: Session):
        self.repository = ApunteRepository(db)
        self.carpeta_repository = CarpetaRepository(db)
    
    def get_apunte(self, apunte_id: int, current_user_id: int) -> Optional[Apunte]:
        """
        Regla 2: Propiedad Exclusiva
        - Solo el usuario puede leer sus propios apuntes
        """
        apunte = self.repository.get_by_id(apunte_id)
        if not apunte:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Apunte no encontrado"
            )
        
        # Verificar propiedad a través de la carpeta
        carpeta = self.carpeta_repository.get_by_id(apunte.carpeta_id)
        if carpeta.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a este apunte"
            )
        
        return apunte
    
    def get_apuntes_by_carpeta(self, carpeta_id: int, current_user_id: int) -> List[Apunte]:
        """
        Regla 2: Propiedad Exclusiva
        """
        # Verificar que la carpeta pertenece al usuario
        carpeta = self.carpeta_repository.get_by_id(carpeta_id)
        if not carpeta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carpeta no encontrada"
            )
        
        if carpeta.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a esta carpeta"
            )
        
        return self.repository.get_all_by_carpeta(carpeta_id)
    
    def create_apunte(self, apunte_data: ApunteCreate, current_user_id: int) -> Apunte:
        """
        Regla 6: Enrutamiento de Apuntes
        - Un apunte debe estar asociado a una carpeta válida y existente
        Regla 7: Contenido Obligatorio
        """
        # Validar contenido no vacío
        if not apunte_data.contenido or apunte_data.contenido.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El contenido del apunte no puede estar vacío"
            )
        
        # Validar título no vacío
        if not apunte_data.titulo or apunte_data.titulo.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El título del apunte no puede estar vacío"
            )
        
        # Verificar que la carpeta existe y pertenece al usuario
        carpeta = self.carpeta_repository.get_by_id(apunte_data.carpeta_id)
        if not carpeta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carpeta no encontrada"
            )
        
        if carpeta.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para crear apuntes en esta carpeta"
            )
        
        apunte = Apunte(
            carpeta_id=apunte_data.carpeta_id,
            titulo=apunte_data.titulo.strip(),
            contenido=apunte_data.contenido.strip()
        )
        return self.repository.create(apunte)
    
    def update_apunte(self, apunte_id: int, apunte_data: ApunteUpdate, current_user_id: int) -> Optional[Apunte]:
        """
        Regla 2: Propiedad Exclusiva
        Regla 7: Contenido Obligatorio
        """
        apunte = self.repository.get_by_id(apunte_id)
        if not apunte:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Apunte no encontrado"
            )
        
        # Verificar propiedad
        carpeta = self.carpeta_repository.get_by_id(apunte.carpeta_id)
        if carpeta.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este apunte"
            )
        
        # Validar contenido no vacío si se está actualizando
        if apunte_data.contenido is not None:
            if apunte_data.contenido.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El contenido del apunte no puede estar vacío"
                )
            apunte.contenido = apunte_data.contenido.strip()
        
        # Validar título no vacío si se está actualizando
        if apunte_data.titulo is not None:
            if apunte_data.titulo.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El título del apunte no puede estar vacío"
                )
            apunte.titulo = apunte_data.titulo.strip()
        
        # Si se cambia de carpeta, verificar que la nueva carpeta existe y pertenece al usuario
        if apunte_data.carpeta_id is not None:
            nueva_carpeta = self.carpeta_repository.get_by_id(apunte_data.carpeta_id)
            if not nueva_carpeta:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Carpeta destino no encontrada"
                )
            
            if nueva_carpeta.usuario_id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para mover el apunte a esta carpeta"
                )
            
            apunte.carpeta_id = apunte_data.carpeta_id
        
        return self.repository.update(apunte)
    
    def delete_apunte(self, apunte_id: int, current_user_id: int) -> bool:
        """
        Regla 2: Propiedad Exclusiva
        """
        apunte = self.repository.get_by_id(apunte_id)
        if not apunte:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Apunte no encontrado"
            )
        
        # Verificar propiedad
        carpeta = self.carpeta_repository.get_by_id(apunte.carpeta_id)
        if carpeta.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar este apunte"
            )
        
        return self.repository.delete(apunte_id)
