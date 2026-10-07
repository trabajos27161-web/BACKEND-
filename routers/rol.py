from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import Rol
from schemas import RolCreate, RolUpdate, RolResponse
from routers.common import commit_or_conflict, get_or_404
router = APIRouter(prefix='/roles', tags=['Roles'])

@router.get('/', response_model=list[RolResponse], summary='Listar roles', responses={422: {'description':'ParÃƒÆ’Ã‚Â¡metros invÃƒÆ’Ã‚Â¡lidos'}})
def listar_roles(q: str | None = Query(None), page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    stmt = select(Rol).order_by(Rol.id)
    if q: stmt = stmt.where(Rol.nombre.ilike(f'%{q}%'))
    return db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all()

@router.get('/{id}', response_model=RolResponse, summary='Obtener rol', responses={404: {'description':'Rol no encontrado'}})
def obtener_rol(id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Rol, id, 'Rol')

@router.post('/', response_model=RolResponse, status_code=status.HTTP_201_CREATED, summary='Crear rol', responses={409: {'description':'Nombre duplicado'}})
def crear_rol(payload: RolCreate, db: Session = Depends(get_db)):
    if db.scalar(select(Rol.id).where(Rol.nombre == payload.nombre)) is not None: raise HTTPException(409, 'Ya existe un rol con ese nombre')
    item = Rol(**payload.model_dump()); db.add(item); commit_or_conflict(db); db.refresh(item); return item

@router.put('/{id}', response_model=RolResponse, summary='Actualizar rol', responses={404: {'description':'Rol no encontrado'},409:{'description':'Nombre duplicado'}})
def actualizar_rol(id: int, payload: RolUpdate, db: Session = Depends(get_db)):
    item = get_or_404(db, Rol, id, 'Rol')
    changes = payload.model_dump(exclude_unset=True)
    if changes.get('nombre') and db.scalar(select(Rol.id).where(Rol.nombre == changes['nombre'], Rol.id != id)) is not None: raise HTTPException(409, 'Ya existe un rol con ese nombre')
    for key, value in changes.items(): setattr(item, key, value)
    commit_or_conflict(db); db.refresh(item); return item

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, summary='Eliminar rol', responses={404:{'description':'Rol no encontrado'},409:{'description':'El rol tiene usuarios relacionados'}})
def eliminar_rol(id: int, db: Session = Depends(get_db)):
    item = get_or_404(db, Rol, id, 'Rol'); db.delete(item); commit_or_conflict(db)
