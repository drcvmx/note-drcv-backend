from sqlalchemy.orm import Session, joinedload
from app.db.models import Lista, ItemLista
from typing import List as ListType, Optional

class ListaRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, lista_id: int) -> Optional[Lista]:
        return self.db.query(Lista).filter(Lista.id == lista_id).first()
    
    def get_all_by_usuario(self, usuario_id: int, include_items: bool = False) -> ListType[Lista]:
        query = self.db.query(Lista).filter(Lista.usuario_id == usuario_id)
        
        # Si include_items es True, cargar los items en la misma consulta (eager loading)
        if include_items:
            query = query.options(joinedload(Lista.items))
        
        return query.order_by(Lista.creado_en.desc()).all()
    
    def create(self, lista: Lista) -> Lista:
        self.db.add(lista)
        self.db.commit()
        self.db.refresh(lista)
        return lista
    
    def update(self, lista: Lista) -> Lista:
        self.db.commit()
        self.db.refresh(lista)
        return lista
    
    def delete(self, lista_id: int) -> bool:
        lista = self.get_by_id(lista_id)
        if lista:
            self.db.delete(lista)
            self.db.commit()
            return True
        return False
    
    # Métodos para items de lista
    def get_items_by_lista(self, lista_id: int) -> ListType[ItemLista]:
        return self.db.query(ItemLista).filter(ItemLista.lista_id == lista_id).order_by(ItemLista.id.asc()).all()
    
    def get_item_by_id(self, item_id: int) -> Optional[ItemLista]:
        return self.db.query(ItemLista).filter(ItemLista.id == item_id).first()
    
    def create_item(self, item: ItemLista) -> ItemLista:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def update_item(self, item: ItemLista) -> ItemLista:
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete_item(self, item_id: int) -> bool:
        item = self.get_item_by_id(item_id)
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False

