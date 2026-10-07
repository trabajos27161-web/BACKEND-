from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import TipoSensor
from schemas import TipoSensorCreate, TipoSensorUpdate, TipoSensorResponse
from routers.common import commit_or_conflict,get_or_404
router=APIRouter(prefix='/tipos-sensor',tags=['Tipos de Sensor'])
@router.get('/',response_model=list[TipoSensorResponse],summary='Listar tipos de sensor')
def listar_tipos_sensor(q:str|None=Query(None),page:int=Query(1,ge=1),page_size:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):
    stmt=select(TipoSensor).order_by(TipoSensor.id)
    if q:stmt=stmt.where(TipoSensor.nombre.ilike(f'%{q}%'))
    return db.scalars(stmt.offset((page-1)*page_size).limit(page_size)).all()
@router.get('/{id}',response_model=TipoSensorResponse,summary='Obtener tipo de sensor',responses={404:{'description':'Tipo de sensor no encontrado'}})
def obtener_tipo_sensor(id:int,db:Session=Depends(get_db)):return get_or_404(db,TipoSensor,id,'Tipo de sensor')
@router.post('/',response_model=TipoSensorResponse,status_code=status.HTTP_201_CREATED,summary='Crear tipo de sensor',responses={409:{'description':'Nombre duplicado'}})
def crear_tipo_sensor(payload:TipoSensorCreate,db:Session=Depends(get_db)):
    if db.scalar(select(TipoSensor.id).where(TipoSensor.nombre==payload.nombre)) is not None:raise HTTPException(409,'Ya existe un tipo de sensor con ese nombre')
    item=TipoSensor(**payload.model_dump());db.add(item);commit_or_conflict(db);db.refresh(item);return item
@router.put('/{id}',response_model=TipoSensorResponse,summary='Actualizar tipo de sensor',responses={404:{'description':'Tipo no encontrado'},409:{'description':'Nombre duplicado'}})
def actualizar_tipo_sensor(id:int,payload:TipoSensorUpdate,db:Session=Depends(get_db)):
    item=get_or_404(db,TipoSensor,id,'Tipo de sensor');changes=payload.model_dump(exclude_unset=True)
    if changes.get('nombre') and db.scalar(select(TipoSensor.id).where(TipoSensor.nombre==changes['nombre'],TipoSensor.id!=id)) is not None:raise HTTPException(409,'Ya existe un tipo de sensor con ese nombre')
    for key,value in changes.items():setattr(item,key,value)
    commit_or_conflict(db);db.refresh(item);return item
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,summary='Eliminar tipo de sensor',responses={404:{'description':'Tipo no encontrado'},409:{'description':'El tipo tiene sensores relacionados'}})
def eliminar_tipo_sensor(id:int,db:Session=Depends(get_db)):
    item=get_or_404(db,TipoSensor,id,'Tipo de sensor');db.delete(item);commit_or_conflict(db)
