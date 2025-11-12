from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    fondo_url = Column(String(512), nullable=True)
    creado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relaciones
    notas = relationship("Nota", back_populates="usuario", cascade="all, delete-orphan")
    carpetas = relationship("Carpeta", back_populates="usuario", cascade="all, delete-orphan")
    listas = relationship("Lista", back_populates="usuario", cascade="all, delete-orphan")


class Nota(Base):
    __tablename__ = "notas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    creado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())
    actualizado_en = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="notas")


class Carpeta(Base):
    __tablename__ = "carpetas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(100), nullable=False)
    carpeta_padre_id = Column(Integer, ForeignKey("carpetas.id", ondelete="CASCADE"), nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="carpetas")
    carpeta_padre = relationship("Carpeta", remote_side=[id], backref="subcarpetas")
    apuntes = relationship("Apunte", back_populates="carpeta", cascade="all, delete-orphan")


class Apunte(Base):
    __tablename__ = "apuntes"
    
    id = Column(Integer, primary_key=True, index=True)
    carpeta_id = Column(Integer, ForeignKey("carpetas.id", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    creado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relaciones
    carpeta = relationship("Carpeta", back_populates="apuntes")


class Lista(Base):
    __tablename__ = "listas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(100), nullable=False)
    creado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="listas")
    items = relationship("ItemLista", back_populates="lista", cascade="all, delete-orphan")


class ItemLista(Base):
    __tablename__ = "items_lista"
    
    id = Column(Integer, primary_key=True, index=True)
    lista_id = Column(Integer, ForeignKey("listas.id", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(50), nullable=True)  # Según tu SQL es VARCHAR(50)
    completado = Column(Boolean, default=False)
    
    # Relaciones
    lista = relationship("Lista", back_populates="items")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expira_en = Column(TIMESTAMP(timezone=True), nullable=False)
    usado = Column(Boolean, default=False)
    creado_en = Column(TIMESTAMP(timezone=True), server_default=func.now())
    
    # Relaciones
    usuario = relationship("Usuario")

