from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.carpeta import CarpetaCreate, CarpetaResponse, CarpetaUpdate
from app.services.carpeta_service import CarpetaService
from app.core.dependencies import get_current_user
from app.db.models import Usuario

router = APIRouter()

@router.post("/", response_model=CarpetaResponse, status_code=status.HTTP_201_CREATED)
def create_carpeta(
    carpeta_data: CarpetaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear una nueva carpeta
    """
    service = CarpetaService(db)
    carpeta = service.create_carpeta(current_user.id, carpeta_data)
    return carpeta

@router.get("/", response_model=List[CarpetaResponse])
def get_carpetas(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las carpetas del usuario autenticado
    """
    service = CarpetaService(db)
    carpetas = service.get_carpetas_by_usuario(current_user.id, current_user.id)
    return carpetas

@router.get("/root", response_model=List[CarpetaResponse])
def get_root_carpetas(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener carpetas raíz (sin padre) del usuario autenticado
    """
    service = CarpetaService(db)
    carpetas = service.get_root_carpetas(current_user.id)
    return carpetas

@router.get("/{carpeta_id}", response_model=CarpetaResponse)
def get_carpeta(
    carpeta_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener una carpeta específica
    """
    service = CarpetaService(db)
    carpeta = service.get_carpeta(carpeta_id, current_user.id)
    return carpeta

@router.get("/{carpeta_id}/subcarpetas", response_model=List[CarpetaResponse])
def get_subcarpetas(
    carpeta_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener subcarpetas de una carpeta específica
    """
    service = CarpetaService(db)
    subcarpetas = service.get_subcarpetas(carpeta_id, current_user.id)
    return subcarpetas

@router.put("/{carpeta_id}", response_model=CarpetaResponse)
def update_carpeta(
    carpeta_id: int,
    carpeta_data: CarpetaUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar una carpeta
    """
    service = CarpetaService(db)
    carpeta = service.update_carpeta(carpeta_id, carpeta_data, current_user.id)
    return carpeta

@router.delete("/{carpeta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_carpeta(
    carpeta_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar una carpeta (y sus subcarpetas/apuntes en cascada)
    """
    service = CarpetaService(db)
    service.delete_carpeta(carpeta_id, current_user.id)
    return None
