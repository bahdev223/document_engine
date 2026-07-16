from __future__ import annotations

from document_engine.models import Document, Chapter
from document_engine.core.registry import Builder, register_builder


class MarkdownBuilder(Builder):
    format = "markdown"

    def build(self, document: Document) -> dict:
        lines: list[str] = []

        if document.title:
            lines.append(f"# {document.title}\n")

        for chapter in document.chapters:
            self._build_chapter(lines, chapter)

        return {
            "markdown": "\n".join(lines),
            "format": "markdown",
        }

    def _build_chapter(self, lines: list[str], chapter: Chapter, depth: int = 0):
        prefix = "#" * min(depth + 2, 6)
        lines.append(f"{prefix} {chapter.title}\n")

        for para in chapter.content.split("\n"):
            stripped = para.strip()
            if stripped:
                lines.append(f"{stripped}\n")

        for code in chapter.code_blocks:
            lang = code.language or ""
            lines.append(f"```{lang}\n{code.content}\n```\n")

        for table in chapter.tables:
            if table.headers:
                lines.append("| " + " | ".join(table.headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(table.headers)) + " |")
                for row in table.rows:
                    lines.append("| " + " | ".join(row) + " |")
            lines.append("")

        for sub in chapter.sub_chapters:
            self._build_chapter(lines, sub, depth + 1)


register_builder(MarkdownBuilder())
