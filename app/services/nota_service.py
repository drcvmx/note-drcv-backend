from sqlalchemy.orm import Session
from app.db.models import Nota
from app.repositories.nota_repository import NotaRepository
from app.schemas.nota import NotaCreate, NotaUpdate
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime

class NotaService:
    def __init__(self, db: Session):
        self.repository = NotaRepository(db)
    
    def get_nota(self, nota_id: int, current_user_id: int) -> Optional[Nota]:
        """
        Regla 2: Propiedad Exclusiva
        - Solo el usuario puede leer sus propias notas
        """
        nota = self.repository.get_by_id(nota_id)
        if not nota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota no encontrada"
            )
        
        # Verificar propiedad
        if nota.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a esta nota"
            )
        
        return nota
    
    def get_notas_by_usuario(self, usuario_id: int, current_user_id: int) -> List[Nota]:
        """
        Regla 2: Propiedad Exclusiva
        - Solo el usuario puede ver sus propias notas
        """
        if usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a estas notas"
            )
        
        return self.repository.get_all_by_usuario(usuario_id)
    
    def create_nota(self, usuario_id: int, nota_data: NotaCreate) -> Nota:
        """
        Regla 7: Contenido Obligatorio
        - El contenido no puede estar vacío
        """
        # Validar contenido no vacío
        if not nota_data.contenido or nota_data.contenido.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El contenido de la nota no puede estar vacío"
            )
        
        # Validar título no vacío
        if not nota_data.titulo or nota_data.titulo.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El título de la nota no puede estar vacío"
            )
        
        nota = Nota(
            usuario_id=usuario_id,
            titulo=nota_data.titulo.strip(),
            contenido=nota_data.contenido.strip()
        )
        return self.repository.create(nota)
    
    def update_nota(self, nota_id: int, nota_data: NotaUpdate, current_user_id: int) -> Optional[Nota]:
        """
        Regla 2: Propiedad Exclusiva
        Regla 7: Contenido Obligatorio
        Regla 10: Actualización automática de actualizado_en
        """
        nota = self.repository.get_by_id(nota_id)
        if not nota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota no encontrada"
            )
        
        # Verificar propiedad
        if nota.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar esta nota"
            )
        
        # Validar contenido no vacío si se está actualizando
        if nota_data.contenido is not None:
            if nota_data.contenido.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El contenido de la nota no puede estar vacío"
                )
            nota.contenido = nota_data.contenido.strip()
        
        # Validar título no vacío si se está actualizando
        if nota_data.titulo is not None:
            if nota_data.titulo.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El título de la nota no puede estar vacío"
                )
            nota.titulo = nota_data.titulo.strip()
        
        # Actualizar timestamp (Regla 10)
        nota.actualizado_en = datetime.utcnow()
        
        return self.repository.update(nota)
    
    def delete_nota(self, nota_id: int, current_user_id: int) -> bool:
        """
        Regla 2: Propiedad Exclusiva
        - Solo el usuario puede eliminar sus propias notas
        """
        nota = self.repository.get_by_id(nota_id)
        if not nota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota no encontrada"
            )
        
        # Verificar propiedad
        if nota.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar esta nota"
            )
        
        return self.repository.delete(nota_id)

