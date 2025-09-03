# agents/agent1_static_analysis.py
import subprocess, json

def run(repo_path: str) -> dict:
    try:
        result = subprocess.run(
            ["pylint", repo_path, "--output-format=json"],
            capture_output=True, text=True, check=False
        )
        findings = json.loads(result.stdout or "[]")
        return {
            "agent": "Static Analysis",
            "summary": f"{len(findings)} issues found",
            "details": findings,
            "severity": "High" if len(findings) > 20 else "Medium",
            "recommendations": "Fix code style, refactor functions, follow PEP8"
        }
    except Exception as e:
        return {"agent": "Static Analysis", "error": str(e)}
