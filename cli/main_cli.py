"""Main CLI entry point."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from agents.protocol_generator import ProtocolGenerator
from config.settings import PROTOCOLS_DIR
from generators.json_generator import JSONGenerator
from generators.markdown_generator import MarkdownGenerator
from utils.file_io import save_protocol_files

app = typer.Typer(
    name="lab-rador",
    help="Lab-Rador: AI-Powered Protocol Automator",
    add_completion=False,
)

console = Console()


@app.command()
def generate(
    description: str = typer.Argument(
        ..., help="Natural language description of the lab procedure"
    ),
    output_dir: str = typer.Option(
        str(PROTOCOLS_DIR), help="Directory to save generated protocols"
    ),
    name: str = typer.Option(
        None, help="Custom name for output files (auto-generated if not provided)"
    ),
    quiet: bool = typer.Option(False, help="Suppress progress messages"),
):
    """
    Generate a structured lab protocol from natural language description.

    Example:
        lab-rador generate "Mix 100 mL of solution A with 50 mL of solution B in a beaker, then heat to 60°C for 15 minutes"
    """
    if not quiet:
        console.print(
            Panel("[bold cyan]Lab-Rador Protocol Automator[/bold cyan]", expand=False)
        )
        console.print(f"📝 Processing description: {description}\n")

    try:
        # Initialize components
        generator = ProtocolGenerator()
        markdown_gen = MarkdownGenerator()
        json_gen = JSONGenerator()

        # Generate protocol with progress display
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            disable=quiet,
        ) as progress:
            task = progress.add_task("Analyzing procedure with AI agent...", total=None)

            protocol = generator.generate_protocol(description)

            progress.update(task, description="Protocol generated successfully!")

        # Generate outputs
        if not quiet:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                disable=quiet,
            ) as progress:
                task = progress.add_task("📄 Generating documentation...", total=None)

                markdown = markdown_gen.generate_protocol_markdown(protocol)
                json_data = json_gen.generate_protocol_json(protocol)

                progress.update(task, description="Documentation generated!")

        # Save files
        if not quiet:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                disable=quiet,
            ) as progress:
                task = progress.add_task("💾 Saving protocol files...", total=None)

                saved_files = save_protocol_files(protocol, output_dir, name)

                progress.update(task, description="Files saved!")

        # Display results
        if not quiet:
            console.print("\n[green]Protocol generated successfully![/green]")
            console.print(f"[blue]Title:[/blue] {protocol.title}")
            console.print(f"[blue]Duration:[/blue] {protocol.duration_minutes} minutes")
            console.print(f"[blue]Steps:[/blue] {len(protocol.steps)}")
            console.print(f"[blue]Files saved to:[/blue] {output_dir}")

            # Show file paths
            for file_path in saved_files:
                console.print(f"  • {file_path}")

    except Exception as e:
        console.print(f"[red]Error generating protocol: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def list_protocols(
    directory: str = typer.Option(
        str(PROTOCOLS_DIR), help="Directory to scan for protocols"
    ),
):
    """
    List all generated protocols in the specified directory.
    """
    from utils.file_io import list_protocol_files

    try:
        protocols = list_protocol_files(directory)

        if not protocols:
            console.print(f"[yellow]No protocols found in {directory}[/yellow]")
            return

        # Create table
        table = Table(title="Generated Protocols")
        table.add_column("Title", style="cyan", no_wrap=True)
        table.add_column("Created", style="green")
        table.add_column("Version", style="yellow")
        table.add_column("Steps", style="magenta")
        table.add_column("File", style="blue")

        for protocol_info in protocols:
            table.add_row(
                protocol_info["title"],
                protocol_info["created_at"].strftime("%Y-%m-%d %H:%M"),
                protocol_info["version"],
                str(protocol_info["steps_count"]),
                protocol_info["filename"],
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing protocols: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def export(
    protocol_id: str = typer.Argument(..., help="Protocol identifier or filename"),
    format: str = typer.Option("markdown", help="Export format (markdown, json)"),
    output: str = typer.Option(
        None, help="Output file path (auto-generated if not provided)"
    ),
):
    """
    Export a protocol in different formats.

    Example:
        lab-rador export "solution_mixing_protocol" --format json
    """
    from utils.file_io import load_protocol_from_file

    try:
        # Load protocol
        protocol = load_protocol_from_file(protocol_id)

        if format.lower() == "markdown":
            from generators.markdown_generator import MarkdownGenerator

            generator = MarkdownGenerator()
            content = generator.generate_protocol_markdown(protocol)
            ext = "md"
        elif format.lower() == "json":
            from generators.json_generator import JSONGenerator

            generator = JSONGenerator()
            content = generator.generate_protocol_json(protocol)
            ext = "json"
        else:
            raise ValueError(f"Unsupported format: {format}")

        # Determine output path
        if not output:
            output = f"{protocol.title.lower().replace(' ', '_')}.{ext}"

        # Save file
        output_path = Path(output)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        console.print(f"[green]Protocol exported to: {output_path}[/green]")

    except Exception as e:
        console.print(f"[red]Error exporting protocol: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
