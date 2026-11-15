"""
Database Initialization Script
Creates all tables in PostgreSQL
"""
import sys
from rich.console import Console
from axomai.db.session import init_db, sync_engine
from axomai.config import settings

console = Console()

def main():
    console.print(f"[bold cyan]Connecting to PostgreSQL...[/bold cyan]")
    console.print(f"Host: {settings.DB_HOST}:{settings.DB_PORT}")
    console.print(f"Database: {settings.DB_NAME}")
    console.print(f"User: {settings.DB_USER}")
    
    try:
        init_db()
        console.print("[bold green]Success: All PostgreSQL tables created successfully![/bold green]")
        
        # Test listing created tables
        from sqlalchemy import inspect
        inspector = inspect(sync_engine)
        tables = inspector.get_table_names()
        console.print(f"[bold yellow]Created Tables in '{settings.DB_NAME}':[/bold yellow] {tables}")
        
    except Exception as e:
        console.print(f"[bold red]Database Init Failed:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

