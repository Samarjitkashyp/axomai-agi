"""
Z4 Nexus - Autonomous Software Engineer & Code Interpreter Agent.
Executes sandboxed Python code, debugs broken scripts with AST diagnostics,
and architects dynamic REST/GraphQL API connectors.
"""

import re
import json
from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z4_nexus.tools.code_sandbox import code_sandbox
from axomai.agents.z4_nexus.tools.bug_fixer import bug_fixer
from axomai.agents.z4_nexus.tools.api_connector import api_connector
from axomai.agents.z4_nexus.tools.tool_forge import tool_forge

class Z4NexusAgent:
    """Enterprise Autonomous Software Engineer & Code Interpreter."""

    def __init__(self):
        self.name = "Z4 Nexus"
        self.role = "Autonomous Software Engineer & Code Interpreter"

    def code_stream(
        self,
        query: str,
        session_id: Optional[str] = "nexus_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Processes software engineering, code execution, debugging, or API tasks with real-time SSE streaming.
        """
        q_lower = query.lower()

        # 1. Determine task type
        is_tool_forge = any(k in q_lower for k in ["forge tool", "create tool", "build tool", "new tool", "dynamic tool", "tool forge", "generate a tool"])
        is_bug_fix = any(k in q_lower for k in ["fix this", "debug", "syntax error", "traceback", "exception in", "why is this code failing"])
        is_api = any(k in q_lower for k in ["integrate api", "api client", "webhook", "swagger", "openapi", "stripe", "razorpay", "shopify", "rest api"])
        is_direct_exec = any(k in q_lower for k in ["run this", "execute this", "calculate with python", "simulate", "benchmark", "compute"]) or ("```python" in query)

        # Extract code snippet if present
        code_match = re.search(r'```(?:python)?\s*(.*?)\s*```', query, re.DOTALL)
        extracted_code = code_match.group(1).strip() if code_match else ""

        # ROUTE A: BUG FIXING & DEBUGGING
        if is_bug_fix and (extracted_code or "def " in query or "import " in query):
            yield {
                "type": "status",
                "stage": "ast_debug",
                "message": "⚙️ Z4 Nexus: Parsing Abstract Syntax Tree (AST) & diagnosing root cause..."
            }

            target_code = extracted_code or query
            fix_res = bug_fixer.analyze_and_fix(target_code, error_context=query)

            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "CODE_DEBUG_AND_FIX",
                "code_snippet": fix_res.get("repaired_code"),
                "diagnosis": fix_res.get("diagnosis"),
                "verified": fix_res.get("verified"),
                "sandbox_output": fix_res.get("sandbox_output"),
                "tools_used": ["ast_parser", "code_sandbox", "llm_brain"]
            }
            yield meta_event

            prompt = (
                f"You are Z4 Nexus, Senior Software Engineer. The user asked: '{query}'.\n"
                f"Root Cause Diagnosis: {fix_res.get('diagnosis')}\n\n"
                f"Repaired Code:\n```python\n{fix_res.get('repaired_code')}\n```\n\n"
                f"Sandbox Execution Verified: {fix_res.get('verified')}\n"
                f"Sandbox Output: {fix_res.get('sandbox_output')}\n\n"
                "Explain the exact bug cleanly in Markdown, present the verified code, and describe why the fix works."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z4 Nexus, Senior Software Engineer.", prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🛠️ Z4 Nexus Debugging Report\n\n**Diagnosis:** {fix_res.get('diagnosis')}\n\n```python\n{fix_res.get('repaired_code')}\n```"
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # ROUTE B: API INTEGRATION CLIENT GENERATOR
        elif is_api:
            yield {
                "type": "status",
                "stage": "api_architect",
                "message": "⚙️ Z4 Nexus: Synthesizing production-grade API client & webhook handler..."
            }

            api_res = api_connector.generate_client(query)
            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "API_INTEGRATION_CLIENT",
                "service_name": api_res.get("service_name"),
                "endpoints": api_res.get("endpoints", []),
                "code_snippet": api_res.get("client_code"),
                "tools_used": ["api_connector", "llm_brain"]
            }
            yield meta_event

            prompt = (
                f"You are Z4 Nexus, Senior API Architect. The user requested API integration: '{query}'.\n"
                f"Generated Service: {api_res.get('service_name')}\n"
                f"Client Code:\n```python\n{api_res.get('client_code')}\n```\n\n"
                "Explain the integration, how to configure credentials, and provide a clear usage example in Markdown."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z4 Nexus, Senior API Architect.", prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🔌 Z4 Nexus API Integration: {api_res.get('service_name')}\n\n```python\n{api_res.get('client_code')}\n```"
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # ROUTE C: SELF-EVOLVING TOOL FORGE (PHASE 3)
        elif is_tool_forge:
            yield {
                "type": "status",
                "stage": "tool_forge",
                "message": "⚙️ Z4 Nexus: Synthesizing custom tool with Z Sentinel AST validation..."
            }

            forge_res = tool_forge.forge_tool(tool_intent=query)
            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "TOOL_FORGE_EVOLUTION",
                "tool_name": forge_res.get("tool_name"),
                "code_snippet": forge_res.get("code"),
                "verified": forge_res.get("success"),
                "security_status": forge_res.get("security_status"),
                "test_output": forge_res.get("test_output"),
                "runtime_ms": forge_res.get("runtime_ms"),
                "tools_used": ["ast_sentinel", "code_sandbox", "custom_tool_registry"]
            }
            yield meta_event

            prompt = (
                f"You are Z4 Nexus, Senior Systems Architect. The user requested forging a tool: '{query}'.\n"
                f"Forged Tool Name: {forge_res.get('tool_name')}\n"
                f"Security Status: {forge_res.get('security_status')}\n"
                f"Generated Code:\n```python\n{forge_res.get('code')}\n```\n\n"
                f"Sandbox Test Output: {json.dumps(forge_res.get('test_output', {}))}\n"
                f"Runtime: {forge_res.get('runtime_ms')} ms\n\n"
                "Explain the tool architecture, security verification via Z Sentinel AST inspection, and how the tool has been registered for reuse."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z4 Nexus, Senior Systems Architect.", prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = (
                    f"### 🛠️ Z4 Nexus Tool Forge: `{forge_res.get('tool_name')}`\n\n"
                    f"🛡️ **Security Audit:** `{forge_res.get('security_status')}` (Verified Zero Malicious AST Nodes)\n\n"
                    f"**Generated & Registered Tool Code:**\n```python\n{forge_res.get('code')}\n```\n\n"
                    f"**Verified Sandbox Output:**\n```json\n{json.dumps(forge_res.get('test_output', {}), indent=2)}\n```\n\n"
                    f"⚡ Runtime: `{forge_res.get('runtime_ms')} ms` — Tool successfully saved to persistent registry."
                )
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # ROUTE D: CODE EXECUTION / CALCULATION SANDBOX
        else:
            yield {
                "type": "status",
                "stage": "sandbox_exec",
                "message": "⚙️ Z4 Nexus: Executing script in isolated Python sandbox runtime..."
            }

            script_to_run = extracted_code
            if not script_to_run:
                # Generate script using LLM first
                gen_prompt = (
                    f"User Query: {query}\n"
                    "Write a concise, standalone Python script that performs this computation and prints the final result with `print()`.\n"
                    "Output Python code only inside a single ```python code block."
                )
                raw_script = llm_brain.generate("You are Z4 Nexus Code Engine. Write code only.", gen_prompt, temperature=0.1)
                sc_match = re.search(r'```(?:python)?\s*(.*?)\s*```', raw_script, re.DOTALL)
                script_to_run = sc_match.group(1).strip() if sc_match else raw_script.strip()

            sandbox_res = code_sandbox.run_code(script_to_run)

            meta_event = {
                "type": "meta",
                "agent": self.name,
                "task_type": "CODE_INTERPRETER_EXECUTION",
                "code_snippet": script_to_run,
                "stdout": sandbox_res["stdout"],
                "stderr": sandbox_res["stderr"],
                "runtime_ms": sandbox_res["execution_time_ms"],
                "tools_used": ["python_sandbox", "llm_brain"]
            }
            yield meta_event

            prompt = (
                f"You are Z4 Nexus, Autonomous Software Engineer. The user asked: '{query}'.\n"
                f"Executed Code:\n```python\n{script_to_run}\n```\n\n"
                f"Execution Output:\n{sandbox_res['stdout'] or sandbox_res['stderr']}\n\n"
                f"Runtime: {sandbox_res['execution_time_ms']} ms\n\n"
                "Provide a crisp, professional technical explanation of the results in GitHub Markdown."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate("You are Z4 Nexus, Autonomous Software Engineer.", prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 💻 Z4 Nexus Execution Results\n\n**Output:**\n```\n{sandbox_res['stdout'] or sandbox_res['stderr']}\n```\n\n**Script:**\n```python\n{script_to_run}\n```"
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}

z4_nexus_agent = Z4NexusAgent()

