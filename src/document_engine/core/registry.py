from __future__ import annotations
from typing import Optional

from document_engine.models import Document


class Extractor:
    format: str = ""

    def supports(self, file_path: str) -> bool:
        return file_path.lower().endswith(f".{self.format}")

    def extract(self, file_path: str) -> Document:
        raise NotImplementedError

    def extract_metadata(self, file_path: str) -> dict:
        raise NotImplementedError

    def extract_text(self, file_path: str) -> str:
        raise NotImplementedError

    def extract_images(self, file_path: str) -> list[dict]:
        raise NotImplementedError

    def extract_tables(self, file_path: str) -> list[dict]:
        raise NotImplementedError


class Analyzer:
    name: str = ""

    def analyze(self, document: Document) -> dict:
        raise NotImplementedError


class Builder:
    format: str = ""

    def build(self, document: Document) -> dict:
        raise NotImplementedError


_extractors: dict[str, Extractor] = {}
_analyzers: dict[str, Analyzer] = {}
_builders: dict[str, Builder] = {}


def register_extractor(extractor: Extractor):
    _extractors[extractor.format] = extractor


def register_analyzer(analyzer: Analyzer):
    _analyzers[analyzer.name] = analyzer


def register_builder(builder: Builder):
    _builders[builder.format] = builder


def get_extractor(file_path: str) -> Optional[Extractor]:
    for ext in _extractors.values():
        if ext.supports(file_path):
            return ext
    return None


def get_analyzer(name: str) -> Optional[Analyzer]:
    return _analyzers.get(name)


def get_builder(format: str) -> Optional[Builder]:
    return _builders.get(format)


def list_extractors() -> list[str]:
    return list(_extractors.keys())


def list_analyzers() -> list[str]:
    return list(_analyzers.keys())


def list_builders() -> list[str]:
    return list(_builders.keys())
