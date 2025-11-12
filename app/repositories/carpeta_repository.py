from sqlalchemy.orm import Session
from app.db.models import Carpeta
from typing import List, Optional

class CarpetaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, carpeta_id: int) -> Optional[Carpeta]:
        return self.db.query(Carpeta).filter(Carpeta.id == carpeta_id).first()
    
    def get_all_by_usuario(self, usuario_id: int) -> List[Carpeta]:
        return self.db.query(Carpeta).filter(Carpeta.usuario_id == usuario_id).all()
    
    def get_root_carpetas(self, usuario_id: int) -> List[Carpeta]:
        """Obtener carpetas raíz (sin padre)"""
        return self.db.query(Carpeta).filter(
            Carpeta.usuario_id == usuario_id,
            Carpeta.carpeta_padre_id.is_(None)
        ).all()
    
    def get_subcarpetas(self, carpeta_padre_id: int) -> List[Carpeta]:
        """Obtener subcarpetas de una carpeta"""
        return self.db.query(Carpeta).filter(
            Carpeta.carpeta_padre_id == carpeta_padre_id
        ).all()
    
    def create(self, carpeta: Carpeta) -> Carpeta:
        self.db.add(carpeta)
        self.db.commit()
        self.db.refresh(carpeta)
        return carpeta
    
    def update(self, carpeta: Carpeta) -> Carpeta:
        self.db.commit()
        self.db.refresh(carpeta)
        return carpeta
    
    def delete(self, carpeta_id: int) -> bool:
        carpeta = self.get_by_id(carpeta_id)
        if carpeta:
            self.db.delete(carpeta)
            self.db.commit()
            return True
        return False
    
    def check_circular_reference(self, carpeta_id: int, new_parent_id: int) -> bool:
        """
        Verificar si mover una carpeta crearía una referencia circular
        Retorna True si hay referencia circular
        """
        if carpeta_id == new_parent_id:
            return True
        
        current_parent_id = new_parent_id
        visited = set()
        
        while current_parent_id is not None:
            if current_parent_id in visited or current_parent_id == carpeta_id:
                return True
            
            visited.add(current_parent_id)
            parent = self.get_by_id(current_parent_id)
            
            if parent is None:
                break
            
            current_parent_id = parent.carpeta_padre_id
        
        return False
