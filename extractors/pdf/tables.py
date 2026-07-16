from __future__ import annotations

import pdfplumber

from document_engine.models import TableElement


class PDFTableExtractor:
    def extract(self, file_path: str) -> list[TableElement]:
        results = []
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                for table_data in page.extract_tables() or []:
                    if not table_data:
                        continue
                    headers = table_data[0] if table_data else []
                    rows = table_data[1:] if len(table_data) > 1 else []
                    results.append(TableElement(
                        headers=[str(h or "") for h in headers],
                        rows=[[str(c or "") for c in row] for row in rows],
                        page_number=page_num,
                    ))
        return results
