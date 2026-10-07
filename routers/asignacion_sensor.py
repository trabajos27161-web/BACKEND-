from fastapi import APIRouter,Depends,HTTPException,Query,status
from sqlalchemy import or_,select
from sqlalchemy.orm import Session
from database import get_db
from models import AsignacionSensor,Sensor,Usuarios
from schemas import AsignacionSensorCreate,AsignacionSensorUpdate,AsignacionSensorResponse
from routers.common import commit_or_conflict,ensure_exists,get_or_404
router=APIRouter(prefix='/asignaciones-sensor',tags=['Asignaciones de Sensor'])
@router.get('/',response_model=list[AsignacionSensorResponse],summary='Listar asignaciones de sensor')
def listar_asignaciones(q:str|None=Query(None,description='Filtra por estado, usuario o sensor'),page:int=Query(1,ge=1),page_size:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):
    stmt=select(AsignacionSensor).join(Usuarios).join(Sensor).order_by(AsignacionSensor.fecha_asignacion.desc())
    if q:stmt=stmt.where(or_(AsignacionSensor.estado.ilike(f'%{q}%'),Usuarios.nombre.ilike(f'%{q}%'),Usuarios.apellido.ilike(f'%{q}%'),Sensor.codigo.ilike(f'%{q}%')))
    return db.scalars(stmt.offset((page-1)*page_size).limit(page_size)).all()
@router.get('/{id}',response_model=AsignacionSensorResponse,summary='Obtener asignaciÃƒÆ’Ã‚Â³n',responses={404:{'description':'AsignaciÃƒÆ’Ã‚Â³n no encontrada'}})
def obtener_asignacion(id:int,db:Session=Depends(get_db)):return get_or_404(db,AsignacionSensor,id,'AsignaciÃƒÆ’Ã‚Â³n de sensor')
@router.post('/',response_model=AsignacionSensorResponse,status_code=status.HTTP_201_CREATED,summary='Crear asignaciÃƒÆ’Ã‚Â³n',responses={422:{'description':'Usuario, sensor o fechas invÃƒÆ’Ã‚Â¡lidos'}})
def crear_asignacion(payload:AsignacionSensorCreate,db:Session=Depends(get_db)):
    data=payload.model_dump(exclude_none=True);ensure_exists(db,Usuarios,data['idusuario'],'Usuario');ensure_exists(db,Sensor,data['idsensor'],'Sensor');item=AsignacionSensor(**data);db.add(item);commit_or_conflict(db);db.refresh(item);return item
@router.put('/{id}',response_model=AsignacionSensorResponse,summary='Actualizar asignaciÃƒÆ’Ã‚Â³n',responses={404:{'description':'AsignaciÃƒÆ’Ã‚Â³n no encontrada'},422:{'description':'RelaciÃƒÆ’Ã‚Â³n, estado o fechas invÃƒÆ’Ã‚Â¡lidas'}})
def actualizar_asignacion(id:int,payload:AsignacionSensorUpdate,db:Session=Depends(get_db)):
    item=get_or_404(db,AsignacionSensor,id,'AsignaciÃƒÆ’Ã‚Â³n de sensor');changes=payload.model_dump(exclude_unset=True)
    if changes.get('idusuario') is not None:ensure_exists(db,Usuarios,changes['idusuario'],'Usuario')
    if changes.get('idsensor') is not None:ensure_exists(db,Sensor,changes['idsensor'],'Sensor')
    inicio=changes.get('fecha_asignacion',item.fecha_asignacion);fin=changes.get('fecha_fin',item.fecha_fin)
    if inicio is not None and fin is not None and fin<inicio:raise HTTPException(422,'fecha_fin debe ser posterior o igual a fecha_asignacion')
    for key,value in changes.items():setattr(item,key,value)
    commit_or_conflict(db);db.refresh(item);return item
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,summary='Eliminar asignaciÃƒÆ’Ã‚Â³n',responses={404:{'description':'AsignaciÃƒÆ’Ã‚Â³n no encontrada'}})
def eliminar_asignacion(id:int,db:Session=Depends(get_db)):
    item=get_or_404(db,AsignacionSensor,id,'AsignaciÃƒÆ’Ã‚Â³n de sensor');db.delete(item);commit_or_conflict(db)
