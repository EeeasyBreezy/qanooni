import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


def _build_database_url() -> str:
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url
    # Default to local Postgres (docker-compose) if not provided
    return "postgresql+psycopg2://qanooni:qanooni@localhost:5432/qanooni"


DATABASE_URL = _build_database_url()

# Engine for Postgres (or other SQLAlchemy-supported DBs)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)

def init_db() -> None:
    # Reload entity module so its Base binding matches this module's Base
    import importlib
    import app.repositories.entities.DocumentEntity as entity_module  # type: ignore
    import app.repositories.entities.DocumentChunkEntity as chunk_module  # type: ignore
    try:
        importlib.reload(entity_module)
        importlib.reload(chunk_module)
    except Exception:
        pass

    # Require Postgres and ensure required extensions BEFORE creating tables that rely on them
    if engine.dialect.name != "postgresql":
        raise RuntimeError("PostgreSQL with pgvector is required. Set DATABASE_URL to a Postgres instance.")
    with engine.connect() as conn:
        # pgvector for embedding column; pg_trgm for text search helpers
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        conn.commit()

    # Create tables
    Base.metadata.create_all(bind=engine)

    # No FTS setup


@contextmanager
def session_scope() -> Generator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


