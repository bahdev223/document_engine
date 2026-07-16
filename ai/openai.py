from __future__ import annotations

from typing import Optional

from document_engine.models import Document


class OpenAIReviewer:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model

    def review(self, document: Document) -> dict:
        return {"review": "OpenAI review not yet implemented", "reviewed_by": "openai"}
