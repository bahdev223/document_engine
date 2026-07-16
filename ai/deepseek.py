from __future__ import annotations

from typing import Optional

import httpx

from document_engine.models import Document


class DeepSeekReviewer:
    def __init__(self, api_key: str, model: str = "deepseek-chat", base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self._client: Optional[httpx.AsyncClient] = None

    async def review(self, document: Document) -> dict:
        prompt = self._build_review_prompt(document)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "Tu es un expert en validation de contenu pédagogique. Analyse la structure et le contenu du document reçu."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                },
                timeout=60.0,
            )
            resp.raise_for_status()
            data = resp.json()
            review_text = data["choices"][0]["message"]["content"]

        return self._parse_review(review_text)

    def _build_review_prompt(self, doc: Document) -> str:
        chapters_summary = "\n".join(
            f"- Chapitre {i+1}: {ch.title} ({ch.word_count} mots, {len(ch.images)} images, {len(ch.tables)} tableaux)"
            for i, ch in enumerate(doc.chapters)
        )
        return f"""Analyse ce document pédagogique :

Titre: {doc.title}
Langue: {doc.language}
Pages: {doc.statistics.page_count if doc.statistics else '?'}
Mots: {doc.statistics.total_words if doc.statistics else '?'}

Chapitres détectés:
{chapters_summary}

Vérifie:
1. La structure des chapitres est-elle cohérente ?
2. Y a-t-il des titres manquants ou mal positionnés ?
3. Des parties qui devraient être des sous-chapitres ?
4. La progression pédagogique est-elle logique ?

Format de réponse: JSON avec les champs issues[], suggestions[], score (0-100)."""

    def _parse_review(self, text: str) -> dict:
        return {"review": text, "reviewed_by": "deepseek"}


class DeepSeekReviewerSync:
    def __init__(self, api_key: str, model: str = "deepseek-chat", base_url: str = "https://api.deepseek.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    def review(self, document: Document) -> dict:
        import httpx as httpx_sync
        prompt = self._build_review_prompt(document)
        with httpx_sync.Client() as client:
            resp = client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "Tu es un expert en validation de contenu pédagogique."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                },
                timeout=60.0,
            )
            resp.raise_for_status()
            data = resp.json()
            review_text = data["choices"][0]["message"]["content"]
        return self._parse_review(review_text)

    def _build_review_prompt(self, doc: Document) -> str:
        chapters_summary = "\n".join(
            f"- Chapitre {i+1}: {ch.title} ({ch.word_count} mots, {len(ch.images)} images, {len(ch.tables)} tableaux)"
            for i, ch in enumerate(doc.chapters)
        )
        return f"""Analyse ce document pédagogique :

Titre: {doc.title}
Langue: {doc.language}
Pages: {doc.statistics.page_count if doc.statistics else '?'}
Mots: {doc.statistics.total_words if doc.statistics else '?'}

Chapitres détectés:
{chapters_summary}

Vérifie:
1. La structure des chapitres est-elle cohérente ?
2. Y a-t-il des titres manquants ou mal positionnés ?
3. Des parties qui devraient être des sous-chapitres ?
4. La progression pédagogique est-elle logique ?

Format de réponse: JSON avec les champs issues[], suggestions[], score (0-100)."""

    def _parse_review(self, text: str) -> dict:
        return {"review": text, "reviewed_by": "deepseek"}
