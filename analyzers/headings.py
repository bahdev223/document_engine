from __future__ import annotations

import re

from document_engine.core.registry import Analyzer, register_analyzer


class HeadingAnalyzer(Analyzer):
    name = "headings"

    H1 = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    PDF_HEADING = re.compile(r"^([A-Z][A-Z\s\-]{2,}|[A-Z][a-zàâçéèêëîïôûùüÿæœ]+:)$", re.MULTILINE)

    def analyze(self, document: dict | object) -> dict:
        text = document.text if hasattr(document, "text") else document.get("text", "")
        headings = []

        for match in self.H1.finditer(text):
            level = len(match.group(1))
            headings.append({"level": level, "text": match.group(2).strip(), "type": "markdown"})

        for match in self.PDF_HEADING.finditer(text):
            heading_text = match.group(0).strip()
            if not any(h["text"] == heading_text for h in headings):
                headings.append({"level": 1, "text": heading_text.rstrip(":"), "type": "pdf"})

        return {"headings": headings, "count": len(headings)}


register_analyzer(HeadingAnalyzer())
