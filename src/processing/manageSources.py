from storage.results import sources
from storage.trustedSources import trustedSources


def filter_sources(uuid: str):
    results = get_sources()

    for result in results:
        label = result.get("label")

        if label == "entailment":
            for source in trustedSources:
                if result.get("source") == source:
                    return source


def get_sources(uuid: str):
    result = sources.get(uuid)

    if result:
        return result

    return {}
