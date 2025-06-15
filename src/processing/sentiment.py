from transformers import pipeline

sentiment = pipeline("sentiment-analysis")


def analyze_sentiment(text1: str, text2: str) -> str:
    """
    Analyze the sentiment of two input texts and determine if they are aligned
    or contradict each other.

    Args:
        text1 (str): The first text input (typically the query).
        text2 (str): The second text input (typically the comparison text from
        scraped data).

    Returns:
        str: "entailment" if both texts share the same sentiment label,
             "contradiction" if their sentiments differ.

    Note:
        This function assumes that if two texts express opposing sentiments,
        they are likely to contradict each other in meaning.
    """
    # Run sentiment analysis on both texts
    sent1 = sentiment(text1)[0]["label"]
    sent2 = sentiment(text2)[0]["label"]

    # Return contradiction if sentiment labels differ
    if sent1 != sent2:
        return "contradiction"
    else:
        return "entailment"
