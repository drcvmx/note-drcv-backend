-- ======================================================================
-- ESQUEMA DE BASE DE DATOS PARA APLICACIÓN DE NOTAS (PostgreSQL)
-- ======================================================================

-- ----------------------------------------------------------------------
-- Eliminación de tablas existentes (Usar solo en entornos de desarrollo/test)
-- La clausura CASCADE asegura que si borras una tabla principal, se borran sus dependencias (llaves foráneas).
-- ----------------------------------------------------------------------
DROP TABLE IF EXISTS items_lista CASCADE;
DROP TABLE IF EXISTS listas CASCADE;
DROP TABLE IF EXISTS apuntes CASCADE;
DROP TABLE IF EXISTS carpetas CASCADE;
DROP TABLE IF EXISTS notas CASCADE;
DROP TABLE IF EXISTS password_reset_tokens CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;


-- ----------------------------------------------------------------------
-- 1. Tabla de Usuarios
-- Almacena la información de autenticación segura y configuración de la aplicación.
-- ----------------------------------------------------------------------
CREATE TABLE usuarios (
    id              SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    
    -- Campos de Login:
    username        VARCHAR(50) NOT NULL UNIQUE, 
    password_hash   TEXT NOT NULL, -- Almacena la contraseña cifrada (hash)
    
    -- Configuración de la App:
    fondo_url       VARCHAR(512), -- URL de la imagen de fondo subida
    creado_en       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
---


-- ----------------------------------------------------------------------
-- 2. Tabla de Tokens de Reseteo de Contraseña
-- Almacena tokens temporales para recuperación de contraseña por email.
-- ----------------------------------------------------------------------
CREATE TABLE password_reset_tokens (
    id              SERIAL PRIMARY KEY,
    usuario_id      INTEGER NOT NULL,
    token           VARCHAR(255) NOT NULL UNIQUE,
    expira_en       TIMESTAMP WITH TIME ZONE NOT NULL,
    usado           BOOLEAN DEFAULT FALSE,
    creado_en       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Llave foránea
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
---


-- ----------------------------------------------------------------------
-- 3. Tabla de Notas Simples (Tipo 1: Notas de tamaño mediano a grande)
-- ----------------------------------------------------------------------
CREATE TABLE notas (
    id              SERIAL PRIMARY KEY,
    usuario_id      INTEGER NOT NULL,
    titulo          VARCHAR(255) NOT NULL,
    contenido       TEXT NOT NULL,
    creado_en       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actualizado_en  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Restricción de llave foránea
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
---


-- ----------------------------------------------------------------------
-- 4. Tabla de Carpetas (Tipo 2: Jerarquía para apuntes)
-- Utiliza una llave foránea recursiva (carpeta_padre_id) para anidación.
-- ----------------------------------------------------------------------
CREATE TABLE carpetas (
    id                  SERIAL PRIMARY KEY,
    usuario_id          INTEGER NOT NULL,
    nombre              VARCHAR(100) NOT NULL,
    
    -- Permite anidación (NULL si es carpeta raíz)
    carpeta_padre_id    INTEGER, 
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    -- Enlaza a sí misma, crucial para la jerarquía de materias/submaterias.
    FOREIGN KEY (carpeta_padre_id) REFERENCES carpetas(id) ON DELETE CASCADE
);
---


-- ----------------------------------------------------------------------
-- 5. Tabla de Apuntes (Tipo 2: Contenido de texto dentro de las carpetas)
-- ----------------------------------------------------------------------
CREATE TABLE apuntes (
    id              SERIAL PRIMARY KEY,
    carpeta_id      INTEGER NOT NULL,
    titulo          VARCHAR(255) NOT NULL,
    contenido       TEXT NOT NULL,
    creado_en       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (carpeta_id) REFERENCES carpetas(id) ON DELETE CASCADE
);
---


-- ----------------------------------------------------------------------
-- 6. Tabla de Listas (Tipo 3: Encabezado de la lista To-Do/Compras)
-- ----------------------------------------------------------------------
CREATE TABLE listas (
    id              SERIAL PRIMARY KEY,
    usuario_id      INTEGER NOT NULL,
    titulo          VARCHAR(100) NOT NULL,
    creado_en       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
---


-- ----------------------------------------------------------------------
-- 7. Tabla de Items de Lista (Tipo 3: Elementos individuales)
-- Incluye 'descripcion' para detalles de la tarea.
-- ----------------------------------------------------------------------
CREATE TABLE items_lista (
    id              SERIAL PRIMARY KEY,
    lista_id        INTEGER NOT NULL,
    
    titulo          VARCHAR(100) NOT NULL,
    descripcion     VARCHAR(50), -- Texto secundario opcional (ej: "Ir al restaurante de la avenida")
    completado      BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (lista_id) REFERENCES listas(id) ON DELETE CASCADE
);
---


-- ----------------------------------------------------------------------
-- Creación de Índices para optimizar la velocidad de búsqueda y consultas frecuentes
-- ----------------------------------------------------------------------
CREATE INDEX idx_notas_usuario ON notas (usuario_id);
CREATE INDEX idx_carpetas_usuario ON carpetas (usuario_id);
CREATE INDEX idx_carpetas_padre ON carpetas (carpeta_padre_id);
CREATE INDEX idx_apuntes_carpeta ON apuntes (carpeta_id);
CREATE INDEX idx_listas_usuario ON listas (usuario_id);
CREATE INDEX idx_items_lista ON items_lista (lista_id);
CREATE INDEX idx_password_reset_token ON password_reset_tokens (token);
CREATE INDEX idx_password_reset_usuario ON password_reset_tokens (usuario_id);
CREATE INDEX idx_password_reset_expira ON password_reset_tokens (expira_en);