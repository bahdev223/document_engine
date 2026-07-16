import os
from pathlib import Path

import pytest

from document_engine.core.registry import get_extractor, list_extractors


class TestExtractors:
    def test_extractors_registered(self):
        extractors = list_extractors()
        assert "pdf" in extractors
        assert "docx" in extractors
        assert "pptx" in extractors
        assert "epub" in extractors
        assert "html" in extractors
        assert "md" in extractors

    def test_get_extractor_pdf(self):
        ext = get_extractor("document.pdf")
        assert ext is not None
        assert ext.supports("document.pdf")

    def test_get_extractor_docx(self):
        ext = get_extractor("document.docx")
        assert ext is not None
        assert ext.supports("document.docx")

    def test_get_extractor_unknown(self):
        ext = get_extractor("document.xyz")
        assert ext is None

    def test_pymupdf_text_extraction(self):
        pdf_path = Path(__file__).parent / "fixtures" / "sample.pdf"
        if not pdf_path.exists():
            pytest.skip("sample.pdf not found")
        ext = get_extractor("sample.pdf")
        text = ext.extract_text(str(pdf_path))
        assert len(text) > 0
