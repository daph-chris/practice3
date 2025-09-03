# agents/agent4_security_scanner.py
import subprocess, json

def run(repo_path: str) -> dict:
    try:
        result = subprocess.run(
            ["bandit", "-r", repo_path, "-f", "json"],
            capture_output=True, text=True
        )
        findings = json.loads(result.stdout or "{}").get("results", [])
        return {
            "agent": "Security Scanner",
            "summary": f"{len(findings)} security issues",
            "details": findings,
            "severity": "Critical" if findings else "Low",
            "recommendations": "Fix insecure code patterns, sanitize inputs"
        }
    except Exception as e:
        return {"agent": "Security Scanner", "error": str(e)}
