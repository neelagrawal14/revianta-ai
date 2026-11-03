import sys
from pathlib import Path

# ---------------------------------------------------------
# Add ai_engine folder to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AI_ENGINE_PATH = PROJECT_ROOT / "ai_engine"

sys.path.insert(0, str(AI_ENGINE_PATH))

from pipeline import ReviantaPipeline

# ---------------------------------------------------------
# Pipeline Test
# ---------------------------------------------------------

def test_revianta_pipeline():

    print("\n======================================")
    print("        REVIANTA PIPELINE TEST")
    print("======================================")

    # -----------------------------------------------------
    # Create pipeline
    # -----------------------------------------------------

    pipeline = ReviantaPipeline()

    # -----------------------------------------------------
    # Sample project
    # -----------------------------------------------------

    project_text = """
    AI-powered satellite image analysis system using
    optical and SAR imagery with deep learning and
    computer vision to detect urban development,
    buildings, roads and infrastructure.
    """

    # -----------------------------------------------------
    # Existing/similar research projects
    # -----------------------------------------------------

    similar_texts = [
        """
        Satellite image analysis using deep learning
        for detecting buildings and urban infrastructure.
        """,

        """
        Computer vision system using optical satellite
        imagery for urban development monitoring.
        """,

        """
        Deep learning model for crop disease detection
        using agricultural images.
        """,

        """
        Web application for student attendance management
        using React and a backend database.
        """
    ]

    # -----------------------------------------------------
    # Research activity data for trend prediction
    # -----------------------------------------------------

    activity_counts = {
        2021: 100,
        2022: 120,
        2023: 145,
        2024: 175,
        2025: 210,
    }

    # -----------------------------------------------------
    # Run complete Revianta pipeline
    # -----------------------------------------------------

    result = pipeline.analyze_project(

        project_text=project_text,

        similar_texts=similar_texts,

        activity_counts=activity_counts,

        dataset_count=2,

        research_dependency_count=4,

        deployment_required=True,

        hardware_required=True,

        real_time_required=False,

        data_quality=0.6,

        market_uncertainty=0.5,
    )

    # -----------------------------------------------------
    # Basic result validation
    # -----------------------------------------------------

    assert result is not None

    assert "project" in result
    assert "embedding" in result
    assert "similarity" in result
    assert "novelty" in result
    assert "research_gap" in result
    assert "complexity" in result
    assert "knowledge_graph" in result
    assert "trend" in result
    assert "nrie" in result
    assert "recommendations" in result

    # -----------------------------------------------------
    # Embedding validation
    # -----------------------------------------------------

    assert result["embedding"]["dimension"] == 384

    # -----------------------------------------------------
    # Similarity validation
    # -----------------------------------------------------

    assert len(result["similarity"]["scores"]) == 4

    assert (
        0 <= result["similarity"]["highest_similarity"] <= 1
    )

    # -----------------------------------------------------
    # Novelty validation
    # -----------------------------------------------------

    assert (
        0 <= result["novelty"]["novelty_score"] <= 100
    )

    # -----------------------------------------------------
    # Research gap validation
    # -----------------------------------------------------

    assert (
        0 <= result["research_gap"]["gap_score"] <= 100
    )

    # -----------------------------------------------------
    # Complexity validation
    # -----------------------------------------------------

    assert (
        0 <= result["complexity"]["complexity_score"] <= 100
    )

    # -----------------------------------------------------
    # Knowledge graph validation
    # -----------------------------------------------------

    assert len(result["knowledge_graph"]["nodes"]) > 0

    assert len(result["knowledge_graph"]["edges"]) > 0

    # -----------------------------------------------------
    # Trend validation
    # -----------------------------------------------------

    assert result["trend"] is not None

    assert "trend" in result["trend"]

    # -----------------------------------------------------
    # NRIE validation
    # -----------------------------------------------------

    assert (
        0 <= result["nrie"]["overall_risk"] <= 100
    )

    assert (
        0 <= result["nrie"]["health_score"] <= 100
    )

    assert "risk_scores" in result["nrie"]

    # Make sure all 7 risk dimensions exist
    expected_risks = [
        "technical",
        "dataset",
        "implementation",
        "novelty",
        "research",
        "deployment",
        "business",
    ]

    for risk in expected_risks:
        assert risk in result["nrie"]["risk_scores"]

    # -----------------------------------------------------
    # Recommendations validation
    # -----------------------------------------------------

    assert result["recommendations"] is not None

    # -----------------------------------------------------
    # Print final result
    # -----------------------------------------------------

    print("\n--------------------------------------")
    print("PIPELINE RESULTS")
    print("--------------------------------------")

    print(
        f"Similarity       : "
        f"{result['similarity']['highest_similarity']:.4f}"
    )

    print(
        f"Novelty          : "
        f"{result['novelty']['novelty_score']:.2f}/100"
    )

    print(
        f"Research Gap     : "
        f"{result['research_gap']['gap_score']:.2f}/100"
    )

    print(
        f"Complexity       : "
        f"{result['complexity']['complexity_score']:.2f}/100"
    )

    print(
        f"Overall Risk     : "
        f"{result['nrie']['overall_risk']:.2f}/100"
    )

    print(
        f"Project Health   : "
        f"{result['nrie']['health_score']:.2f}/100"
    )

    print(
        f"Graph Nodes      : "
        f"{len(result['knowledge_graph']['nodes'])}"
    )

    print(
        f"Graph Edges      : "
        f"{len(result['knowledge_graph']['edges'])}"
    )

    print(
        f"Trend            : "
        f"{result['trend']['trend']}"
    )

    print("\n======================================")
    print("   REVIANTA PIPELINE TEST PASSED")
    print("======================================\n")


# ---------------------------------------------------------
# Run directly with Python
# ---------------------------------------------------------

if __name__ == "__main__":
    test_revianta_pipeline()