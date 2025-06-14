from transformers import pipeline

# Load a zero-shot classification pipeline using BART-large-MNLI,
# which is well-suited for natural language inference (entailment,
# contradiction, neutral).
classifier = pipeline("text-classification", model="facebook/bart-large-mnli")


def compare(text1: str, text2: str) -> list:
    """
    Compares two input texts using a Natural Language Inference (NLI) model.

    The model returns a list of label-score dictionaries indicating whether the
    relationship between the texts is one of 'entailment', 'contradiction',
    or 'neutral'.

    Args:
        text1 (str): The premise (usually the known or reference statement).
        text2 (str): The hypothesis (usually the claim to verify).

    Returns:
        list: A list of dictionaries with labels and confidence scores.
              Example:
              [
                  {'label': 'ENTAILMENT', 'score': 0.87},
                  {'label': 'NEUTRAL', 'score': 0.11},
                  {'label': 'CONTRADICTION', 'score': 0.02}
              ]
    """
    # BART-style format: premise + separator + hypothesis
    result = classifier(f"{text1} </s></s> {text2}")
    return result
