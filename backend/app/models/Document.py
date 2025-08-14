from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    file_name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    # Extracted plain text for FTS
    text: Mapped[str] = mapped_column(Text, nullable=False)

    # Extracted metadata
    agreement_type: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    industry: Mapped[Optional[str]] = mapped_column(String(128), index=True)
    geography_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )


