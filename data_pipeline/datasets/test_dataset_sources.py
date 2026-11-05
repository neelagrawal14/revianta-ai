from dataset_sources import DatasetSources


def print_dataset(dataset, number):

    print(f"\n#{number}")
    print(f"Source      : {dataset['source']}")
    print(f"Name        : {dataset['name']}")
    print(f"Owner       : {dataset['owner']}")
    print(f"Description : {dataset['description']}")
    print(f"License     : {dataset['license']}")
    print(f"Downloads   : {dataset['downloads']}")
    print(f"Votes/Likes : {dataset['votes']}")
    print(f"URL         : {dataset['url']}")


def validate_dataset(dataset):

    required_fields = [
        "source",
        "external_id",
        "name",
        "description",
        "url",
        "owner",
        "license",
        "tags",
        "downloads",
        "votes",
        "usability",
        "created_at",
        "updated_at",
    ]

    for field in required_fields:

        if field not in dataset:

            raise AssertionError(
                f"Missing field '{field}' "
                f"from {dataset.get('source')} dataset."
            )


def main():

    print("=" * 70)
    print("          REVIANTA DATASET SOURCES TEST")
    print("=" * 70)

    query = "pothole detection"

    print(f"\nQuery: {query}")

    client = DatasetSources()

    # ============================================================
    # KAGGLE
    # ============================================================

    print("\n" + "-" * 70)
    print("1. KAGGLE")
    print("-" * 70)

    kaggle_datasets = client.search_kaggle(
        query,
        max_results=5
    )

    print(
        f"Datasets retrieved: "
        f"{len(kaggle_datasets)}"
    )

    for i, dataset in enumerate(
        kaggle_datasets,
        start=1
    ):
        print_dataset(dataset, i)

    # ============================================================
    # HUGGING FACE
    # ============================================================

    print("\n" + "-" * 70)
    print("2. HUGGING FACE")
    print("-" * 70)

    hf_datasets = client.search_huggingface(
        query,
        max_results=5
    )

    print(
        f"Datasets retrieved: "
        f"{len(hf_datasets)}"
    )

    for i, dataset in enumerate(
        hf_datasets,
        start=1
    ):
        print_dataset(dataset, i)

    # ============================================================
    # VALIDATION
    # ============================================================

    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)

    if len(kaggle_datasets) == 0:
        raise AssertionError(
            "Kaggle returned no datasets."
        )

    if len(hf_datasets) == 0:
        raise AssertionError(
            "Hugging Face returned no datasets."
        )

    all_datasets = (
        kaggle_datasets
        + hf_datasets
    )

    for dataset in all_datasets:
        validate_dataset(dataset)

    print(
        "All normalized dataset records "
        "contain the required fields."
    )

    print("\nSource counts:")
    print(
        f"Kaggle         : "
        f"{len(kaggle_datasets)}"
    )
    print(
        f"Hugging Face   : "
        f"{len(hf_datasets)}"
    )
    print(
        f"Total           : "
        f"{len(all_datasets)}"
    )

    print("\n" + "=" * 70)
    print("        DATASET SOURCES TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()