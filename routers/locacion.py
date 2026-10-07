from fastapi import APIRouter,Depends,Query,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import Dpto,Locacion
from schemas import LocacionCreate,LocacionUpdate,LocacionResponse
from routers.common import commit_or_conflict,ensure_exists,get_or_404
router=APIRouter(prefix='/locaciones',tags=['Locaciones'])
@router.get('/',response_model=list[LocacionResponse],summary='Listar locaciones')
def listar_locaciones(q:str|None=Query(None),page:int=Query(1,ge=1),page_size:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):
    stmt=select(Locacion).order_by(Locacion.id)
    if q:stmt=stmt.where(Locacion.nombre.ilike(f'%{q}%'))
    return db.scalars(stmt.offset((page-1)*page_size).limit(page_size)).all()
@router.get('/{id}',response_model=LocacionResponse,summary='Obtener locaciÃƒÆ’Ã‚Â³n',responses={404:{'description':'LocaciÃƒÆ’Ã‚Â³n no encontrada'}})
def obtener_locacion(id:int,db:Session=Depends(get_db)):return get_or_404(db,Locacion,id,'LocaciÃƒÆ’Ã‚Â³n')
@router.post('/',response_model=LocacionResponse,status_code=status.HTTP_201_CREATED,summary='Crear locaciÃƒÆ’Ã‚Â³n',responses={422:{'description':'Departamento inexistente o coordenadas invÃƒÆ’Ã‚Â¡lidas'}})
def crear_locacion(payload:LocacionCreate,db:Session=Depends(get_db)):
    data=payload.model_dump();ensure_exists(db,Dpto,data['iddpto'],'Departamento');item=Locacion(**data);db.add(item);commit_or_conflict(db);db.refresh(item);return item
@router.put('/{id}',response_model=LocacionResponse,summary='Actualizar locaciÃƒÆ’Ã‚Â³n',responses={404:{'description':'LocaciÃƒÆ’Ã‚Â³n no encontrada'},422:{'description':'Departamento inexistente o coordenadas invÃƒÆ’Ã‚Â¡lidas'}})
def actualizar_locacion(id:int,payload:LocacionUpdate,db:Session=Depends(get_db)):
    item=get_or_404(db,Locacion,id,'LocaciÃƒÆ’Ã‚Â³n');changes=payload.model_dump(exclude_unset=True)
    if changes.get('iddpto') is not None:ensure_exists(db,Dpto,changes['iddpto'],'Departamento')
    for key,value in changes.items():setattr(item,key,value)
    commit_or_conflict(db);db.refresh(item);return item
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,summary='Eliminar locaciÃƒÆ’Ã‚Â³n',responses={404:{'description':'LocaciÃƒÆ’Ã‚Â³n no encontrada'},409:{'description':'La locaciÃƒÆ’Ã‚Â³n tiene lecturas relacionadas'}})
def eliminar_locacion(id:int,db:Session=Depends(get_db)):
    item=get_or_404(db,Locacion,id,'LocaciÃƒÆ’Ã‚Â³n');db.delete(item);commit_or_conflict(db)
