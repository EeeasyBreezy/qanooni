from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db import Base

try:
    # Optional at import time; table can still be created even if pgvector not installed in dev
    from pgvector.sqlalchemy import Vector  # type: ignore
except Exception:  # pragma: no cover - fallback for environments without pgvector
    Vector = None  # type: ignore


class DocumentChunkEntity(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Embedding vector (nullable until embeddings are computed). Dimension set for all-MiniLM-L6-v2 (384).
    if Vector is not None:
        embedding = mapped_column(Vector(384), nullable=True)  # type: ignore
    else:
        # Fallback to Text to keep schema creatable without pgvector installed
        embedding = mapped_column(Text, nullable=True)  # type: ignore

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )


