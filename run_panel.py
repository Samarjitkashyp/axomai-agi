import sys
import argparse
from pathlib import Path

# Add src to pythonpath
src_dir = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(src_dir))

import uvicorn
from rich.console import Console
from rich.panel import Panel

console = Console()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Z1 Alpha Web Intelligence Panel Launcher")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port to run the web server on (default: 8080)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host IP (default: 127.0.0.1)")
    args = parser.parse_args()

    console.print(Panel(
        f"[bold cyan]🚀 Starting Z1 Alpha Web Intelligence Panel...[/bold cyan]\n"
        f"[bold green]URL:[/bold green] [underline]http://{args.host}:{args.port}[/underline]\n"
        f"[dim]PostgreSQL Database: axomai_agi | Agent: Z1 Alpha[/dim]",
        border_style="cyan"
    ))
    uvicorn.run("axomai.api.app:app", host=args.host, port=args.port, reload=True)
