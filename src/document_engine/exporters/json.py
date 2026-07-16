from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone

from document_engine.models import Document
from document_engine.core.registry import Builder, register_builder


class JSONExporter(Builder):
    format = "json"

    def build(self, document: Document) -> dict:
        chapters_data = []
        for ch in document.flat_chapters() if hasattr(document, "flat_chapters") else document.chapters:
            chapters_data.append({
                "title": ch.title,
                "level": ch.level,
                "word_count": ch.word_count,
                "content_preview": ch.content[:300] if ch.content else "",
                "images_count": len(ch.images),
                "tables_count": len(ch.tables),
                "code_blocks_count": len(ch.code_blocks),
            })

        stats = asdict(document.statistics) if document.statistics else {}

        result = {
            "document": {
                "title": document.title,
                "file_path": document.file_path,
                "file_format": document.file_format,
                "file_size_bytes": document.file_size_bytes,
                "language": document.language,
            },
            "statistics": stats,
            "chapters": chapters_data,
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "version": "0.1.0",
        }

        return {
            "json": result,
            "format": "json",
        }


register_builder(JSONExporter())
