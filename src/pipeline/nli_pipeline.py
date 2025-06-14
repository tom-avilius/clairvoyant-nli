import requests
from data import queries
from processing.nli import classify
from processing.semantics import cosine_similarity_minilm
from processing.score import compute_score


# URL of the local scraper service
url = "http://localhost:7000/scrape"


def nli_pipeline():

    # Loop over each query in the input dataset
    for query in queries:
        q = query["news"].lower()  # Normalize the headline to lowercase

        # Optional: use text cleaning like lemmatization if needed
        # q = clean_text(query)

        # Send a GET request to the scraping backend with the query
        params = {"query": q}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error for bad responses

        # Extract result list from JSON
        data = response.json().get("result", [])

        allResults = []

        # Process each of the returned headlines/articles
        for d in data:
            d_lower = d.lower()

            # Compare the query and scraped text using NLI model
            res = classify(q, d_lower)

            # If prediction is neutral, fall back to cosine similarity
            if res[0]["label"] == "neutral":
                sim = cosine_similarity_minilm(q, d_lower)
                if sim > 0.74:
                    res[0]["label"] = "entailment"
                else:
                    res[0]["label"] = "contradiction"

            # Accumulate all results
            allResults.extend(res)

        # Compute the fake news score based on the label distribution
        score, counts = compute_score(allResults)

        # Print mismatches between expected label and computed score
        if (query["flag"] is True and score < 0) or (
            query["flag"] is False and score > 0
        ):
            print(query)
            print("Counts: ", counts)
            print("Score: ", score)
