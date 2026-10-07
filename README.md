# ElectroQuímica

Aplicación con frontend SvelteKit en `frontend/` y API FastAPI en la raíz del proyecto. FastAPI conecta con PostgreSQL/Neon usando `DATABASE_URL` del archivo `.env`.

## Backend

Desde la raíz del repositorio, instala y ejecuta:

```powershell
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Configura `DATABASE_URL` en `.env` (puedes partir de `.env.example`). Swagger está en `http://127.0.0.1:8000/docs` y el estado en `/health`. Define `CORS_ORIGINS` con el dominio de Netlify al desplegar en Render.

## Frontend

En otra terminal:

```powershell
Set-Location frontend
npm install
npm run dev
```

Configura `PUBLIC_API_BASE_URL` en `frontend/.env` para apuntar a `http://127.0.0.1:8000` en local o a la URL pública de Render en Netlify.

El backend ofrece CRUD independiente para roles, módulos, usuarios, permisos, tipos de sensor, sensores, departamentos, locaciones, lecturas y asignaciones. Las tablas deben existir previamente en PostgreSQL; la API no crea ni migra el esquema.
