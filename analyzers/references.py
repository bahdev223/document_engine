from __future__ import annotations

import re

from document_engine.core.registry import Analyzer, register_analyzer


URL_PATTERN = re.compile(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:/[-\w$.+!*'(),;:@&=?~#%]*)?", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
DOI_PATTERN = re.compile(r"10\.\d{4,}/[-._;()/:A-Za-z0-9]+")
ISBN_PATTERN = re.compile(r"(?:ISBN[-]?(?:1[03])?[ ]?(:)?[ ]?)?(?:97[89][ ]?\d{1,5}[ ]?\d{1,7}[ ]?\d{1,6}[ ]?\d)", re.IGNORECASE)


class ReferenceAnalyzer(Analyzer):
    name = "references"

    def analyze(self, document: dict | object) -> dict:
        text = document.text if hasattr(document, "text") else document.get("text", "")
        urls = list(set(URL_PATTERN.findall(text)))
        emails = list(set(EMAIL_PATTERN.findall(text)))
        dois = list(set(DOI_PATTERN.findall(text)))
        isbns = [m.group(0) for m in ISBN_PATTERN.finditer(text)]
        reference_lines = self._find_reference_section(text)

        return {
            "references": {
                "urls": urls,
                "emails": emails,
                "dois": dois,
                "isbns": list(set(isbns)),
            },
            "counts": {
                "urls": len(urls),
                "emails": len(emails),
                "dois": len(dois),
                "isbns": len(set(isbns)),
            },
            "has_reference_section": bool(reference_lines),
            "reference_lines_count": len(reference_lines),
        }

    def _find_reference_section(self, text: str) -> list[str]:
        lines = text.split("\n")
        ref_section = False
        ref_lines = []
        for line in lines:
            stripped = line.strip().lower()
            if stripped in ("references", "bibliography", "références", "bibliographie", "works cited"):
                ref_section = True
                continue
            if ref_section:
                if stripped and not stripped.startswith(("chapter", "appendix", "annex")):
                    ref_lines.append(line)
                else:
                    break
        return ref_lines


register_analyzer(ReferenceAnalyzer())
