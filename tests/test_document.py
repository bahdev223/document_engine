from document_engine.models import Document, Chapter, ImageElement, TableElement, CodeBlock


class TestDocument:
    def test_create_document(self):
        doc = Document(title="Test", file_format="pdf")
        assert doc.title == "Test"
        assert doc.file_format == "pdf"
        assert doc.errors == []

    def test_flat_chapters(self):
        doc = Document(title="Test")
        sub = Chapter(title="Sous-chapitre", level=2)
        ch = Chapter(title="Chapitre 1", level=1, sub_chapters=[sub])
        doc.chapters.append(ch)
        flat = doc.flat_chapters()
        assert len(flat) == 2
        assert flat[0].title == "Chapitre 1"
        assert flat[1].title == "Sous-chapitre"

    def test_add_images(self):
        doc = Document()
        doc.images.append(ImageElement(path="test.png", format="png", size_bytes=1024))
        assert len(doc.images) == 1

    def test_add_tables(self):
        doc = Document()
        doc.tables.append(TableElement(headers=["A"], rows=[["1"]]))
        assert len(doc.tables) == 1

    def test_add_code_blocks(self):
        doc = Document()
        doc.code_blocks.append(CodeBlock(language="python", content="print('hello')"))
        assert len(doc.code_blocks) == 1
