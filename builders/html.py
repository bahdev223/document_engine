from __future__ import annotations

from html import escape

from document_engine.models import Document, Chapter
from document_engine.core.registry import Builder, register_builder


class HTMLBuilder(Builder):
    format = "html"

    def build(self, document: Document) -> dict:
        parts: list[str] = [
            "<!DOCTYPE html>",
            "<html><head>",
            f"<meta charset='utf-8'><title>{escape(document.title or 'Document')}</title>",
            "</head><body>",
        ]

        if document.title:
            parts.append(f"<h1>{escape(document.title)}</h1>")

        for chapter in document.chapters:
            self._build_chapter(parts, chapter)

        parts.append("</body></html>")

        return {
            "html": "\n".join(parts),
            "format": "html",
        }

    def _build_chapter(self, parts: list[str], chapter: Chapter):
        tag = f"h{min(chapter.level + 1, 6)}"
        parts.append(f"<{tag}>{escape(chapter.title)}</{tag}>")

        for para in chapter.content.split("\n"):
            stripped = para.strip()
            if stripped:
                parts.append(f"<p>{escape(stripped)}</p>")

        for code in chapter.code_blocks:
            lang_attr = f' class="language-{escape(code.language)}"' if code.language else ""
            parts.append(f"<pre{lang_attr}><code>{escape(code.content)}</code></pre>")

        for table in chapter.tables:
            parts.append("<table>")
            if table.headers:
                parts.append("<tr>" + "".join(f"<th>{escape(h)}</th>" for h in table.headers) + "</tr>")
            for row in table.rows:
                parts.append("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in row) + "</tr>")
            parts.append("</table>")

        for sub in chapter.sub_chapters:
            self._build_chapter(parts, sub)


register_builder(HTMLBuilder())
