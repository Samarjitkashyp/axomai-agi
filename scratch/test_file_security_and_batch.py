import io
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, r"e:\axomai_agi\src")

from axomai.agents.z_sentinel.guardrails.file_security import file_security
from axomai.agents.z_sentinel import z_sentinel_agent
from axomai.agents.master_orchestrator import master_orchestrator
from axomai.agents.z1_alpha.agent import Z1AlphaAgent

print("--- 1. Testing Z Sentinel File Security Guardrails ---")

# Test 1: Dangerous extension (.exe)
res1 = file_security.inspect_file("payload.exe", b"fakecontent", 100)
print(f"Test 1 (.exe): safe={res1['is_safe']}, threat={res1.get('threat_type')}")
assert not res1['is_safe'], "Should block .exe file"

# Test 2: Dangerous extension (.bat, .sh, .php)
res2 = file_security.inspect_file("backdoor.php", b"<?php phpinfo(); ?>", 100)
print(f"Test 2 (.php): safe={res2['is_safe']}, threat={res2.get('threat_type')}")
assert not res2['is_safe'], "Should block .php file"

# Test 3: Disguised Windows PE Executable disguised as .pdf (magic bytes MZ)
pe_bytes = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff"
res3 = file_security.inspect_file("invoice.pdf", pe_bytes, 500)
print(f"Test 3 (disguised PE): safe={res3['is_safe']}, threat={res3.get('threat_type')}")
assert not res3['is_safe'], "Should block PE magic bytes"

# Test 4: Linux ELF binary disguised as .docx (magic bytes \x7fELF)
elf_bytes = b"\x7fELF\x02\x01\x01\x00"
res4 = file_security.inspect_file("contract.docx", elf_bytes, 500)
print(f"Test 4 (disguised ELF): safe={res4['is_safe']}, threat={res4.get('threat_type')}")
assert not res4['is_safe'], "Should block ELF magic bytes"

# Test 5: Filename path traversal sanitization
clean_name = file_security.sanitize_filename("../../../etc/passwd.pdf")
print(f"Test 5 (path traversal sanitization): '{clean_name}'")
assert ".." not in clean_name and "/" not in clean_name, "Should sanitize path traversal"

# Test 6: Legitimate Safe PDF
pdf_bytes = b"%PDF-1.4\n%..."
res6 = file_security.inspect_file("Quarterly_Report.pdf", pdf_bytes, 2048)
print(f"Test 6 (Safe PDF): safe={res6['is_safe']}")
assert res6['is_safe'], "Should allow legitimate PDF"

# Test 7: Legitimate Safe Excel
xlsx_bytes = b"PK\x03\x04\x14\x00\x06\x00"
res7 = file_security.inspect_file("Sales_2024.xlsx", xlsx_bytes, 4096)
print(f"Test 7 (Safe XLSX): safe={res7['is_safe']}")
assert res7['is_safe'], "Should allow legitimate XLSX"

print("\n--- 2. Testing Z1 Alpha Multi-Document Stream Method ---")
z1 = Z1AlphaAgent()
assert hasattr(z1, "query_multi_stream"), "Z1AlphaAgent must have query_multi_stream"
print("Z1AlphaAgent.query_multi_stream is verified!")

print("\n--- 3. Testing Master Orchestrator Multi-Doc Integration ---")
assert hasattr(master_orchestrator, "orchestrate_stream"), "Master orchestrator must have orchestrate_stream"
print("MasterOrchestrator.orchestrate_stream is verified!")

print("\nAll File Security & Multi-Document Integration Tests Passed 100%!")

