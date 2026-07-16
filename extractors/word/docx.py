from __future__ import annotations

from pathlib import Path

from docx import Document as DocxDocument

from document_engine.models import Document, ImageElement, TableElement
from document_engine.core.registry import Extractor, register_extractor


class DocxExtractor(Extractor):
    format = "docx"

    def extract(self, file_path: str) -> Document:
        docx = DocxDocument(file_path)
        p = Path(file_path)

        document = Document(
            title=p.stem,
            file_path=file_path,
            file_format="docx",
            file_size_bytes=p.stat().st_size,
        )

        paragraphs: list[str] = []
        for para in docx.paragraphs:
            paragraphs.append(para.text)
        document.text = "\n".join(paragraphs)

        for i, table in enumerate(docx.tables):
            headers = [cell.text for cell in table.rows[0].cells] if table.rows else []
            rows = [[cell.text for cell in row.cells] for row in table.rows[1:]]
            document.tables.append(TableElement(headers=headers, rows=rows))

        document.raw_metadata["paragraph_count"] = len(docx.paragraphs)
        document.raw_metadata["table_count"] = len(docx.tables)
        document.raw_metadata["section_count"] = len(docx.sections)

        return document

    def extract_text(self, file_path: str) -> str:
        docx = DocxDocument(file_path)
        return "\n".join(p.text for p in docx.paragraphs)


register_extractor(DocxExtractor())
