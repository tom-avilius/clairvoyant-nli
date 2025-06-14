from collections import Counter


def compute_score(results):
    """
    Computes a 'fake news' score based on entailment, contradiction,
    and neutral counts.

    Parameters:
    - results (list of dict): A list where each element is a dictionary with:
        - 'label': one of 'entailment', 'contradiction', or 'neutral'
        - 'score': confidence/probability for the corresponding label

    Returns:
    - score (float): A fake news score based on the relationship of the labels.
        - Positive → more entailment (possibly true)
        - Negative → more contradiction (possibly fake)
        - Near zero → mostly neutral or uncertain
    - counts (collections.Counter): A dictionary-like object showing how many
    times
      each label appeared in the results

    Score Calculation Logic:
    - If all results are neutral (no entailments or contradictions),
    average their confidence scores.
    - If there are any entailments or contradictions:
        - Calculate: (entailments - contradictions) / total
        - Multiply by the number of neutrals to scale based on uncertainty
        - This gives a balanced score factoring in supportive, opposing,
        and neutral evidence
    """

    # Count occurrences of each label
    counts = Counter([r["label"] for r in results])

    entailments = counts["entailment"]
    contradictions = counts["contradiction"]
    neutrals = counts["neutral"]
    total = entailments + contradictions + neutrals

    # Case: Only neutrals present
    if entailments == 0 and contradictions == 0:
        score = sum(r["score"] for r in results) / total if total != 0 else 0.0
        return score, counts

    # Case: Avoid division by zero just in case
    if total == 0:
        return 0.0, counts

    # Main scoring formula: accounts for support vs contradiction, scaled
    # by uncertainty
    score = (entailments - contradictions) / total
    score *= neutrals  # Weight the score by neutral count
    return score, counts
