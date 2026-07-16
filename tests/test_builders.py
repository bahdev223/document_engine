from document_engine.exporters import JSONExporter, MarkdownExporter, HTMLExporter
from document_engine.tests.conftest import make_sample_document


class TestExporters:
    def test_markdown_exporter(self):
        doc = make_sample_document()
        exporter = MarkdownExporter()
        result = exporter.build(doc)
        assert result["format"] == "markdown"
        assert "# Introduction à Python" in result["markdown"]

    def test_html_exporter(self):
        doc = make_sample_document()
        exporter = HTMLExporter()
        result = exporter.build(doc)
        assert result["format"] == "html"
        assert "<h1>" in result["html"]

    def test_json_exporter(self):
        doc = make_sample_document()
        exporter = JSONExporter()
        result = exporter.build(doc)
        assert result["format"] == "json"
        assert result["json"]["document"]["title"] == "Introduction à Python"
