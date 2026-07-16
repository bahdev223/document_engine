from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from document_engine.core.pipeline import Pipeline

app = typer.Typer(name="doc-engine", help="Document Intelligence Engine")
console = Console()


@app.command()
def analyze(
    file: Path = typer.Argument(..., help="Path to the document file", exists=True),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
    no_analyzers: bool = typer.Option(False, "--no-analyzers", help="Skip analysis step"),
):
    """Analyze a document and display its structure."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True,
    ) as progress:
        progress.add_task(description="Extracting and analyzing...", total=None)
        pipeline = Pipeline()
        result = pipeline.import_document(str(file), run_analyzers=not no_analyzers)

    if json_output:
        console.print(json.dumps(_to_serializable(result), indent=2, ensure_ascii=False))
        return

    doc = result.document
    console.print(f"\n[bold cyan]📄 {doc.title}[/bold cyan]")
    console.print(f"   Format: {doc.file_format.upper()} | Pages: {doc.statistics.page_count if doc.statistics else '?'} | Langue: {doc.language or '?'}")
    console.print(f"   Temps total: {result.total_duration_ms:.1f}ms")

    table = Table(title="Analyse du document")
    table.add_column("Métrique", style="cyan")
    table.add_column("Valeur", style="green")
    stats = doc.statistics
    if stats:
        table.add_row("Mots", str(stats.total_words))
        table.add_row("Images", str(stats.total_images))
        table.add_row("Tableaux", str(stats.total_tables))
        table.add_row("Blocs de code", str(stats.total_code_blocks))
        table.add_row("Formules", str(stats.total_math_formulas))
        table.add_row("Liens", str(stats.total_links))
        table.add_row("Chapitres", str(stats.total_chapters))
    console.print(table)

    if doc.chapters:
        console.print("\n[bold]📑 Chapitres détectés :[/bold]")
        for i, ch in enumerate(doc.chapters):
            console.print(f"  {i+1}. {ch.title} ({ch.word_count} mots)")

    console.print("\n[bold]📊 Étapes du pipeline :[/bold]")
    for step in result.steps:
        icon = "✅" if step.success else "❌"
        console.print(f"  {icon} {step.name} ({step.duration_ms:.1f}ms)")


@app.command()
def extract(
    file: Path = typer.Argument(..., help="Path to the document file", exists=True),
    output: Path = typer.Option(Path("output.json"), "--output", "-o", help="Output file"),
    format: str = typer.Option("json", "--format", "-f", help="Output format (json, tiptap, markdown, html)"),
):
    """Extract and export document to a structured format."""
    pipeline = Pipeline()
    result = pipeline.import_document(str(file))
    doc = result.document

    if format == "tiptap":
        from document_engine.builders.tiptap import TipTapBuilder
        builder = TipTapBuilder()
        data = builder.build(doc)
    elif format == "markdown":
        from document_engine.builders.markdown import MarkdownBuilder
        builder = MarkdownBuilder()
        data = builder.build(doc)
    elif format == "html":
        from document_engine.builders.html import HTMLBuilder
        builder = HTMLBuilder()
        data = builder.build(doc)
    else:
        from document_engine.builders.json import JSONBuilder
        builder = JSONBuilder()
        data = builder.build(doc)

    output.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    console.print(f"[green]✓[/green] Exported to {output}")


@app.command()
def list():
    """List available extractors and analyzers."""
    from document_engine.core.registry import list_extractors, list_analyzers, list_builders

    console.print("[bold cyan]Extracteurs disponibles :[/bold cyan]")
    for name in list_extractors():
        console.print(f"  • {name}")

    console.print("\n[bold cyan]Analyseurs disponibles :[/bold cyan]")
    for name in list_analyzers():
        console.print(f"  • {name}")

    console.print("\n[bold cyan]Builders disponibles :[/bold cyan]")
    for name in list_builders():
        console.print(f"  • {name}")


def _to_serializable(obj):
    if hasattr(obj, "__dict__"):
        return {k: _to_serializable(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
    elif isinstance(obj, list):
        return [_to_serializable(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    return obj


if __name__ == "__main__":
    app()
