"""
Z4 Nexus - Codebase Knowledge Graph & AST Repository Indexer.
Extracts project-wide symbol tables, file dependencies, classes, functions,
and provides multi-file semantic context for deep codebase understanding.
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

class RepoIndexer:
    """AST and semantic repository indexer."""

    IGNORE_DIRS = {
        ".git", ".venv", "venv", "node_modules", "__pycache__",
        ".pytest_cache", ".idea", ".vscode", "dist", "build", "coverage"
    }

    IGNORE_EXTS = {
        ".pyc", ".pyo", ".pyd", ".png", ".jpg", ".jpeg", ".ico",
        ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".zip", ".tar", ".gz"
    }

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = Path(workspace_root or "e:/axomai_agi")

    def build_file_tree(self, max_depth: int = 3) -> str:
        """Returns a clean ASCII tree of the workspace."""
        lines = []

        def _walk(directory: Path, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return
            try:
                entries = sorted(
                    [p for p in directory.iterdir() if p.name not in self.IGNORE_DIRS],
                    key=lambda x: (not x.is_dir(), x.name.lower())
                )
            except Exception:
                return

            for i, entry in enumerate(entries):
                is_last = (i == len(entries) - 1)
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{entry.name}{'/' if entry.is_dir() else ''}")
                if entry.is_dir():
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    _walk(entry, new_prefix, depth + 1)

        lines.append(self.workspace_root.name + "/")
        _walk(self.workspace_root)
        return "\n".join(lines[:120])

    def index_workspace_symbols(self, max_files: int = 150) -> Dict[str, Any]:
        """
        Parses Python and JS/TS files to extract classes, functions, and imports.
        """
        symbols: Dict[str, List[Dict[str, Any]]] = {}
        files_scanned = 0
        total_loc = 0

        for path in self.workspace_root.rglob("*"):
            if files_scanned >= max_files:
                break
            if any(part in self.IGNORE_DIRS for part in path.parts):
                continue
            if not path.is_file() or path.suffix in self.IGNORE_EXTS:
                continue

            rel_path = str(path.relative_to(self.workspace_root)).replace("\\", "/")

            if path.suffix == ".py":
                files_scanned += 1
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                    total_loc += len(content.splitlines())
                    tree = ast.parse(content)
                    file_symbols = []

                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            file_symbols.append({"type": "class", "name": node.name, "line": node.lineno})
                        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                            file_symbols.append({"type": "function", "name": node.name, "line": node.lineno})

                    if file_symbols:
                        symbols[rel_path] = file_symbols
                except Exception:
                    pass

            elif path.suffix in [".js", ".jsx", ".ts", ".tsx"]:
                files_scanned += 1
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                    total_loc += len(content.splitlines())
                    file_symbols = []
                    # Regex for classes & functions
                    for m in re.finditer(r'(?:export\s+)?(?:default\s+)?class\s+([A-Za-z0-9_]+)', content):
                        file_symbols.append({"type": "class", "name": m.group(1), "line": content[:m.start()].count("\n") + 1})
                    for m in re.finditer(r'(?:export\s+)?(?:async\s+)?function\s+([A-Za-z0-9_]+)', content):
                        file_symbols.append({"type": "function", "name": m.group(1), "line": content[:m.start()].count("\n") + 1})
                    for m in re.finditer(r'(?:const|let|var)\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>', content):
                        file_symbols.append({"type": "arrow_func", "name": m.group(1), "line": content[:m.start()].count("\n") + 1})

                    if file_symbols:
                        symbols[rel_path] = file_symbols
                except Exception:
                    pass

        return {
            "files_scanned": files_scanned,
            "total_loc": total_loc,
            "symbols_indexed": sum(len(v) for v in symbols.values()),
            "symbol_map": symbols
        }

    def search_symbols(self, query: str) -> List[Dict[str, Any]]:
        """Finds definition files for a given symbol name."""
        idx = self.index_workspace_symbols()
        q_lower = query.lower()
        matches = []
        for file_path, sym_list in idx["symbol_map"].items():
            for s in sym_list:
                if q_lower in s["name"].lower():
                    matches.append({
                        "file": file_path,
                        "type": s["type"],
                        "name": s["name"],
                        "line": s["line"]
                    })
        return matches[:25]

    def get_context_for_query(self, query: str, max_chars: int = 4000) -> str:
        """Finds most relevant files and returns excerpts to enrich LLM prompt."""
        matches = self.search_symbols(query)
        if not matches:
            # Fallback to file tree
            return f"Project File Structure:\n{self.build_file_tree(max_depth=2)}"

        context_chunks = []
        seen_files = set()
        for m in matches:
            f = m["file"]
            if f in seen_files:
                continue
            seen_files.add(f)
            p = self.workspace_root / f
            if p.exists():
                try:
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    lines = text.splitlines()
                    # Grab excerpt around line
                    start = max(0, m["line"] - 10)
                    end = min(len(lines), m["line"] + 35)
                    excerpt = "\n".join(lines[start:end])
                    context_chunks.append(f"--- File: {f} (around line {m['line']}) ---\n{excerpt}\n")
                except Exception:
                    pass

        combined = "\n".join(context_chunks)
        return combined[:max_chars] if combined else f"Project File Structure:\n{self.build_file_tree(max_depth=2)}"

repo_indexer = RepoIndexer()
