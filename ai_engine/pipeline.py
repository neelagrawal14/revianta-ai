"""
Revianta AI Engine Pipeline

Main orchestration layer for the Revianta intelligence system.

The pipeline connects the individual AI modules into
one end-to-end analysis flow.
"""

from typing import Dict, List, Optional, Any
from .nlp.nlp_pipeline import NLPAnalyzer
from .embeddings.embedding_service import EmbeddingService
from .similarity.similarity_engine import SimilarityEngine
from .novelty.novelty_engine import NoveltyEngine
from .research_gap.gap_detector import ResearchGapDetector
from .complexity.complexity_predictor import ComplexityPredictor
from .knowledge_graph.graph_builder import KnowledgeGraphBuilder
from .trend_prediction.trend_predictor import TrendPredictor
from .risk_engine.nrie import NRIE
from .recommendation.recommendation_engine import RecommendationEngine


class ReviantaPipeline:
    """
    Main orchestration pipeline for Revianta AI.

    This class connects all intelligence modules and produces
    one structured project analysis result.

    Individual algorithms are implemented in their own modules.
    The pipeline is responsible only for orchestration.
    """

    def __init__(self):
        print("Initializing Revianta AI Pipeline...")

        # =====================================================
        # CORE AI SERVICES
        # =====================================================

        self.nlp = NLPAnalyzer()
        self.embedding_service = EmbeddingService()
        self.similarity_engine = SimilarityEngine(
            self.embedding_service
        )

        # =====================================================
        # INTELLIGENCE ENGINES
        # =====================================================

        self.novelty_engine = NoveltyEngine()

        self.gap_detector = ResearchGapDetector()

        self.complexity_predictor = ComplexityPredictor()

        # =====================================================
        # KNOWLEDGE & TREND
        # =====================================================

        self.graph_builder = KnowledgeGraphBuilder()

        self.trend_predictor = TrendPredictor()

        # =====================================================
        # RECOMMENDATION & RISK
        # =====================================================

        self.recommendation_engine = RecommendationEngine()

        self.nrie = NRIE()

        print("Revianta AI Pipeline initialized successfully.")

    # =========================================================
    # MAIN PROJECT ANALYSIS
    # =========================================================

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
    ) -> Dict[str, Any]:
        """
        Run the complete Revianta intelligence pipeline.

        Parameters
        ----------
        project_text:
            User's project/research idea.

        similar_texts:
            Existing research/project descriptions used for
            semantic similarity analysis.

        activity_counts:
            Historical technology/research activity by year.

        dataset_count:
            Number of datasets required by the project.

        research_dependency_count:
            Number of major research dependencies.

        deployment_required:
            Whether deployment is required.

        hardware_required:
            Whether specialized hardware is required.

        real_time_required:
            Whether real-time processing is required.

        data_quality:
            Estimated quality of available data, between 0 and 1.

        market_uncertainty:
            Estimated market uncertainty, between 0 and 1.

        Returns
        -------
        Dict[str, Any]
            Structured Revianta analysis result.
        """

        # =====================================================
        # INPUT VALIDATION
        # =====================================================

        if not project_text or not project_text.strip():
            raise ValueError("Project text cannot be empty.")

        project_text = project_text.strip()

        # =====================================================
        # STEP 1 â€” NLP ANALYSIS
        # =====================================================

        print("\n========== REVIANTA AI ANALYSIS ==========\n")

        print("[1/10] Running NLP analysis...")

        nlp_result = self.nlp.analyze(
            project_text
        )

        keywords = nlp_result["keywords"]

        technologies = nlp_result["technologies"]

        print(
            f"Keywords detected: "
            f"{len(keywords)}"
        )

        print(
            f"Technologies detected: "
            f"{len(technologies)}"
        )

        # =====================================================
        # STEP 2 â€” PROJECT EMBEDDING
        # =====================================================

        print("\n[2/10] Generating project embedding...")

        project_embedding = (
            self.embedding_service.generate_embedding(
                project_text
            )
        )

        embedding_dimension = len(
            project_embedding
        )

        print(
            f"Embedding dimension: "
            f"{embedding_dimension}"
        )

        # =====================================================
        # STEP 3 â€” SIMILARITY ANALYSIS
        # =====================================================

        print("\n[3/10] Running similarity analysis...")

        if similar_texts:

            similarity_scores = []

            for text in similar_texts:

                if not text or not text.strip():
                    continue

                # Generate embedding only for the existing text.
                comparison_embedding = (
                    self.embedding_service.generate_embedding(
                        text
                    )
                )

                # Reuse the project embedding generated in Step 2.
                similarity = (
                    self.similarity_engine.compare_embeddings(
                        project_embedding,
                        comparison_embedding,
                    )
                )

                similarity_scores.append(
                    similarity
                )

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
        # STEP 4 â€” NOVELTY ANALYSIS
        # =====================================================

        print("\n[4/10] Calculating novelty...")

        novelty_result = (
            self.novelty_engine.analyze(
                similarity_scores
            )
        )

        novelty_score = (
            novelty_result["novelty_score"]
        )

        print(
            f"Novelty score: "
            f"{novelty_score:.2f}/100"
        )

        # =====================================================
        # STEP 5 â€” RESEARCH GAP ANALYSIS
        # =====================================================

        print("\n[5/10] Detecting research gap...")

        gap_result = (
            self.gap_detector.analyze(
                similarity_scores
            )
        )

        research_gap_score = (
            gap_result["gap_score"]
        )

        print(
            f"Research gap score: "
            f"{research_gap_score:.2f}/100"
        )

        # =====================================================
        # STEP 6 â€” COMPLEXITY ANALYSIS
        # =====================================================

        print(
            "\n[6/10] Predicting project complexity..."
        )

        complexity_result = (
            self.complexity_predictor.analyze(
                project_name="Current Project",
                technology_count=len(
                    technologies
                ),
                dataset_count=dataset_count,
                research_dependency_count=(
                    research_dependency_count
                ),
                deployment_required=(
                    deployment_required
                ),
                hardware_required=(
                    hardware_required
                ),
                real_time_required=(
                    real_time_required
                ),
            )
        )

        print(
            f"Complexity score: "
            f"{complexity_result['complexity_score']:.2f}/100"
        )

        print(
            f"Complexity level: "
            f"{complexity_result['complexity_level']}"
        )

        # =====================================================
        # STEP 7 â€” KNOWLEDGE GRAPH
        # =====================================================

        print(
            "\n[7/10] Building knowledge graph..."
        )

        graph = (
            self.graph_builder.build_project_graph(
                project_name="Current Project",
                technologies=technologies,
                keywords=keywords,
            )
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
        # STEP 8 â€” TREND ANALYSIS
        # =====================================================

        print(
            "\n[8/10] Running trend analysis..."
        )

        trend_result = None

        if activity_counts:

            trend_result = (
                self.trend_predictor.analyze(
                    topic="Project Technology",
                    years=list(
                        activity_counts.keys()
                    ),
                    activity_counts=list(
                        activity_counts.values()
                    ),
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
        # STEP 9 â€” NRIE RISK ANALYSIS
        # =====================================================

        print(
            "\n[9/10] Running NRIE risk analysis..."
        )

        nrie_result = self.nrie.analyze(

            technology_count=len(
                technologies
            ),

            dataset_count=dataset_count,

            research_dependency_count=(
                research_dependency_count
            ),

            novelty_score=novelty_score,

            research_gap_score=(
                research_gap_score
            ),

            highest_similarity=(
                highest_similarity
            ),

            deployment_required=(
                deployment_required
            ),

            hardware_required=(
                hardware_required
            ),

            real_time_required=(
                real_time_required
            ),

            data_quality=data_quality,

            market_uncertainty=(
                market_uncertainty
            ),
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
        # STEP 10 â€” RECOMMENDATIONS
        # =====================================================

        print(
            "\n[10/10] Generating recommendations..."
        )

        recommendation_result = (
            self.recommendation_engine
            .generate_recommendations(

                technologies=technologies,

                similarity_scores=(
                    similarity_scores
                ),

                novelty_score=novelty_score,

                gap_score=research_gap_score,

                gap_type=gap_result[
                    "gap_type"
                ],
            )
        )

        # =====================================================
        # FINAL STRUCTURED RESULT
        # =====================================================

        result = {

            "project": {

                "text": project_text,

                "keywords": keywords,

                "technologies": technologies,
            },

            "embedding": {

                "dimension": embedding_dimension,
            },

            "similarity": {

                "scores": similarity_scores,

                "highest_similarity": (
                    highest_similarity
                ),
            },

            "novelty": novelty_result,

            "research_gap": gap_result,

            "complexity": complexity_result,

            "knowledge_graph": graph,

            "trend": trend_result,

            "nrie": nrie_result,

            "recommendations": (
                recommendation_result
            ),
        }

        return result

