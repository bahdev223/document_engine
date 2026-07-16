from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from document_engine.models import Document, DocumentStatistics
from document_engine.core.result import PipelineResult, StepResult
from document_engine.core.registry import get_extractor
from document_engine.analyzers.chapters import ChapterAnalyzer
from document_engine.analyzers.headings import HeadingAnalyzer
from document_engine.analyzers.language import LanguageAnalyzer
from document_engine.analyzers.code_blocks import CodeBlockAnalyzer
from document_engine.analyzers.math import MathAnalyzer
from document_engine.analyzers.references import ReferenceAnalyzer
from document_engine.analyzers.statistics import StatisticsAnalyzer
from document_engine.builders.tiptap import TipTapBuilder


class Pipeline:
    def __init__(self):
        self._analyzers = [
            ChapterAnalyzer(),
            HeadingAnalyzer(),
            LanguageAnalyzer(),
            CodeBlockAnalyzer(),
            MathAnalyzer(),
            ReferenceAnalyzer(),
            StatisticsAnalyzer(),
        ]
        self._builders = {
            "tiptap": TipTapBuilder(),
        }
        self._ai_reviewer = None

    def set_ai_reviewer(self, reviewer):
        self._ai_reviewer = reviewer

    def import_document(
        self,
        file_path: str | Path,
        run_analyzers: bool = True,
        run_builders: bool = True,
        run_ai_review: bool = False,
    ) -> PipelineResult:
        file_path = str(file_path)
        steps: list[StepResult] = []
        t_start = time.perf_counter()

        metadata_step = self._run_step("metadata", self._extract_metadata, file_path)
        steps.append(metadata_step)

        extractor = get_extractor(file_path)
        if not extractor:
            return PipelineResult(
                document=Document(file_path=file_path, errors=[f"No extractor for {file_path}"]),
                steps=steps,
                success=False,
            )

        extract_step = self._run_step("extraction", extractor.extract, file_path)
        steps.append(extract_step)
        document = extract_step.details.get("result")
        if not document:
            return PipelineResult(document=Document(file_path=file_path, errors=["Extraction failed"]), steps=steps, success=False)

        if run_analyzers:
            for analyzer in self._analyzers:
                a_step = self._run_step(f"analyzer:{analyzer.name}", analyzer.analyze, document)
                steps.append(a_step)
                if a_step.details:
                    self._merge_analysis(document, a_step.name, a_step.details)

        if run_builders:
            for fmt, builder in self._builders.items():
                b_step = self._run_step(f"builder:{fmt}", builder.build, document)
                steps.append(b_step)

        if run_ai_review and self._ai_reviewer:
            ai_step = self._run_step("ai:review", self._ai_reviewer.review, document)
            steps.append(ai_step)

        if not document.statistics:
            self._compute_statistics(document)

        total = (time.perf_counter() - t_start) * 1000
        return PipelineResult(document=document, steps=steps, total_duration_ms=total, success=not document.errors)

    def _run_step(self, name: str, fn, *args) -> StepResult:
        t0 = time.perf_counter()
        try:
            result = fn(*args)
            elapsed = (time.perf_counter() - t0) * 1000
            details = {"result": result} if not isinstance(result, dict) else result
            return StepResult(name=name, success=True, duration_ms=elapsed, details=details)
        except Exception as e:
            elapsed = (time.perf_counter() - t0) * 1000
            return StepResult(name=name, success=False, duration_ms=elapsed, error=str(e))

    def _extract_metadata(self, file_path: str) -> dict:
        p = Path(file_path)
        return {
            "file_name": p.name,
            "file_size_bytes": p.stat().st_size,
            "file_format": p.suffix.lstrip(".").lower(),
        }

    def _merge_analysis(self, document: Document, name: str, details: dict):
        if name == "analyzer:language" and "language" in details:
            document.language = details["language"]

    def _compute_statistics(self, document: Document):
        chapters = document.flat_chapters()
        is_scanned = document.raw_metadata.get("is_scanned", False)
        document.statistics = DocumentStatistics(
            page_count=document.raw_metadata.get("page_count", 0),
            total_words=sum(c.word_count for c in chapters) or len(document.text.split()),
            total_images=len(document.images),
            total_tables=len(document.tables),
            total_code_blocks=len(document.code_blocks),
            total_math_formulas=len(document.formulas),
            total_links=len(document.links),
            total_chapters=len(chapters),
            has_toc=bool(document.chapters),
            language=document.language,
            ocr_required=is_scanned,
        )
