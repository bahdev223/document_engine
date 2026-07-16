from docx import Document as DocxDocument

from document_engine.models import TableElement


class WordTableExtractor:
    def extract(self, file_path: str) -> list[TableElement]:
        docx = DocxDocument(file_path)
        tables = []
        for table in docx.tables:
            headers = [cell.text for cell in table.rows[0].cells] if table.rows else []
            rows = [[cell.text for cell in row.cells] for row in table.rows[1:]]
            tables.append(TableElement(headers=headers, rows=rows))
        return tables
