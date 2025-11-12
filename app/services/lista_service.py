from sqlalchemy.orm import Session
from app.db.models import Lista, ItemLista
from app.repositories.lista_repository import ListaRepository
from app.schemas.lista import ListaCreate, ListaUpdate, ItemListaCreate, ItemListaUpdate
from typing import List as ListType, Optional
from fastapi import HTTPException, status

class ListaService:
    def __init__(self, db: Session):
        self.repository = ListaRepository(db)
    
    def get_lista(self, lista_id: int, current_user_id: int) -> Optional[Lista]:
        """
        Regla 2: Propiedad Exclusiva
        - Solo el usuario puede leer sus propias listas
        """
        lista = self.repository.get_by_id(lista_id)
        if not lista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lista no encontrada"
            )
        
        # Verificar propiedad
        if lista.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a esta lista"
            )
        
        return lista
    
    def get_listas_by_usuario(self, usuario_id: int, current_user_id: int, include_items: bool = False) -> ListType[Lista]:
        """
        Regla 2: Propiedad Exclusiva
        - Solo el usuario puede ver sus propias listas
        
        Parámetros:
        - include_items: Si es True, carga los items en la misma consulta (más eficiente)
        """
        if usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a estas listas"
            )
        
        return self.repository.get_all_by_usuario(usuario_id, include_items=include_items)
    
    def create_lista(self, usuario_id: int, lista_data: ListaCreate) -> Lista:
        """
        Validar título no vacío
        """
        if not lista_data.titulo or lista_data.titulo.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El título de la lista no puede estar vacío"
            )
        
        lista = Lista(
            usuario_id=usuario_id,
            titulo=lista_data.titulo.strip()
        )
        return self.repository.create(lista)
    
    def update_lista(self, lista_id: int, lista_data: ListaUpdate, current_user_id: int) -> Optional[Lista]:
        """
        Regla 2: Propiedad Exclusiva
        """
        lista = self.repository.get_by_id(lista_id)
        if not lista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lista no encontrada"
            )
        
        # Verificar propiedad
        if lista.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar esta lista"
            )
        
        if lista_data.titulo is not None:
            if lista_data.titulo.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El título de la lista no puede estar vacío"
                )
            lista.titulo = lista_data.titulo.strip()
        
        return self.repository.update(lista)
    
    def delete_lista(self, lista_id: int, current_user_id: int) -> bool:
        """
        Regla 2: Propiedad Exclusiva
        Regla 5: Borrado en Cascada (manejado por PostgreSQL)
        """
        lista = self.repository.get_by_id(lista_id)
        if not lista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lista no encontrada"
            )
        
        # Verificar propiedad
        if lista.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar esta lista"
            )
        
        return self.repository.delete(lista_id)
    
    # Métodos para items de lista
    def get_items_by_lista(self, lista_id: int, current_user_id: int) -> ListType[ItemLista]:
        """
        Obtener todos los items de una lista
        Regla 2: Propiedad Exclusiva
        """
        # Verificar que la lista existe y pertenece al usuario
        lista = self.repository.get_by_id(lista_id)
        if not lista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lista no encontrada"
            )
        
        if lista.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a los items de esta lista"
            )
        
        return self.repository.get_items_by_lista(lista_id)
    
    def create_item(self, lista_id: int, item_data: ItemListaCreate, current_user_id: int) -> Optional[ItemLista]:
        """
        Regla 2: Propiedad Exclusiva
        Regla 8: Límite de Descripción (255 caracteres)
        """
        # Verificar que la lista existe y pertenece al usuario
        lista = self.repository.get_by_id(lista_id)
        if not lista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lista no encontrada"
            )
        
        if lista.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para agregar items a esta lista"
            )
        
        # Validar título no vacío
        if not item_data.titulo or item_data.titulo.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El título del item no puede estar vacío"
            )
        
        # Validar límite de descripción (Regla 8)
        descripcion = item_data.descripcion
        if descripcion and len(descripcion) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La descripción no puede exceder 255 caracteres"
            )
        
        item = ItemLista(
            lista_id=lista_id,
            titulo=item_data.titulo.strip(),
            descripcion=descripcion.strip() if descripcion else None,
            completado=item_data.completado
        )
        return self.repository.create_item(item)
    
    def update_item(self, item_id: int, item_data: ItemListaUpdate, current_user_id: int) -> Optional[ItemLista]:
        """
        Regla 2: Propiedad Exclusiva
        Regla 8: Límite de Descripción
        Regla 9: Estado de Tarea
        """
        item = self.repository.get_item_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item no encontrado"
            )
        
        # Verificar propiedad a través de la lista
        lista = self.repository.get_by_id(item.lista_id)
        if lista.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este item"
            )
        
        if item_data.titulo is not None:
            if item_data.titulo.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El título del item no puede estar vacío"
                )
            item.titulo = item_data.titulo.strip()
        
        if item_data.descripcion is not None:
            # Validar límite de descripción (Regla 8)
            if len(item_data.descripcion) > 255:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La descripción no puede exceder 255 caracteres"
                )
            item.descripcion = item_data.descripcion.strip()
        
        # Regla 9: Estado de Tarea
        if item_data.completado is not None:
            item.completado = item_data.completado
        
        return self.repository.update_item(item)
    
    def delete_item(self, item_id: int, current_user_id: int) -> bool:
        """
        Regla 2: Propiedad Exclusiva
        """
        item = self.repository.get_item_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item no encontrado"
            )
        
        # Verificar propiedad a través de la lista
        lista = self.repository.get_by_id(item.lista_id)
        if lista.usuario_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar este item"
            )
        
        return self.repository.delete_item(item_id)

