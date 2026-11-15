"""
AxomAI Agency - Sovereign Encrypted Credential Vault.
Provides military-grade AES encryption (Fernet) for user-authorized web credentials,
session tokens, and service keys. Strictly isolates secrets, enforces zero-leakage masking,
and records comprehensive security audit trails for all credential retrievals.
"""

import os
import json
import base64
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from cryptography.fernet import Fernet
from axomai.config import settings

VAULT_DIR = settings.STORAGE_DIR / "vault"
VAULT_KEY_PATH = VAULT_DIR / ".vault_key"
VAULT_DATA_PATH = VAULT_DIR / "sovereign_vault.enc"

class SovereignCredentialVault:
    """Encrypted credential vault with zero-leakage masking for autonomous web operations."""

    def __init__(self):
        VAULT_DIR.mkdir(parents=True, exist_ok=True)
        self.fernet = self._init_fernet()
        self.audit_log: List[Dict[str, Any]] = []

    def _init_fernet(self) -> Fernet:
        """Loads or creates a persistent local encryption key."""
        if VAULT_KEY_PATH.exists():
            key = VAULT_KEY_PATH.read_bytes()
        else:
            key = Fernet.generate_key()
            VAULT_KEY_PATH.write_bytes(key)
        return Fernet(key)

    def _load_vault(self) -> Dict[str, Any]:
        """Loads and decrypts vault data."""
        if not VAULT_DATA_PATH.exists():
            return {}
        try:
            encrypted_data = VAULT_DATA_PATH.read_bytes()
            decrypted_json = self.fernet.decrypt(encrypted_data).decode("utf-8")
            return json.loads(decrypted_json)
        except Exception:
            return {}

    def _save_vault(self, data: Dict[str, Any]) -> None:
        """Encrypts and persists vault data."""
        serialized = json.dumps(data).encode("utf-8")
        encrypted = self.fernet.encrypt(serialized)
        VAULT_DATA_PATH.write_bytes(encrypted)

    def store_credential(
        self,
        service_id: str,
        service_name: str,
        username: str,
        secret: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Securely stores and encrypts an authorized service credential.
        """
        vault = self._load_vault()
        now = datetime.now(timezone.utc).isoformat()
        
        vault[service_id] = {
            "service_id": service_id,
            "service_name": service_name,
            "username": username,
            "secret": secret,
            "metadata": metadata or {},
            "stored_at": now,
            "last_accessed": None
        }
        self._save_vault(vault)

        self._log_audit(service_id, "STORE_CREDENTIAL", granted=True)
        return {
            "service_id": service_id,
            "service_name": service_name,
            "username": username,
            "status": "SECURED_IN_ENCRYPTED_VAULT",
            "timestamp": now
        }

    def get_credential(self, service_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves decrypted credential for an authorized operational task.
        """
        vault = self._load_vault()
        if service_id not in vault:
            self._log_audit(service_id, "GET_CREDENTIAL", granted=False, reason="SERVICE_NOT_FOUND")
            return None

        cred = vault[service_id]
        cred["last_accessed"] = datetime.now(timezone.utc).isoformat()
        self._save_vault(vault)
        self._log_audit(service_id, "GET_CREDENTIAL", granted=True)
        return dict(cred)

    def list_services_masked(self) -> List[Dict[str, Any]]:
        """
        Lists all registered services with passwords strictly masked.
        Zero-leakage display for UI / logs.
        """
        vault = self._load_vault()
        return [
            {
                "service_id": c["service_id"],
                "service_name": c["service_name"],
                "username": c["username"],
                "secret_masked": "********",
                "stored_at": c.get("stored_at"),
                "last_accessed": c.get("last_accessed")
            }
            for c in vault.values()
        ]

    def _log_audit(self, service_id: str, action: str, granted: bool, reason: str = "SUCCESS"):
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service_id": service_id,
            "action": action,
            "granted": granted,
            "reason": reason
        }
        self.audit_log.append(record)
        if len(self.audit_log) > 50:
            self.audit_log.pop(0)

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        return list(self.audit_log[-15:])

credential_vault = SovereignCredentialVault()

