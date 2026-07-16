from document_engine.analyzers.chapters import ChapterAnalyzer
from document_engine.analyzers.language import LanguageAnalyzer
from document_engine.analyzers.headings import HeadingAnalyzer
from document_engine.analyzers.code_blocks import CodeBlockAnalyzer
from document_engine.analyzers.math import MathAnalyzer
from document_engine.analyzers.references import ReferenceAnalyzer
from document_engine.analyzers.statistics import StatisticsAnalyzer
from document_engine.tests.conftest import make_sample_document


class TestAnalyzers:
    def test_chapter_detection(self):
        doc = make_sample_document()
        analyzer = ChapterAnalyzer()
        result = analyzer.analyze(doc)
        assert result["count"] >= 1

    def test_language_detection(self):
        doc = make_sample_document()
        doc.text = "Le langage Python est utilisé pour la programmation. Les variables sont des conteneurs."
        analyzer = LanguageAnalyzer()
        result = analyzer.analyze(doc)
        assert result["language"] == "fr"

    def test_language_english(self):
        doc = make_sample_document()
        doc.text = "Python is a programming language used for web development and data science."
        analyzer = LanguageAnalyzer()
        result = analyzer.analyze(doc)
        assert result["language"] == "en"

    def test_heading_markdown(self):
        doc = make_sample_document()
        doc.text = "# Title\n\n## Section 1\n\nContent here.\n\n### Sub-section\n\nMore content."
        analyzer = HeadingAnalyzer()
        result = analyzer.analyze(doc)
        assert result["count"] == 3

    def test_code_block_detection(self):
        doc = make_sample_document()
        doc.text = "Some text\n\n```python\ndef hello():\n    print('hi')\n```\n\nMore text"
        analyzer = CodeBlockAnalyzer()
        result = analyzer.analyze(doc)
        assert result["count"] >= 1
        assert any(b["language"] == "python" for b in result["code_blocks"])

    def test_math_detection(self):
        doc = make_sample_document()
        doc.text = "The formula $$E = mc^2$$ is famous. Also $a^2 + b^2 = c^2$."
        analyzer = MathAnalyzer()
        result = analyzer.analyze(doc)
        assert result["count"] >= 2

    def test_reference_detection(self):
        doc = make_sample_document()
        doc.text = "Visit https://example.com or contact test@email.com"
        analyzer = ReferenceAnalyzer()
        result = analyzer.analyze(doc)
        assert result["counts"]["urls"] >= 1
        assert result["counts"]["emails"] >= 1

    def test_statistics(self):
        doc = make_sample_document()
        analyzer = StatisticsAnalyzer()
        result = analyzer.analyze(doc)
        assert result["total_chapters"] == 3
        assert result["total_images"] == 1
