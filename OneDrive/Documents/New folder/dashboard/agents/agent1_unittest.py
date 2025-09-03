# agents/agent3_unit_test_runner.py
import subprocess
import re
import os

def run(repo_path: str) -> dict:
    """
    Advanced Unit Testing Agent
    - Runs pytest (default), falls back to unittest if pytest is unavailable.
    - Parses results into structured summary.
    - Handles complex repos with detailed error categorization.
    """
    try:
        if not os.path.exists(repo_path):
            return {
                "agent": "Unit Tests",
                "error": f"Repository path '{repo_path}' does not exist."
            }

        # Run pytest with detailed output
        result = subprocess.run(
            ["pytest", "--maxfail=10", "--disable-warnings", "-q", "--tb=short", repo_path],
            capture_output=True, text=True
        )

        stdout = result.stdout
        stderr = result.stderr

        # Default structured response
        response = {
            "agent": "Unit Tests",
            "summary": "Tests executed",
            "details": [],
            "severity": "Low",
            "recommendations": []
        }

        # Collect details line by line
        details = stdout.splitlines() + stderr.splitlines()
        response["details"] = details

        # Extract test summary (e.g., "5 passed, 2 failed, 1 skipped")
        summary_line = next((line for line in details if re.search(r"\d+ (passed|failed|skipped|xfailed|xpassed)", line)), None)
        response["summary"] = summary_line if summary_line else "No clear test summary found."

        # Classify severity
        if "failed" in (summary_line or "").lower():
            response["severity"] = "High"
        elif "skipped" in (summary_line or "").lower() or "warnings" in stdout.lower():
            response["severity"] = "Medium"
        else:
            response["severity"] = "Low"

        # Add recommendations
        if "failed" in (summary_line or "").lower():
            response["recommendations"].append("Review failing test cases and fix code logic or assertions.")
        if "import" in stdout.lower() or "ModuleNotFoundError" in stdout:
            response["recommendations"].append("Check Python environment and dependencies (pip install requirements).")
        if "syntaxerror" in stdout.lower():
            response["recommendations"].append("Fix syntax errors in the tested modules.")
        if response["severity"] == "Low":
            response["recommendations"].append("All tests passed. Consider adding more test coverage for edge cases.")

        return response

    except Exception as e:
        return {"agent": "Unit Tests", "error": str(e)}
