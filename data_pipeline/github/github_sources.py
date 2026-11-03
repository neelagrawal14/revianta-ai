import requests
from typing import Any, Dict, List, Optional


class GitHubSources:
    """
    GitHub repository search client for Revianta AI.

    Returns normalized repository records that can later
    be stored in PostgreSQL and analyzed by the AI engine.
    """

    BASE_URL = "https://api.github.com"

    def __init__(
        self,
        token: Optional[str] = None,
        timeout: int = 30
    ):
        self.token = token
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def search_repositories(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:

        if not query or not query.strip():
            raise ValueError(
                "GitHub search query cannot be empty."
            )

        params = {
            "q": query.strip(),
            "per_page": min(max_results, 100),
            "sort": "stars",
            "order": "desc"
        }

        response = requests.get(
            f"{self.BASE_URL}/search/repositories",
            params=params,
            headers=self._headers(),
            timeout=self.timeout
        )

        if response.status_code == 403:
            raise RuntimeError(
                "GitHub API rate limit reached or access denied."
            )

        response.raise_for_status()

        data = response.json()

        return [
            self._normalize_repository(repo)
            for repo in data.get("items", [])
        ]

    @staticmethod
    def _normalize_repository(
        repo: Dict[str, Any]
    ) -> Dict[str, Any]:

        license_info = repo.get("license") or {}

        owner = repo.get("owner") or {}

        return {
            "source": "github",
            "external_id": str(repo.get("id")),
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "description": repo.get("description"),
            "owner": owner.get("login"),
            "url": repo.get("html_url"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "watchers": repo.get("watchers_count", 0),
            "open_issues": repo.get("open_issues_count", 0),
            "language": repo.get("language"),
            "topics": repo.get("topics", []),
            "license": license_info.get("spdx_id"),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "pushed_at": repo.get("pushed_at"),
            "default_branch": repo.get("default_branch"),
            "is_fork": repo.get("fork", False),
            "archived": repo.get("archived", False),
            "has_issues": repo.get("has_issues", False),
            "has_wiki": repo.get("has_wiki", False),
        }