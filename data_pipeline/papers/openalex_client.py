import requests
from typing import Any, Dict, List, Optional


class OpenAlexClient:
    """
    Client for retrieving research papers from OpenAlex.

    This class is responsible only for communicating with
    the OpenAlex API and returning raw API records.
    """

    BASE_URL = "https://api.openalex.org/works"

    def __init__(self, mailto: Optional[str] = None, timeout: int = 30):
        self.timeout = timeout
        self.mailto = mailto

    def search_works(
        self,
        query: str,
        max_results: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search OpenAlex works using a text query.

        Parameters
        ----------
        query:
            Research topic or project query.

        max_results:
            Maximum number of papers to retrieve.

        Returns
        -------
        list:
            Raw OpenAlex work records.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        params = {
            "search": query.strip(),
            "per-page": min(max_results, 100),
        }

        if self.mailto:
            params["mailto"] = self.mailto

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        return data.get("results", [])

    def get_work(self, work_id: str) -> Dict[str, Any]:
        """
        Retrieve one OpenAlex work by ID.
        """

        if not work_id:
            raise ValueError("work_id cannot be empty.")

        url = f"{self.BASE_URL}/{work_id}"

        params = {}

        if self.mailto:
            params["mailto"] = self.mailto

        response = requests.get(
            url,
            params=params,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.json()