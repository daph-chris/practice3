from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RepoForm
from .agents import (
    agent1_unittest,
    agent2_static,
    agent3_dependency,
    agent4_security,
    agent5_performance,
    agent6_license,
    agent7_autofix,
)
import tempfile
from reportlab.pdfgen import canvas

# Cache to store results between requests
results_cache = {}


def index(request):
    form = RepoForm()
    return render(request, "dashboard/index.html", {"form": form, "results": results_cache})


def run_tests(request):
    if request.method == "POST":
        form = RepoForm(request.POST)
        if form.is_valid():
            repo_url = form.cleaned_data["repo_url"]

            # Run all 7 agents
            results = {
                "Unit Tests": agent1_unittest.run(repo_url),
                "Static Analysis": agent2_static.run(repo_url),
                "Dependency Audit": agent3_dependency.run(repo_url),
                "Security Scan": agent4_security.run(repo_url),
                "Performance Check": agent5_performance.run(repo_url),
                "License Compliance": agent6_license.run(repo_url),
                "Auto-fix Suggestions": agent7_autofix.run(repo_url),
            }

            global results_cache
            results_cache = results

            return render(
                request,
                "dashboard/index.html",
                {"form": form, "results": results},
            )
    return redirect("index")


def download_report(request):
    """Generate PDF report with results"""
    if not results_cache:
        return redirect("index")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        p = canvas.Canvas(tmpfile.name)
        p.drawString(100, 800, "Automated Testing & Hardening Report")
        y = 760
        for agent, res in results_cache.items():
            p.drawString(100, y, f"{agent}: {res}")
            y -= 20
        p.save()
        tmpfile.seek(0)
        pdf_data = tmpfile.read()

    response = HttpResponse(pdf_data, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=report.pdf"
    return response
