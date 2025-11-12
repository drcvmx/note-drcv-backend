from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.apunte import ApunteCreate, ApunteResponse, ApunteUpdate
from app.services.apunte_service import ApunteService
from app.core.dependencies import get_current_user
from app.db.models import Usuario

router = APIRouter()

@router.post("/", response_model=ApunteResponse, status_code=status.HTTP_201_CREATED)
def create_apunte(
    apunte_data: ApunteCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo apunte en una carpeta
    """
    service = ApunteService(db)
    apunte = service.create_apunte(apunte_data, current_user.id)
    return apunte

@router.get("/carpeta/{carpeta_id}", response_model=List[ApunteResponse])
def get_apuntes_by_carpeta(
    carpeta_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los apuntes de una carpeta específica
    """
    service = ApunteService(db)
    apuntes = service.get_apuntes_by_carpeta(carpeta_id, current_user.id)
    return apuntes

@router.get("/{apunte_id}", response_model=ApunteResponse)
def get_apunte(
    apunte_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener un apunte específico
    """
    service = ApunteService(db)
    apunte = service.get_apunte(apunte_id, current_user.id)
    return apunte

@router.put("/{apunte_id}", response_model=ApunteResponse)
def update_apunte(
    apunte_id: int,
    apunte_data: ApunteUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar un apunte
    """
    service = ApunteService(db)
    apunte = service.update_apunte(apunte_id, apunte_data, current_user.id)
    return apunte

@router.delete("/{apunte_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_apunte(
    apunte_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar un apunte
    """
    service = ApunteService(db)
    service.delete_apunte(apunte_id, current_user.id)
    return None
