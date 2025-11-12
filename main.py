from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import usuarios, notas, listas, carpetas, apuntes, password_reset

app = FastAPI(
    title="Notes API",
    description="API para aplicación de notas con FastAPI",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(usuarios.router, prefix="/api/v1/usuarios", tags=["usuarios"])
app.include_router(notas.router, prefix="/api/v1/notas", tags=["notas"])
app.include_router(carpetas.router, prefix="/api/v1/carpetas", tags=["carpetas"])
app.include_router(apuntes.router, prefix="/api/v1/apuntes", tags=["apuntes"])
app.include_router(listas.router, prefix="/api/v1/listas", tags=["listas"])
app.include_router(password_reset.router, prefix="/api/v1/auth", tags=["autenticación"])

@app.get("/")
def read_root():
    return {"message": "Notes API - FastAPI Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

