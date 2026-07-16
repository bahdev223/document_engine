# Document Intelligence Engine

Moteur universel de traitement documentaire. Extrait, analyse et transforme des documents (PDF, DOCX, PPTX, EPUB, HTML, Markdown) en données structurées.

```python
from document_engine import Engine

engine = Engine()
doc = engine.load("cours.pdf")

print(doc.statistics)
# → page_count=248, total_words=45200, total_images=38, total_tables=12

for chapter in doc.chapters:
    print(f"{chapter.title} — {chapter.word_count} mots / {len(chapter.images)} images")
```

## Architecture

```
Document
  ↓
Détection du format
  ↓
Extraction (PDF/Word/PPT/EPUB/HTML/MD)
  ↓
Analyse (chapitres, titres, code, formules, langue, stats)
  ↓
Export (JSON, Markdown, HTML)
  ↓
Review IA (optionnel)
  ↓
Document structuré
```

## Installation

```bash
pip install campus-doc-engine
```

Avec support IA :

```bash
pip install campus-doc-engine[ai]
```

## Utilisation

### Pipeline complète

```python
from document_engine import Pipeline

pipeline = Pipeline()
result = pipeline.import_document("cours.pdf")

doc = result.document
print(f"Titre: {doc.title}")
print(f"Pages: {doc.statistics.page_count}")
print(f"Chapitres: {len(doc.chapters)}")
```

### Extraction seule

```python
from document_engine.extractors.pdf import PyMuPDFExtractor

extractor = PyMuPDFExtractor()
doc = extractor.extract("cours.pdf")
print(f"Texte extrait: {len(doc.text)} caractères")
print(f"Images: {len(doc.images)}")
```

### Analyse

```python
from document_engine.analyzers import ChapterAnalyzer, LanguageAnalyzer

lang = LanguageAnalyzer().analyze(doc)
print(f"Langue: {lang['language']} (confiance: {lang['confidence']})")

chapters = ChapterAnalyzer().analyze(doc)
print(f"Chapitres détectés: {chapters['count']}")
```

### Export

```python
from document_engine.exporters import JSONExporter, MarkdownExporter, HTMLExporter

json_data = JSONExporter().build(doc)
markdown = MarkdownExporter().build(doc)
html = HTMLExporter().build(doc)
```

### CLI

```bash
# Analyse d'un document
doc-engine analyze cours.pdf

# Export structuré
doc-engine extract cours.pdf --format json --output cours.json

# Liste des extracteurs disponibles
doc-engine list
```

## Plugins

- `document-engine-tiptap` — export TipTap JSON pour éditeurs React
- `document-engine-ai` — review IA (DeepSeek, OpenAI)

## Formats supportés

| Format | Extracteur | Statut |
|--------|-----------|--------|
| PDF | PyMuPDF + pdfplumber | ✅ |
| DOCX | python-docx | ✅ |
| PPTX | python-pptx | ✅ |
| EPUB | (planifié) | 🚧 |
| HTML | lxml | ✅ |
| Markdown | markdown-it-py | ✅ |

## Licence

MIT
