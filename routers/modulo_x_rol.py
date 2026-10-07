from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import Modulo, ModuloXRol, Rol
from schemas import ModuloXRolCreate, ModuloXRolUpdate, ModuloXRolResponse
from routers.common import commit_or_conflict, ensure_exists, get_or_404
router=APIRouter(prefix='/modulo-x-rol',tags=['MÃƒÆ’Ã‚Â³dulo x Rol'])

@router.get('/',response_model=list[ModuloXRolResponse],summary='Listar permisos de mÃƒÆ’Ã‚Â³dulos por rol')
def listar_modulos_x_rol(q:int|None=Query(None,description='Filtra por idrol o idmodulo'),page:int=Query(1,ge=1),page_size:int=Query(50,ge=1,le=100),db:Session=Depends(get_db)):
    stmt=select(ModuloXRol).order_by(ModuloXRol.id)
    if q is not None: stmt=stmt.where((ModuloXRol.idrol==q)|(ModuloXRol.idmodulo==q))
    return db.scalars(stmt.offset((page-1)*page_size).limit(page_size)).all()

@router.get('/{id}',response_model=ModuloXRolResponse,summary='Obtener permiso mÃƒÆ’Ã‚Â³dulo-rol',responses={404:{'description':'RelaciÃƒÆ’Ã‚Â³n no encontrada'}})
def obtener_modulo_x_rol(id:int,db:Session=Depends(get_db)): return get_or_404(db,ModuloXRol,id,'RelaciÃƒÆ’Ã‚Â³n mÃƒÆ’Ã‚Â³dulo-rol')

@router.post('/',response_model=ModuloXRolResponse,status_code=status.HTTP_201_CREATED,summary='Crear permiso mÃƒÆ’Ã‚Â³dulo-rol',responses={409:{'description':'La combinaciÃƒÆ’Ã‚Â³n ya existe'},422:{'description':'Rol o mÃƒÆ’Ã‚Â³dulo inexistente'}})
def crear_modulo_x_rol(payload:ModuloXRolCreate,db:Session=Depends(get_db)):
    data=payload.model_dump();ensure_exists(db,Rol,data['idrol'],'Rol');ensure_exists(db,Modulo,data['idmodulo'],'MÃƒÆ’Ã‚Â³dulo')
    if db.scalar(select(ModuloXRol.id).where(ModuloXRol.idrol==data['idrol'],ModuloXRol.idmodulo==data['idmodulo'])) is not None: raise HTTPException(409,'El mÃƒÆ’Ã‚Â³dulo ya estÃƒÆ’Ã‚Â¡ asignado al rol')
    item=ModuloXRol(**data);db.add(item);commit_or_conflict(db);db.refresh(item);return item

@router.put('/{id}',response_model=ModuloXRolResponse,summary='Actualizar permiso mÃƒÆ’Ã‚Â³dulo-rol',responses={404:{'description':'RelaciÃƒÆ’Ã‚Â³n no encontrada'},409:{'description':'La combinaciÃƒÆ’Ã‚Â³n ya existe'},422:{'description':'Rol o mÃƒÆ’Ã‚Â³dulo inexistente'}})
def actualizar_modulo_x_rol(id:int,payload:ModuloXRolUpdate,db:Session=Depends(get_db)):
    item=get_or_404(db,ModuloXRol,id,'RelaciÃƒÆ’Ã‚Â³n mÃƒÆ’Ã‚Â³dulo-rol');changes=payload.model_dump(exclude_unset=True)
    if changes.get('idrol') is not None:ensure_exists(db,Rol,changes['idrol'],'Rol')
    if changes.get('idmodulo') is not None:ensure_exists(db,Modulo,changes['idmodulo'],'MÃƒÆ’Ã‚Â³dulo')
    target_rol=changes.get('idrol',item.idrol);target_modulo=changes.get('idmodulo',item.idmodulo)
    if db.scalar(select(ModuloXRol.id).where(ModuloXRol.idrol==target_rol,ModuloXRol.idmodulo==target_modulo,ModuloXRol.id!=id)) is not None: raise HTTPException(409,'El mÃƒÆ’Ã‚Â³dulo ya estÃƒÆ’Ã‚Â¡ asignado al rol')
    for key,value in changes.items():setattr(item,key,value)
    commit_or_conflict(db);db.refresh(item);return item

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT,summary='Eliminar permiso mÃƒÆ’Ã‚Â³dulo-rol',responses={404:{'description':'RelaciÃƒÆ’Ã‚Â³n no encontrada'}})
def eliminar_modulo_x_rol(id:int,db:Session=Depends(get_db)):
    item=get_or_404(db,ModuloXRol,id,'RelaciÃƒÆ’Ã‚Â³n mÃƒÆ’Ã‚Â³dulo-rol');db.delete(item);commit_or_conflict(db)
