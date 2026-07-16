from __future__ import annotations

from document_engine.models import Document, Chapter
from document_engine.core.registry import Builder, register_builder


class TipTapBuilder(Builder):
    format = "tiptap"

    def build(self, document: Document) -> dict:
        doc = {
            "type": "doc",
            "content": [],
        }

        if document.title:
            doc["content"].append({
                "type": "heading",
                "attrs": {"level": 1},
                "content": [{"type": "text", "text": document.title}],
            })

        for chapter in document.chapters:
            self._build_chapter(doc["content"], chapter)

        return {
            "tiptap": doc,
            "format": "tiptap",
            "node_count": len(doc["content"]),
            "chapters_built": len(document.chapters),
        }

    def _build_chapter(self, target: list, chapter: Chapter):
        target.append({
            "type": "heading",
            "attrs": {"level": min(chapter.level + 1, 6)},
            "content": [{"type": "text", "text": chapter.title}],
        })

        for para in chapter.content.split("\n"):
            stripped = para.strip()
            if not stripped:
                continue
            target.append({
                "type": "paragraph",
                "content": [{"type": "text", "text": stripped}],
            })

        for img in chapter.images:
            target.append({
                "type": "image",
                "attrs": {
                    "src": img.path,
                    "alt": img.alt_text or "",
                },
            })

        for code in chapter.code_blocks:
            target.append({
                "type": "codeBlock",
                "attrs": {"language": code.language} if code.language else {},
                "content": [{"type": "text", "text": code.content}],
            })

        for table in chapter.tables:
            target.append(self._build_table(table))

        for sub in chapter.sub_chapters:
            self._build_chapter(target, sub)

    def _build_table(self, table) -> dict:
        tip_table = {
            "type": "table",
            "content": [],
        }
        if table.headers:
            row = {"type": "tableRow", "content": []}
            for h in table.headers:
                row["content"].append({"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": h}]}]})
            tip_table["content"].append(row)
        for row_data in table.rows:
            row = {"type": "tableRow", "content": []}
            for cell in row_data:
                row["content"].append({"type": "tableCell", "content": [{"type": "paragraph", "content": [{"type": "text", "text": cell}]}]})
            tip_table["content"].append(row)
        return tip_table


register_builder(TipTapBuilder())
