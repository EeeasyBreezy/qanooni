import os
from typing import Iterable, Optional
from sqlalchemy import create_engine, text


class DatabaseCleaner:
    def __init__(self, database_url: Optional[str] = None) -> None:
        self._url = database_url or os.getenv("DATABASE_URL", "postgresql+psycopg2://qanooni:qanooni@localhost:5432/qanooni")
        self._engine = create_engine(self._url, future=True)

    def delete_documents_by_file_names(self, file_names: Iterable[str]) -> None:
        names = list(file_names)
        if not names:
            return
        with self._engine.begin() as conn:
            for name in names:
                conn.execute(text("DELETE FROM document_chunks WHERE document_id IN (SELECT id FROM documents WHERE file_name = :name)"), {"name": name})
                conn.execute(text("DELETE FROM documents WHERE file_name = :name"), {"name": name})


