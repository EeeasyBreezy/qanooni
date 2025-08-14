from dataclasses import dataclass


@dataclass
class File:
    file_name: str
    mime_type: str
    size_bytes: int
    content: bytes