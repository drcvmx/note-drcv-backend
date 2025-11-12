from sqlalchemy.orm import Session
from app.db.models import Apunte
from typing import List, Optional

class ApunteRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, apunte_id: int) -> Optional[Apunte]:
        return self.db.query(Apunte).filter(Apunte.id == apunte_id).first()
    
    def get_all_by_carpeta(self, carpeta_id: int) -> List[Apunte]:
        return self.db.query(Apunte).filter(
            Apunte.carpeta_id == carpeta_id
        ).order_by(Apunte.creado_en.desc()).all()
    
    def create(self, apunte: Apunte) -> Apunte:
        self.db.add(apunte)
        self.db.commit()
        self.db.refresh(apunte)
        return apunte
    
    def update(self, apunte: Apunte) -> Apunte:
        self.db.commit()
        self.db.refresh(apunte)
        return apunte
    
    def delete(self, apunte_id: int) -> bool:
        apunte = self.get_by_id(apunte_id)
        if apunte:
            self.db.delete(apunte)
            self.db.commit()
            return True
        return False
