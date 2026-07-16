from __future__ import annotations

import re
from typing import Optional

from document_engine.models import Document, Chapter
from document_engine.core.registry import Analyzer, register_analyzer


CHAPTER_PATTERNS = [
    re.compile(r"^(chapitre|ch|chapter|chap\.?)\s*[0-9IVXL]+[\.:]?\s*.+", re.IGNORECASE),
    re.compile(r"^(partie|part|part\.?|partie\s*[0-9IVXL]+)[\.:]?\s*.+", re.IGNORECASE),
    re.compile(r"^(section|sec\.?)\s*[0-9]+[\.:]?\s*.+", re.IGNORECASE),
    re.compile(r"^(module|module\s*[0-9]+)[\.:]?\s*.+", re.IGNORECASE),
    re.compile(r"^(leçon|lecon|lesson|leçon\s*[0-9]+)[\.:]?\s*.+", re.IGNORECASE),
    re.compile(r"^(unité|unite|unité\s*[0-9]+)[\.:]?\s*.+", re.IGNORECASE),
    re.compile(r"^(titre|title|titre\s*[0-9IVXL]+)[\.:]?\s*.+", re.IGNORECASE),
]


class ChapterAnalyzer(Analyzer):
    name = "chapters"

    def analyze(self, document: Document) -> dict:
        lines = document.text.split("\n")
        chapters: list[Chapter] = []
        current: Optional[Chapter] = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue

            match, level = self._detect_chapter(stripped)
            if match:
                if current:
                    self._finalize_chapter(current, lines, i)
                    chapters.append(current)

                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                current = Chapter(
                    title=stripped,
                    level=level,
                    page_start=i,
                    content=next_line,
                )
            elif current:
                current.content += stripped + "\n"

        if current:
            self._finalize_chapter(current, lines, len(lines))
            chapters.append(current)

        if not chapters:
            chapters = [Chapter(title=document.title or "Document", level=1, content=document.text[:500])]

        return {"chapters": chapters, "count": len(chapters)}

    def _detect_chapter(self, line: str) -> tuple[bool, int]:
        for pattern in CHAPTER_PATTERNS:
            match = pattern.match(line)
            if match:
                level = 1
                prefix = match.group(1).lower()
                if prefix.startswith(("section", "sec")):
                    level = 2
                elif prefix.startswith(("sous", "sub")):
                    level = 3
                elif prefix.startswith(("part", "partie")):
                    level = 0
                return True, level
        return False, 1

    def _finalize_chapter(self, chapter: Chapter, lines: list[str], end: int):
        chapter.word_count = len(chapter.content.split())
        for img in self._find_images_in_range(lines, chapter.page_start, end):
            chapter.images.append(img)

    def _find_images_in_range(self, lines: list[str], start: int, end: int) -> list:
        return []


register_analyzer(ChapterAnalyzer())
