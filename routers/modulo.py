from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import Modulo
from schemas import ModuloCreate, ModuloUpdate, ModuloResponse
from routers.common import commit_or_conflict, get_or_404
router = APIRouter(prefix='/modulos', tags=['MÃƒÆ’Ã‚Â³dulos'])

@router.get('/', response_model=list[ModuloResponse], summary='Listar mÃƒÆ’Ã‚Â³dulos')
def listar_modulos(q: str | None = Query(None), page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    stmt = select(Modulo).order_by(Modulo.id)
    if q: stmt = stmt.where(Modulo.nombre.ilike(f'%{q}%'))
    return db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all()

@router.get('/{id}', response_model=ModuloResponse, summary='Obtener mÃƒÆ’Ã‚Â³dulo', responses={404:{'description':'MÃƒÆ’Ã‚Â³dulo no encontrado'}})
def obtener_modulo(id: int, db: Session = Depends(get_db)):
    return get_or_404(db, Modulo, id, 'MÃƒÆ’Ã‚Â³dulo')

@router.post('/', response_model=ModuloResponse, status_code=status.HTTP_201_CREATED, summary='Crear mÃƒÆ’Ã‚Â³dulo', responses={409:{'description':'Nombre duplicado'}})
def crear_modulo(payload: ModuloCreate, db: Session = Depends(get_db)):
    if db.scalar(select(Modulo.id).where(Modulo.nombre == payload.nombre)) is not None: raise HTTPException(409, 'Ya existe un mÃƒÆ’Ã‚Â³dulo con ese nombre')
    item = Modulo(**payload.model_dump()); db.add(item); commit_or_conflict(db); db.refresh(item); return item

@router.put('/{id}', response_model=ModuloResponse, summary='Actualizar mÃƒÆ’Ã‚Â³dulo', responses={404:{'description':'MÃƒÆ’Ã‚Â³dulo no encontrado'},409:{'description':'Nombre duplicado'}})
def actualizar_modulo(id: int, payload: ModuloUpdate, db: Session = Depends(get_db)):
    item = get_or_404(db, Modulo, id, 'MÃƒÆ’Ã‚Â³dulo'); changes = payload.model_dump(exclude_unset=True)
    if changes.get('nombre') and db.scalar(select(Modulo.id).where(Modulo.nombre == changes['nombre'], Modulo.id != id)) is not None: raise HTTPException(409, 'Ya existe un mÃƒÆ’Ã‚Â³dulo con ese nombre')
    for key,value in changes.items(): setattr(item,key,value)
    commit_or_conflict(db); db.refresh(item); return item

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, summary='Eliminar mÃƒÆ’Ã‚Â³dulo', responses={404:{'description':'MÃƒÆ’Ã‚Â³dulo no encontrado'},409:{'description':'El mÃƒÆ’Ã‚Â³dulo tiene permisos relacionados'}})
def eliminar_modulo(id: int, db: Session = Depends(get_db)):
    item=get_or_404(db,Modulo,id,'MÃƒÆ’Ã‚Â³dulo'); db.delete(item); commit_or_conflict(db)
