from typing import Dict, List

from .keyword_extractor import KeywordExtractor
from .technology_extractor import TechnologyExtractor

class NLPAnalyzer:
    """
    Main NLP pipeline for Revianta AI.

    Combines:
    1. Keyword extraction
    2. Technology extraction
    """

    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        self.technology_extractor = TechnologyExtractor()

    def analyze(self, text: str) -> Dict[str, List]:
        """
        Analyze a project description and return
        keywords and detected technologies.
        """

        if not text or not text.strip():
            return {
                "keywords": [],
                "technologies": []
            }

        # Step 1: Extract research keywords
        keywords = self.keyword_extractor.extract_keywords(
            text,
            max_keywords=15
        )

        # Step 2: Extract technologies
        technology_results = self.technology_extractor.extract_technologies(
            text
        )

        # Keep only canonical technology names
        technologies = [
            item["technology"]
            for item in technology_results
        ]

        return {
            "keywords": keywords,
            "technologies": technologies
        }


if __name__ == "__main__":

    project_description = """
    An AI-powered satellite image analysis system that detects
    urban development and changes using optical and SAR imagery.
    The system uses deep learning, computer vision and geospatial
    data to identify buildings, roads and other infrastructure.
    """

    analyzer = NLPAnalyzer()

    result = analyzer.analyze(project_description)

    print("\n========== REVIANTA AI NLP PIPELINE ==========\n")

    print("Project Description:")
    print(project_description.strip())

    print("\nExtracted Keywords:")

    if not result["keywords"]:
        print("No keywords found.")
    else:
        for index, keyword in enumerate(result["keywords"], start=1):
            print(f"{index}. {keyword}")

    print("\nDetected Technologies:")

    if not result["technologies"]:
        print("No technologies found.")
    else:
        for index, technology in enumerate(
            result["technologies"],
            start=1
        ):
            print(f"{index}. {technology}")

    print("\n==============================================\n")