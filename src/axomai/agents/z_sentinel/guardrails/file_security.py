"""
Z Sentinel - Enterprise File Security & Anti-Malware Guardrail.
Validates file extensions, inspects binary magic bytes, sanitizes filenames,
blocks executable payloads (PE, ELF, PHP, shell scripts), and enforces upload limits.
"""

import re
from pathlib import Path
from typing import Dict, Any, Tuple

class FileSecurityGuard:
    """Enterprise file scanner and malware barrier."""

    ALLOWED_EXTENSIONS = {
        # Documents & Spreadsheets
        ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt",
        ".csv", ".tsv", ".txt", ".md", ".markdown", ".rst", ".tex",
        # Images
        ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".svg", ".gif", ".ico", ".tiff",
        # Source Code & Engineering Files for AI Analysis
        ".py", ".js", ".ts", ".tsx", ".jsx", ".cpp", ".c", ".cc", ".cxx", ".h", ".hpp",
        ".java", ".cs", ".go", ".rs", ".php", ".rb", ".html", ".htm", ".css", ".scss", ".sass", ".less",
        ".sql", ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat",
        ".json", ".yaml", ".yml", ".toml", ".xml", ".env", ".ini", ".cfg", ".conf", ".properties", ".log",
        ".dart", ".swift", ".kt", ".kts", ".scala", ".r", ".m", ".vue", ".svelte", ".astro",
        ".graphql", ".gql", ".proto", ".prisma", ".sol", ".lua", ".pl", ".pm", ".ex", ".exs",
        ".erl", ".hs", ".clj", ".cljs", ".tf", ".lock", ".sum", ".mod", ".ipynb", ".diff", ".patch"
    }

    KNOWN_TEXT_FILENAMES = {
        "dockerfile", "makefile", "license", "procfile", "gemfile",
        "vagrantfile", "caddyfile", "readme", ".gitignore", ".env", ".bashrc", ".zshrc"
    }

    DANGEROUS_EXTENSIONS = {
        ".exe", ".scr", ".msi", ".dll", ".so", ".bin", ".elf",
        ".com", ".hta", ".cpl", ".wsf"
    }

    MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024 # 50 MB
    MAX_BATCH_FILES = 10

    def sanitize_filename(self, filename: str) -> str:
        """Removes directory traversal, null bytes, and non-safe characters."""
        clean = Path(filename).name
        clean = re.sub(r'[\x00-\x1f\x7f]', '', clean)
        clean = re.sub(r'[\\/:*?"<>|]', '_', clean)
        clean = clean.replace('..', '_')
        if len(clean) > 80:
            stem = Path(clean).stem[:70]
            suffix = Path(clean).suffix
            clean = f"{stem}{suffix}"
        return clean or "unnamed_document"

    def inspect_file(self, filename: str, header_bytes: bytes, file_size: int) -> Dict[str, Any]:
        """
        Inspects file extension, size, and header magic bytes.
        Returns:
            {
                "is_safe": bool,
                "sanitized_name": str,
                "threat_type": Optional[str],
                "reason": Optional[str]
            }
        """
        sanitized_name = self.sanitize_filename(filename)
        clean_lower = sanitized_name.lower()
        ext = Path(sanitized_name).suffix.lower()

        # 1. Extension & Known Filename Verification
        is_known_text_file = (
            clean_lower in self.KNOWN_TEXT_FILENAMES
            or any(clean_lower.startswith(k) for k in ["dockerfile", "makefile", "license", "readme"])
            or (b"\x00" not in header_bytes[:1024])
        )

        if ext in self.DANGEROUS_EXTENSIONS:
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "EXECUTABLE_FILE_BLOCKED",
                "reason": f"Z Sentinel blocked compiled executable binary extension '{ext}'."
            }

        # If extension is not explicitly listed, allow if it's verifiable plain text / source code
        if ext not in self.ALLOWED_EXTENSIONS and not is_known_text_file:
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "UNSUPPORTED_BINARY_EXTENSION",
                "reason": f"Z Sentinel blocked unsupported binary extension '{ext}'."
            }

        # 2. File Size Verification
        if file_size > self.MAX_FILE_SIZE_BYTES:
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "FILE_TOO_LARGE",
                "reason": f"File exceeds maximum allowed size of 50 MB ({round(file_size/(1024*1024), 1)} MB)."
            }

        # 3. Magic Byte & Binary Executable Inspection
        # Windows PE executable / DLL (starts with MZ)
        if header_bytes.startswith(b"MZ"):
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "EXECUTABLE_MAGIC_BYTES (PE_HEADER)",
                "reason": "Z Sentinel intercepted executable binary payload (Windows PE header)."
            }

        # Linux ELF binary (starts with \x7fELF)
        if header_bytes.startswith(b"\x7fELF"):
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "EXECUTABLE_MAGIC_BYTES (ELF_BINARY)",
                "reason": "Z Sentinel intercepted Linux binary executable payload."
            }

        # Mach-O binary
        if header_bytes[:4] in [b"\xfe\xed\xfa\xce", b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe"]:
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "EXECUTABLE_MAGIC_BYTES (MACHO_BINARY)",
                "reason": "Z Sentinel intercepted Mach-O executable payload."
            }

        # Web shells & Script injections in binary media files (e.g. polyglot image exploits)
        image_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".ico", ".tiff"}
        if ext in image_extensions:
            header_text = header_bytes[:512].lower()
            if b"<?php" in header_text or b"<script" in header_text or b"#!/bin/sh" in header_text or b"#!/bin/bash" in header_text:
                return {
                    "is_safe": False,
                    "sanitized_name": sanitized_name,
                    "threat_type": "POLYGLOT_IMAGE_EXPLOIT",
                    "reason": "Z Sentinel detected embedded script instructions inside uploaded image binary."
                }

        return {
            "is_safe": True,
            "sanitized_name": sanitized_name,
            "threat_type": None,
            "reason": None
        }

file_security = FileSecurityGuard()

