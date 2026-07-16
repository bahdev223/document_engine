from document_engine.builders.tiptap import TipTapBuilder
from document_engine.builders.markdown import MarkdownBuilder
from document_engine.builders.html import HTMLBuilder
from document_engine.builders.json import JSONBuilder
from document_engine.tests.conftest import make_sample_document


class TestBuilders:
    def test_tiptap_builder(self):
        doc = make_sample_document()
        builder = TipTapBuilder()
        result = builder.build(doc)
        assert result["format"] == "tiptap"
        assert "tiptap" in result
        assert result["tiptap"]["type"] == "doc"

    def test_markdown_builder(self):
        doc = make_sample_document()
        builder = MarkdownBuilder()
        result = builder.build(doc)
        assert result["format"] == "markdown"
        assert "# Introduction à Python" in result["markdown"]

    def test_html_builder(self):
        doc = make_sample_document()
        builder = HTMLBuilder()
        result = builder.build(doc)
        assert result["format"] == "html"
        assert "<h1>" in result["html"]

    def test_json_builder(self):
        doc = make_sample_document()
        builder = JSONBuilder()
        result = builder.build(doc)
        assert result["format"] == "json"
        assert result["json"]["document"]["title"] == "Introduction à Python"
