import requests
from typing import Any, Dict, List, Optional


class DatasetSources:
    """
    Unified dataset search client for:
    1. Kaggle
    2. Hugging Face

    All successful sources return the same normalized structure.
    """

    KAGGLE_API_URL = "https://www.kaggle.com/api/v1/datasets/list"
    HF_API_URL = "https://huggingface.co/api/datasets"

    def __init__(
        self,
        kaggle_username: Optional[str] = None,
        kaggle_key: Optional[str] = None,
        hf_token: Optional[str] = None,
        timeout: int = 30
    ):
        self.kaggle_username = kaggle_username
        self.kaggle_key = kaggle_key
        self.hf_token = hf_token
        self.timeout = timeout

    # ============================================================
    # KAGGLE
    # ============================================================

    def search_kaggle(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:

        if not query or not query.strip():
            raise ValueError(
                "Kaggle query cannot be empty."
            )

        params = {
            "search": query.strip(),
            "page": 1,
            "pageSize": min(max_results, 100)
        }

        headers = {}

        if self.kaggle_username and self.kaggle_key:
            headers["Authorization"] = (
                f"Basic "
                f"{self.kaggle_username}:"
                f"{self.kaggle_key}"
            )

        response = requests.get(
            self.KAGGLE_API_URL,
            params=params,
            headers=headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        return [
            self._normalize_kaggle(item)
            for item in data
        ]

    @staticmethod
    def _normalize_kaggle(
        dataset: Dict[str, Any]
    ) -> Dict[str, Any]:

        owner = (
            dataset.get("ownerUser")
            or dataset.get("ownerName")
        )

        return {
            "source": "kaggle",
            "external_id": dataset.get("ref"),
            "name": dataset.get("title"),
            "description": dataset.get("description"),
            "url": (
                "https://www.kaggle.com/datasets/"
                + dataset.get("ref", "")
            ),
            "owner": owner,
            "license": dataset.get("licenseName"),
            "tags": dataset.get("tags", []),
            "downloads": dataset.get(
                "downloadCount",
                0
            ),
            "votes": dataset.get(
                "voteCount",
                0
            ),
            "usability": dataset.get(
                "usabilityRating"
            ),
            "created_at": dataset.get(
                "creationDate"
            ),
            "updated_at": dataset.get(
                "lastUpdated"
            ),
        }

    # ============================================================
    # HUGGING FACE
    # ============================================================

    def search_huggingface(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:

        if not query or not query.strip():
            raise ValueError(
                "Hugging Face query cannot be empty."
            )

        params = {
            "search": query.strip(),
            "limit": min(max_results, 100)
        }

        headers = {}

        if self.hf_token:
            headers["Authorization"] = (
                f"Bearer {self.hf_token}"
            )

        response = requests.get(
            self.HF_API_URL,
            params=params,
            headers=headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        return [
            self._normalize_huggingface(item)
            for item in data
        ]

    @staticmethod
    def _normalize_huggingface(
        dataset: Dict[str, Any]
    ) -> Dict[str, Any]:

        card_data = (
            dataset.get("cardData")
            or {}
        )

        return {
            "source": "huggingface",
            "external_id": dataset.get("id"),
            "name": dataset.get("id"),
            "description": (
                card_data.get("description")
                or dataset.get("description")
            ),
            "url": (
                "https://huggingface.co/datasets/"
                + dataset.get("id", "")
            ),
            "owner": (
                dataset.get("author")
                or (
                    dataset.get("id", "")
                    .split("/")[0]
                )
            ),
            "license": card_data.get(
                "license"
            ),
            "tags": dataset.get(
                "tags",
                []
            ),
            "downloads": dataset.get(
                "downloads",
                0
            ),
            "votes": dataset.get(
                "likes",
                0
            ),
            "usability": None,
            "created_at": None,
            "updated_at": dataset.get(
                "lastModified"
            ),
        }

    # ============================================================
    # SEARCH ALL DATASET SOURCES
    # ============================================================

    def search_all(
        self,
        query: str,
        max_results_per_source: int = 10
    ) -> Dict[str, List[Dict[str, Any]]]:

        results = {
            "kaggle": [],
            "huggingface": []
        }

        try:
            results["kaggle"] = self.search_kaggle(
                query,
                max_results_per_source
            )
        except Exception as error:
            print(
                f"Kaggle warning: {error}"
            )

        try:
            results["huggingface"] = (
                self.search_huggingface(
                    query,
                    max_results_per_source
                )
            )
        except Exception as error:
            print(
                f"Hugging Face warning: {error}"
            )

        return results

    def search_all_flat(
        self,
        query: str,
        max_results_per_source: int = 10
    ) -> List[Dict[str, Any]]:

        results = self.search_all(
            query,
            max_results_per_source
        )

        datasets = []

        for source_results in results.values():
            datasets.extend(source_results)

        return datasets