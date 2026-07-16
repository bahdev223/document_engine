from __future__ import annotations

import fitz

from document_engine.models import Link


class PDFLinkExtractor:
    def extract(self, file_path: str) -> list[Link]:
        doc = fitz.open(file_path)
        links = []
        for page_num, page in enumerate(doc, start=1):
            for link in page.get_links():
                links.append(Link(
                    url=link.get("uri", ""),
                    text=link.get("text", ""),
                    page_number=page_num,
                    is_internal=link.get("kind") == fitz.LINK_GOTO,
                ))
        doc.close()
        return links
