# Document Engine

Moteur universel de traitement documentaire. Extrait, analyse et transforme des documents (PDF, Word, PowerPoint, EPUB) en contenu structuré.

## Philosophie

L'IA n'est pas le moteur. L'IA est l'expert qui valide et ameliore.

```
Document -> Extraction -> Analyse -> Construction -> Validation IA -> Export
```

Chaque etape est un outil independant. L'IA intervient en dernier, sur un document deja structure.

## Installation

```bash
pip install -e .
```

Avec support IA :

```bash
pip install -e ".[ai]"
```

## Utilisation

```python
from document_engine import Pipeline

pipeline = Pipeline()
result = pipeline.import_document("cours.pdf")

print(result.document.statistics)
print(result.document.chapters)
print(result.document.images)
```

## Architecture

```
document_engine/
    core/           Pipeline, Document, Registry
    extractors/     PDF, Word, PowerPoint, EPUB, HTML, Markdown
    analyzers/      Chapitres, titres, langue, code, formules
    builders/       TipTap, Markdown, HTML, JSON
    ai/             DeepSeek, OpenAI (facultatif)
    cli/            Interface en ligne de commande
```

### Objet Document

Tous les outils lisent et ecrivent dans un seul objet :

```python
document.text           # Texte brut
document.images         # Images extraites
document.tables         # Tableaux detectes
document.chapters       # Chapitres structures
document.code_blocks    # Blocs de code
document.formulas       # Formules mathematiques
document.links          # Liens
document.statistics     # Statistiques du document
document.language       # Langue detectee
```

### Plugins

Chaque format est un plugin independant :

```python
from document_engine.core.registry import Extractor, register_extractor

class MonExtracteur(Extractor):
    format = "xyz"

    def extract(self, file_path: str) -> Document:
        ...

register_extractor(MonExtracteur())
```

## CLI

```bash
doc-engine analyze cours.pdf
doc-engine extract cours.pdf --format json
```

## License

MIT
