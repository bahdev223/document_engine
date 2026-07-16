from __future__ import annotations

import json
from pathlib import Path

from document_engine.models import Document, Chapter, ImageElement, TableElement, CodeBlock, DocumentStatistics


SAMPLE_PDF = Path(__file__).parent / "fixtures" / "sample.pdf"
SAMPLE_DOCX = Path(__file__).parent / "fixtures" / "sample.docx"


def make_sample_document() -> Document:
    return Document(
        title="Introduction à Python",
        file_path=str(SAMPLE_PDF) if SAMPLE_PDF.exists() else "",
        file_format="pdf",
        file_size_bytes=102400,
        text="""Introduction\nPython est un langage de programmation.\n\nChapitre 1 : Variables\nLes variables stockent des données.\n\nChapitre 2 : Fonctions\nLes fonctions sont des blocs réutilisables.""",
        chapters=[
            Chapter(title="Introduction", level=1, page_start=1, page_end=2, content="Python est un langage de programmation.", word_count=5),
            Chapter(title="Variables", level=1, page_start=3, page_end=5, content="Les variables stockent des données.", word_count=5),
            Chapter(title="Fonctions", level=1, page_start=6, page_end=8, content="Les fonctions sont des blocs réutilisables.", word_count=7),
        ],
        images=[ImageElement(path="img1.png", format="png", size_bytes=2048, page_number=1)],
        tables=[TableElement(headers=["Nom", "Type"], rows=[["age", "int"], ["nom", "str"]])],
        code_blocks=[CodeBlock(language="python", content="x = 1")],
        statistics=DocumentStatistics(
            page_count=8,
            total_words=17,
            total_images=1,
            total_tables=1,
            total_code_blocks=1,
            total_chapters=3,
        ),
    )
