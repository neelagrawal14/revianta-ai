from data_pipeline.normalizers.paper_normalizer import normalize_paper
import requests


HUGGINGFACE_DATASETS_URL = "https://huggingface.co/api/datasets"


def search_datasets(query: str, limit: int = 10):

    params = {
        "search": query,
        "limit": limit,
    }

    headers = {
        "User-Agent": "ReviantaAI-DataPipeline/1.0",
    }

    response = requests.get(
        HUGGINGFACE_DATASETS_URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    datasets = []

    for dataset in data[:limit]:

        dataset_id = dataset.get("id")

        if not dataset_id:
            continue

        normalized_dataset = normalize_paper(
            title=dataset_id,
            authors=[],
            abstract="",
            year=None,
            doi=None,
            url=f"https://huggingface.co/datasets/{dataset_id}",
            source="huggingface",
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
        print("URL:", dataset["url"])
        print("Source:", dataset["source"])