from __future__ import annotations

from datetime import datetime

import fitz

from document_engine.models import DocumentMetadata


class PDFMetadataExtractor:
    def extract(self, file_path: str) -> DocumentMetadata:
        doc = fitz.open(file_path)
        meta = doc.metadata or {}

        def parse_date(s: Optional[str]) -> Optional[str]:
            if not s:
                return None
            try:
                return datetime.strptime(s.replace("'", ""), "D:%Y%m%d%H%M%S%z").isoformat()
            except (ValueError, TypeError):
                return s

        result = DocumentMetadata(
            title=meta.get("title"),
            author=meta.get("author"),
            subject=meta.get("subject"),
            keywords=[k.strip() for k in (meta.get("keywords", "") or "").split(",") if k.strip()],
            creator=meta.get("creator"),
            producer=meta.get("producer"),
            page_count=len(doc),
            file_format="pdf",
            created_at=parse_date(meta.get("creationDate")),
            modified_at=parse_date(meta.get("modDate")),
            pdf_version=meta.get("format"),
            raw=dict(meta),
        )

        doc.close()
        return result
