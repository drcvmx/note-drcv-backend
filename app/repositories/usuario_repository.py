from sqlalchemy.orm import Session
from app.db.models import Usuario
from typing import Optional

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    def get_by_username(self, username: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def create(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
    
    def update(self, usuario: Usuario) -> Usuario:
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
    
    def delete(self, usuario_id: int) -> bool:
        usuario = self.get_by_id(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

