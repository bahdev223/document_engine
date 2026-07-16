from __future__ import annotations

from document_engine.models import Document, DocumentStatistics
from document_engine.core.registry import Analyzer, register_analyzer


class StatisticsAnalyzer(Analyzer):
    name = "statistics"

    def analyze(self, document: Document) -> dict:
        chapters = document.flat_chapters() if hasattr(document, "flat_chapters") else []
        all_words = document.text.split() if document.text else []
        total_words = sum(c.word_count for c in chapters) if chapters else len(all_words)

        stats = DocumentStatistics(
            page_count=document.raw_metadata.get("page_count", 0) if hasattr(document, "raw_metadata") else 0,
            total_words=total_words,
            total_images=len(document.images) if hasattr(document, "images") else 0,
            total_tables=len(document.tables) if hasattr(document, "tables") else 0,
            total_code_blocks=len(document.code_blocks) if hasattr(document, "code_blocks") else 0,
            total_math_formulas=len(document.formulas) if hasattr(document, "formulas") else 0,
            total_links=len(document.links) if hasattr(document, "links") else 0,
            total_chapters=len(chapters),
            duplicate_images=sum(1 for img in (document.images or []) if img.is_duplicate),
            corrupted_images=sum(1 for img in (document.images or []) if img.is_corrupted),
            has_toc=bool(chapters),
            language=document.language if hasattr(document, "language") else None,
        )

        return {
            "statistics": stats,
            "page_count": stats.page_count,
            "total_words": stats.total_words,
            "total_images": stats.total_images,
            "total_chapters": stats.total_chapters,
            "total_tables": stats.total_tables,
            "total_code_blocks": stats.total_code_blocks,
            "total_math_formulas": stats.total_math_formulas,
            "total_links": stats.total_links,
        }


register_analyzer(StatisticsAnalyzer())
