# Backward-compat re-exports — use document_engine.exporters directly
from document_engine.exporters import JSONExporter, MarkdownExporter, HTMLExporter

__all__ = ["JSONExporter", "MarkdownExporter", "HTMLExporter"]
