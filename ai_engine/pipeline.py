"""
Revianta AI Engine Pipeline

Main orchestration layer for the Revianta intelligence system.

The pipeline connects the individual AI modules into
one end-to-end analysis flow.
"""

from typing import Dict, List, Optional

from nlp.nlp_pipeline import NLPAnalyzer
from embeddings.embedding_service import EmbeddingService
from similarity.similarity_engine import SimilarityEngine
from novelty.novelty_engine import NoveltyEngine
from research_gap.gap_detector import ResearchGapDetector
from complexity.complexity_predictor import ComplexityPredictor
from knowledge_graph.graph_builder import KnowledgeGraphBuilder
from trend_prediction.trend_predictor import TrendPredictor
from recommendation.recommendation_engine import RecommendationEngine
from risk_engine.nrie import NRIE


class ReviantaPipeline:

    def __init__(self):
        print("Initializing Revianta AI Pipeline...")

        self.nlp = NLPAnalyzer()
        self.embedding_service = EmbeddingService()
        self.similarity_engine = SimilarityEngine()
        self.novelty_engine = NoveltyEngine()
        self.gap_detector = ResearchGapDetector()
        self.complexity_predictor = ComplexityPredictor()
        self.graph_builder = KnowledgeGraphBuilder()
        self.trend_predictor = TrendPredictor()
        self.recommendation_engine = RecommendationEngine()
        self.nrie = NRIE()

        print("Revianta AI Pipeline initialized successfully.")

    def analyze_project(
        self,
        project_text: str,
        similar_texts: Optional[List[str]] = None,
        activity_counts: Optional[Dict[int, int]] = None,
        dataset_count: int = 1,
        research_dependency_count: int = 2,
        deployment_required: bool = False,
        hardware_required: bool = False,
        real_time_required: bool = False,
        data_quality: float = 0.6,
        market_uncertainty: float = 0.5,
    ) -> Dict:

        if not project_text or not project_text.strip():
            raise ValueError("Project text cannot be empty.")

        print("\n========== REVIANTA AI ANALYSIS ==========\n")

        # =====================================================
        # STEP 1 — NLP
        # =====================================================

        print("[1/10] Running NLP analysis...")

        nlp_result = self.nlp.analyze(project_text)

        keywords = nlp_result["keywords"]
        technologies = nlp_result["technologies"]

        print(f"Keywords detected: {len(keywords)}")
        print(f"Technologies detected: {len(technologies)}")

        # =====================================================
        # STEP 2 — PROJECT EMBEDDING
        # =====================================================

        print("\n[2/10] Generating project embedding...")

        project_embedding = (
            self.embedding_service.generate_embedding(
                project_text
            )
        )

        print(
            f"Embedding dimension: "
            f"{len(project_embedding)}"
        )

        # =====================================================
        # STEP 3 — SIMILARITY
        # =====================================================

        print("\n[3/10] Running similarity analysis...")

        if similar_texts:

            if similar_texts:
                similarity_scores = [
                            self.similarity_engine.compare_texts(
                                project_text,
                                text
                            )
                            for text in similar_texts
                        ]
            else:
                similarity_scores = []

        highest_similarity = (
            max(similarity_scores)
            if similarity_scores
            else 0.0
        )

        print(
            f"Similar items analyzed: "
            f"{len(similarity_scores)}"
        )

        print(
            f"Highest similarity: "
            f"{highest_similarity:.4f}"
        )

        # =====================================================
        # STEP 4 — NOVELTY
        # =====================================================

        print("\n[4/10] Calculating novelty...")

        novelty_result = self.novelty_engine.analyze(
            similarity_scores
        )

        novelty_score = novelty_result["novelty_score"]

        print(
            f"Novelty score: "
            f"{novelty_score:.2f}/100"
        )

        # =====================================================
        # STEP 5 — RESEARCH GAP
        # =====================================================

        print("\n[5/10] Detecting research gap...")

        gap_result = self.gap_detector.analyze(
            similarity_scores
        )

        research_gap_score = gap_result["gap_score"]

        print(
            f"Research gap score: "
            f"{research_gap_score:.2f}/100"
        )

        # =====================================================
        # STEP 6 — COMPLEXITY
        # =====================================================

        print("\n[6/10] Predicting project complexity...")

        complexity_result = self.complexity_predictor.analyze(
            project_name="Current Project",
            technology_count=len(technologies),
            dataset_count=dataset_count,
            research_dependency_count=research_dependency_count,
            deployment_required=deployment_required,
            hardware_required=hardware_required,
            real_time_required=real_time_required,
        )

        print(
            f"Complexity score: "
            f"{complexity_result['complexity_score']:.2f}/100"
        )

        # =====================================================
        # STEP 7 — KNOWLEDGE GRAPH
        # =====================================================

        print("\n[7/10] Building knowledge graph...")

        graph = self.graph_builder.build_project_graph(
            project_name="Current Project",
            technologies=technologies,
            keywords=keywords,
        )

        print(
            f"Graph nodes: "
            f"{len(graph['nodes'])}"
        )

        print(
            f"Graph edges: "
            f"{len(graph['edges'])}"
        )

        # =====================================================
        # STEP 8 — TREND ANALYSIS
        # =====================================================

        print("\n[8/10] Running trend analysis...")

        trend_result = None

        if activity_counts:

            trend_result = (
                self.trend_predictor.analyze(
                    topic="Project Technology",
                    years=list(activity_counts.keys()),
                    activity_counts=list(activity_counts.values()),
                )
            )

            print(
                f"Trend: "
                f"{trend_result['trend']}"
            )

        else:

            print(
                "No historical activity data provided."
            )

        # =====================================================
        # STEP 9 — NRIE
        # =====================================================

        print("\n[9/10] Running NRIE risk analysis...")

        nrie_result = self.nrie.analyze(

            technology_count=len(technologies),

            dataset_count=dataset_count,

            research_dependency_count=(
                research_dependency_count
            ),

            novelty_score=novelty_score,

            research_gap_score=research_gap_score,

            highest_similarity=highest_similarity,

            deployment_required=deployment_required,

            hardware_required=hardware_required,

            real_time_required=real_time_required,

            data_quality=data_quality,

            market_uncertainty=market_uncertainty,
        )

        print(
            f"Overall risk: "
            f"{nrie_result['overall_risk']:.2f}/100"
        )

        print(
            f"Project health: "
            f"{nrie_result['health_score']:.2f}/100"
        )

        # =====================================================
        # STEP 10 — RECOMMENDATIONS
        # =====================================================

        print("\n[10/10] Generating recommendations...")

        recommendation_result = (
            self.recommendation_engine.generate_recommendations(
                technologies=technologies,
                similarity_scores=similarity_scores,
                novelty_score=novelty_score,
                gap_score=research_gap_score,
                gap_type=gap_result["gap_type"],
            )
        )

        # =====================================================
        # FINAL RESULT
        # =====================================================

        return {

            "project": {
                "text": project_text,
                "keywords": keywords,
                "technologies": technologies,
            },

            "embedding": {
                "dimension": len(project_embedding),
            },

            "similarity": {
                "scores": similarity_scores,
                "highest_similarity": highest_similarity,
            },

            "novelty": novelty_result,

            "research_gap": gap_result,

            "complexity": complexity_result,

            "knowledge_graph": graph,

            "trend": trend_result,

            "nrie": nrie_result,

            "recommendations": recommendation_result,
        }


