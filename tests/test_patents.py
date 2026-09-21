import requests
from unittest.mock import patch

from data_pipeline.collectors.patents import search_patents


def test_patent_collector_without_api_key():
    with patch.dict("os.environ", {}, clear=True):
        result = search_patents("artificial intelligence", 5)

    assert result == []


def test_patent_collector_handles_request_failure():
    with patch(
        "data_pipeline.collectors.patents.requests.post"
    ) as mock_post:
        mock_post.side_effect = requests.exceptions.ConnectionError(
            "test connection failure"
        )

        with patch.dict(
            "os.environ",
            {"PATENTSVIEW_API_KEY": "test-key"},
        ):
            result = search_patents("artificial intelligence", 5)

    assert result == []
