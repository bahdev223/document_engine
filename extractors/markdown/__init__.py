from __future__ import annotations

from pathlib import Path

from markdown_it import MarkdownIt

from document_engine.models import Document, Link, CodeBlock
from document_engine.core.registry import Extractor, register_extractor


class MarkdownExtractor(Extractor):
    format = "md"

    def extract(self, file_path: str) -> Document:
        p = Path(file_path)
        raw = p.read_text(encoding="utf-8")
        md = MarkdownIt()
        tokens = md.parse(raw)

        document = Document(
            title=p.stem,
            file_path=file_path,
            file_format="markdown",
            file_size_bytes=p.stat().st_size,
            text=raw,
        )

        in_code_block = False
        code_content: list[str] = []
        code_lang: str | None = None

        for token in tokens:
            if token.type == "fence":
                document.code_blocks.append(CodeBlock(
                    language=token.info.strip() if token.info else None,
                    content=token.content,
                ))

            if token.type == "link_open":
                href = token.attrs.get("href", "") if token.attrs else ""
                document.links.append(Link(url=href))

        return document

    def extract_text(self, file_path: str) -> str:
        p = Path(file_path)
        return p.read_text(encoding="utf-8")


register_extractor(MarkdownExtractor())
