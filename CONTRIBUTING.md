# Contributing

## Dev

```bash
pip install -e ".[dev]"
pytest
```

## Structure

- `models/` — objets métier (Document, Chapter, Image, etc.)
- `core/` — Pipeline, Registry
- `extractors/` — un sous-dossier par format
- `analyzers/` — un fichier par analyseur
- `exporters/` — un fichier par format d'export
- `plugins/` — plugins externes optionnels
- `cli/` — interface en ligne de commande

## Principes

1. Aucune dépendance framework (Django, FastAPI, etc.)
2. Chaque extracteur est indépendant et testable
3. Les analyseurs ne lisent que le `Document` (jamais le fichier source)
4. TipStay est un plugin optionnel
