from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ElementType(str, Enum):
    TEXT = "text"
    HEADING = "heading"
    IMAGE = "image"
    TABLE = "table"
    CODE_BLOCK = "code"
    MATH_FORMULA = "math"
    LIST = "list"
    LINK = "link"


@dataclass
class Paragraph:
    text: str = ""
    style: Optional[str] = None
    page_number: Optional[int] = None


@dataclass
class Section:
    title: str = ""
    level: int = 1
    content: str = ""
    word_count: int = 0


@dataclass
class ImageElement:
    path: str
    alt_text: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    format: str = "png"
    size_bytes: int = 0
    page_number: Optional[int] = None
    is_duplicate: bool = False
    is_corrupted: bool = False


@dataclass
class TableElement:
    headers: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    page_number: Optional[int] = None
    caption: Optional[str] = None


@dataclass
class CodeBlock:
    language: Optional[str] = None
    content: str = ""
    page_number: Optional[int] = None


@dataclass
class Link:
    url: str
    text: Optional[str] = None
    page_number: Optional[int] = None
    is_internal: bool = False


@dataclass
class MathFormula:
    latex: str = ""
    page_number: Optional[int] = None


@dataclass
class Chapter:
    title: str = ""
    level: int = 1
    page_start: int = 0
    page_end: int = 0
    content: str = ""
    images: list[ImageElement] = field(default_factory=list)
    tables: list[TableElement] = field(default_factory=list)
    code_blocks: list[CodeBlock] = field(default_factory=list)
    formulas: list[MathFormula] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)
    sub_chapters: list[Chapter] = field(default_factory=list)
    word_count: int = 0
    confidence: float = 1.0


@dataclass
class DocumentStatistics:
    page_count: int = 0
    total_words: int = 0
    total_images: int = 0
    total_tables: int = 0
    total_code_blocks: int = 0
    total_math_formulas: int = 0
    total_links: int = 0
    total_chapters: int = 0
    duplicate_images: int = 0
    corrupted_images: int = 0
    has_toc: bool = False
    language: Optional[str] = None
    ocr_required: bool = False
    extraction_time_ms: float = 0.0


@dataclass
class Document:
    title: str = ""
    file_path: Optional[str] = None
    file_format: str = ""
    file_size_bytes: int = 0
    text: str = ""
    images: list[ImageElement] = field(default_factory=list)
    tables: list[TableElement] = field(default_factory=list)
    code_blocks: list[CodeBlock] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)
    formulas: list[MathFormula] = field(default_factory=list)
    chapters: list[Chapter] = field(default_factory=list)
    statistics: Optional[DocumentStatistics] = None
    language: Optional[str] = None
    raw_metadata: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def flat_chapters(self) -> list[Chapter]:
        result: list[Chapter] = []
        def walk(ch: Chapter):
            result.append(ch)
            for sub in ch.sub_chapters:
                walk(sub)
        for ch in self.chapters:
            walk(ch)
        return result
