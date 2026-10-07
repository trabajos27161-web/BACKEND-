import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.rol import router as rol_router
from routers.modulo import router as modulo_router
from routers.usuarios import router as usuarios_router
from routers.modulo_x_rol import router as modulo_x_rol_router
from routers.tipo_sensor import router as tipo_sensor_router
from routers.sensor import router as sensor_router
from routers.dpto import router as dpto_router
from routers.locacion import router as locacion_router
from routers.lectura import router as lectura_router
from routers.asignacion_sensor import router as asignacion_sensor_router


# ============================================================
# VARIABLES DE ENTORNO
# ============================================================

load_dotenv()


# ============================================================
# CREACIÓN DE LA APLICACIÓN
# ============================================================

app = FastAPI(
    title="Sistema de Gestión de Sensores de pH",
    description=(
        "API para administrar roles, usuarios, sensores, "
        "lecturas y locaciones."
    ),
    version="1.0.0",
)


# ============================================================
# CONFIGURACIÓN CORS
# ============================================================

# Puedes configurar CORS_ORIGINS en Render como:
#
# https://verdant-basbousa-cfd10c.netlify.app,http://localhost:5173,http://localhost:3000
#
# Si la variable no existe, se utilizan estos valores por defecto.

default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://verdant-basbousa-cfd10c.netlify.app",
]

cors_origins_env = os.getenv("CORS_ORIGINS", "")

if cors_origins_env.strip():
    origins = [
        origin.strip()
        for origin in cors_origins_env.split(",")
        if origin.strip()
    ]
else:
    origins = default_origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(rol_router)
app.include_router(modulo_router)
app.include_router(usuarios_router)
app.include_router(modulo_x_rol_router)
app.include_router(tipo_sensor_router)
app.include_router(sensor_router)
app.include_router(dpto_router)
app.include_router(locacion_router)
app.include_router(lectura_router)
app.include_router(asignacion_sensor_router)


# ============================================================
# RUTA PRINCIPAL
# ============================================================

@app.get(
    "/",
    tags=["Health"],
    summary="Información de la API",
)
def inicio():
    return {
        "message": "API del Sistema de Gestión de Sensores de pH",
        "docs": "/docs",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get(
    "/health",
    tags=["Health"],
    summary="Estado de la API",
    response_description="La API está activa",
)
def health():
    return {
        "status": "ok"
    }
