"""
Unit test for Z4 Nexus Self-Evolving Tool Forge and Z Sentinel AST Security.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from axomai.agents.z4_nexus.tools.tool_forge import tool_forge

def test_ast_security_blocks_malicious():
    print("Testing malicious code blocking...")
    malicious_snippets = [
        "import os\ndef tool_hack(): os.system('calc')",
        "import subprocess\ndef tool_pwn(): subprocess.run(['ls'])",
        "def tool_eval(x): return eval(x)",
        "def tool_open(): return open('/etc/passwd').read()",
        "import socket\ndef tool_net(): return socket.socket()"
    ]

    for snip in malicious_snippets:
        sec = tool_forge.validate_code_security(snip)
        assert not sec["safe"], f"Expected security violation for: {snip}"
        print(f"  [BLOCKED AS EXPECTED]: {sec['violations']}")

    print("PASS: AST Security successfully blocked all malicious patterns!\n")

def test_forge_and_execute_tool():
    print("Testing Tool Forge tool creation and registration...")
    res = tool_forge.forge_tool(
        tool_intent="Calculate Assam agricultural flood loss index given inundated hectares and crop yield",
        requested_name="assam_crop_loss"
    )

    print(f"Tool Name: {res['tool_name']}")
    print(f"Success: {res['success']}")
    print(f"Security: {res['security_status']}")
    print(f"Test Output: {res['test_output']}")
    print(f"Runtime: {res['runtime_ms']} ms")
    assert res["success"] is True

    print("\nTesting execution of registered tool...")
    exec_res = tool_forge.execute_tool(
        tool_name=res["tool_name"],
        params={"base_value": 500000, "growth_rate": 0.08, "years": 4}
    )
    print(f"Execution Success: {exec_res['success']}")
    print(f"Execution Result: {exec_res['result']}")
    print(f"Execution Runtime: {exec_res['execution_time_ms']} ms")
    assert exec_res["success"] is True

    tools = tool_forge.list_tools()
    print(f"\nTotal Registered Tools: {len(tools)}")
    print("PASS: Tool Forge passed 100%!")

if __name__ == "__main__":
    test_ast_security_blocks_malicious()
    test_forge_and_execute_tool()

