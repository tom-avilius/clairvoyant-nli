import requests
import uuid
from processing.nli import classify
from processing.semantics import cosine_similarity_mpnet
from processing.score import compute_score
from processing.sentiment import analyze_sentiment
from storage.results import sources


# URL of the local scraper service
url = "http://localhost:7000/scrape"


def nli_pipeline(query):
    """
    Evaluates the credibility of a news headline using a hybrid NLI
    (Natural Language Inference) and semantic similarity approach.

    Steps performed:
    1. Converts the input query to lowercase for normalization.
    2. Sends the query to a scraping service to retrieve relevant
    headlines/articles.
    3. Uses a pre-trained NLI model to classify each comparison as
    entailment, contradiction, or neutral.
    4. For neutral results, applies cosine similarity to refine
    classification.
    5. Computes a final credibility score based on the distribution of
    classification labels.

    Args:
        query (str): The input news headline.

    Returns:
        float: A credibility score.
               - A positive score suggests support from scraped results.
               - A negative score suggests contradiction.
               - A score near zero indicates uncertainty or low correlation.

    Note:
        This function assumes that external request errors (e.g., network
        failure) will be handled upstream
        or allowed to raise unhandled exceptions naturally.
    """
    # Generate a result ID
    resultId = str(uuid.uuid4())
    query = query.lower()  # Normalize the headline to lowercase

    # Optional: use text cleaning like lemmatization if needed
    # WARN: Kinda results in anomalies
    # q = clean_text(query)

    # Send a GET request to the scraping backend with the query
    params = {"query": query}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error for bad responses

    # Extract result list from JSON
    data = response.json().get("result", [])

    allResults = []
    # compilation of computations
    compilation = []

    data = data[5:]

    # Process each of the returned headlines/articles
    for d in data:
        d_lower = d["headline"].lower()

        # Compare the query and scraped text using NLI model
        res = classify(query, d_lower)

        # If prediction is neutral, perform futher pipelining
        if res[0]["label"] == "neutral":
            # analyze sentiment for both texts
            res[0]["label"] = analyze_sentiment(query, d_lower)
            # find cosine similarity
            similarity = cosine_similarity_mpnet(query, d_lower)

            # control entailments with low semantic threshold
            if res[0]["label"] == "entailment" and similarity < 0.5:
                res[0]["label"] = "contradiction"
            # control contradictions with high semantic threshold
            elif res[0]["label"] == "contradiction" and similarity > 0.75:
                res[0]["label"] = "entailment"

        # Accumulate all results
        allResults.extend(res)
        compilation.append(
            {
                "source": d.get("source"),
                "headline": d.get("headline"),
                "label": res[0]["label"],
            }
        )

    # Compute the fake news score based on the label distribution
    score, counts = compute_score(allResults)
    # store the result of the computation
    sources[resultId] = compilation
    return score, resultId
