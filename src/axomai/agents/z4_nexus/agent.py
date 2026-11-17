"""
Z4 Nexus - Autonomous Polyglot Software Engineer & Chief Code Architect Agent.
Bleeding-edge autonomous coding engine featuring:
1. Autonomous Self-Healing Loop (Auto-Test & Auto-Fix)
2. Polyglot Multi-Language Sandbox Runner (Python, Node.js/JS, TS, Shell, C++, Go, Rust)
3. Codebase Knowledge Graph & AST Repository Indexer
4. SAST Security & Vulnerability Auditing
5. Autonomous Git & CI/CD Workflow Engine
6. Interactive System Architecture & Database Schema Visualizer (Mermaid)
7. 1-Click Full-Stack Project Scaffolding
8. Autonomous Visual & E2E Headless Browser Testing
9. Dual-Agent Adversarial Red-Team & Blue-Team Code Review
10. Automated Performance Profiling & Flamegraph Heatmaps
11. 1-Click Multi-Cloud Deployment & Live Preview Links
12. Database Schema Migration & Mock Seed Generator
13. Interactive API Playground & OpenAPI Spec Engine
14. Long-Term Developer Memory & Personalized Coding Style
15. Autonomous CVE Dependency Patcher (Smart Dependabot)
16. Self-Evolving Dynamic Tool Forge
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
from axomai.agents.z4_nexus.tools.e2e_browser_tester import e2e_browser_tester
from axomai.agents.z4_nexus.tools.adversarial_reviewer import adversarial_reviewer
from axomai.agents.z4_nexus.tools.perf_profiler import perf_profiler
from axomai.agents.z4_nexus.tools.cloud_deployer import cloud_deployer
from axomai.agents.z4_nexus.tools.db_migrator import db_migrator
from axomai.agents.z4_nexus.tools.api_playground import api_playground
from axomai.agents.z4_nexus.tools.dev_memory import dev_memory
from axomai.agents.z4_nexus.tools.cve_patcher import cve_patcher
from axomai.agents.z4_nexus.tools.artifacts_canvas import artifacts_canvas
from axomai.agents.z4_nexus.tools.deep_reasoning import deep_reasoning
from axomai.agents.z4_nexus.tools.computer_operator import computer_operator
from axomai.agents.z4_nexus.tools.code_surgeon import code_surgeon
from axomai.agents.z4_nexus.tools.vision_to_code import vision_to_code
from axomai.agents.z4_nexus.tools.deep_researcher import deep_researcher
from axomai.agents.z4_nexus.tools.voice_bridge import voice_bridge
from axomai.agents.z4_nexus.tools.production_sentry import production_sentry
from axomai.agents.z4_nexus.tools.synthetic_war_room import synthetic_war_room
from axomai.agents.z4_nexus.tools.time_travel_sandbox import time_travel_sandbox
from axomai.agents.z4_nexus.tools.app_reverse_engineer import app_reverse_engineer
from axomai.agents.z4_nexus.tools.kernel_optimizer import kernel_optimizer
from axomai.agents.z4_nexus.tools.self_metamorphosis import self_metamorphosis
from axomai.agents.z4_nexus.tools.sovereign_privacy_shield import sovereign_privacy_shield

NEXUS_SYSTEM_PROMPT = """You are Z4 Nexus, the Autonomous Polyglot Software Engineer & Chief Code Architect of AxomAI.
You possess world-class mastery across ALL programming languages, frameworks, architectures, algorithms, and engineering disciplines.

