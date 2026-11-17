"""
Z4 Nexus - Autonomous Polyglot Software Engineer & Chief Code Architect Agent.
World-class autonomous coding engine featuring:
1. Autonomous Self-Healing Loop (Auto-Test & Auto-Fix)
2. Polyglot Multi-Language Sandbox Runner (Python, Node.js/JS, TS, Shell, C++, Go, Rust)
3. Codebase Knowledge Graph & AST Repository Indexer
4. SAST Security & Vulnerability Auditing
5. Autonomous Git & CI/CD Workflow Engine
6. Interactive System Architecture & Database Schema Visualizer (Mermaid)
7. 1-Click Full-Stack Project Scaffolding
8. Self-Evolving Dynamic Tool Forge
"""

import re
import json
from typing import Dict, Any, Generator, Optional
from axomai.core.llm import llm_brain
from axomai.agents.z4_nexus.tools.code_sandbox import code_sandbox
from axomai.agents.z4_nexus.tools.bug_fixer import bug_fixer
from axomai.agents.z4_nexus.tools.api_connector import api_connector
from axomai.agents.z4_nexus.tools.tool_forge import tool_forge
from axomai.agents.z4_nexus.tools.polyglot_runner import polyglot_runner
from axomai.agents.z4_nexus.tools.self_healing_engine import self_healing_engine
from axomai.agents.z4_nexus.tools.repo_indexer import repo_indexer
from axomai.agents.z4_nexus.tools.security_scanner import security_scanner
from axomai.agents.z4_nexus.tools.git_workflow import git_workflow
from axomai.agents.z4_nexus.tools.arch_visualizer import arch_visualizer
from axomai.agents.z4_nexus.tools.project_scaffolder import project_scaffolder

NEXUS_SYSTEM_PROMPT = """You are Z4 Nexus, the Autonomous Polyglot Software Engineer & Chief Code Architect of AxomAI.
You possess elite mastery across ALL programming languages, system architectures, algorithms, and engineering domains.

Your Capabilities & Standards:
1. Multi-Language Polyglot Mastery:
   - Python, JavaScript (ES6+), TypeScript, React, Next.js, Node.js, Vue, Angular, HTML5, CSS3, Tailwind CSS
   - C, C++, C#, Java, Kotlin, Swift, Rust, Go, PHP, Ruby, Scala
   - SQL (PostgreSQL, MySQL, SQLite, DuckDB), NoSQL (MongoDB, Redis), GraphQL
   - Linux Shell / Bash, PowerShell, Docker, Docker Compose, Kubernetes, CI/CD pipelines
2. Engineering Rigor:
   - Write clean, complete, production-grade, bug-free, well-commented code.
   - Never use lazy placeholder comments like `// TODO: implement later` or `...`. Always provide complete, runnable implementations.
   - Follow language-specific idiomatic best practices (PEP 8 for Python, ESLint/Prettier for JS/TS, modern C++20 guidelines, Rust safety).
   - Analyze time and space complexity (Big-O notation) for algorithms and data structures.
   - Include thorough error handling, input validation, and typing (type hints, TypeScript interfaces, etc.).
3. Problem Solving & Communication:
   - For conceptual questions: Explain with crystal clarity, architectural diagrams/tables, and clear code examples.
   - For debugging: Pinpoint the exact root cause, explain why the bug occurred, and provide the fully corrected code.
   - Communicate helpfully, articulate step-by-step instructions, and present code in clean syntax-highlighted GitHub markdown blocks.
   - Converse naturally in English, Hinglish, or Hindi according to user preference.
"""

