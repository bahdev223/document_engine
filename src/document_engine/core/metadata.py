from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExtractionMetrics:
    duration_ms: float = 0.0
    items_found: int = 0
    duplicates: int = 0
    corrupted: int = 0
    total_size_bytes: int = 0
    confidence: float = 1.0
    method: str = ""


@dataclass
class DocumentMetadata:
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: list[str] = field(default_factory=list)
    creator: Optional[str] = None
    producer: Optional[str] = None
    page_count: int = 0
    file_size_bytes: int = 0
    file_format: str = ""
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    is_scanned: bool = False
    is_password_protected: bool = False
    pdf_version: Optional[str] = None
    has_embedded_fonts: bool = False
    has_forms: bool = False
    has_javascript: bool = False
    raw: dict = field(default_factory=dict)
