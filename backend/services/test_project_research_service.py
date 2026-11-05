
"""
Test Project Research Service.
"""

from pathlib import Path
import os
import sys
import getpass

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.project_research_service import (
    ProjectResearchService,
)


def main():
    print("=" * 60)
    print("       REVIANTA PROJECT RESEARCH TEST")
    print("=" * 60)

    password = os.getenv("POSTGRES_PASSWORD")

    if not password:
        password = getpass.getpass(
            "\nEnter PostgreSQL password: "
        )

    service = ProjectResearchService(password=password)

    print("\n[1/3] Creating project...")

    project_id = service.create_project(
        name="Satellite Intelligence",
        title="AI Powered Satellite Image Analysis",
        description=(
            "AI-powered analysis of satellite imagery using "
            "computer vision, optical and SAR data."
        ),
        created_by="revianta",
    )

    print(f"Project created: {project_id}")

    print("\n[2/3] Finding relevant research...")

    context = service.build_project_context(
        project_id=project_id,
        query="AI powered satellite image analysis",
        minimum_relevance=0.20,
        limit=10,
    )

    print("\nResearch context:")

    for source, count in context["counts"].items():
        print(f"   {source:10}: {count}")

    print("\n[3/3] Selected records:")

    for source, records in context["results"].items():
        print(f"\n{source.upper()}")

        for record in records[:5]:
            title = (
                record.get("title")
                or record.get("name")
                or "Untitled"
            )

            print(
                f"   [{record['relevance_score']:.3f}] "
                f"{title}"
            )

    print("\n" + "=" * 60)
    print("       PROJECT RESEARCH TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