class Z4NexusAgent:
    """Enterprise Autonomous Polyglot Software Engineer & Code Architect."""

    def __init__(self):
        self.name = "Z4 Nexus"
        self.role = "Autonomous Polyglot Software Engineer & Code Architect"

    def code_stream(
        self,
        query: str,
        session_id: Optional[str] = "nexus_session",
        doc_id: Optional[str] = None
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Processes software engineering, code execution, debugging, or architectural tasks with real-time SSE streaming.
        """
        q_lower = query.lower()

        # Extract code snippet if present
        code_match = re.search(r'```(?:[a-zA-Z0-9_-]+)?\s*(.*?)\s*```', query, re.DOTALL)
        extracted_code = code_match.group(1).strip() if code_match else ""

        # Intent Detection
        is_security_audit = any(k in q_lower for k in ["security audit", "vulnerability", "vulnerabilities", "scan code", "sast", "check security", "security check", "leak", "injection check"])
        is_self_healing = any(k in q_lower for k in ["self heal", "self-healing", "auto test", "auto-test", "verify and fix", "test and heal", "run test loop", "unit test pass", "test loop"])
        is_scaffold = any(k in q_lower for k in ["scaffold", "scaffold project", "boilerplate", "create fullstack", "generate repo", "build fullstack app", "create project", "setup project"])
        is_arch_diagram = any(k in q_lower for k in ["architecture diagram", "system design", "er diagram", "database schema", "sequence diagram", "mermaid", "flowchart", "c4 diagram"])
        is_git = any(k in q_lower for k in ["git commit", "commit message", "git diff", "git status", "pull request", "pr description", "pr dossier"])
        is_repo_query = any(k in q_lower for k in ["codebase", "workspace symbols", "where is function", "search codebase", "repo map", "file structure", "symbol table"])
        is_tool_forge = any(k in q_lower for k in ["forge tool", "create tool", "build tool", "new tool", "dynamic tool", "tool forge", "generate a tool"])
        is_api = any(k in q_lower for k in ["integrate api", "api client", "webhook", "swagger", "openapi", "stripe", "razorpay", "shopify", "rest api client"])
        is_direct_exec = any(k in q_lower for k in ["run this", "execute this", "run python", "run javascript", "run node", "execute code", "run code", "eval code"]) and ("```" in query or "print(" in query or "console.log" in query or "import " in query or "def " in query)
        is_bug_fix = any(k in q_lower for k in ["fix this", "debug", "syntax error", "traceback", "exception in", "why is this code failing", "fix code", "find bug"])

        # =========================================================================
        # 1. SAST SECURITY & VULNERABILITY AUDITING ROUTE
        # =========================================================================
        if is_security_audit and (extracted_code or "code" in q_lower or "def " in query):
            yield {
                "type": "status",
                "stage": "security_audit",
                "message": "🛡️ Z4 Nexus: Running enterprise SAST vulnerability & secrets inspection..."
            }

            audit_target = extracted_code or query
            audit_res = security_scanner.scan_code(audit_target)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "SAST_SECURITY_AUDIT",
                "security_score": audit_res["security_score"],
                "status": audit_res["status"],
                "total_issues": audit_res["total_issues"],
                "tools_used": ["sast_security_scanner", "llm_neural_core"]
            }

            prompt = (
                f"User requested Security Audit: '{query}'\n\n"
                f"SAST Scan Results:\n"
                f"- Security Score: {audit_res['security_score']}/100 ({audit_res['status']})\n"
                f"- Findings Count: {audit_res['total_issues']}\n"
                f"- Details: {json.dumps(audit_res['findings'], indent=2)}\n\n"
                "Provide a comprehensive, professional Security Audit Report in GitHub Markdown:\n"
                "1. Executive Summary & Security Score\n"
                "2. Breakdown of each vulnerability detected (Severity, Line, Impact)\n"
                "3. Secure, remediated code with zero vulnerabilities."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate(NEXUS_SYSTEM_PROMPT, prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🛡️ Z4 Nexus Security Audit\n\n**Score:** `{audit_res['security_score']}/100` ({audit_res['status']})\n\n**Total Issues:** `{audit_res['total_issues']}`"
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 2. AUTONOMOUS SELF-HEALING LOOP (AUTO-TEST & AUTO-FIX)
        # =========================================================================
        elif is_self_healing or (is_bug_fix and extracted_code):
            yield {
                "type": "status",
                "stage": "self_healing_loop",
                "message": "⚙️ Z4 Nexus: Executing autonomous self-healing test & repair loop..."
            }

            target_code = extracted_code or query
            detected_lang = polyglot_runner.detect_language(target_code)
            heal_res = self_healing_engine.heal_and_verify(
                code=target_code,
                language=detected_lang,
                intent=query
            )

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "AUTONOMOUS_SELF_HEALING",
                "status": heal_res["status"],
                "iterations": heal_res["iterations"],
                "execution_time_ms": heal_res["execution_time_ms"],
                "tools_used": ["self_healing_engine", "polyglot_runner", "llm_neural_core"]
            }

            prompt = (
                f"User Goal: {query}\n\n"
                f"Autonomous Self-Healing Verification Report:\n"
                f"- Status: {heal_res['status']}\n"
                f"- Iterations Required: {heal_res['iterations']}\n"
                f"- Test Output: {heal_res['test_output']}\n"
                f"- Runtime: {heal_res['execution_time_ms']} ms\n\n"
                f"Final Verified Code:\n```{detected_lang}\n{heal_res['final_code']}\n```\n\n"
                "Present the verified solution clearly with an explanation of root cause fixes and verification passes."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate(NEXUS_SYSTEM_PROMPT, prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = (
                    f"### ⚙️ Z4 Nexus Self-Healing Verification: `{heal_res['status']}`\n\n"
                    f"**Iterations:** `{heal_res['iterations']}` | **Runtime:** `{heal_res['execution_time_ms']} ms`\n\n"
                    f"```{detected_lang}\n{heal_res['final_code']}\n```"
                )
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 3. 1-CLICK FULL-STACK PROJECT SCAFFOLDING
        # =========================================================================
        elif is_scaffold:
            yield {
                "type": "status",
                "stage": "project_scaffolder",
                "message": "🚀 Z4 Nexus: Synthesizing multi-file full-stack project scaffold..."
            }

            scaffold_res = project_scaffolder.scaffold_project(
                project_name="app",
                template_or_description=query
            )

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "PROJECT_SCAFFOLDING",
                "project_name": scaffold_res["project_name"],
                "files_count": scaffold_res["files_count"],
                "stack": scaffold_res["stack_summary"],
                "tools_used": ["project_scaffolder", "llm_brain"]
            }

            prompt = (
                f"User Request: {query}\n\n"
                f"Generated Scaffold for Project: '{scaffold_res['project_name']}'\n"
                f"Tech Stack: {scaffold_res['stack_summary']}\n"
                f"Files Generated: {scaffold_res['files_count']}\n"
                f"Manifest:\n{json.dumps(scaffold_res['files'], indent=2)}\n\n"
                "Present the project structure in a clean ASCII tree, display key files with complete code, and provide step-by-step setup instructions."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate(NEXUS_SYSTEM_PROMPT, prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🚀 Z4 Nexus Project Scaffold: `{scaffold_res['project_name']}`\n\nGenerated `{scaffold_res['files_count']}` files for `{scaffold_res['stack_summary']}`."
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 4. SYSTEM ARCHITECTURE & SCHEMA VISUALIZER (MERMAID)
        # =========================================================================
        elif is_arch_diagram:
            yield {
                "type": "status",
                "stage": "arch_visualizer",
                "message": "📐 Z4 Nexus: Synthesizing system architecture & data modeling diagram..."
            }

            diag_type = "er_diagram" if ("er" in q_lower or "database" in q_lower or "schema" in q_lower) else ("sequence" if "sequence" in q_lower or "flow" in q_lower else "architecture")
            diag_res = arch_visualizer.generate_diagram(
                intent=query,
                diagram_type=diag_type
            )

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "ARCHITECTURE_DIAGRAM",
                "diagram_type": diag_type,
                "tools_used": ["arch_visualizer", "mermaid_engine", "llm_brain"]
            }

            full_answer = diag_res.get("full_response") or f"### 📐 Z4 Nexus Architecture Diagram\n\n{diag_res.get('mermaid_raw')}"
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 5. AUTONOMOUS GIT & CI/CD WORKFLOW
        # =========================================================================
        elif is_git:
            yield {
                "type": "status",
                "stage": "git_workflow",
                "message": "🌿 Z4 Nexus: Inspecting repository diffs & preparing Git release dossier..."
            }

            status = git_workflow.get_status()
            if "pr" in q_lower or "pull request" in q_lower:
                doc = git_workflow.generate_pr_dossier()
            else:
                doc = git_workflow.generate_commit_message(context_hint=query)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "GIT_WORKFLOW_RELEASE",
                "branch": status["branch"],
                "modified_files": status["modified_files"],
                "tools_used": ["git_workflow", "llm_brain"]
            }

            full_answer = f"### 🌿 Z4 Nexus Git Release Dossier\n\n**Current Branch:** `{status['branch']}` | **Modified Files:** `{len(status['modified_files'])}`\n\n{doc}"
            for tok in full_answer.split(" "):
                yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 6. CODEBASE KNOWLEDGE GRAPH & REPOSITORY INDEXER
        # =========================================================================
        elif is_repo_query:
            yield {
                "type": "status",
                "stage": "repo_indexer",
                "message": "🔍 Z4 Nexus: Traversing codebase AST & extracting workspace symbols..."
            }

            idx = repo_indexer.index_workspace_symbols(max_files=100)
            tree = repo_indexer.build_file_tree(max_depth=2)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "CODEBASE_AST_INDEX",
                "files_scanned": idx["files_scanned"],
                "total_loc": idx["total_loc"],
                "symbols_indexed": idx["symbols_indexed"],
                "tools_used": ["repo_indexer", "ast_parser"]
            }

            prompt = (
                f"User Query about Codebase: '{query}'\n\n"
                f"Repository Metrics:\n"
                f"- Files Scanned: {idx['files_scanned']}\n"
                f"- Total LOC: {idx['total_loc']}\n"
                f"- Symbols Indexed: {idx['symbols_indexed']}\n\n"
                f"Project Structure:\n```\n{tree}\n```\n\n"
                "Answer the user query thoroughly based on this codebase context."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate(NEXUS_SYSTEM_PROMPT, prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🔍 Codebase Index\n\n**Files:** `{idx['files_scanned']}` | **LOC:** `{idx['total_loc']}` | **Symbols:** `{idx['symbols_indexed']}`\n\n```\n{tree}\n```"
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 7. MULTI-LANGUAGE POLYGLOT SANDBOX EXECUTION
        # =========================================================================
        elif is_direct_exec and extracted_code:
            detected_lang = polyglot_runner.detect_language(extracted_code)
            yield {
                "type": "status",
                "stage": "polyglot_sandbox_exec",
                "message": f"⚡ Z4 Nexus: Executing {detected_lang.upper()} script in isolated runtime..."
            }

            exec_res = polyglot_runner.run(extracted_code, language=detected_lang)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "POLYGLOT_EXECUTION",
                "language": detected_lang,
                "success": exec_res["success"],
                "runtime_ms": exec_res["execution_time_ms"],
                "tools_used": ["polyglot_runner", "llm_brain"]
            }

            prompt = (
                f"User Query: '{query}'\n\n"
                f"Language: {detected_lang}\n"
                f"Code:\n```{detected_lang}\n{extracted_code}\n```\n\n"
                f"Execution Output:\n{exec_res['stdout'] or exec_res['stderr']}\n"
                f"Runtime: {exec_res['execution_time_ms']} ms (Exit Code: {exec_res['exit_code']})\n\n"
                "Explain the execution results with technical precision."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate(NEXUS_SYSTEM_PROMPT, prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = (
                    f"### ⚡ Z4 Nexus {detected_lang.upper()} Execution Results\n\n"
                    f"**Output:**\n```\n{exec_res['stdout'] or exec_res['stderr']}\n```\n\n"
                    f"⚡ Runtime: `{exec_res['execution_time_ms']} ms`"
                )
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 8. API INTEGRATION CLIENT GENERATOR
        # =========================================================================
        elif is_api:
            yield {
                "type": "status",
                "stage": "api_architect",
                "message": "⚙️ Z4 Nexus: Synthesizing production-grade API client & webhook handler..."
            }

            api_res = api_connector.generate_client(query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "API_INTEGRATION_CLIENT",
                "service_name": api_res.get("service_name"),
                "endpoints": api_res.get("endpoints", []),
                "code_snippet": api_res.get("client_code"),
                "tools_used": ["api_connector", "llm_brain"]
            }

            prompt = (
                f"You are Z4 Nexus, Senior API Architect. The user requested API integration: '{query}'.\n"
                f"Generated Service: {api_res.get('service_name')}\n"
                f"Client Code:\n```python\n{api_res.get('client_code')}\n```\n\n"
                "Explain the integration, how to configure credentials, and provide a clear usage example in Markdown."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate(NEXUS_SYSTEM_PROMPT, prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 🔌 Z4 Nexus API Integration: {api_res.get('service_name')}\n\n```python\n{api_res.get('client_code')}\n```"
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 9. SELF-EVOLVING DYNAMIC TOOL FORGE
        # =========================================================================
        elif is_tool_forge:
            yield {
                "type": "status",
                "stage": "tool_forge",
                "message": "⚙️ Z4 Nexus: Synthesizing custom tool with Z Sentinel AST validation..."
            }

            forge_res = tool_forge.forge_tool(tool_intent=query)
            yield {
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

            prompt = (
                f"You are Z4 Nexus, Senior Systems Architect. The user requested forging a tool: '{query}'.\n"
                f"Forged Tool Name: {forge_res.get('tool_name')}\n"
                f"Security Status: {forge_res.get('security_status')}\n"
                f"Generated Code:\n```python\n{forge_res.get('code')}\n```\n\n"
                f"Sandbox Test Output: {json.dumps(forge_res.get('test_output', {}))}\n"
                f"Runtime: {forge_res.get('runtime_ms')} ms\n\n"
                "Explain the tool architecture, security verification, and how it has been registered."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate(NEXUS_SYSTEM_PROMPT, prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = (
                    f"### 🛠️ Z4 Nexus Tool Forge: `{forge_res.get('tool_name')}`\n\n"
                    f"🛡️ **Security Audit:** `{forge_res.get('security_status')}`\n\n"
                    f"```python\n{forge_res.get('code')}\n```\n\n"
                    f"⚡ Runtime: `{forge_res.get('runtime_ms')} ms`"
                )
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 10. UNIVERSAL POLYGLOT SOFTWARE ENGINEERING (DEFAULT ROUTE)
        # =========================================================================
        else:
            yield {
                "type": "status",
                "stage": "code_architect",
                "message": "⚙️ Z4 Nexus: Formulating software architecture, optimal logic & production-ready code..."
            }

            # Enriched multi-file repository context if query mentions project/files
            repo_context = ""
            if any(k in q_lower for k in ["project", "file", "function", "class", "module", "component", "route", "service"]):
                repo_context = repo_indexer.get_context_for_query(query, max_chars=1500)

            yield {
                "type": "meta",
                "agent": "Z4 Nexus (Polyglot Software Engineer)",
                "task_type": "POLYGLOT_SOFTWARE_ENGINEERING",
                "tools_used": ["polyglot_code_architect", "system_designer", "repo_indexer", "llm_neural_core"]
            }

            prompt = (
                f"User Request: {query}\n\n"
                f"{('Codebase Context:\n' + repo_context + '\n\n') if repo_context else ''}"
                "As Z4 Nexus Senior Polyglot Software Engineer & Code Architect:\n"
                "1. Deliver a complete, robust, production-ready solution in the requested language/framework.\n"
                "2. Provide full code with zero missing placeholders or TODOs.\n"
                "3. If algorithms or data structures are involved, analyze Time & Space Complexity (Big-O).\n"
                "4. Include usage examples, testing tips, and clear markdown documentation."
            )

            full_answer = ""
            if llm_brain.is_available:
                for chunk in llm_brain.stream_generate(NEXUS_SYSTEM_PROMPT, prompt):
                    full_answer += chunk
                    yield {"type": "token", "content": chunk}
            else:
                full_answer = f"### 💻 Z4 Nexus Code Architecture\n\n```\n// Solution for: {query}\n```"
                for tok in full_answer.split(" "):
                    yield {"type": "token", "content": tok + " "}

            yield {"type": "done", "answer": full_answer}

z4_nexus_agent = Z4NexusAgent()
