from __future__ import annotations

from typing import Optional

import fitz


class TOCEntry:
    def __init__(self, title: str, level: int, page: int):
        self.title = title
        self.level = level
        self.page = page


class PDFTOCExtractor:
    def extract(self, file_path: str) -> list[TOCEntry]:
        doc = fitz.open(file_path)
        toc = doc.get_toc()
        doc.close()
        return [
            TOCEntry(title=entry[1], level=entry[0], page=entry[2])
            for entry in toc
        ]

    def has_toc(self, file_path: str) -> bool:
        doc = fitz.open(file_path)
        has = len(doc.get_toc()) > 0
        doc.close()
        return has
