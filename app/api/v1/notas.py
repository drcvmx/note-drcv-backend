from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.nota import NotaCreate, NotaResponse, NotaUpdate
from app.services.nota_service import NotaService
from app.core.dependencies import get_current_user
from app.db.models import Usuario

router = APIRouter()

@router.post("/", response_model=NotaResponse, status_code=status.HTTP_201_CREATED)
def create_nota(
    nota_data: NotaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crear una nueva nota
    """
    service = NotaService(db)
    nota = service.create_nota(current_user.id, nota_data)
    return nota

@router.get("/", response_model=List[NotaResponse])
def get_notas(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las notas del usuario autenticado
    """
    service = NotaService(db)
    notas = service.get_notas_by_usuario(current_user.id, current_user.id)
    return notas

@router.get("/{nota_id}", response_model=NotaResponse)
def get_nota(
    nota_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener una nota específica
    """
    service = NotaService(db)
    nota = service.get_nota(nota_id, current_user.id)
    return nota

@router.put("/{nota_id}", response_model=NotaResponse)
def update_nota(
    nota_id: int,
    nota_data: NotaUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar una nota
    """
    service = NotaService(db)
    nota = service.update_nota(nota_id, nota_data, current_user.id)
    return nota

@router.delete("/{nota_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nota(
    nota_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar una nota
    """
    service = NotaService(db)
    service.delete_nota(nota_id, current_user.id)
    return None