if __name__ == "__main__":

    pipeline = ReviantaPipeline()

    sample_project = """
    AI-powered satellite image analysis system using
    optical and SAR imagery with deep learning and
    computer vision to detect urban development,
    buildings, roads and infrastructure.
    """

    sample_similar_projects = [

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
        """,
    ]

    result = pipeline.analyze_project(
        project_text=sample_project,
        similar_texts=sample_similar_projects,
        activity_counts={
            2021: 100,
            2022: 120,
            2023: 145,
            2024: 175,
            2025: 210,
        },
        dataset_count=2,
        research_dependency_count=4,
        deployment_required=True,
        hardware_required=True,
        real_time_required=False,
        data_quality=0.6,
        market_uncertainty=0.5,
    )

    print("\n")
    print("=" * 65)
    print("              FINAL REVIANTA ANALYSIS")
    print("=" * 65)

    print("\nPROJECT")
    print(
        result["project"]["text"].strip()
    )

    print("\nTECHNOLOGIES")

    for technology in result["project"]["technologies"]:
        print(f"- {technology}")

    print("\nNOVELTY")
    print(
        f"Score: "
        f"{result['novelty']['novelty_score']:.2f}/100"
    )

    print("\nRESEARCH GAP")
    print(
        f"Score: "
        f"{result['research_gap']['gap_score']:.2f}/100"
    )

    print("\nCOMPLEXITY")
    print(
        f"Score: "
        f"{result['complexity']['complexity_score']:.2f}/100"
    )

    print("\nNRIE")

    print(
        f"Overall Risk: "
        f"{result['nrie']['overall_risk']:.2f}/100"
    )

    print(
        f"Project Health: "
        f"{result['nrie']['health_score']:.2f}/100"
    )

    print("\nTREND")

    if result["trend"]:
        print(
            f"Trend: "
            f"{result['trend']['trend']}"
        )

    else:
        print("No trend data available.")

    print("\n" + "=" * 65)
    print("          REVIANTA PIPELINE TEST COMPLETE")
    print("=" * 65)