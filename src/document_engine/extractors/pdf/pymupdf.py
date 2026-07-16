from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF

from document_engine.models import (
    Document, ImageElement, Link, DocumentStatistics,
)
from document_engine.core.registry import Extractor, register_extractor


class PyMuPDFExtractor(Extractor):
    format = "pdf"

    def supports(self, file_path: str) -> bool:
        return file_path.lower().endswith(".pdf")

    def extract_from_stream(self, stream: bytes, filename: str = "upload.pdf") -> Document:
        doc = fitz.open(stream=stream, filetype="pdf")
        document = Document(
            title=doc.metadata.get("title", Path(filename).stem),
            file_path=filename,
            file_format="pdf",
            file_size_bytes=len(stream),
            raw_metadata=dict(doc.metadata or {}),
        )
        return self._process_pages(doc, document)

    def extract(self, file_path: str) -> Document:
        doc = fitz.open(file_path)
        p = Path(file_path)
        document = Document(
            title=doc.metadata.get("title", p.stem),
            file_path=file_path,
            file_format="pdf",
            file_size_bytes=p.stat().st_size,
            raw_metadata=dict(doc.metadata or {}),
        )
        return self._process_pages(doc, document)

    def _process_pages(self, doc: fitz.Document, document: Document) -> Document:
        document.raw_metadata["page_count"] = len(doc)
        full_text: list[str] = []

        for page_num, page in enumerate(doc, start=1):
            full_text.append(page.get_text("text"))

            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                    document.images.append(ImageElement(
                        path=f"page_{page_num}_img_{img_index}.{base_image['ext']}",
                        format=base_image["ext"],
                        size_bytes=base_image.get("width", 0) * base_image.get("height", 0) * 3,
                        width=base_image.get("width"),
                        height=base_image.get("height"),
                        page_number=page_num,
                    ))
                except Exception:
                    document.images.append(ImageElement(
                        path=f"page_{page_num}_img_{img_index}.png",
                        is_corrupted=True,
                        page_number=page_num,
                    ))

            for link in page.get_links():
                document.links.append(Link(
                    url=link.get("uri", ""),
                    text=link.get("text", ""),
                    page_number=page_num,
                    is_internal=link.get("kind") == fitz.LINK_GOTO,
                ))

        page_count = len(doc)
        document.text = "\n".join(full_text)
        doc.close()
        is_scanned = page_count > 0 and len(document.text.strip()) == 0
        document.raw_metadata["is_scanned"] = is_scanned
        if is_scanned:
            document.errors.append("Document scanné — OCR nécessaire")
        document.statistics = DocumentStatistics(
            page_count=page_count,
            total_words=len(document.text.split()),
            total_images=len(document.images),
            total_tables=0,
            total_code_blocks=0,
            total_math_formulas=0,
            total_links=len(document.links),
            total_chapters=0,
            ocr_required=is_scanned,
            language=None,
        )
        return document

    def extract_text(self, file_path: str) -> str:
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text("text") for page in doc)
        doc.close()
        return text

    def extract_images(self, file_path: str) -> list[dict]:
        doc = fitz.open(file_path)
        images = []
        for page_num, page in enumerate(doc, start=1):
            for img in page.get_images(full=True):
                xref = img[0]
                base = doc.extract_image(xref)
                images.append({
                    "page": page_num,
                    "ext": base["ext"],
                    "width": base.get("width"),
                    "height": base.get("height"),
                    "size": len(base.get("image", b"")),
                })
        doc.close()
        return images

    def extract_metadata(self, file_path: str) -> dict:
        doc = fitz.open(file_path)
        meta = dict(doc.metadata or {})
        meta["page_count"] = len(doc)
        doc.close()
        return meta


register_extractor(PyMuPDFExtractor())
