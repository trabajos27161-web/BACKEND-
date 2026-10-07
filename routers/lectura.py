from fastapi import APIRouter,Depends,Query,status
from sqlalchemy import String,cast,or_,select
from sqlalchemy.orm import Session
from database import get_db
from models import Lectura,Locacion,Sensor
from schemas import LecturaCreate,LecturaUpdate,LecturaResponse
from routers.common import commit_or_conflict,ensure_exists,get_or_404
router=APIRouter(prefix='/lecturas',tags=['Lecturas'])
@router.get('/',response_model=list[LecturaResponse],summary='Listar lecturas')
def listar_lecturas(q:str|None=Query(None,description='Busca por cÃƒÆ’Ã‚Â³digo de sensor, locaciÃƒÆ’Ã‚Â³n, calidad o pH'),page:int=Query(1,ge=1),page_size:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):
    stmt=select(Lectura).join(Sensor).join(Locacion).order_by(Lectura.fecha_hora.desc(),Lectura.id.desc())
    if q:stmt=stmt.where(or_(Sensor.codigo.ilike(f'%{q}%'),Locacion.nombre.ilike(f'%{q}%'),Lectura.calidad.ilike(f'%{q}%'),cast(Lectura.valor,String).ilike(f'%{q}%')))
    return db.scalars(stmt.offset((page-1)*page_size).limit(page_size)).all()
@router.get('/{id}',response_model=LecturaResponse,summary='Obtener lectura',responses={404:{'description':'Lectura no encontrada'}})
def obtener_lectura(id:int,db:Session=Depends(get_db)):return get_or_404(db,Lectura,id,'Lectura')
@router.post('/',response_model=LecturaResponse,status_code=status.HTTP_201_CREATED,summary='Crear lectura',responses={422:{'description':'Sensor, locaciÃƒÆ’Ã‚Â³n o pH invÃƒÆ’Ã‚Â¡lido'}})
def crear_lectura(payload:LecturaCreate,db:Session=Depends(get_db)):
    data=payload.model_dump(exclude_none=True);ensure_exists(db,Sensor,data['idsensor'],'Sensor');ensure_exists(db,Locacion,data['idlocacion'],'LocaciÃƒÆ’Ã‚Â³n');item=Lectura(**data);db.add(item);commit_or_conflict(db);db.refresh(item);return item
@router.put('/{id}',response_model=LecturaResponse,summary='Actualizar lectura',responses={404:{'description':'Lectura no encontrada'},422:{'description':'Sensor, locaciÃƒÆ’Ã‚Â³n o pH invÃƒÆ’Ã‚Â¡lido'}})
def actualizar_lectura(id:int,payload:LecturaUpdate,db:Session=Depends(get_db)):
    item=get_or_404(db,Lectura,id,'Lectura');changes=payload.model_dump(exclude_unset=True)
    if changes.get('idsensor') is not None:ensure_exists(db,Sensor,changes['idsensor'],'Sensor')
    if changes.get('idlocacion') is not None:ensure_exists(db,Locacion,changes['idlocacion'],'LocaciÃƒÆ’Ã‚Â³n')
    for key,value in changes.items():setattr(item,key,value)
    commit_or_conflict(db);db.refresh(item);return item
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,summary='Eliminar lectura',responses={404:{'description':'Lectura no encontrada'}})
def eliminar_lectura(id:int,db:Session=Depends(get_db)):
    item=get_or_404(db,Lectura,id,'Lectura');db.delete(item);commit_or_conflict(db)
