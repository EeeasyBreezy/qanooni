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


def _ensure_postgres_fts_objects() -> None:
    # Ensure Postgres FTS generated column and index exist
    if engine.dialect.name != "postgresql":
        return
    with engine.connect() as conn:
        # Create extensions if possible
        try:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        except Exception:
            pass
        # Add generated tsvector column and GIN index
        conn.execute(
            text(
                """
                ALTER TABLE documents
                ADD COLUMN IF NOT EXISTS text_tsv tsvector
                GENERATED ALWAYS AS (to_tsvector('simple', text)) STORED;
                """
            )
        )
        conn.execute(
            text(
                """
                CREATE INDEX IF NOT EXISTS idx_documents_text_tsv
                ON documents USING GIN (text_tsv);
                """
            )
        )
        conn.commit()


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

    # Create tables
    Base.metadata.create_all(bind=engine)
    # Ensure Postgres FTS objects
    _ensure_postgres_fts_objects()


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


