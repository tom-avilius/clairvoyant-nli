# Clairvoyant‑NLI 🚀

A hybrid NLI (Natural Language Inference) pipeline designed to **evaluate news headlines** for factual accuracy by combining entailment classification, sentiment analysis, and semantic similarity.

---

## 🔍 Features

* **Entailment / Contradiction / Neutral detection** using BART‑Large‑MNLI
* **Sentiment‑based fallback** for neutral cases
* **Cosine similarity refinement** (MiniLM or MPNet) to correct over/under-classification
* **Composite scoring** to quantify the likelihood of a headline being true or false

---

## 🧩 Architecture Overview

```
Request at Port 7000/scrape <- NLI pipeline → Scoring logic → JSON response
```

* **FastAPI** handles `/analyze` POST requests with JSON payload: `{"news": "..."}`
* The pipeline runs NLI + sentiment + similarity logic, and returns a numeric credibility score.

---

## 🛠️ Installation

```bash
git clone https://github.com/tom-avilius/clairvoyant-nli.git
cd clairvoyant-nli

pip install fastapi uvicorn transformers sentence-transformers spacy requests
python -m spacy download en_core_web_sm
```

> Assumes an external scraping service already running (e.g., at `http://localhost:7000/scrape`).
> See: [Clairvoyant-Scraper](https://github.com/tom-avilius/clairvoyant-scraper)

---

## ⚙️ Usage

Start your scraping service ([Clairvoyant-Scraper](https://github.com/tom-avilius/clairvoyant-scraper)), then launch the API server:

```bash
uvicorn main:app --reload
```

You can test the API with `curl`:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"news": "NASA confirms water on the sunlit surface of the moon"}'
```

**Response:**

```json
{"score": 0.42}
```

* **Positive** → likely true
* **Negative** → likely false
* **Near zero** → uncertain

---

## 🧠 Pipeline Insights

1. **NLI Classification**
   `facebook/bart-large-mnli` predicts `entailment`, `neutral`, or `contradiction`.

2. **Neutral Refinement**
   If neutral → use `analyze``sentiment() → fallback to` cosine similary mpnet  (cosine similarity).

3. **Contradiction Control**
   Re-check with semantic similarity to avoid false contradictions.

4. **Scoring Function**
   Calculates a final credibility score based on label distribution.

---

## 📋 Example: Headline Workflow

* **Query**: "Google DeepMind released AlphaFold 3 in 2024."
* Scraped snippets include relevant articles (some neutral/old) (Scraping is a separate service).
* BART outputs or sentiment toss if neutral.
* Similarity logic prevents spurious contradictions or entailments.
* Final scoring computes whether the claim is supported or refuted.

---

## 🧪 Testing & Tuning

* Modify thresholds for similarity (`0.5` to `0.85`) or sentiment confidence to tweak performance.
* Monitor performance on known real/fake headlines & fine-tune logic.
* Optionally integrate a **cross-encoder** for targeted decisions if needed.

---

## 📌 Contributions

* Add unit tests for each module (NLI, sentiment, similarity, scoring)
* Improve scraper reliability.
* Provide Docker setup for deployment.

---
