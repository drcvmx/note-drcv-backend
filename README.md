# DRCV Note Backend

![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-compatible-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-supported-4169E1?logo=postgresql&logoColor=white)
![Estado](https://img.shields.io/badge/estado-prototipo%20funcional-orange)

Backend monolítico en Python, organizado por capas, para una aplicación de notas y productividad. Expone una API REST con FastAPI, persiste la información en PostgreSQL y separa autenticación, lógica de negocio, acceso a datos y modelos dentro de una única aplicación desplegable. El repositorio es una base funcional para el portafolio; no incluye todavía automatización de despliegue, migraciones ni una configuración completa de producción.

## Problema que resuelve

Centraliza en una API los distintos tipos de información personal de una aplicación de productividad, manteniendo cada recurso asociado a un usuario autenticado. Esto permite gestionar notas, apuntes organizados en carpetas y listas con sus elementos desde un mismo backend, además de ofrecer registro, inicio de sesión y recuperación de contraseña.

## Funcionalidades principales

- Registro, inicio de sesión y consulta del usuario autenticado.
- Autenticación mediante tokens JWT y protección de endpoints con Bearer tokens.
- Hash de contraseñas con `passlib` y `bcrypt`.
- CRUD de notas simples.
- CRUD de carpetas con jerarquía de subcarpetas y apuntes asociados.
- CRUD de listas y de sus elementos, incluido el estado `completado`.
- Recuperación de contraseña por email: solicitud, validación de token y cambio de contraseña.
- Expiración de tokens de recuperación en una hora y uso único.
- Validación de entrada y respuestas con esquemas Pydantic.
- Endpoints básicos `/` y `/health`.

## Arquitectura utilizada

Es un monolito en Python con separación interna por responsabilidades, no una arquitectura de microservicios:

1. `api/v1`: recibe las peticiones HTTP y declara las rutas.
2. `services`: concentra los casos de uso y reglas de negocio.
3. `repositories`: encapsula las consultas y operaciones de persistencia.
4. `schemas`: valida entradas y serializa respuestas con Pydantic.
5. `db`: define modelos SQLAlchemy y sesiones de base de datos.
6. `core`: configura la aplicación, la seguridad y las dependencias.

El aislamiento de los datos se implementa a nivel de aplicación: los servicios reciben el usuario autenticado y consultan los recursos por su `usuario_id` (o por la carpeta/lista perteneciente a ese usuario). La base de datos refuerza la integridad mediante claves foráneas y borrado en cascada.

### Estructura de carpetas y responsabilidades por capa

La aplicación está organizada como un monolito modular, donde cada carpeta tiene una responsabilidad clara y el flujo típico de una petición es:

`API -> Service -> Repository -> SQLAlchemy -> PostgreSQL`

```text
.
├── main.py                              # Arranque de FastAPI y registro de routers
├── requirements.txt                     # Dependencias del proyecto
├── create_tables.py                     # Script de creación de tablas (desarrollo)
├── estructure.sql                      # Esquema SQL de PostgreSQL y relaciones
├── test_password_reset.py               # Script manual para probar recuperación de contraseña
└── app/
    ├── api/
    │   └── v1/                          # Capa HTTP: endpoints y rutas REST
    │       ├── usuarios.py              # Registro, login, perfil y autenticación
    │       ├── notas.py                 # CRUD de notas del usuario
    │       ├── carpetas.py              # CRUD de carpetas y subcarpetas
    │       ├── apuntes.py               # CRUD de apuntes dentro de carpetas
    │       ├── listas.py                # CRUD de listas y su contenido
    │       └── password_reset.py         # Solicitud, validación y cambio de contraseña
    │
    ├── core/
    │   ├── config.py                     # Variables de entorno y configuración global
    │   ├── dependencies.py               # Dependencias FastAPI: JWT, usuario autenticado
    │   └── security.py                   # Generación/validación de JWT, hashing de contraseñas
    │
    ├── db/
    │   ├── models.py                     # Modelos SQLAlchemy: Usuario, Nota, Carpeta, Apunte, Lista
    │   └── session.py                    # Engine, sessionmaker y Base declarativa
    │
    ├── repositories/
    │   ├── usuario_repository.py         # Consultas de usuarios (find, create, update, delete)
    │   ├── nota_repository.py            # Acceso a notas
    │   ├── carpeta_repository.py         # Acceso a carpetas
    │   ├── apunte_repository.py          # Acceso a apuntes
    │   ├── lista_repository.py           # Acceso a listas e items
    │   └── password_reset_repository.py  # Gestión de tokens de recuperación
    │
    ├── schemas/
    │   ├── usuario.py                    # Validación de usuarios y autenticación
    │   ├── nota.py                       # Validación de notas
    │   ├── carpeta.py                   # Validación de carpetas
    │   ├── apunte.py                    # Validación de apuntes
    │   ├── lista.py                     # Validación de listas
    │   └── password_reset.py            # Validación del flujo de reset
    │
    ├── services/
    │   ├── usuario_service.py            # Reglas de negocio de usuarios
    │   ├── nota_service.py               # Lógica de notas y permisos
    │   ├── carpeta_service.py            # Lógica de carpetas y jerarquías
    │   ├── apunte_service.py             # Lógica de apuntes
    │   ├── lista_service.py              # Lógica de listas e items
    │   ├── password_reset_service.py     # Validación y generación de tokens
    │   └── email_service.py              # Envío de emails SMTP para recuperación
    │
    └── __init__.py
```

#### Qué hace cada capa

- Capa de entrada (`app/api/v1`):
  - Recibe las peticiones HTTP.
  - Valida el payload con Pydantic al entrar a la ruta.
  - Inyecta dependencias como la sesión de base de datos y el usuario autenticado.
  - Llama al servicio correspondiente y devuelve la respuesta JSON.

- Capa de negocio (`app/services`):
  - Contiene la lógica de negocio.
  - Verifica permisos, validaciones específicas y reglas de dominio.
  - Coordina las operaciones con el repositorio y encapsula la lógica que no debe vivir en la API.

- Capa de acceso a datos (`app/repositories`):
  - Es la puerta de acceso a PostgreSQL/SQLAlchemy.
  - Ejecuta consultas de lectura y escritura.
  - Encapsula CRUD y búsquedas por usuario, email, token o recurso.

- Modelado y persistencia (`app/db`):
  - Define los modelos SQLAlchemy con sus relaciones.
  - Guarda el esquema de entidades como `Usuario`, `Nota`, `Carpeta`, `Apunte`, `Lista` y `PasswordResetToken`.
  - Administra la conexión y las sesiones.

- Validación y contratos (`app/schemas`):
  - Define los requests y responses con Pydantic.
  - Garantiza que los datos entrantes cumplen estructura y tipos antes de llegar a la lógica de negocio.

- Configuración y seguridad (`app/core`):
  - Carga las variables de entorno.
  - Implementa JWT, hashing de contraseñas y dependencias de autenticación.
  - Centraliza la configuración del proyecto.

- Punto de arranque (`main.py`):
  - Crea la aplicación FastAPI.
  - Configura CORS.
  - Registra los routers de cada recurso.
  - Expone endpoints como `/`, `/health` y el prefijo `/api/v1`.

Esta organización facilita mantener el proyecto escalable sin mezclar HTTP, reglas de negocio y acceso a datos en el mismo archivo. Cada capa tiene una misión distinta y el backend se vuelve más fácil de mantener, probar y extender.

### Diagrama ASCII

```text
[Cliente web o móvil]
          |
          v
 [FastAPI / API v1]
          |
   +------+------+
   |             |
   v             v
[Dependencias] [Schemas]
   |             |
   +------v------+
          |
     [Services]
          |
     [Repositories]
          |
          v
 [SQLAlchemy / Session]
          |
          v
     [PostgreSQL]

 [EmailService] ---> [SMTP Gmail]
```

## Stack tecnológico real

| Área | Tecnología | Uso en el repositorio |
| --- | --- | --- |
| Runtime | Python | Ejecución de la API y scripts |
| API | FastAPI `0.109.0` | Rutas REST, dependencias y documentación OpenAPI |
| Servidor | Uvicorn `0.27.0` | Ejecución ASGI |
| Persistencia | PostgreSQL + `psycopg2-binary` | Base de datos relacional |
| ORM | SQLAlchemy `2.0.25` | Modelos, relaciones y sesiones |
| Validación | Pydantic `2.5.3` + `pydantic-settings` | Esquemas y configuración |
| Autenticación | `python-jose` | Firma y validación de JWT |
| Contraseñas | `passlib` + `bcrypt==4.0.1` | Hash y verificación |
| Email | SMTP mediante biblioteca estándar | Recuperación de contraseña |
| Configuración | `python-dotenv` | Lectura de `.env` |

Las versiones declaradas están en [requirements.txt](requirements.txt). El repositorio no contiene código de migraciones, `Dockerfile`, `docker-compose.yml`, configuración de PM2 ni configuración de Cloudflare.

## Diagramas

### Arquitectura general

```mermaid
flowchart LR
    Client[Cliente] --> API[FastAPI API v1]
    API --> Security[Core: JWT y dependencias]
    API --> Schemas[Pydantic schemas]
    API --> Services[Services]
    Services --> Repositories[Repositories]
    Repositories --> ORM[SQLAlchemy]
    ORM --> DB[(PostgreSQL)]
    Services --> Mail[EmailService]
    Mail --> SMTP[Servidor SMTP]
```

### Flujo principal de una petición protegida

```mermaid
sequenceDiagram
    participant C as Cliente
    participant A as FastAPI
    participant D as Dependencia JWT
    participant S as Service
    participant R as Repository
    participant DB as PostgreSQL

    C->>A: Petición con Bearer token
    A->>D: Validar y resolver usuario
    D->>DB: Buscar usuario por username
    DB-->>D: Usuario autenticado
    D-->>A: current_user
    A->>S: Ejecutar caso de uso
    S->>R: Consultar o modificar recurso del usuario
    R->>DB: SQLAlchemy
    DB-->>R: Resultado
    R-->>S: Entidad
    S-->>A: Resultado validado
    A-->>C: Respuesta JSON
```

### Autenticación y datos

```mermaid
flowchart TD
    Register[POST /usuarios/register] --> Hash[Hash bcrypt]
    Hash --> Users[(usuarios)]
    Login[POST /usuarios/login] --> Verify[Verificar credenciales]
    Verify --> JWT[Emitir JWT con exp]
    JWT --> Protected[Endpoints protegidos]
    Protected --> User[Resolver current_user]
    User --> Scope[Filtrar por usuario_id]
    Scope --> Notes[(notas)]
    Scope --> Folders[(carpetas)]
    Folders --> Apuntes[(apuntes)]
    Scope --> Lists[(listas)]
    Lists --> Items[(items_lista)]
    Forgot[POST /auth/forgot-password] --> Reset[(password_reset_tokens)]
    Reset --> Email[Email con token de una hora]
```

### Despliegue

```mermaid
flowchart LR
    Client[Cliente] --> Edge[Cloudflare Tunnel opcional]
    Edge --> Process[Uvicorn / proceso local]
    Process --> App[main:app]
    App --> DB[(PostgreSQL)]
    App --> SMTP[SMTP Gmail]
    PM2[PM2 opcional] -. supervisa .-> Process
```

El último diagrama representa el entorno operativo descrito en el README anterior. PM2, Cloudflare Tunnel y Docker/Supabase no están configurados ni incluidos en este repositorio, por lo que no forman parte de una instalación local reproducible.

## Estructura del proyecto

```text
.
├── main.py                    # Aplicación FastAPI y registro de routers
├── requirements.txt           # Dependencias fijadas
├── create_tables.py           # Creación de tablas mediante SQLAlchemy
├── estructure.sql             # Esquema SQL de PostgreSQL e índices
├── test_password_reset.py     # Script manual del flujo de recuperación
└── app/
    ├── api/v1/                # Endpoints REST
    ├── core/                  # Configuración, seguridad y dependencias
    ├── db/                    # Sesión y modelos SQLAlchemy
    ├── repositories/          # Acceso a datos
    ├── schemas/               # Contratos Pydantic
    └── services/              # Lógica de negocio
```

## Instalación local

Requisitos: Python compatible con las versiones de `requirements.txt` y una instancia accesible de PostgreSQL.

```bash
git clone <url-del-repositorio>
cd note-drcv-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Configura las variables de entorno, crea la base de datos y aplica el esquema:

```bash
psql "$DATABASE_URL" -f estructure.sql
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

También puedes ejecutar `python create_tables.py` para crear las tablas definidas por los modelos. El script SQL es preferible cuando se necesitan además los índices declarados en `estructure.sql`.

La API queda disponible en `http://127.0.0.1:8000`; la documentación interactiva de FastAPI está en `/docs` y `/redoc`.

## Variables de entorno

`app/core/config.py` define estos valores y permite sobreescribirlos desde `.env`:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/notes_db
SECRET_KEY=cambia-esta-clave
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-cuenta@gmail.com
SMTP_PASSWORD=tu-credencial-smtp
FROM_EMAIL=noreply@tudominio.com
FRONTEND_URL=http://localhost:3000
```

No incluyas `.env` ni credenciales en el control de versiones. `SECRET_KEY` y `SMTP_PASSWORD` son ejemplos: deben reemplazarse antes de usar el servicio fuera de un entorno local.

## Despliegue

El repositorio no proporciona un pipeline ni archivos de infraestructura. Una ejecución manual basada en el entorno descrito previamente puede usar Uvicorn detrás de un gestor de procesos:

```bash
pm2 start venv/bin/uvicorn --name note-backend -- main:app --host 0.0.0.0 --port 8000
pm2 save
```

Para publicar la API mediante Cloudflare Tunnel, configura `cloudflared` para reenviar hacia `http://127.0.0.1:8000`. Esa configuración, el servidor PostgreSQL, TLS, firewall, copias de seguridad y observabilidad quedan fuera de este repositorio y deben revisarse por separado.

## Aprendizajes técnicos

- Organización de un monolito por capas sin mezclar HTTP, reglas de negocio y persistencia.
- Uso de dependencias de FastAPI para obtener sesiones y usuarios autenticados.
- Modelado de relaciones, jerarquías recursivas y borrado en cascada con SQLAlchemy/PostgreSQL.
- Emisión de JWT con expiración y hash de contraseñas con bcrypt.
- Diseño de un flujo de recuperación que no revela si un email existe.
- Configuración de CORS, SMTP y conexión a base de datos mediante variables de entorno.

## Mejoras pendientes antes de producción

- Añadir migraciones versionadas, por ejemplo con Alembic, y separar mejor los scripts destructivos de desarrollo.
- Incorporar pruebas automatizadas unitarias y de integración para autenticación, autorización y todos los recursos.
- Revisar límites de tasa, bloqueo ante intentos repetidos, rotación de claves JWT y gestión de secretos.
- Añadir validación y normalización de configuración al arrancar, además de logging estructurado y métricas.
- Configurar un proveedor SMTP de producción con manejo de errores y reintentos controlados.
- Definir despliegue reproducible, health checks de dependencias, backups, restauración y observabilidad.
- Auditar de forma específica el aislamiento por usuario, CORS y las políticas de borrado en cascada.
- Fijar una versión de Python soportada y documentar una matriz de compatibilidad.

## Estado actual

**Prototipo funcional en desarrollo.** El código contiene los flujos principales de usuarios, notas, carpetas, apuntes, listas y recuperación de contraseña. Hay un script manual para probar el reseteo de contraseña, pero no existe una suite automatizada completa ni evidencia en el repositorio de un despliegue reproducible. No debe considerarse listo para producción sin completar las mejoras anteriores.
