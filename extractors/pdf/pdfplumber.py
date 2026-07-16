from __future__ import annotations

import pdfplumber

from document_engine.models import TableElement
from document_engine.core.registry import Extractor, register_extractor


class PDFPlumberExtractor(Extractor):
    format = "pdf"

    def extract(self, file_path: str) -> dict:
        tables = self.extract_tables(file_path)
        return {"tables": tables}

    def extract_tables(self, file_path: str) -> list[dict]:
        results = []
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                page_tables = page.extract_tables()
                for table_data in page_tables or []:
                    if not table_data:
                        continue
                    headers = table_data[0] if table_data else []
                    rows = table_data[1:] if len(table_data) > 1 else []
                    results.append(TableElement(
                        headers=[str(h or "") for h in headers],
                        rows=[[str(c or "") for c in row] for row in rows],
                        page_number=page_num,
                    ))
        return [t.__dict__ for t in results]


register_extractor(PDFPlumberExtractor())
