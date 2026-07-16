from __future__ import annotations

import re

from document_engine.core.registry import Analyzer, register_analyzer


MATH_PATTERNS = [
    re.compile(r"\$\$(.*?)\$\$", re.DOTALL),
    re.compile(r"\$(.*?)\$"),
    re.compile(r"\\\[(.*?)\\\]", re.DOTALL),
    re.compile(r"\\\((.*?)\\\)"),
    re.compile(r"\\(?:frac|sum|int|alpha|beta|gamma|delta|theta|lambda|pi|infty|rightarrow|leftrightarrow|partial|nabla)", re.IGNORECASE),
]


class MathAnalyzer(Analyzer):
    name = "math"

    def analyze(self, document: dict | object) -> dict:
        text = document.text if hasattr(document, "text") else document.get("text", "")
        formulas = []
        for pattern in MATH_PATTERNS:
            for match in pattern.finditer(text):
                content = match.group(1) if match.lastindex else match.group(0)
                is_display = bool(match.group(0).startswith(("$$", "\\[")))
                formulas.append({
                    "latex": content[:150],
                    "display": is_display,
                    "confidence": 1.0 if not content.startswith("$") else 0.8,
                })

        return {"math_formulas": formulas, "count": len(formulas)}


register_analyzer(MathAnalyzer())
