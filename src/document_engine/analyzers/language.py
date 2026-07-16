from __future__ import annotations

import re
from typing import Optional

from document_engine.core.registry import Analyzer, register_analyzer


LANG_PATTERNS: dict[str, list[re.Pattern]] = {
    "fr": [re.compile(r"\b(le|la|les|un|une|des|du|de|d'|ce|cet|cette|ces|mon|ton|son|qui|que|dont|où|sur|dans|avec|pour|par|est|sont|ont|fait|être|avoir|faire|nous|vous|ils|elles)\b", re.IGNORECASE)],
    "en": [re.compile(r"\b(the|a|an|is|are|was|were|have|has|do|does|did|will|would|shall|should|can|could|may|might|this|that|these|those|with|from|into|upon|about)\b", re.IGNORECASE)],
}


class LanguageAnalyzer(Analyzer):
    name = "language"

    def analyze(self, document: dict | object) -> dict:
        text = document.text if hasattr(document, "text") else document.get("text", "")
        if not text.strip():
            return {"language": None, "confidence": 0.0}

        words = text.split()
        word_count = len(words)
        if word_count < 10:
            return {"language": None, "confidence": 0.0}

        scores: dict[str, int] = {}
        for lang, patterns in LANG_PATTERNS.items():
            count = 0
            for pattern in patterns:
                count += len(pattern.findall(text))
            scores[lang] = count

        if not scores:
            return {"language": None, "confidence": 0.0}

        best_lang = max(scores, key=scores.get)
        total_matches = sum(scores.values())
        confidence = scores[best_lang] / max(total_matches, 1)

        return {
            "language": best_lang,
            "confidence": round(confidence, 2),
            "scores": scores,
        }


register_analyzer(LanguageAnalyzer())
