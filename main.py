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
#
# Frontend actual en Netlify:
# https://gilded-entremet-c6b323.netlify.app
#
# Se mantiene también el dominio anterior por compatibilidad.
# Los localhost permiten trabajar durante desarrollo local.
#

origins = [
    # NUEVO FRONTEND NETLIFY
    "https://gilded-entremet-c6b323.netlify.app",

    # FRONTEND NETLIFY ANTERIOR
    "https://verdant-basbousa-cfd10c.netlify.app",

    # DESARROLLO LOCAL
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


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
