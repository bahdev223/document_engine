from __future__ import annotations

from pathlib import Path

import fitz

from document_engine.models import ImageElement
from document_engine.extractors.pdf.pymupdf import PyMuPDFExtractor


class PDFImageExtractor(PyMuPDFExtractor):
    """Specialized image extraction with duplicate detection."""

    def extract_images(self, file_path: str) -> list[dict]:
        doc = fitz.open(file_path)
        seen_hashes: set[int] = set()
        images = []
        for page_num, page in enumerate(doc, start=1):
            for img in page.get_images(full=True):
                xref = img[0]
                base = doc.extract_image(xref)
                img_bytes = base.get("image", b"")
                img_hash = hash(img_bytes[:1024])
                is_dup = img_hash in seen_hashes
                seen_hashes.add(img_hash)
                images.append(ImageElement(
                    path=f"page_{page_num}_img_{xref}.{base['ext']}",
                    format=base["ext"],
                    size_bytes=len(img_bytes),
                    width=base.get("width"),
                    height=base.get("height"),
                    page_number=page_num,
                    is_duplicate=is_dup,
                ))
        doc.close()
        return images
