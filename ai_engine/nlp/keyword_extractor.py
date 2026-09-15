import spacy
from typing import List


class KeywordExtractor:
    """
    Revianta AI - NLP Keyword Extraction

    Extracts meaningful research keywords from
    project and research descriptions.

    Features:
    - Noun phrase extraction
    - Named entity extraction
    - Important noun extraction
    - Technical terminology preservation
    - AI-powered phrase preservation
    - Duplicate removal
    - Generic word filtering
    - Redundant keyword removal
    """

    def __init__(self):
        """
        Initialize the spaCy NLP model.
        """

        self.nlp = spacy.load("en_core_web_sm")

        # Words that are generally not useful
        # as research keywords.
        self.custom_stop_words = {
            "project",
            "system",
            "application",
            "method",
            "approach",
            "process",
            "using",
            "use",
            "used",
            "based",
            "make",
            "making",
            "develop",
            "developing",
            "new",
            "that",
            "this",
            "these",
            "those",
        }

        # Generic words that should not appear
        # independently as keywords.
        self.generic_words = {
            "thing",
            "way",
            "part",
            "type",
            "result",
            "information",
            "problem",
            "idea",
            "change",
        }

        # Technical terms that should be preserved
        # instead of aggressively lemmatized.
        self.technical_terms = {
            "ai",
            "data",
            "imagery",
            "satellite",
            "optical",
            "geospatial",
            "learning",
            "analysis",
            "computer",
            "vision",
            "infrastructure",
            "deep",
            "sar",
            "cnn",
            "nlp",
            "gpu",
            "api",
            "ml",
            "llm",
            "transformer",
            "transformers",
            "embedding",
            "embeddings",
            "pytorch",
            "tensorflow",
            "python",
            "react",
            "postgresql",
        }

    # ============================================================
    # CLEAN PHRASE
    # ============================================================

    def clean_phrase(self, phrase: str) -> str:
        """
        Clean an extracted phrase while preserving
        technical terminology.

        Special handling is included for terms such as:
        - AI-powered
        - SAR
        - CNN
        - NLP
        - GPU
        """

        # --------------------------------------------------------
        # Protect important hyphenated technical terms
        # before spaCy tokenization.
        # --------------------------------------------------------

        phrase = phrase.replace(
            "AI-powered",
            "AI_POWERED"
        )

        phrase = phrase.replace(
            "ai-powered",
            "AI_POWERED"
        )

        doc = self.nlp(phrase)

        words = []

        for token in doc:

            original = token.text.strip()

            # Ignore empty tokens
            if not original:
                continue

            # ----------------------------------------------------
            # Restore AI-powered
            # ----------------------------------------------------

            if original == "AI_POWERED":
                words.append("AI-powered")
                continue

            # Ignore punctuation, numbers and symbols
            if not token.is_alpha:
                continue

            # Ignore spaCy stop words
            if token.is_stop:
                continue

            # Ignore custom stop words
            if original.lower() in self.custom_stop_words:
                continue

            # Ignore very short words
            if len(original) < 3:
                continue

            # ----------------------------------------------------
            # Preserve uppercase technical acronyms
            #
            # Examples:
            # AI
            # SAR
            # CNN
            # NLP
            # GPU
            # API
            # ----------------------------------------------------

            if original.isupper():
                word = original

            # ----------------------------------------------------
            # Preserve known technical terms
            # ----------------------------------------------------

            elif original.lower() in self.technical_terms:
                word = original.lower()

            # ----------------------------------------------------
            # Lemmatize normal words
            # ----------------------------------------------------

            else:
                word = token.lemma_.lower()

            words.append(word)

        return " ".join(words)

    # ============================================================
    # EXTRACT KEYWORDS
    # ============================================================

    def extract_keywords(
        self,
        text: str,
        max_keywords: int = 15
    ) -> List[str]:
        """
        Extract meaningful research keywords.

        Parameters
        ----------
        text : str
            Project or research description.

        max_keywords : int
            Maximum number of keywords to return.

        Returns
        -------
        List[str]
            Extracted research keywords.
        """

        # --------------------------------------------------------
        # Validate input
        # --------------------------------------------------------

        if not text or not text.strip():
            return []

        # --------------------------------------------------------
        # Process the complete text
        # --------------------------------------------------------

        doc = self.nlp(text)

        candidates = []

        # ========================================================
        # 1. NOUN PHRASES
        # ========================================================

        for chunk in doc.noun_chunks:

            phrase = self.clean_phrase(chunk.text)

            if not phrase:
                continue

            if len(phrase) < 3:
                continue

            candidates.append(phrase)

        # ========================================================
        # 2. NAMED ENTITIES
        # ========================================================

        for entity in doc.ents:

            phrase = self.clean_phrase(entity.text)

            if not phrase:
                continue

            candidates.append(phrase)

        # ========================================================
        # 3. IMPORTANT NOUNS / PROPER NOUNS
        # ========================================================

        for token in doc:

            original = token.text.strip()

            if not original:
                continue

            # Ignore punctuation/numbers
            if not token.is_alpha:
                continue

            # Ignore stop words
            if token.is_stop:
                continue

            # Ignore short words
            if len(original) < 3:
                continue

            # Ignore custom stop words
            if original.lower() in self.custom_stop_words:
                continue

            # ----------------------------------------------------
            # Preserve technical acronyms
            # ----------------------------------------------------

            if original.isupper():
                word = original

            # ----------------------------------------------------
            # Preserve technical terminology
            # ----------------------------------------------------

            elif original.lower() in self.technical_terms:
                word = original.lower()

            # ----------------------------------------------------
            # Lemmatize normal words
            # ----------------------------------------------------

            else:
                word = token.lemma_.lower()

            # Only nouns and proper nouns
            if token.pos_ in {"NOUN", "PROPN"}:

                candidates.append(word)

        # ========================================================
        # 4. REMOVE DUPLICATES
        # ========================================================

        unique_keywords = []

        seen = set()

        for keyword in candidates:

            keyword = keyword.strip()

            if not keyword:
                continue

            key = keyword.lower()

            if key in seen:
                continue

            seen.add(key)

            unique_keywords.append(keyword)

        # ========================================================
        # 5. REMOVE GENERIC WORDS
        # ========================================================

        filtered_keywords = []

        for keyword in unique_keywords:

            if keyword.lower() in self.generic_words:
                continue

            filtered_keywords.append(keyword)

        # ========================================================
        # 6. SEPARATE MULTI-WORD AND SINGLE-WORD TERMS
        # ========================================================

        multi_word_keywords = []

        single_word_keywords = []

        for keyword in filtered_keywords:

            if len(keyword.split()) > 1:
                multi_word_keywords.append(keyword)

            else:
                single_word_keywords.append(keyword)

        # ========================================================
        # 7. REMOVE REDUNDANT SINGLE WORDS
        # ========================================================

        redundant_words = set()

        for word in single_word_keywords:

            word_lower = word.lower()

            for phrase in multi_word_keywords:

                phrase_words = phrase.lower().split()

                if word_lower in phrase_words:
                    redundant_words.add(word_lower)
                    break

        useful_single_words = [
            word
            for word in single_word_keywords
            if word.lower() not in redundant_words
        ]

        # ========================================================
        # 8. COMBINE RESULTS
        # ========================================================

        final_keywords = (
            multi_word_keywords
            + useful_single_words
        )

        # ========================================================
        # 9. FINAL DUPLICATE CHECK
        # ========================================================

        final_result = []

        seen = set()

        for keyword in final_keywords:

            key = keyword.lower()

            if key in seen:
                continue

            seen.add(key)

            final_result.append(keyword)

        # ========================================================
        # 10. LIMIT RESULT
        # ========================================================

        return final_result[:max_keywords]


# ================================================================
# TEST
# ================================================================

if __name__ == "__main__":

    extractor = KeywordExtractor()

    project_description = """
    An AI-powered satellite image analysis system that detects
    urban development and changes using optical and SAR imagery.
    The system uses deep learning, computer vision and geospatial
    data to identify buildings, roads and other infrastructure.
    """

    keywords = extractor.extract_keywords(
        project_description,
        max_keywords=15
    )

    print("\n========== REVIANTA AI NLP ==========\n")

    print("Project Description:")
    print(project_description.strip())

    print("\nExtracted Keywords:")

    if not keywords:

        print("No keywords found.")

    else:

        for index, keyword in enumerate(
            keywords,
            start=1
        ):

            print(f"{index}. {keyword}")

    print("\n=====================================\n")