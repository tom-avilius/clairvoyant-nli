from fastapi import FastAPI  # FastAPI is used to create the web API
# Pydantic is used for request validation and parsing
from pydantic import BaseModel
# Import the custom NLI pipeline function
from pipeline.nli_pipeline import nli_pipeline

# Create a FastAPI instance
app = FastAPI()

# Define the structure of the expected request body


class NewsRequest(BaseModel):
    news: str  # The news headline to be analyzed


@app.post("/analyze")
def analyze_news(request: NewsRequest):
    """
    Analyze a news headline to assess its credibility.

    This endpoint accepts a news headline, processes it through the
    NLI pipeline, and returns a score indicating its likely truthfulness.

    Request Body:
    {
        "news": "string"
    }

    Returns:
        JSON object containing:
        - score (float): A numerical value representing the credibility
                         of the news.
                         A positive score implies the news is likely true.
                         A negative score implies it may be false or
                         misleading.
                         A score near zero suggests neutrality or lack of
                         strong evidence.
    """
    # Call the NLI pipeline to get the score for the input news
    score, uuid = nli_pipeline(request.news)

    # Return the result in JSON format
    return {"score": score, "uuid": uuid}
