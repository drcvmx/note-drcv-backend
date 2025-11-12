from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.lista import ListaCreate, ListaResponse, ListaUpdate, ItemListaCreate, ItemListaResponse, ItemListaUpdate
from app.services.lista_service import ListaService
from app.core.dependencies import get_current_user
from app.db.models import Usuario

router = APIRouter()

# Endpoints de Listas
@router.post("/", response_model=ListaResponse, status_code=status.HTTP_201_CREATED)
def create_lista(
    lista_data: ListaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear una nueva lista
    """
    service = ListaService(db)
    lista = service.create_lista(current_user.id, lista_data)
    return lista

@router.get("/", response_model=List[ListaResponse])
def get_listas(
    include_items: bool = False,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las listas del usuario autenticado
    
    Parámetros:
    - include_items: Si es True, incluye los items de cada lista en una sola consulta (más eficiente)
    """
    service = ListaService(db)
    listas = service.get_listas_by_usuario(current_user.id, current_user.id, include_items=include_items)
    return listas

@router.get("/{lista_id}", response_model=ListaResponse)
def get_lista(
    lista_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener una lista específica
    """
    service = ListaService(db)
    lista = service.get_lista(lista_id, current_user.id)
    return lista

@router.put("/{lista_id}", response_model=ListaResponse)
def update_lista(
    lista_id: int,
    lista_data: ListaUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar una lista
    """
    service = ListaService(db)
    lista = service.update_lista(lista_id, lista_data, current_user.id)
    return lista

@router.delete("/{lista_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lista(
    lista_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar una lista
    """
    service = ListaService(db)
    service.delete_lista(lista_id, current_user.id)
    return None


# Endpoints de Items de Lista
@router.get("/{lista_id}/items", response_model=List[ItemListaResponse])
def get_items(
    lista_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los items de una lista
    """
    service = ListaService(db)
    items = service.get_items_by_lista(lista_id, current_user.id)
    return items

@router.post("/{lista_id}/items", response_model=ItemListaResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    lista_id: int,
    item_data: ItemListaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Agregar un item a una lista
    """
    service = ListaService(db)
    item = service.create_item(lista_id, item_data, current_user.id)
    return item

@router.put("/items/{item_id}", response_model=ItemListaResponse)
def update_item(
    item_id: int,
    item_data: ItemListaUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar un item de lista
    """
    service = ListaService(db)
    item = service.update_item(item_id, item_data, current_user.id)
    return item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar un item de lista
    """
    service = ListaService(db)
    service.delete_item(item_id, current_user.id)
    return None

