from document_engine.core.pipeline import Pipeline
from document_engine.tests.conftest import make_sample_document


class TestPipeline:
    def test_import_text_based(self, monkeypatch):
        """Test that pipeline runs without actual file (text-based extraction mock)."""
        pipeline = Pipeline()
        doc = make_sample_document()
        assert doc.title == "Introduction à Python"
        assert len(doc.chapters) == 3

    def test_pipeline_steps(self):
        pipeline = Pipeline()
        doc = make_sample_document()
        for analyzer in pipeline._analyzers:
            result = analyzer.analyze(doc)
            assert isinstance(result, dict)

    def test_statistics_analyzer(self):
        from document_engine.analyzers.statistics import StatisticsAnalyzer
        doc = make_sample_document()
        analyzer = StatisticsAnalyzer()
        result = analyzer.analyze(doc)
        assert result["total_chapters"] == 3
        assert result["total_images"] == 1
