"""
Script para crear las tablas en la base de datos
Ejecutar: python create_tables.py
"""
from app.db.session import engine, Base
from app.db.models import Usuario, Nota, Carpeta, Apunte, Lista, ItemLista, PasswordResetToken

def create_tables():
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas exitosamente!")

if __name__ == "__main__":
    create_tables()
