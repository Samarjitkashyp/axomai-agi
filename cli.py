import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown

from axomai.agents.z1_alpha.agent import Z1AlphaAgent
from axomai.db.session import SyncSessionLocal
from axomai.db.models import Document, AgentTaskLog

console = Console()

def print_banner():
    console.print(Panel(
        "[bold cyan]🧠 Z1 ALPHA — AUTONOMOUS FILE INTELLIGENCE AGENT[/bold cyan]\n"
        "[dim white]Core Engine: AxomAI AGI Framework | Database: PostgreSQL ('axomai_agi')[/dim white]",
        border_style="cyan"
    ))

def inspect_db():
    """Display current documents and logs stored in PostgreSQL"""
    with SyncSessionLocal() as db:
        docs = db.query(Document).all()
        logs = db.query(AgentTaskLog).order_by(AgentTaskLog.created_at.desc()).limit(10).all()

        console.print(f"\n[bold green]📊 PostgreSQL Database Inspection ('axomai_agi')[/bold green]")
        
        # Documents Table
        doc_table = Table(title="Cached Documents in PostgreSQL", show_header=True, header_style="bold magenta")
        doc_table.add_column("Filename", style="cyan")
        doc_table.add_column("Type", style="yellow")
        doc_table.add_column("Pages/Sheets", justify="right")
        doc_table.add_column("Size (KB)", justify="right")
        doc_table.add_column("Hash (SHA256)", style="dim")

        for d in docs:
            doc_table.add_row(
                d.filename,
                d.file_type,
                str(d.page_count),
                f"{d.file_size_bytes / 1024:.1f}",
                d.file_hash[:12] + "..."
            )
        console.print(doc_table)

        # Logs Table
        if logs:
            log_table = Table(title="Recent Agent Task Logs", show_header=True, header_style="bold blue")
            log_table.add_column("Time", style="dim")
            log_table.add_column("Task Type", style="green")
            log_table.add_column("User Query", style="white")
            log_table.add_column("Evidence Count", justify="center")

            for l in logs:
                log_table.add_row(
                    l.created_at.strftime("%H:%M:%S"),
                    l.task_type or "N/A",
                    l.user_query[:40] + ("..." if len(l.user_query) > 40 else ""),
                    str(len(l.evidence or []))
                )
            console.print(log_table)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Z1 Alpha File Intelligence CLI")
    parser.add_argument("--file", "-f", type=str, help="Path to file to process")
    parser.add_argument("--query", "-q", type=str, help="Question to ask about the file")
    parser.add_argument("--status", action="store_true", help="Inspect PostgreSQL records")
    args = parser.parse_args()

    if args.status:
        inspect_db()
        return

    agent = Z1AlphaAgent()

    if args.file and args.query:
        # One-shot command line run
        console.print(f"\n[bold yellow]User Query:[/bold yellow] {args.query}")
        result = agent.query(args.query, args.file)
        console.print(Panel(Markdown(result["answer"]), title="[bold green]Z1 Alpha Response[/bold green]", border_style="green"))
        if result["evidence"]:
            console.print(f"[dim]Evidence: {result['evidence']}[/dim]")
        return

    if args.file and not args.query:
        # Just parse and cache
        udm = agent.process_file(args.file)
        console.print(Panel(
            f"[bold]Filename:[/bold] {udm.file.filename}\n"
            f"[bold]Type:[/bold] {udm.file.file_type}\n"
            f"[bold]Pages/Sheets:[/bold] {udm.page_count}\n"
            f"[bold]Tables Extracted:[/bold] {len(udm.tables)}\n"
            f"[bold]Images Extracted:[/bold] {len(udm.images)}\n"
            f"[bold]Total Words:[/bold] {udm.stats.get('total_words', 'N/A')}",
            title="[bold green]File Parsed & Cached in PostgreSQL (UDM)[/bold green]"
        ))
        return

    # Interactive Loop
    console.print("\n[bold yellow]Entering Interactive Mode...[/bold yellow]")
    file_path = input("Enter path to file (or press Enter to inspect DB): ").strip().strip('"').strip("'")
    if not file_path:
        inspect_db()
        return

    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]Error: File does not exist at '{file_path}'[/red]")
        return

    # Process and store UDM
    udm = agent.process_file(path)
    console.print(Panel(
        f"[bold]File:[/bold] {udm.file.filename} | [bold]Type:[/bold] {udm.file.file_type} | [bold]Pages/Sheets:[/bold] {udm.page_count}\n"
        f"Ready to answer questions! Type 'exit' or 'quit' to stop.",
        title="[bold green]Z1 Alpha Ready[/bold green]"
    ))

    session_id = "cli_session"
    while True:
        try:
            query = input("\n[Z1 Alpha Question] > ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit", "q"]:
                console.print("[dim]Goodbye![/dim]")
                break
            if query.lower() == "status":
                inspect_db()
                continue

            result = agent.query(query, path, session_id=session_id)
            console.print(Panel(Markdown(result["answer"]), title=f"[bold green]Z1 Alpha ({result['task_type']})[/bold green]", border_style="green"))
            if result["evidence"]:
                console.print(f"[dim]Evidence: {result['evidence']}[/dim]")

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error during execution: {e}[/red]")

if __name__ == "__main__":
    main()

