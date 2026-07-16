from __future__ import annotations

from pathlib import Path

from document_engine.models import Document
from document_engine.ai.deepseek import DeepSeekReviewerSync


class AIOrchestrator:
    def __init__(self, deepseek_api_key: Optional[str] = None, openai_api_key: Optional[str] = None):
        self.reviewers = {}
        if deepseek_api_key:
            self.reviewers["deepseek"] = DeepSeekReviewerSync(api_key=deepseek_api_key)
        if openai_api_key:
            from document_engine.ai.openai import OpenAIReviewer
            self.reviewers["openai"] = OpenAIReviewer(api_key=openai_api_key)

    def review(self, document: Document, preferred: str = "deepseek") -> dict:
        if preferred in self.reviewers:
            return self.reviewers[preferred].review(document)
        if self.reviewers:
            name = next(iter(self.reviewers))
            return self.reviewers[name].review(document)
        return {"review": "No AI reviewer configured", "reviewed_by": None}
