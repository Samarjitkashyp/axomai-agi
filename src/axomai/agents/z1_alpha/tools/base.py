import hashlib
import mimetypes
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Set, Dict, Any, Optional
from axomai.core.udm import UnifiedDocumentModel, FileInfo

class BaseFileTool(ABC):
    """Abstract Base Class for all Z1 Alpha File Readers"""
    name: str = "base_tool"
    description: str = "Base file reader"
    supported_extensions: Set[str] = set()

    def can_handle(self, file_path: str | Path) -> bool:
        path = Path(file_path)
        return path.suffix.lower() in self.supported_extensions

    def get_file_info(self, file_path: str | Path, file_type: str) -> FileInfo:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Compute SHA256 hash for deduplication/caching
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        file_hash = sha256.hexdigest()

        mime, _ = mimetypes.guess_type(str(path))

        return FileInfo(
            filename=path.name,
            file_path=str(path.resolve()),
            file_type=file_type.upper(),
            mime_type=mime or "application/octet-stream",
            file_size_bytes=path.stat().st_size,
            file_hash=file_hash
        )

    @abstractmethod
    def parse(self, file_path: str | Path, options: Optional[Dict[str, Any]] = None) -> UnifiedDocumentModel:
        """Parse the file and return a standardized UnifiedDocumentModel"""
        pass

