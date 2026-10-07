from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_,select
from sqlalchemy.orm import Session
from database import get_db
from models import Sensor,TipoSensor
from schemas import SensorCreate,SensorUpdate,SensorResponse
from routers.common import commit_or_conflict,ensure_exists,get_or_404
router=APIRouter(prefix='/sensores',tags=['Sensores'])
@router.get('/',response_model=list[SensorResponse],summary='Listar sensores')
def listar_sensores(q:str|None=Query(None),page:int=Query(1,ge=1),page_size:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):
    stmt=select(Sensor).order_by(Sensor.id)
    if q:stmt=stmt.where(or_(Sensor.codigo.ilike(f'%{q}%'),Sensor.nombre.ilike(f'%{q}%'),Sensor.fabricante.ilike(f'%{q}%')))
    return db.scalars(stmt.offset((page-1)*page_size).limit(page_size)).all()
@router.get('/{id}',response_model=SensorResponse,summary='Obtener sensor',responses={404:{'description':'Sensor no encontrado'}})
def obtener_sensor(id:int,db:Session=Depends(get_db)):return get_or_404(db,Sensor,id,'Sensor')
@router.post('/',response_model=SensorResponse,status_code=status.HTTP_201_CREATED,summary='Crear sensor',responses={409:{'description':'CÃƒÆ’Ã‚Â³digo duplicado'},422:{'description':'Tipo de sensor inexistente'}})
def crear_sensor(payload:SensorCreate,db:Session=Depends(get_db)):
    data=payload.model_dump(exclude_none=True);ensure_exists(db,TipoSensor,data['idtiposensor'],'Tipo de sensor')
    if db.scalar(select(Sensor.id).where(Sensor.codigo==data['codigo'])) is not None:raise HTTPException(409,'Ya existe un sensor con ese cÃƒÆ’Ã‚Â³digo')
    item=Sensor(**data);db.add(item);commit_or_conflict(db);db.refresh(item);return item
@router.put('/{id}',response_model=SensorResponse,summary='Actualizar sensor',responses={404:{'description':'Sensor no encontrado'},409:{'description':'CÃƒÆ’Ã‚Â³digo duplicado'},422:{'description':'Tipo inexistente'}})
def actualizar_sensor(id:int,payload:SensorUpdate,db:Session=Depends(get_db)):
    item=get_or_404(db,Sensor,id,'Sensor');changes=payload.model_dump(exclude_unset=True)
    if changes.get('idtiposensor') is not None:ensure_exists(db,TipoSensor,changes['idtiposensor'],'Tipo de sensor')
    if changes.get('codigo') and db.scalar(select(Sensor.id).where(Sensor.codigo==changes['codigo'],Sensor.id!=id)) is not None:raise HTTPException(409,'Ya existe un sensor con ese cÃƒÆ’Ã‚Â³digo')
    for key,value in changes.items():setattr(item,key,value)
    commit_or_conflict(db);db.refresh(item);return item
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,summary='Eliminar sensor',responses={404:{'description':'Sensor no encontrado'},409:{'description':'El sensor tiene lecturas o asignaciones'}})
def eliminar_sensor(id:int,db:Session=Depends(get_db)):
    item=get_or_404(db,Sensor,id,'Sensor');db.delete(item);commit_or_conflict(db)
