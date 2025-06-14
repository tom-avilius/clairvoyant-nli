from fastapi import FastAPI, Query
from pipeline import nli_pipeline

app = FastAPI()


@app.post("/analyze")
def analyze_news(news: str):
    score, counts = run_inference(news.headline, news.flag)
    return {
        "score": score,
        "label_counts": counts,
        "verdict": "fake" if score < 0 else "real",
    }
