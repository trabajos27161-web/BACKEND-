from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

def get_or_404(db: Session, model: type, record_id: int, entity_name: str):
    record = db.get(model, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f'{entity_name} no encontrado')
    return record

def commit_or_conflict(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        code = getattr(getattr(exc.orig, 'diag', None), 'sqlstate', None) or getattr(exc.orig, 'pgcode', None)
        if code == '23502':
            raise HTTPException(status_code=422, detail='Falta un campo obligatorio o se enviÃƒÆ’Ã‚Â³ como nulo') from exc
        if code == '23505':
            raise HTTPException(status_code=409, detail='Ya existe un registro con ese valor ÃƒÆ’Ã‚Âºnico') from exc
        if code == '23503':
            raise HTTPException(status_code=409, detail='La operaciÃƒÆ’Ã‚Â³n afecta registros relacionados') from exc
        if code == '23514':
            raise HTTPException(status_code=422, detail='Los datos no cumplen una restricciÃƒÆ’Ã‚Â³n de la base de datos') from exc
        raise HTTPException(status_code=409, detail='No se pudo completar la operaciÃƒÆ’Ã‚Â³n por una restricciÃƒÆ’Ã‚Â³n de integridad') from exc

def ensure_exists(db: Session, model: type, record_id: int, entity_name: str) -> None:
    if db.get(model, record_id) is None:
        raise HTTPException(status_code=422, detail=f'{entity_name} indicado no existe')
