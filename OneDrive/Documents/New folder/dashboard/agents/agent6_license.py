# agents/agent6_code_quality.py
import subprocess, json

def run(repo_path: str) -> dict:
    try:
        result = subprocess.run(
            ["radon", "cc", "-j", repo_path],
            capture_output=True, text=True
        )
        findings = json.loads(result.stdout or "{}")
        return {
            "agent": "Code Quality",
            "summary": "Code complexity analysis done",
            "details": findings,
            "severity": "High" if any(v for v in findings.values() if len(v) > 10) else "Low",
            "recommendations": "Reduce complexity, refactor long functions"
        }
    except Exception as e:
        return {"agent": "Code Quality", "error": str(e)}