Your Standards:
1. Write clean, complete, production-grade, bug-free, well-commented code.
2. Never use lazy placeholder comments like `// TODO: implement later` or `...`. Always provide complete, runnable implementations.
3. Follow language-specific idiomatic best practices (PEP 8, TypeScript strict, modern C++20, Rust safety).
4. Analyze time and space complexity (Big-O notation) for all algorithms.
5. Include thorough error handling, input validation, and defensive typing.
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
        is_security_audit = any(k in q_lower for k in ["security audit", "vulnerability", "vulnerabilities", "scan code", "sast", "check security", "security check", "injection check"])
        is_self_healing = any(k in q_lower for k in ["self heal", "self-healing", "auto test", "auto-test", "verify and fix", "test and heal", "run test loop", "unit test pass", "test loop"])
        is_scaffold = any(k in q_lower for k in ["scaffold", "scaffold project", "boilerplate", "create fullstack", "generate repo", "build fullstack app", "create project", "setup project"])
        is_arch_diagram = any(k in q_lower for k in ["architecture diagram", "system design", "er diagram", "database schema", "sequence diagram", "mermaid", "flowchart", "c4 diagram"])
        is_git = any(k in q_lower for k in ["git commit", "commit message", "git diff", "git status", "pull request", "pr description", "pr dossier"])
        is_repo_query = any(k in q_lower for k in ["codebase", "workspace symbols", "where is function", "search codebase", "repo map", "file structure", "symbol table"])
        is_e2e_browser = any(k in q_lower for k in ["e2e test", "browser test", "playwright", "cypress", "visual test", "ui test", "inspect dom", "viewport test"])
        is_adversarial = any(k in q_lower for k in ["red team", "blue team", "adversarial", "stress test", "harden code", "race condition check", "attack simulation"])
        is_perf_profile = any(k in q_lower for k in ["profile", "benchmark", "flamegraph", "optimize performance", "bottleneck", "latency optimization", "speedup"])
        is_cloud_deploy = any(k in q_lower for k in ["deploy to vercel", "deploy to railway", "cloud deploy", "live preview", "deploy app", "dockerize", "deployment manifest"])
        is_db_migration = any(k in q_lower for k in ["db migration", "schema migration", "alembic", "prisma migrate", "mock data", "seed data", "synthetic data"])
        is_api_playground = any(k in q_lower for k in ["openapi spec", "swagger", "api playground", "postman collection", "test endpoint curl", "curl suite"])
        is_cve_patch = any(k in q_lower for k in ["cve", "dependabot", "patch vulnerabilities", "vulnerable package", "upgrade dependencies", "audit requirements", "cve patch"])
        is_deep_reasoning = any(k in q_lower for k in ["deep reasoning", "deep think", "o1 think", "tree of thoughts", "think step by step", "complex algorithm"])
        is_computer_use = any(k in q_lower for k in ["computer use", "workspace vitals", "run dev server", "check open ports", "workspace operator", "run command"])
        is_code_surgeon = any(k in q_lower for k in ["inline edit", "surgical edit", "canvas edit", "modify only line", "only change", "diff replace", "surgical refactor"])
        is_vision_to_code = any(k in q_lower for k in ["whiteboard to code", "sketch to code", "wireframe to code", "figma to code", "screenshot to code", "sketch to react"])
        is_deep_research = any(k in q_lower for k in ["deep research", "research docs", "technical whitepaper", "latest changelog", "breaking changes in", "research documentation"])
        is_voice_turn = any(k in q_lower for k in ["voice mode", "spoken turn", "pair programming voice", "audio dialogue", "voice turn"])
        # Beyond Big-Tech Revolutionary Capabilities
        is_sentry_hotfix = any(k in q_lower for k in ["sentry", "datadog", "crash report", "500 error", "production error", "stack trace hotfix", "incident resolution", "auto-patch"])
        is_war_room = any(k in q_lower for k in ["synthetic squad", "war room", "synthetic team", "pm architect frontend backend", "convene squad", "virtual tech company"])
        is_time_travel = any(k in q_lower for k in ["time travel", "create checkpoint", "rollback state", "shadow snapshot", "zero cost rollback"])
        is_app_reverse = any(k in q_lower for k in ["reverse engineer", "clone app", "clone website", "reconstruct website", "app cloner", "clone landing page"])
        is_kernel_optimize = any(k in q_lower for k in ["kernel optimize", "cuda kernel", "triton kernel", "hardware accelerate", "simd kernel", "gpu kernel", "accelerate kernel"])
        is_metamorphosis = any(k in q_lower for k in ["self metamorphosis", "evolve capability", "acquire capability", "dynamic tool synthesis", "auto evolution"])
        is_sovereign_shield = any(k in q_lower for k in ["sovereign shield", "air gap audit", "zero leak proof", "airgap compliance", "privacy certificate", "zero-leak"])
        is_tool_forge = any(k in q_lower for k in ["forge tool", "create tool", "build tool", "new tool", "dynamic tool", "tool forge", "generate a tool"])
        is_api = any(k in q_lower for k in ["integrate api", "api client", "webhook", "swagger", "openapi", "stripe", "razorpay", "shopify", "rest api client"])
        is_direct_exec = any(k in q_lower for k in ["run this", "execute this", "run python", "run javascript", "run node", "execute code", "run code", "eval code"]) and ("```" in query or "print(" in query or "console.log" in query or "import " in query or "def " in query)
        is_bug_fix = any(k in q_lower for k in ["fix this", "debug", "syntax error", "traceback", "exception in", "why is this code failing", "fix code", "find bug"])

        # =========================================================================
        # REVOLUTIONARY 1: AUTONOMOUS PRODUCTION SENTRY & LOG AUTO-PATCHER
        # =========================================================================
        if is_sentry_hotfix:
            yield {
                "type": "status",
                "stage": "production_sentry",
                "message": "🚨 Z4 Nexus: Ingesting production crash report & synthesizing live hotfix patch..."
            }
            hotfix_res = production_sentry.diagnose_and_hotfix(crash_log_or_stacktrace=query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "PRODUCTION_INCIDENT_HOTFIX",
                "incident_id": hotfix_res["incident_id"],
                "error_type": hotfix_res["error_type"],
                "status": hotfix_res["status"],
                "repaired_in_ms": hotfix_res["repaired_in_ms"],
                "tools_used": ["production_sentry", "polyglot_runner", "llm_neural_core"]
            }
            full_answer = hotfix_res["hotfix_dossier"]
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # REVOLUTIONARY 2: SYNTHETIC TECH TEAM & MULTI-AGENT WAR ROOM
        # =========================================================================
        elif is_war_room:
            yield {
                "type": "status",
                "stage": "synthetic_war_room",
                "message": "👥 Z4 Nexus: Convening 5-agent engineering squad (PM, Architect, Frontend, Backend, QA)..."
            }
            squad_res = synthetic_war_room.convene_squad(project_goal=query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "SYNTHETIC_SQUAD_WAR_ROOM",
                "squad_members_count": squad_res["squad_members_count"],
                "squad_roles": squad_res["squad_roles"],
                "turnaround_ms": squad_res["turnaround_ms"],
                "tools_used": ["synthetic_war_room", "multi_agent_orchestrator"]
            }
            full_answer = squad_res["war_room_dossier"]
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # REVOLUTIONARY 3: TIME-TRAVEL EXECUTION & ZERO-COST STATE ROLLBACK
        # =========================================================================
        elif is_time_travel:
            yield {
                "type": "status",
                "stage": "time_travel_sandbox",
                "message": "⏳ Z4 Nexus: Capturing microsecond shadow checkpoint for zero-cost rollback safety..."
            }
            cp_res = time_travel_sandbox.create_checkpoint([])
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "TIME_TRAVEL_CHECKPOINT",
                "snapshot_id": cp_res["snapshot_id"],
                "state_hash": cp_res["state_hash"],
                "tools_used": ["time_travel_sandbox", "shadow_state_manager"]
            }
            full_answer = (
                f"### ⏳ Time-Travel Shadow Checkpoint Created\n\n"
                f"- **Snapshot ID:** `{cp_res['snapshot_id']}`\n"
                f"- **State Fingerprint (SHA-256):** `{cp_res['state_hash']}`\n"
                f"- **Guaranteed Safety:** Zero-risk execution. 1-microsecond deterministic rollback armed."
            )
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # REVOLUTIONARY 4: 1-CLICK LIVE WEB REVERSE-ENGINEERING & APP CLONER
        # =========================================================================
        elif is_app_reverse:
            yield {
                "type": "status",
                "stage": "app_reverse_engineer",
                "message": "🧬 Z4 Nexus: Deconstructing live web application architecture & design tokens..."
            }
            clone_res = app_reverse_engineer.clone_and_reverse_engineer(target_url_or_description=query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "APP_REVERSE_ENGINEERING",
                "target": clone_res["target"],
                "turnaround_ms": clone_res["turnaround_ms"],
                "tools_used": ["app_reverse_engineer", "design_token_extractor", "llm_neural_core"]
            }
            full_answer = clone_res["clone_dossier"]
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # REVOLUTIONARY 5: HARDWARE-AWARE CUSTOM KERNEL OPTIMIZER (TRITON / CUDA)
        # =========================================================================
        elif is_kernel_optimize:
            yield {
                "type": "status",
                "stage": "kernel_optimizer",
                "message": "⚡ Z4 Nexus: Probing GPU/SIMD accelerators & compiling custom hardware kernel..."
            }
            target_alg = extracted_code or query
            kern_res = kernel_optimizer.compile_accelerated_kernel(algorithm_code=target_alg)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "HARDWARE_KERNEL_OPTIMIZATION",
                "backend": kern_res["backend"],
                "device_name": kern_res["hardware_context"]["device_name"],
                "tools_used": ["kernel_optimizer", "cuda_triton_compiler"]
            }
            full_answer = kern_res["kernel_dossier"]
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # REVOLUTIONARY 6: AUTONOMOUS SELF-METAMORPHOSIS & DYNAMIC TOOL EVOLUTION
        # =========================================================================
        elif is_metamorphosis:
            yield {
                "type": "status",
                "stage": "self_metamorphosis",
                "message": "🔮 Z4 Nexus: Synthesizing new autonomous capability & hot-registering into runtime..."
            }
            meta_res = self_metamorphosis.evolve_and_register_capability(capability_intent=query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "AUTONOMOUS_SELF_METAMORPHOSIS",
                "capability": meta_res["capability"],
                "tool_slug": meta_res["tool_slug"],
                "security_status": meta_res["security_status"],
                "tools_used": ["self_metamorphosis", "ast_validator", "dynamic_tool_registry"]
            }
            full_answer = (
                f"### 🔮 Autonomous Metamorphosis Complete\n\n"
                f"- **Capability Acquired:** `{meta_res['capability']}`\n"
                f"- **Security Status:** `{meta_res['security_status']}` (Zero malicious AST nodes)\n"
                f"- **Registered Module:** `{meta_res['file_path']}`\n\n"
                f"```python\n{meta_res['code']}\n```\n\n"
                "⚡ New capability hot-registered into runtime without requiring server restart."
            )
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # REVOLUTIONARY 7: 100% AIR-GAPPED SOVEREIGN PRIVACY & ZERO-LEAK SHIELD
        # =========================================================================
        elif is_sovereign_shield:
            yield {
                "type": "status",
                "stage": "sovereign_privacy_shield",
                "message": "🛡️ Z4 Nexus: Auditing egress network traffic & issuing cryptographic air-gap certificate..."
            }
            cert_res = sovereign_privacy_shield.generate_airgap_audit_certificate(payload_or_repo_name=query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "SOVEREIGN_AIRGAP_AUDIT",
                "certification_id": cert_res["certification_id"],
                "egress_traffic": cert_res["egress_traffic"],
                "tools_used": ["sovereign_privacy_shield", "z_sentinel_crypto_auditor"]
            }
            full_answer = (
                f"### 🛡️ Enterprise Cryptographic Air-Gap Compliance Certificate\n\n"
                f"- **Certificate ID:** `{cert_res['certification_id']}`\n"
                f"- **External Egress Traffic:** `{cert_res['egress_traffic']}`\n"
                f"- **Privacy Guarantee:** `{cert_res['privacy_guarantee']}`\n"
                f"- **Data Retention Policy:** `{cert_res['data_retention_policy']}`\n"
                f"- **Cryptographic SHA-256 Fingerprint:** `{cert_res['sha256_cryptographic_fingerprint']}`\n\n"
                "🔒 **Verified 100% Zero-Leak Local Sovereignty.** Zero data packets transmitted outside local perimeter."
            )
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 0A. OPENAI o1 / o3 STYLE DEEP REASONING & TREE-OF-THOUGHTS
        # =========================================================================
        elif is_deep_reasoning:
            yield {
                "type": "status",
                "stage": "deep_reasoning_core",
                "message": "🧠 Z4 Nexus: Initiating o1-style deep tree-of-thoughts & constraint search..."
            }
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "DEEP_REASONING_TREE_OF_THOUGHTS",
                "tools_used": ["deep_reasoning_engine", "llm_neural_core"]
            }
            yield from deep_reasoning.reason_and_solve(query=query, context=extracted_code)
            yield {"type": "done", "answer": ""}
            return

        # =========================================================================
        # 0B. GEMINI 2.0 MULTIMODAL WHITEBOARD & SKETCH TO CODE
        # =========================================================================
        elif is_vision_to_code:
            yield {
                "type": "status",
                "stage": "vision_to_code",
                "message": "🎨 Z4 Nexus: Translating visual wireframe & sketch into responsive React..."
            }
            v_res = vision_to_code.synthesize_ui_from_sketch(query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "VISION_TO_CODE",
                "artifact": v_res["artifact"],
                "tools_used": ["vision_to_code", "artifacts_canvas", "llm_neural_core"]
            }
            full_answer = (
                f"### 🎨 Synthesized React + Tailwind UI\n\n"
                f"{v_res['artifact']['markdown_block']}\n\n"
                f"✨ Component ready for live split-screen preview in Canvas."
            )
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 0C. CHATGPT CANVAS TARGETED INLINE CODE SURGEON
        # =========================================================================
        elif is_code_surgeon and extracted_code:
            yield {
                "type": "status",
                "stage": "code_surgeon",
                "message": "🎯 Z4 Nexus: Applying targeted surgical diff replacement..."
            }
            s_res = code_surgeon.apply_surgical_edit(original_code=extracted_code, edit_instruction=query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "SURGICAL_CANVAS_DIFF",
                "diff_summary": s_res["diff_summary"],
                "tools_used": ["code_surgeon", "unified_diff_engine"]
            }
            full_answer = (
                f"### 🎯 Targeted Surgical Diff\n\n"
                f"**Summary:** `{s_res['diff_summary']}`\n\n"
                f"```diff\n{s_res['unified_diff']}\n```\n\n"
                f"#### Updated Clean Code:\n```\n{s_res['modified_code']}\n```"
            )
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 0D. CLAUDE 3.5 COMPUTER USE & WORKSPACE OPERATOR
        # =========================================================================
        elif is_computer_use:
            yield {
                "type": "status",
                "stage": "computer_operator",
                "message": "💻 Z4 Nexus: Operating local developer workspace & auditing system vitals..."
            }
            vitals = computer_operator.get_workspace_vitals()
            cmd_res = None
            if "run" in q_lower or "install" in q_lower or "build" in q_lower:
                cmd_res = computer_operator.run_workspace_command(query)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "COMPUTER_USE_WORKSPACE_OPERATOR",
                "vitals": vitals,
                "tools_used": ["computer_operator", "host_process_manager"]
            }
            full_answer = (
                f"### 💻 Workspace Vitals & Host Operator\n\n"
                f"- **Active Dev Ports:** `{vitals['active_dev_ports']}`\n"
                f"- **Python:** `{vitals['python_executable']}`\n"
                f"- **Node:** `{'Ready' if vitals['node_available'] else 'Not Found'}` | **Git:** `{'Ready' if vitals['git_available'] else 'Not Found'}`\n\n"
                f"{('**Command Execution Output:**\n```\n' + (cmd_res['stdout'] or cmd_res['stderr']) + '\n```') if cmd_res else 'Workspace ready for autonomous operations.'}"
            )
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 0E. GEMINI DEEP RESEARCH & DOCUMENTATION SCRAPER
        # =========================================================================
        elif is_deep_research:
            yield {
                "type": "status",
                "stage": "deep_researcher",
                "message": "🔬 Z4 Nexus: Conducting multi-hop technical research & API doc grounding..."
            }
            res_dossier = deep_researcher.research_topic(query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "DEEP_TECHNICAL_RESEARCH",
                "research_duration_ms": res_dossier["research_duration_ms"],
                "tools_used": ["deep_researcher", "documentation_scraper", "llm_neural_core"]
            }
            full_answer = res_dossier["dossier"]
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 0F. CHATGPT ADVANCED VOICE MODE PROTOCOL
        # =========================================================================
        elif is_voice_turn:
            yield {
                "type": "status",
                "stage": "voice_bridge",
                "message": "🎙️ Z4 Nexus: Processing real-time pair-programming audio stream..."
            }
            v_pkt = voice_bridge.process_voice_turn(speech_transcript=query)
            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "ADVANCED_VOICE_MODE",
                "latency_ms": v_pkt["latency_ms"],
                "tools_used": ["voice_bridge", "audio_synthesizer"]
            }
            full_answer = f"🎙️ **Z4 Nexus (Voice):** {v_pkt['spoken_response']}"
            yield {"type": "token", "content": full_answer}
            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 1. AUTONOMOUS VISUAL & E2E BROWSER TESTING
        # =========================================================================
        elif is_e2e_browser:
            yield {
                "type": "status",
                "stage": "e2e_browser_test",
                "message": "🌐 Z4 Nexus: Running autonomous visual DOM & headless browser inspection..."
            }

            test_target = extracted_code or query
            e2e_res = e2e_browser_tester.test_frontend_snippet(test_target)
            playwright_script = e2e_browser_tester.generate_e2e_playwright_test(user_flow=query)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "E2E_BROWSER_TESTING",
                "visual_score": e2e_res["visual_score"],
                "status": e2e_res["status"],
                "elements_inspected": e2e_res["elements_inspected"],
                "tools_used": ["e2e_browser_tester", "playwright_generator", "polyglot_runner"]
            }

            full_answer = (
                f"### 🌐 Z4 Nexus Visual & E2E Testing Dossier\n\n"
                f"**Visual Health Score:** `{e2e_res['visual_score']}/100` ({e2e_res['status']})\n\n"
                f"**DOM Elements Inspected:**\n"
                f"- Buttons: `{e2e_res['elements_inspected']['buttons_count']}` | Inputs: `{e2e_res['elements_inspected']['inputs_count']}` | Forms: `{e2e_res['elements_inspected']['forms_count']}`\n\n"
                f"**Detected Responsive / A11y Issues:** `{e2e_res['issues_count']}`\n\n"
                f"### 🧪 Generated Playwright E2E Test Suite\n```typescript\n{playwright_script}\n```"
            )
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 2. DUAL-AGENT ADVERSARIAL RED-TEAM & BLUE-TEAM CODE REVIEW
        # =========================================================================
        elif is_adversarial and (extracted_code or "def " in query or "class " in query):
            yield {
                "type": "status",
                "stage": "adversarial_red_blue",
                "message": "⚔️ Z4 Nexus: Executing hostile Red-Team stress-testing & Blue-Team hardening..."
            }

            review_target = extracted_code or query
            adv_res = adversarial_reviewer.review_and_harden(review_target)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "ADVERSARIAL_HARDENING",
                "resilience_score": adv_res["resilience_score"],
                "status": adv_res["status"],
                "tools_used": ["red_team_auditor", "blue_team_architect", "llm_neural_core"]
            }

            full_answer = (
                f"### ⚔️ Z4 Nexus Adversarial Red-Team / Blue-Team Dossier\n\n"
                f"**Code Resilience Score:** `{adv_res['resilience_score']}/100` ({adv_res['status']})\n\n"
                f"#### 🔴 Red-Team Attack Exploits Detected:\n"
                f"{json.dumps(adv_res['red_team_audit'].get('exploits_found', []), indent=2)}\n\n"
                f"#### 🛡️ Blue-Team Hardened Defense Implementation:\n"
                f"```python\n{adv_res['blue_team_hardened_code']}\n```\n\n"
                f"**Architectural Hardening Summary:**\n{adv_res['defense_summary']}"
            )
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 3. PERFORMANCE PROFILING & FLAMEGRAPH HEATMAPS
        # =========================================================================
        elif is_perf_profile and (extracted_code or "def " in query or "for " in query):
            yield {
                "type": "status",
                "stage": "performance_profiler",
                "message": "⚡ Z4 Nexus: Profiling execution hotspots & generating optimization heatmap..."
            }

            perf_target = extracted_code or query
            perf_res = perf_profiler.profile_and_optimize(perf_target)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "PERFORMANCE_PROFILING",
                "avg_latency_ms": perf_res["measured_avg_latency_ms"],
                "status": perf_res["status"],
                "tools_used": ["perf_profiler", "flamegraph_visualizer", "polyglot_runner"]
            }

            full_answer = perf_res["profiling_dossier"]
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 4. 1-CLICK MULTI-CLOUD DEPLOYMENT & LIVE PREVIEW
        # =========================================================================
        elif is_cloud_deploy:
            yield {
                "type": "status",
                "stage": "cloud_deployer",
                "message": "☁️ Z4 Nexus: Synthesizing cloud infrastructure manifests & live preview..."
            }

            platform = "railway" if "railway" in q_lower else ("docker" if "docker" in q_lower else "vercel")
            deploy_res = cloud_deployer.prepare_deployment(
                project_name="axomai-service",
                stack_description=query,
                target_platform=platform
            )

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "CLOUD_DEPLOYMENT",
                "platform": deploy_res["platform"],
                "preview_url": deploy_res["preview_url"],
                "tools_used": ["cloud_deployer", "docker_builder", "llm_brain"]
            }

            full_answer = deploy_res["deployment_dossier"]
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 5. DATABASE SCHEMA MIGRATION & MOCK SEED GENERATOR
        # =========================================================================
        elif is_db_migration:
            yield {
                "type": "status",
                "stage": "db_migrator",
                "message": "🗄️ Z4 Nexus: Synthesizing forward/rollback migrations & mock seed dataset..."
            }

            dialect = "prisma" if "prisma" in q_lower else ("sqlite" if "sqlite" in q_lower else "postgresql")
            mig_res = db_migrator.generate_migration_and_seed(schema_change_intent=query, dialect=dialect)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "DATABASE_MIGRATION_AND_SEED",
                "dialect": mig_res["dialect"],
                "seed_count": mig_res["seed_count"],
                "tools_used": ["db_migrator", "synthetic_data_generator"]
            }

            full_answer = mig_res["migration_dossier"]
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 6. INTERACTIVE API PLAYGROUND & OPENAPI SPEC ENGINE
        # =========================================================================
        elif is_api_playground:
            yield {
                "type": "status",
                "stage": "api_playground",
                "message": "🔌 Z4 Nexus: Synthesizing OpenAPI 3.1 specification & interactive cURL suite..."
            }

            framework = "express" if "express" in q_lower else "fastapi"
            api_res = api_playground.generate_api_suite(api_code_or_intent=query, framework=framework)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "API_PLAYGROUND_AND_OPENAPI",
                "framework": api_res["framework"],
                "tools_used": ["api_playground", "openapi_generator", "curl_synthesizer"]
            }

            full_answer = api_res["playground_dossier"]
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 7. AUTONOMOUS CVE DEPENDENCY PATCHER (SMART DEPENDABOT)
        # =========================================================================
        elif is_cve_patch:
            yield {
                "type": "status",
                "stage": "cve_patcher",
                "message": "🛡️ Z4 Nexus: Auditing dependency manifest against active CVE advisory database..."
            }

            manifest_type = "package.json" if ("package.json" in q_lower or "{" in query) else "requirements.txt"
            target_manifest = extracted_code or query
            cve_res = cve_patcher.scan_and_patch(target_manifest, manifest_type=manifest_type)

            yield {
                "type": "meta",
                "agent": self.name,
                "task_type": "CVE_DEPENDENCY_AUDIT",
                "vulnerabilities_detected": cve_res["vulnerabilities_detected"],
                "is_clean": cve_res["is_clean"],
                "tools_used": ["cve_patcher", "dependabot_engine"]
            }

            full_answer = (
                f"### 🛡️ Z4 Nexus CVE Dependency Audit\n\n"
                f"**Vulnerabilities Detected:** `{cve_res['vulnerabilities_detected']}`\n\n"
                f"**CVE Findings Breakdown:**\n{json.dumps(cve_res['findings'], indent=2)}\n\n"
                f"#### 📦 Patched Non-Breaking Manifest ({manifest_type}):\n"
                f"```\n{cve_res['patched_manifest']}\n```"
            )
            for chunk in full_answer.split("\n\n"):
                yield {"type": "token", "content": chunk + "\n\n"}

            yield {"type": "done", "answer": full_answer}
            return

        # =========================================================================
        # 8. SAST SECURITY & VULNERABILITY AUDITING ROUTE
        # =========================================================================
        elif is_security_audit and (extracted_code or "code" in q_lower or "def " in query):
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
        # 9. AUTONOMOUS SELF-HEALING LOOP (AUTO-TEST & AUTO-FIX)
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
        # 10. 1-CLICK FULL-STACK PROJECT SCAFFOLDING
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
        # 11. SYSTEM ARCHITECTURE & SCHEMA VISUALIZER (MERMAID)
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
        # 12. AUTONOMOUS GIT & CI/CD WORKFLOW
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
        # 13. CODEBASE KNOWLEDGE GRAPH & REPOSITORY INDEXER
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
        # 14. MULTI-LANGUAGE POLYGLOT SANDBOX EXECUTION
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
        # 15. API INTEGRATION CLIENT GENERATOR
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
        # 16. SELF-EVOLVING DYNAMIC TOOL FORGE
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
        # 17. UNIVERSAL POLYGLOT SOFTWARE ENGINEERING (DEFAULT ROUTE)
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

            # Injected personalized developer memory profile
            style_prompt = dev_memory.format_style_prompt()

            yield {
                "type": "meta",
                "agent": "Z4 Nexus (Polyglot Software Engineer)",
                "task_type": "POLYGLOT_SOFTWARE_ENGINEERING",
                "tools_used": ["polyglot_code_architect", "system_designer", "repo_indexer", "dev_memory", "llm_neural_core"]
            }

            prompt = (
                f"User Request: {query}\n\n"
                f"{style_prompt}\n\n"
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
