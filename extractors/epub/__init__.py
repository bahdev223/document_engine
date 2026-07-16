from __future__ import annotations

from pathlib import Path

from document_engine.models import Document
from document_engine.core.registry import Extractor, register_extractor


class EpubExtractor(Extractor):
    format = "epub"

    def extract(self, file_path: str) -> Document:
        p = Path(file_path)
        document = Document(
            title=p.stem,
            file_path=file_path,
            file_format="epub",
            file_size_bytes=p.stat().st_size,
            raw_metadata={"error": "EPUB extraction not yet implemented"},
            errors=["EPUB extraction requires ebooklib"],
        )
        return document

    def extract_text(self, file_path: str) -> str:
        return ""


register_extractor(EpubExtractor())
