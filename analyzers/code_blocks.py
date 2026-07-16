from __future__ import annotations

import re

from document_engine.core.registry import Analyzer, register_analyzer


CODE_PATTERNS = [
    (re.compile(r"```(\w*)\n(.*?)```", re.DOTALL), "fenced"),
    (re.compile(r"(?:^|\n)(?: {4}|\t)(.+)$", re.MULTILINE), "indented"),
    (re.compile(r"`([^`]+)`"), "inline"),
]

LANGUAGE_PATTERNS: dict[str, list[str]] = {
    "python": ["def ", "import ", "class ", "self", "print(", "return ", "if __name__"],
    "javascript": ["function ", "const ", "let ", "var ", "=>", "console.log"],
    "typescript": [": string", ": number", ": boolean", "interface ", "type "],
    "java": ["public class", "private ", "static ", "void main", "System.out"],
    "html": ["<div", "<p>", "<span", "<head", "<body", "<!DOCTYPE"],
    "css": ["{", "margin:", "padding:", "color:", "font-size"],
    "bash": ["#!/bin", "echo ", "export ", "sudo ", "apt-get"],
    "sql": ["SELECT ", "FROM ", "WHERE ", "INSERT INTO", "CREATE TABLE"],
    "json": ['"name"', '"id"', '"type"', '"value"'],
}


class CodeBlockAnalyzer(Analyzer):
    name = "code_blocks"

    def analyze(self, document: dict | object) -> dict:
        text = document.text if hasattr(document, "text") else document.get("text", "")
        blocks = []
        for pattern, style in CODE_PATTERNS:
            for match in pattern.finditer(text):
                content = match.group(2).strip() if style == "fenced" else match.group(1).strip()
                lang_tag = match.group(1).strip() if style == "fenced" else None
                lang = self._detect_language(content, lang_tag)
                blocks.append({
                    "language": lang,
                    "content": content[:200],
                    "style": style,
                    "length": len(content),
                })

        return {"code_blocks": blocks, "count": len(blocks)}

    def _detect_language(self, content: str, tag_hint: str | None = None) -> str | None:
        if tag_hint and tag_hint in LANGUAGE_PATTERNS:
            return tag_hint
        for lang, patterns in LANGUAGE_PATTERNS.items():
            for p in patterns:
                if p in content:
                    return lang
        return None


register_analyzer(CodeBlockAnalyzer())
