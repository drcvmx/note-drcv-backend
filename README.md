# 🚀 DRCV Note - Core Backend 

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python 3.14](https://img.shields.io/badge/Python_3.14-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![PM2](https://img.shields.io/badge/PM2-2B037A?style=for-the-badge&logo=pm2&logoColor=white)
![Cloudflare Tunnels](https://img.shields.io/badge/Cloudflare_Zero_Trust-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)

Backend monolítico de alto rendimiento construido para soportar e impulsar todo el ecosistema de productividad "DRCV Note". Diseñado con una arquitectura On-Premise escalable, prescinde de *Backend-as-a-Service* limitantes para la autenticación, gestionando su propia lógica de seguridad, inyección de dependencias y exposición pública.

## 🏗️ Arquitectura del Sistema

### Patrón Monolítico Moderno
El servicio está estructurado como un monolito bien particionado sobre la base de **FastAPI**. A diferencia de aplicaciones acopladas a la autenticación nativa de SaaS (como el Auth nativo de Supabase), esta API asume el control total de su seguridad y flujos.

- **Autenticación Nativa Customizada**: Emisión y validación de `JWT` tokens mediante `python-jose`, aislando la lógica de negocio del proveedor de base de datos.
- **Encriptación Segura**: Manejo estricto de contraseñas usando `bcrypt` acoplado al backend.
- **ORM Predictivo**: `SQLAlchemy 2.0` con modelos reflectivos manejando las relaciones relacionales de Usuarios, Notas, Listas y Carpetas mediante jerarquías lógicas.
- **Validación de Datos**: Tipado estricto bidireccional manejado nativamente por `Pydantic v2`.

---

## 🌩️ Arquitectura de Despliegue (On-Premise)

El sistema completo fue diseñado, aprovisionado y desplegado en un servidor físico de alto rendimiento (Sistema Operativo `CachyOS`), logrando una exposición global con latencia optimizada aplicando prácticas *Zero-Trust*.

### Diagrama de Flujo de Red y Ejecución

```text
[ Cliente Web / Móvil ] 
       │
       ▼ (Tráfico encriptado globalmente vía HTTPS)
[ Cloudflare Zero Trust Edge ]
       │
       ▼ (Túnel Inverso - No hay puertos abiertos en el router local)
[ cloudflared daemon locally ]
       │
       ▼ (Reverse Proxy re-direccionado a localhost:8000)
[ PM2 (Gestor de Procesos en Background) ]
       │
       ▼
[ FastAPI + Uvicorn (Ejecución bajo Python 3.14) ]
       │
       ▼ (Conexión TCP directa por puerto local 54332)
[ Contenedor Docker: Supabase PostgreSQL Local ]
```

### Decisiones Clave de Ingeniería y DevOps

1. **Motor de Vida Súper Ligero (PM2):** Aunque el backend es de Python nativo, utilizamos `PM2` para la daemonización directa del ejecutable `uvicorn` (en lugar de Systemd base). Esto otorga monitoreo en caliente (`pm2 logs`), reinicio automático ante caídas críticas por picos de memoria, e inyección dinámica de logs sin apilamiento severo.
2. **Defensa Zero-Trust Global:** Se eliminó la exposición tradicional atacable (no hay *"Port-Forwarding"*, no hay VPN requerida para el usuario final). El servidor On-Premise llama *hacia afuera* a la red Edge de Cloudflare, la cual actúa de *Proxy* mundial bloqueando ataques DDoS.
3. **Gestión de DB Contenedorizada Local:** La base de datos subyacente es un ecosistema local de Supabase confinado en contenedores Docker mapeados hacia la serie de puertos `5433x` para mitigar colisiones con los propios servicios pre-existentes del propio servidor CachyOS.
4. **Política CORS Estricta por Túnel:** El framework gestiona dominios permitidos (Localhost y el Wildcard Tunnelling), bloqueando ataques directos desde origenes web que intenten enlazarse sin autorización.

---

## 🛠️ Guía Rápida de Instalación y Resiliencia

El entorno corre sobre las ramificaciones más modernas del ecosistema, por lo que requiere exactitud en la recreación.

### 1. Entorno de Virtualización
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> **⚠️ Ingeniería de Resolución de Dependencias (Python 3.14 Bleeding Edge):**
> Dado que la máquina utiliza el intérprete moderno experimental `Python 3.14`, resolvimos mitigaciones del ciclo de vida de los paquetes pre-compilados:
> - **Inyeción de Email:** Actualización de Pydantic desvinculó su validador. Se auto-inyecta compilando aisladamente `pip install email-validator`.
> - **Bypass de Auto-test Bcrypt:** Las versiones de `passlib` modernas enfrentaron el drop del formato Legacy en el check de Passlib. Re-estructuramos el árbol de dependencias con `pip install "bcrypt<4.0.0"` para habilitar *hashings stables* sin sobrecargar re-escrituras de la librería.

### 2. Variables de Entorno y Capa Lógica (`.env`)
Se debe inyectar la matriz de configuración en `.env` (excluida del control de versiones por seguridad):
```env
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:54332/postgres
SECRET_KEY=TU_LLAVE_CRIPTOGRAFICA_SECRETA_AQUI
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:3003", "https://api-note.tudominio.online"]
```

### 3. Exposición en Producción (PM2)
Activación de la orquestación:
```bash
# Apuntando al binario absoluto del VENV para garantizar asincronía correcta
pm2 start venv/bin/uvicorn --name note-backend -- main:app --host 0.0.0.0 --port 8000
pm2 save
```

### 4. Networking y Enlace Edge
Por último, el daemon de Cloudflare enlaza `localhost:8000` pasándolo hacia la sub-red protegida de la web, validando al instante la entrada pública hacia la API por puertos 80/443 de salida directa de Cloudflare.
