import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


def _default_sqlite_path() -> str:
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "legalintel.db")


def _build_database_url() -> str:
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url
    db_file = _default_sqlite_path()
    return f"sqlite:///{db_file}"


DATABASE_URL = _build_database_url()

# For SQLite in FastAPI threads
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _sqlite_object_exists(name: str, type_: str) -> bool:
    with engine.connect() as conn:
        res = conn.execute(
            text(
                "SELECT 1 FROM sqlite_master WHERE type = :type AND name = :name LIMIT 1"
            ),
            {"type": type_, "name": name},
        ).first()
        return res is not None


def _ensure_sqlite_fts5_objects() -> None:
    # Create FTS5 virtual table and triggers if they don't exist
    if not DATABASE_URL.startswith("sqlite"):
        return

    # Ensure base table exists before creating FTS and triggers
    from app.repositories.entities.DocumentEntity import DocumentEntity  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # doc_fts virtual table mirrors documents.text with content sync
    if not _sqlite_object_exists("doc_fts", "table"):
        with engine.connect() as conn:
            conn.execute(
                text(
                    """
                    CREATE VIRTUAL TABLE doc_fts USING fts5(
                        text,
                        content='documents',
                        content_rowid='id'
                    );
                    """
                )
            )
            conn.commit()

    # Triggers for sync
    triggers = {
        "documents_ai": """
            CREATE TRIGGER documents_ai AFTER INSERT ON documents BEGIN
                INSERT INTO doc_fts(rowid, text) VALUES (new.id, new.text);
            END;
        """,
        "documents_au": """
            CREATE TRIGGER documents_au AFTER UPDATE ON documents BEGIN
                UPDATE doc_fts SET text = new.text WHERE rowid = new.id;
            END;
        """,
        "documents_ad": """
            CREATE TRIGGER documents_ad AFTER DELETE ON documents BEGIN
                INSERT INTO doc_fts(doc_fts, rowid, text) VALUES ('delete', old.id, old.text);
            END;
        """,
    }

    with engine.connect() as conn:
        for name, ddl in triggers.items():
            if not _sqlite_object_exists(name, "trigger"):
                conn.execute(text(ddl))
        conn.commit()


def init_db() -> None:
    # Reload entity module so its Base binding matches this module's Base
    import importlib
    import app.repositories.entities.DocumentEntity as entity_module  # type: ignore
    try:
        importlib.reload(entity_module)
    except Exception:
        pass

    # Create tables, then FTS objects
    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_fts5_objects()


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


