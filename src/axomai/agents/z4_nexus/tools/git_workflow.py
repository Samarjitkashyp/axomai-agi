"""
Z4 Nexus - Autonomous Git, PR & CI/CD Workflow Engine.
Inspects repository diffs, synthesizes Conventional Commits, authors GitHub Pull Request
dossiers, and performs CI preflight sanity checks before code merges.
"""

import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from axomai.core.llm import llm_brain

class GitWorkflow:
    """Enterprise Git & CI/CD automation assistant."""

    def __init__(self, repo_path: str = "e:/axomai_agi"):
        self.repo_path = repo_path
        self.git_bin = shutil.which("git") or "git"

    def _run_git(self, args: List[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            [self.git_bin] + args,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

    def get_status(self) -> Dict[str, Any]:
        """Gets Git status including branch, staged, modified, untracked files."""
        res_branch = self._run_git(["branch", "--show-current"])
        branch = res_branch.stdout.strip() or "main"

        res_status = self._run_git(["status", "--porcelain"])
        lines = res_status.stdout.strip().splitlines()

        staged, modified, untracked = [], [], []
        for line in lines:
            if not line:
                continue
            code = line[:2]
            file_path = line[3:].strip()
            if code[0] in ["M", "A", "D", "R"]:
                staged.append(file_path)
            if code[1] == "M":
                modified.append(file_path)
            elif code == "??":
                untracked.append(file_path)

        return {
            "branch": branch,
            "is_clean": len(lines) == 0,
            "staged_count": len(staged),
            "staged_files": staged,
            "modified_count": len(modified),
            "modified_files": modified,
            "untracked_count": len(untracked),
            "untracked_files": untracked
        }

    def get_diff(self, staged: bool = False, max_chars: int = 4000) -> str:
        """Gets current git diff."""
        args = ["diff", "--cached"] if staged else ["diff"]
        res = self._run_git(args)
        diff_text = res.stdout.strip()
        if not diff_text and not staged:
            # Try staged
            res_staged = self._run_git(["diff", "--cached"])
            diff_text = res_staged.stdout.strip()
        return diff_text[:max_chars]

    def generate_commit_message(self, context_hint: str = "") -> str:
        """Generates a Conventional Commit message based on git diff."""
        diff = self.get_diff(max_chars=3000)
        status = self.get_status()

        if not diff and status["is_clean"]:
            return "chore: no active changes detected"

        if not llm_brain.is_available:
            return f"feat(agent): update {', '.join(status['modified_files'][:3]) or 'codebase'}"

        prompt = (
            f"Git Status:\nBranch: {status['branch']}\n"
            f"Modified Files: {status['modified_files']}\n"
            f"Diff Excerpt:\n```diff\n{diff}\n```\n\n"
            f"User Intent: {context_hint}\n\n"
            "Generate a professional Conventional Commit message in this format:\n"
            "<type>(<scope>): <short imperative subject line>\n\n"
            "- <detailed bullet 1>\n- <detailed bullet 2>\n\n"
            "Output the commit message text directly."
        )

        res = llm_brain.generate("You are Z4 Nexus Git Release Engineer.", prompt, temperature=0.1)
        return res.strip()

    def generate_pr_dossier(self, target_branch: str = "main") -> str:
        """Generates a GitHub Pull Request description in Markdown."""
        diff = self.get_diff(max_chars=4000)
        status = self.get_status()

        prompt = (
            f"Branch: {status['branch']} -> Target: {target_branch}\n"
            f"Modified Files: {status['modified_files'] + status['staged_files']}\n"
            f"Diff:\n```diff\n{diff}\n```\n\n"
            "Write a production-ready GitHub Pull Request description with:\n"
            "## 📌 Overview & Motivation\n"
            "## 🚀 Key Changes\n"
            "## 🧪 Verification & Test Results\n"
            "## 🛡️ Risk Assessment & Rollback Plan\n"
        )

        if not llm_brain.is_available:
            return (
                f"## 📌 PR: Changes on branch `{status['branch']}`\n\n"
                f"- Modified {len(status['modified_files'])} files.\n"
                f"- Ready for review."
            )

        res = llm_brain.generate("You are Z4 Nexus Lead Software Architect.", prompt, temperature=0.2)
        return res.strip()

git_workflow = GitWorkflow()
