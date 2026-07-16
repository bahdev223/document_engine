from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional

from document_engine.models import Document, DocumentStatistics


@dataclass
class StepResult:
    name: str
    success: bool
    duration_ms: float = 0.0
    details: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    warnings: list[str] = field(default_factory=list)


@dataclass
class PipelineResult:
    document: Document
    steps: list[StepResult] = field(default_factory=list)
    total_duration_ms: float = 0.0
    success: bool = True

    @property
    def statistics(self) -> Optional[DocumentStatistics]:
        return self.document.statistics

    def step(self, name: str) -> Optional[StepResult]:
        for s in self.steps:
            if s.name == name:
                return s
        return None
