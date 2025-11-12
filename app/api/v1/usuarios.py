from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin, Token, UsuarioUpdate
from app.services.usuario_service import UsuarioService
from app.core.security import create_access_token
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.db.models import Usuario

router = APIRouter()

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario
    """
    service = UsuarioService(db)
    usuario = service.create_usuario(usuario_data)
    return usuario

@router.post("/login", response_model=Token)
def login(credentials: UsuarioLogin, db: Session = Depends(get_db)):
    """
    Iniciar sesión y obtener token JWT
    """
    service = UsuarioService(db)
    usuario = service.authenticate_usuario(credentials.username, credentials.password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UsuarioResponse)
def get_current_user_info(current_user: Usuario = Depends(get_current_user)):
    """
    Obtener información del usuario autenticado
    """
    return current_user

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar información del usuario
    """
    service = UsuarioService(db)
    usuario = service.update_usuario(usuario_id, usuario_data, current_user.id)
    return usuario

