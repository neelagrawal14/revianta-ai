from github_sources import GitHubSources


def print_repository(repo, number):

    print(f"\n#{number}")
    print(f"Name        : {repo['name']}")
    print(f"Full Name   : {repo['full_name']}")
    print(f"Owner       : {repo['owner']}")
    print(f"Description : {repo['description']}")
    print(f"Language    : {repo['language']}")
    print(f"Stars       : {repo['stars']}")
    print(f"Forks       : {repo['forks']}")
    print(f"Topics      : {', '.join(repo['topics'])}")
    print(f"License     : {repo['license']}")
    print(f"URL         : {repo['url']}")


def main():

    print("=" * 70)
    print("          REVIANTA GITHUB SOURCES TEST")
    print("=" * 70)

    query = "pothole detection AI"

    print(f"\nQuery: {query}")

    client = GitHubSources()

    print("\n" + "-" * 70)
    print("GITHUB REPOSITORY SEARCH")
    print("-" * 70)

    repositories = client.search_repositories(
        query,
        max_results=10
    )

    print(
        f"Repositories retrieved: "
        f"{len(repositories)}"
    )

    for i, repository in enumerate(
        repositories,
        start=1
    ):
        print_repository(
            repository,
            i
        )

    # ============================================================
    # VALIDATION
    # ============================================================

    print("\n" + "=" * 70)
    print("VALIDATION")
    print("=" * 70)

    if len(repositories) == 0:
        raise AssertionError(
            "GitHub returned no repositories."
        )

    required_fields = [
        "source",
        "external_id",
        "name",
        "full_name",
        "description",
        "owner",
        "url",
        "stars",
        "forks",
        "watchers",
        "open_issues",
        "language",
        "topics",
        "license",
        "created_at",
        "updated_at",
        "pushed_at",
        "default_branch",
        "is_fork",
        "archived",
        "has_issues",
        "has_wiki",
    ]

    for repository in repositories:

        for field in required_fields:

            if field not in repository:

                raise AssertionError(
                    f"Missing field '{field}' "
                    f"from GitHub repository."
                )

    print(
        "All GitHub repository records "
        "contain the required fields."
    )

    print("\nRepositories retrieved:")
    print(len(repositories))

    print("\n" + "=" * 70)
    print("        GITHUB SOURCES TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()