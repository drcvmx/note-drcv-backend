from sqlalchemy.orm import Session
from app.db.models import Nota
from typing import List, Optional

class NotaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, nota_id: int) -> Optional[Nota]:
        return self.db.query(Nota).filter(Nota.id == nota_id).first()
    
    def get_all_by_usuario(self, usuario_id: int) -> List[Nota]:
        return self.db.query(Nota).filter(Nota.usuario_id == usuario_id).order_by(Nota.actualizado_en.desc()).all()
    
    def create(self, nota: Nota) -> Nota:
        self.db.add(nota)
        self.db.commit()
        self.db.refresh(nota)
        return nota
    
    def update(self, nota: Nota) -> Nota:
        self.db.commit()
        self.db.refresh(nota)
        return nota
    
    def delete(self, nota_id: int) -> bool:
        nota = self.get_by_id(nota_id)
        if nota:
            self.db.delete(nota)
            self.db.commit()
            return True
        return False

