import re
from typing import List, Dict


class TechnologyExtractor:
    """
    Revianta AI - Technology Extraction

    Identifies technologies and technical concepts
    from a project/research description.

    Features:
    - Controlled technology vocabulary
    - Case-insensitive matching
    - Multi-word technology matching
    - Acronym preservation
    - Duplicate removal
    - Redundant technology removal
    """

    def __init__(self):

        # ========================================================
        # TECHNOLOGY VOCABULARY
        # ========================================================

        self.technology_vocabulary = {

            # ----------------------------------------------------
            # Artificial Intelligence / Machine Learning
            # ----------------------------------------------------

            "artificial intelligence":
                "Artificial Intelligence",

            "ai":
                "Artificial Intelligence",

            "machine learning":
                "Machine Learning",

            "ml":
                "Machine Learning",

            "deep learning":
                "Deep Learning",

            "reinforcement learning":
                "Reinforcement Learning",

            "supervised learning":
                "Supervised Learning",

            "unsupervised learning":
                "Unsupervised Learning",

            # ----------------------------------------------------
            # Computer Vision
            # ----------------------------------------------------

            "computer vision":
                "Computer Vision",

            "image processing":
                "Image Processing",

            "image analysis":
                "Image Analysis",

            "object detection":
                "Object Detection",

            "image classification":
                "Image Classification",

            "semantic segmentation":
                "Semantic Segmentation",

            "instance segmentation":
                "Instance Segmentation",

            "change detection":
                "Change Detection",

            # ----------------------------------------------------
            # Neural Networks
            # ----------------------------------------------------

            "convolutional neural network":
                "CNN",

            "convolutional neural networks":
                "CNN",

            "cnn":
                "CNN",

            "recurrent neural network":
                "RNN",

            "recurrent neural networks":
                "RNN",

            "rnn":
                "RNN",

            "transformer":
                "Transformer",

            "transformers":
                "Transformer",

            "vision transformer":
                "Vision Transformer",

            "vit":
                "Vision Transformer",

            # ----------------------------------------------------
            # NLP
            # ----------------------------------------------------

            "natural language processing":
                "Natural Language Processing",

            "nlp":
                "Natural Language Processing",

            "large language model":
                "Large Language Model",

            "large language models":
                "Large Language Model",

            "llm":
                "Large Language Model",

            # ----------------------------------------------------
            # Embeddings / Search
            # ----------------------------------------------------

            "embedding":
                "Embeddings",

            "embeddings":
                "Embeddings",

            "vector embedding":
                "Embeddings",

            "vector embeddings":
                "Embeddings",

            "semantic search":
                "Semantic Search",

            "similarity search":
                "Similarity Search",

            # ----------------------------------------------------
            # Satellite / Remote Sensing
            # ----------------------------------------------------

            "satellite imagery":
                "Satellite Imagery",

            "satellite image analysis":
                "Satellite Image Analysis",

            "satellite image":
                "Satellite Image Analysis",

            "remote sensing":
                "Remote Sensing",

            "synthetic aperture radar":
                "SAR",

            "sar":
                "SAR",

            "optical imagery":
                "Optical Imagery",

            "optical image":
                "Optical Imagery",

            "optical":
                "Optical Imagery",

            "multispectral imagery":
                "Multispectral Imagery",

            "multispectral":
                "Multispectral Imaging",

            "hyperspectral imagery":
                "Hyperspectral Imaging",

            "hyperspectral":
                "Hyperspectral Imaging",

            # ----------------------------------------------------
            # Geospatial
            # ----------------------------------------------------

            "geospatial data":
                "Geospatial Data",

            "geospatial analysis":
                "Geospatial Analysis",

            "gis":
                "GIS",

            "geographic information system":
                "Geographic Information System",

            # ----------------------------------------------------
            # AI Frameworks
            # ----------------------------------------------------

            "pytorch":
                "PyTorch",

            "tensorflow":
                "TensorFlow",

            "keras":
                "Keras",

            "scikit-learn":
                "Scikit-learn",

            "sklearn":
                "Scikit-learn",

            # ----------------------------------------------------
            # Programming / Backend
            # ----------------------------------------------------

            "python":
                "Python",

            "java":
                "Java",

            "javascript":
                "JavaScript",

            "typescript":
                "TypeScript",

            "react":
                "React",

            "fastapi":
                "FastAPI",

            "postgresql":
                "PostgreSQL",

            "postgres":
                "PostgreSQL",

            "sql":
                "SQL",

            # ----------------------------------------------------
            # Data / Vector Technologies
            # ----------------------------------------------------

            "vector database":
                "Vector Database",

            "vector databases":
                "Vector Database",

            "pgvector":
                "pgvector",

            "database":
                "Database",

            # ----------------------------------------------------
            # Graph Technologies
            # ----------------------------------------------------

            "knowledge graph":
                "Knowledge Graph",

            "graph neural network":
                "Graph Neural Network",

            "graph neural networks":
                "Graph Neural Network",

            "gnn":
                "Graph Neural Network",
        }

    # ============================================================
    # NORMALIZE TEXT
    # ============================================================

    def normalize_text(self, text: str) -> str:
        """
        Normalize input text before matching.
        """

        text = text.lower()

        # Normalize whitespace
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ============================================================
    # EXTRACT TECHNOLOGIES
    # ============================================================

    def extract_technologies(
        self,
        text: str
    ) -> List[Dict[str, str]]:
        """
        Extract technologies from a project description.

        Returns:

        [
            {
                "technology": "Deep Learning",
                "matched_text": "deep learning"
            }
        ]
        """

        if not text or not text.strip():
            return []

        normalized_text = self.normalize_text(text)

        technologies = []

        # ========================================================
        # SORT LONGEST TERMS FIRST
        # ========================================================

        vocabulary_items = sorted(
            self.technology_vocabulary.items(),
            key=lambda item: len(item[0]),
            reverse=True
        )

        found_canonical_names = set()

        # ========================================================
        # SEARCH TECHNOLOGY VOCABULARY
        # ========================================================

        for search_term, canonical_name in vocabulary_items:

            pattern = (
                r"\b"
                + re.escape(search_term)
                + r"\b"
            )

            match = re.search(
                pattern,
                normalized_text
            )

            if not match:
                continue

            # ----------------------------------------------------
            # Prevent duplicate canonical technologies
            # ----------------------------------------------------

            if canonical_name in found_canonical_names:
                continue

            found_canonical_names.add(
                canonical_name
            )

            technologies.append(
                {
                    "technology": canonical_name,
                    "matched_text": match.group(0)
                }
            )

        # ========================================================
        # REMOVE REDUNDANT TECHNOLOGIES
        # ========================================================
        #
        # Example:
        #
        # Satellite Image Analysis
        # Image Analysis
        #
        # "Image Analysis" is redundant because it is already
        # contained inside "Satellite Image Analysis".
        # ========================================================

        final_technologies = []

        for technology in technologies:

            current_name = technology[
                "technology"
            ].lower()

            is_redundant = False

            for existing in final_technologies:

                existing_name = existing[
                    "technology"
                ].lower()

                if (
                    current_name in existing_name
                    and current_name != existing_name
                ):
                    is_redundant = True
                    break

            if not is_redundant:
                final_technologies.append(
                    technology
                )

        return final_technologies


# ================================================================
# TEST
# ================================================================

if __name__ == "__main__":

    extractor = TechnologyExtractor()

    project_description = """
    An AI-powered satellite image analysis system that detects
    urban development and changes using optical and SAR imagery.
    The system uses deep learning, computer vision and geospatial
    data to identify buildings, roads and other infrastructure.
    """

    technologies = extractor.extract_technologies(
        project_description
    )

    print(
        "\n========== "
        "REVIANTA AI TECHNOLOGY EXTRACTION "
        "==========\n"
    )

    print("Project Description:")
    print(
        project_description.strip()
    )

    print("\nDetected Technologies:")

    if not technologies:

        print("No technologies found.")

    else:

        for index, item in enumerate(
            technologies,
            start=1
        ):

            print(
                f"{index}. "
                f"{item['technology']} "
                f"← \"{item['matched_text']}\""
            )

    print(
        "\n=======================================================\n"
    )