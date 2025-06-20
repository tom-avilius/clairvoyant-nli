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
    # retrieve the sources by user id
    results = get_sources(uuid)

    # loops through all the results
    # OPTIMIZE: Too much nesting. Reduce indents and optimize logic.
    for result in results:
        # get the label
        label = result.get("label")

        # if the label is an entailment
        if label == "entailment":
            # compare and find if the source is trustworthy
            for source in trustedSources:
                if result.get("source") and result.get("source").startswith(source):
                    result["trusted"] = True  # flag trustworthy
                    return result

    # loop again if no trusted source was found
    # OPTIMIZE: Redundant loop (repeated). Implement better logic
    for result in results:
        label = result.get("label")

        if label == "entailment" and result.get("source"):
            result["trusted"] = False  # flag untrustworthy
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
    # get the source by uuid
    result = sources.get(uuid)

    if result:
        return result

    return {}
