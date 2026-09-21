from data_pipeline.normalizers.paper_normalizer import normalize_paper
import requests


KAGGLE_DATASETS_URL = "https://www.kaggle.com/api/v1/datasets/list"


def search_datasets(query: str, limit: int = 10):

    params = {
        "search": query,
        "pageSize": limit,
    }

    headers = {
        "User-Agent": "ReviantaAI-DataPipeline/1.0",
    }

    response = requests.get(
        KAGGLE_DATASETS_URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    datasets = []

    for dataset in data:

        owner = dataset.get("ownerName")

        authors = [owner] if owner else []

        normalized_dataset = normalize_paper(
            title=dataset.get("title"),
            authors=authors,
            abstract=dataset.get("subtitle") or "",
            year=None,
            doi=None,
            url=f"https://www.kaggle.com/datasets/{dataset.get('ref')}",
            source="kaggle",
        )
        normalized_dataset["record_type"] = "dataset"

        datasets.append(normalized_dataset)

    return datasets


if __name__ == "__main__":

    datasets = search_datasets(
        "artificial intelligence",
        5
    )

    print(f"Found {len(datasets)} datasets")

    for dataset in datasets:

        print("\n-------------------------")
        print("Title:", dataset["title"])
        print("Owner:", dataset["authors"])
        print("Description:", dataset["abstract"])
        print("URL:", dataset["url"])
        print("Source:", dataset["source"])
