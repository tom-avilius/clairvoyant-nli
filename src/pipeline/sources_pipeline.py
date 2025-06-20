from processing.manageSources import filter_sources


# NOTE: May look obosolete but it does encapsulate the
# function to maintain uniformity,
def filter_source(uuid: str):
    return filter_sources(uuid)
