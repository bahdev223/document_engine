from __future__ import annotations

from pathlib import Path

from lxml import etree

from document_engine.models import Document, Link
from document_engine.core.registry import Extractor, register_extractor


class HTMLExtractor(Extractor):
    format = "html"

    def extract(self, file_path: str) -> Document:
        p = Path(file_path)
        raw = p.read_text(encoding="utf-8")
        tree = etree.HTML(raw)

        document = Document(
            title=tree.findtext(".//title") or p.stem,
            file_path=file_path,
            file_format="html",
            file_size_bytes=p.stat().st_size,
        )

        for element in tree.iter("p", "h1", "h2", "h3", "h4", "h5", "h6", "li"):
            if element.text and element.text.strip():
                document.text += element.text.strip() + "\n"

        for a in tree.iter("a"):
            href = a.get("href", "")
            if href:
                document.links.append(Link(url=href, text=a.text))

        document.raw_metadata["encoding"] = tree.docinfo.encoding if hasattr(tree.docinfo, "encoding") else "utf-8"

        return document

    def extract_text(self, file_path: str) -> str:
        p = Path(file_path)
        raw = p.read_text(encoding="utf-8")
        tree = etree.HTML(raw)
        return "\n".join(
            element.text.strip()
            for element in tree.iter("p", "h1", "h2", "h3", "h4", "h5", "h6", "li")
            if element.text and element.text.strip()
        )


register_extractor(HTMLExtractor())
