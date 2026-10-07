from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from database import get_db
from models import Rol, Usuarios
from schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from routers.common import commit_or_conflict, ensure_exists, get_or_404
from security import hash_password
router = APIRouter(prefix='/usuarios', tags=['Usuarios'])

@router.get('/', response_model=list[UsuarioResponse], summary='Listar usuarios')
def listar_usuarios(q: str | None = Query(None), page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    stmt=select(Usuarios).order_by(Usuarios.id)
    if q: stmt=stmt.where(or_(Usuarios.nombre.ilike(f'%{q}%'),Usuarios.apellido.ilike(f'%{q}%'),Usuarios.correo.ilike(f'%{q}%')))
    return db.scalars(stmt.offset((page-1)*page_size).limit(page_size)).all()

@router.get('/{id}', response_model=UsuarioResponse, summary='Obtener usuario', responses={404:{'description':'Usuario no encontrado'}})
def obtener_usuario(id:int, db:Session=Depends(get_db)):
    return get_or_404(db,Usuarios,id,'Usuario')

@router.post('/', response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary='Crear usuario', responses={409:{'description':'Correo duplicado'},422:{'description':'Rol inexistente o datos invÃƒÆ’Ã‚Â¡lidos'}})
def crear_usuario(payload:UsuarioCreate, db:Session=Depends(get_db)):
    data=payload.model_dump(); ensure_exists(db,Rol,data['idrol'],'Rol')
    if db.scalar(select(Usuarios.id).where(Usuarios.correo==str(data['correo']))) is not None: raise HTTPException(409,'Ya existe un usuario con ese correo')
    data['correo']=str(data['correo']); data['password']=hash_password(data['password']); item=Usuarios(**data); db.add(item); commit_or_conflict(db); db.refresh(item); return item

@router.put('/{id}', response_model=UsuarioResponse, summary='Actualizar usuario', responses={404:{'description':'Usuario no encontrado'},409:{'description':'Correo duplicado'},422:{'description':'Rol inexistente'}})
def actualizar_usuario(id:int,payload:UsuarioUpdate,db:Session=Depends(get_db)):
    item=get_or_404(db,Usuarios,id,'Usuario'); changes=payload.model_dump(exclude_unset=True)
    if changes.get('idrol') is not None: ensure_exists(db,Rol,changes['idrol'],'Rol')
    if changes.get('correo') is not None:
        changes['correo']=str(changes['correo'])
        if db.scalar(select(Usuarios.id).where(Usuarios.correo==changes['correo'],Usuarios.id!=id)) is not None: raise HTTPException(409,'Ya existe un usuario con ese correo')
    if changes.get('password'): changes['password']=hash_password(changes['password'])
    for key,value in changes.items(): setattr(item,key,value)
    commit_or_conflict(db); db.refresh(item); return item

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, summary='Eliminar usuario', responses={404:{'description':'Usuario no encontrado'},409:{'description':'El usuario tiene asignaciones relacionadas'}})
def eliminar_usuario(id:int,db:Session=Depends(get_db)):
    item=get_or_404(db,Usuarios,id,'Usuario'); db.delete(item); commit_or_conflict(db)
