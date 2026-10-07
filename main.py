import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
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

load_dotenv()
app = FastAPI(title='Sistema de GestiÃƒÆ’Ã‚Â³n de Sensores de pH', description='API para administrar roles, usuarios, sensores, lecturas y locaciones.', version='1.0.0')
origins = [origin.strip() for origin in os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',') if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
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

@app.get('/', tags=['Health'], summary='InformaciÃƒÆ’Ã‚Â³n de la API')
def inicio():
    return {'message': 'API del Sistema de GestiÃƒÆ’Ã‚Â³n de Sensores de pH', 'docs': '/docs'}

@app.get('/health', tags=['Health'], summary='Estado de la API', response_description='La API estÃƒÆ’Ã‚Â¡ activa')
def health():
    return {'status': 'ok'}
