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
        ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt",
        ".csv", ".txt", ".md", ".json", ".png", ".jpg", ".jpeg", ".webp", ".bmp"
    }

    DANGEROUS_EXTENSIONS = {
        ".exe", ".bat", ".cmd", ".sh", ".vbs", ".ps1", ".scr", ".jar",
        ".msi", ".py", ".php", ".phtml", ".dll", ".so", ".bin", ".elf",
        ".com", ".hta", ".cpl", ".wsf", ".asp", ".aspx", ".jsp", ".cgi"
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
        ext = Path(sanitized_name).suffix.lower()

        # 1. Extension Verification
        if not ext:
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "MISSING_EXTENSION",
                "reason": "Z Sentinel blocked file: Extension is missing or undefined."
            }

        if ext in self.DANGEROUS_EXTENSIONS:
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "EXECUTABLE_FILE_BLOCKED",
                "reason": f"Z Sentinel blocked executable/script extension '{ext}'. Only documents, spreadsheets, and images are permitted."
            }

        if ext not in self.ALLOWED_EXTENSIONS:
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "UNSUPPORTED_EXTENSION",
                "reason": f"Z Sentinel blocked unsupported extension '{ext}'."
            }

        # 2. File Size Verification
        if file_size > self.MAX_FILE_SIZE_BYTES:
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "FILE_TOO_LARGE",
                "reason": f"File exceeds maximum allowed size of 50 MB ({round(file_size/(1024*1024), 1)} MB)."
            }

        # 3. Magic Byte & Binary Inspection
        # Windows PE executable (starts with MZ)
        if header_bytes.startswith(b"MZ"):
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "EXECUTABLE_MAGIC_BYTES (PE_HEADER)",
                "reason": "Z Sentinel intercepted executable binary payload (Windows PE header) disguised as a document."
            }

        # Linux ELF binary (starts with \x7fELF)
        if header_bytes.startswith(b"\x7fELF"):
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "EXECUTABLE_MAGIC_BYTES (ELF_BINARY)",
                "reason": "Z Sentinel intercepted Linux binary executable payload disguised as a document."
            }

        # Web shells & Script injections in text/image files
        header_text = header_bytes[:512].lower()
        if b"<?php" in header_text or b"<script" in header_text or b"#!/bin/sh" in header_text or b"#!/bin/bash" in header_text:
            return {
                "is_safe": False,
                "sanitized_name": sanitized_name,
                "threat_type": "SCRIPT_PAYLOAD_DETECTED",
                "reason": "Z Sentinel detected embedded web shell or script instructions inside uploaded content."
            }

        return {
            "is_safe": True,
            "sanitized_name": sanitized_name,
            "threat_type": None,
            "reason": None
        }

file_security = FileSecurityGuard()

