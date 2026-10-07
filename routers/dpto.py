from fastapi import APIRouter,Depends,HTTPException,Query,status
from sqlalchemy import or_,select
from sqlalchemy.orm import Session
from database import get_db
from models import Dpto
from schemas import DptoCreate,DptoUpdate,DptoResponse
from routers.common import commit_or_conflict,get_or_404
router=APIRouter(prefix='/dptos',tags=['Departamentos'])
@router.get('/',response_model=list[DptoResponse],summary='Listar departamentos')
def listar_dptos(q:str|None=Query(None),page:int=Query(1,ge=1),page_size:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):
    stmt=select(Dpto).order_by(Dpto.id)
    if q:stmt=stmt.where(or_(Dpto.nombre.ilike(f'%{q}%'),Dpto.codigo.ilike(f'%{q}%')))
    return db.scalars(stmt.offset((page-1)*page_size).limit(page_size)).all()
@router.get('/{id}',response_model=DptoResponse,summary='Obtener departamento',responses={404:{'description':'Departamento no encontrado'}})
def obtener_dpto(id:int,db:Session=Depends(get_db)):return get_or_404(db,Dpto,id,'Departamento')
@router.post('/',response_model=DptoResponse,status_code=status.HTTP_201_CREATED,summary='Crear departamento',responses={409:{'description':'Nombre o cÃƒÆ’Ã‚Â³digo duplicado'}})
def crear_dpto(payload:DptoCreate,db:Session=Depends(get_db)):
    if db.scalar(select(Dpto.id).where(Dpto.nombre==payload.nombre)) is not None:raise HTTPException(409,'Ya existe un departamento con ese nombre')
    if payload.codigo and db.scalar(select(Dpto.id).where(Dpto.codigo==payload.codigo)) is not None:raise HTTPException(409,'Ya existe un departamento con ese cÃƒÆ’Ã‚Â³digo')
    item=Dpto(**payload.model_dump());db.add(item);commit_or_conflict(db);db.refresh(item);return item
@router.put('/{id}',response_model=DptoResponse,summary='Actualizar departamento',responses={404:{'description':'Departamento no encontrado'},409:{'description':'Nombre o cÃƒÆ’Ã‚Â³digo duplicado'}})
def actualizar_dpto(id:int,payload:DptoUpdate,db:Session=Depends(get_db)):
    item=get_or_404(db,Dpto,id,'Departamento');changes=payload.model_dump(exclude_unset=True)
    if changes.get('nombre') and db.scalar(select(Dpto.id).where(Dpto.nombre==changes['nombre'],Dpto.id!=id)) is not None:raise HTTPException(409,'Ya existe un departamento con ese nombre')
    if changes.get('codigo') and db.scalar(select(Dpto.id).where(Dpto.codigo==changes['codigo'],Dpto.id!=id)) is not None:raise HTTPException(409,'Ya existe un departamento con ese cÃƒÆ’Ã‚Â³digo')
    for key,value in changes.items():setattr(item,key,value)
    commit_or_conflict(db);db.refresh(item);return item
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,summary='Eliminar departamento',responses={404:{'description':'Departamento no encontrado'},409:{'description':'El departamento tiene locaciones relacionadas'}})
def eliminar_dpto(id:int,db:Session=Depends(get_db)):
    item=get_or_404(db,Dpto,id,'Departamento');db.delete(item);commit_or_conflict(db)
