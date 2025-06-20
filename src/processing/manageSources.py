# data created through user queries.
from storage.results import sources
# data containing a list of trusted sources.
from storage.trustedSources import trustedSources


def filter_sources(uuid: str):
    """
    params
    uuid: str
    The unique sent to the client along with the response
    when the analyze request was sent.

    returns
    result: dict

    Filters all the sources to get entailments then compares
    against the list of trusted sources.

    Returns a dictionary that contains the sources schema along
    with a trusted or not trusted flag.
    """
    results = get_sources(uuid)

    for result in results:
        label = result.get("label")

        if label == "entailment":
            for source in trustedSources:
                if result.get("source") and result.get("source").startswith(source):
                    result["trusted"] = True
                    return result

    for result in results:
        label = result.get("label")

        if label == "entailment" and result.get("source"):
            result["trusted"] = False
            return result


def get_sources(uuid: str):
    """
    params
    uuid: str
    The unique id sent to the user when the analyze request
    was made.

    returns
    result: dict

    Retreives the source query result by the uuid provided by
    the client.
    """
    result = sources.get(uuid)

    if result:
        return result

    return {}
