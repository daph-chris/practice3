# agents/agent2_dependency_scanner.py
import subprocess, json, os

def run(repo_path: str) -> dict:
    req = os.path.join(repo_path, "requirements.txt")
    if not os.path.exists(req):
        return {"agent": "Dependency Scanner", "summary": "No requirements.txt found"}
    try:
        result = subprocess.run(
            ["pip-audit", "-r", req, "-f", "json"],
            capture_output=True, text=True
        )
        findings = json.loads(result.stdout or "[]")
        return {
            "agent": "Dependency Scanner",
            "summary": f"{len(findings)} vulnerable packages",
            "details": findings,
            "severity": "High" if findings else "Low",
            "recommendations": "Update vulnerable dependencies"
        }
    except Exception as e:
        return {"agent": "Dependency Scanner", "error": str(e)}
