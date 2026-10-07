import os
from functools import lru_cache
from collections.abc import Generator
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

@lru_cache(maxsize=4)
def _session_factory(database_url: str):
    url = make_url(database_url)
    if url.drivername == 'postgresql':
        url = url.set(drivername='postgresql+psycopg2')
    engine = create_engine(url, pool_pre_ping=True, pool_recycle=300)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db() -> Generator[Session, None, None]:
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise HTTPException(status_code=503, detail='Configura DATABASE_URL en el archivo .env.')
    db = _session_factory(database_url)()
    try:
        yield db
    finally:
        db.close()
